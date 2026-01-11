from typing import Any, cast, override
from contextlib import contextmanager
from importlib import import_module
from pathlib import Path
from logging import info

from llvmlite import ir as lir, binding as llvm

from gem.c_registry import CRegistry
from gem.passes import CompilerPass
from gem import ir
from gem.codegen_utils import (
    NULL, NULL_BYTE, create_static_buffer, create_struct_value, define_identified_type, create_string_constant,
    get_allocated_struct_field_value, llint, get_struct_field, zero
)


def code_type_to_ir_type(type: lir.Type, scope: ir.Scope):
    if isinstance(type, lir.IntType):
        match type.width:
            case 1:
                return scope.type_map.get('bool')
            case 32:
                return scope.type_map.get('int')
    elif isinstance(type, lir.FloatType):
        return scope.type_map.get('float')
    elif isinstance(type, lir.IdentifiedStructType):
        return scope.type_map.get(type.name)
    elif isinstance(type, lir.LiteralStructType):
        if len(type.elements) == 1 and isinstance(
            (elem := type.elements[0]), lir.PointerType
        ) and isinstance(getattr(elem, 'pointee'), lir.IntType):
            return scope.type_map.get('FILE')
    elif isinstance(type, lir.VoidType):
        return scope.type_map.get('nil')
    elif isinstance(type, lir.PointerType):
        return scope.type_map.get('pointer')
        
    raise NotImplementedError(type)

class CodeGenerationPass(CompilerPass):
    def __init__(self, file: ir.File):
        super().__init__(file)
        
        self.module = lir.Module(file.path.stem, lir.Context())
        self.module.triple = llvm.get_default_triple()
        
        self.c_registry = CRegistry(self.module, self.file)
        
        self.builder = lir.IRBuilder()
        
        self.codegen_types = {}
        # self.params = {}
        
        self.string_type = define_identified_type('string', [
            lir.PointerType(lir.IntType(8)),
            lir.IntType(32)
        ], self.module.context)
        
        self.while_merge_block = None
        self.while_test_block = None
    
    @contextmanager
    @override
    def child_scope(self, builder: lir.IRBuilder):
        old_builder = self.builder
        self.builder = builder
        yield super().child_scope()
        self.builder = old_builder
    
    def visit_Program(self, node: ir.Program):
        for stmt in node.nodes:
            self.visit(stmt)
        
        return str(self.module)
    
    def visit_Type(self, node: ir.Type):
        match node.type:
            case 'int':
                return lir.IntType(32)
            case 'float':
                return lir.FloatType()
            case 'string':
                return self.string_type
            case 'bool':
                return lir.IntType(1)
            case 'nil':
                return lir.VoidType()
            case 'pointer' | 'any':
                return lir.PointerType(lir.IntType(8))
            case 'FILE':
                return lir.LiteralStructType([lir.PointerType(lir.IntType(8))])
            case _:
                if node.type in self.codegen_types:
                    return self.codegen_types[node.type]
                
                node.pos.comptime_error(self.file, f'unknown type \'{node.type}\'')
    
    def visit_ReferenceType(self, node: ir.ReferenceType):
        typ = self.visit(node.type)
        return lir.PointerType(typ)
    
    def visit_Arg(self, node: ir.Arg):
        return self.visit(node.value)

    def visit_Param(self, node: ir.Param):
        return self.visit(node.type)

    def visit_Body(self, node: ir.Body):
        for stmt in node.nodes:
            self.visit(stmt)
    
    def visit_Function(self, node: ir.Function):
        if node.name in self.module.globals:
            return self.module.get_global(node.name)
        
        if node.is_generic:
            for overload in node.overloads:
                self.visit(overload)
            
            self.scope.symbol_table.add(ir.Symbol(node.name, self.scope.type_map.get('function'), node, self.file))
            return node
        
        ret_type = self.visit(node.ret_type)
        func_type = lir.FunctionType(ret_type, [self.visit(param) for param in node.params])
        func = lir.Function(self.module, func_type, node.name)
        for i, param in enumerate(node.params):
            func.args[i].name = f'{param.name}_param'
            
            # self.params[param.name] = param
        
        if node.flags.extern:
            cobjects = CRegistry.get_all_cobjects()
            cobj = cobjects[node.name]
            if cobj.llvm_name is not None:
                func.name = cobj.llvm_name
            
            func.linkage = 'external'
        
        self.scope.symbol_table.add(ir.Symbol(node.name, self.scope.type_map.get('function'), func, self.file))
        for overload in node.overloads:
            self.visit(overload)
        
        if node.body is not None:
            builder = lir.IRBuilder(func.append_basic_block('entry'))
            with self.child_scope(builder):
                for i, param in enumerate(node.params):
                    ptr = self.builder.alloca(self.visit(param.type), name=f'{param.name}_ptr')
                    self.builder.store(func.args[i], ptr)
                    
                    self.scope.symbol_table.add(ir.Symbol(param.name, param.type, ptr, self.file, is_mutable=param.is_mutable))
                
                self.visit(node.body)
                
                if ret_type == lir.VoidType() and not cast(lir.Block, self.builder.block).is_terminated:
                    self.builder.ret_void()
        
        return func
    
    def visit_Variable(self, node: ir.Variable):
        value = self.visit(node.value)
        ptr = self.builder.alloca(value.type, name=f'{node.name}_ptr')
        self.builder.store(value, ptr)
        self.scope.symbol_table.add(ir.Symbol(node.name, value.type, ptr, self.file, is_mutable=node.is_mutable))
        return ptr
    
    def visit_Assignment(self, node: ir.Assignment):
        value = self.visit(node.value)
        symbol = cast(ir.Symbol, self.scope.symbol_table.get(node.name))
        symbol.value = value
        return self.builder.store(value, symbol.value)
    
    def visit_If(self, node: ir.If):
        func = cast(lir.Function, self.builder.function)
        merge_block = func.append_basic_block('if_merge')
        then_block = func.append_basic_block('if_then')

        elif_test_blocks = []
        elif_then_blocks = []

        for i in range(len(node.elseifs)):
            elif_test_blocks.append(func.append_basic_block(f'elif_test_{i}'))
            elif_then_blocks.append(func.append_basic_block(f'elif_then_{i}'))

        else_block = func.append_basic_block('if_else') if node.else_body is not None else merge_block

        cond = self.visit(node.cond)
        first_elif_test = elif_test_blocks[0] if elif_test_blocks else else_block
        self.builder.cbranch(cond, then_block, first_elif_test)

        self.builder.position_at_end(then_block)
        then_value = self.visit(node.body)
        if not cast(lir.Block, self.builder.block).is_terminated:
            self.builder.branch(merge_block)

        elif_end_blocks = []
        elif_values = []
        for i, elif_node in enumerate(node.elseifs):
            self.builder.position_at_end(elif_test_blocks[i])
            elif_cond = self.visit(elif_node.cond)

            next_target = elif_test_blocks[i + 1] if i + 1 < len(elif_test_blocks) else else_block
            self.builder.cbranch(elif_cond, elif_then_blocks[i], next_target)

            self.builder.position_at_end(elif_then_blocks[i])
            elif_value = self.visit(elif_node.body)
            if not cast(lir.Block, self.builder.block).is_terminated:
                self.builder.branch(merge_block)

            elif_end_blocks.append(self.builder.block)
            elif_values.append(elif_value)
        
        if else_block is not merge_block:
            self.builder.position_at_end(else_block)
            else_value = self.visit(cast(ir.Node, node.else_body))
            if not cast(lir.Block, self.builder.block).is_terminated:
                self.builder.branch(merge_block)

            else_end_block = self.builder.block
        else:
            else_value = None
            else_end_block = None

        self.builder.position_at_end(merge_block)

        all_values = [then_value] + elif_values + ([else_value] if else_value is not None else [])
        all_blocks = [then_block] + elif_end_blocks + ([else_end_block] if else_end_block is not None else [])

        if all(v is not None for v in all_values):
            phi = self.builder.phi(all_values[0].type)
            for val, blk in zip(all_values, all_blocks):
                phi.add_incoming(val, blk)

            return phi
    
    def visit_While(self, node: ir.While):
        func = cast(lir.Function, self.builder.function)

        cond_block = func.append_basic_block('while_cond')
        body_block = func.append_basic_block('while_body')
        merge_block = func.append_basic_block('while_merge')

        self.builder.branch(cond_block)

        self.builder.position_at_end(cond_block)
        cond = self.visit(node.cond)
        self.builder.cbranch(cond, body_block, merge_block)

        self.builder.position_at_end(body_block)
        self.while_merge_block = merge_block
        self.while_test_block = cond_block
        self.visit(node.body)
        if not cast(lir.Block, self.builder.block).is_terminated:
            self.builder.branch(cond_block)

        self.builder.position_at_end(merge_block)
    
    def visit_Break(self, _):
        self.builder.branch(self.while_merge_block)

    def visit_Continue(self, _):
        self.builder.branch(self.while_test_block)
    
    def use_py(self, py_file: Path, lib_name: str):
        file = ir.File(py_file, ir.Scope(), self.file.options)
        codegen = CodeGenerationPass(file)
        
        module = import_module(f'gem.stdlib.{lib_name}.{py_file.stem}')
        instance = getattr(module, lib_name)(file)
        for obj in instance.attrs.values():
            codegen.visit_Function(obj)
            
        for symbol in file.scope.symbol_table.symbols.values():
            func = symbol.value
            if isinstance(func, lir.Function):
                new_func = lir.Function(self.module, func.function_type, func.name)
                new_func.linkage = 'external'
        
        self.scope.merge(file.scope)
        
        info(f'Imported python stdlib file {lib_name}')
    
    def use_gem(self, gem_file: Path, lib_name: str):
        from gem import compile_to_obj
        
        file = ir.File(gem_file, ir.Scope(), self.file.options)
        obj_file = compile_to_obj(file)
        
        for symbol in file.scope.symbol_table.symbols.values():
            func = symbol.value
            if isinstance(func, lir.Function):
                new_func = lir.Function(self.module, func.function_type, func.name)
                new_func.linkage = 'external'
            elif isinstance(func, ir.Function) and func.is_generic:
                self.visit(func)
        
        self.file.codegen_data.object_files.append(obj_file)
        self.scope.merge(file.scope)
        
        info(f'Imported gem library {lib_name}')
    
    def visit_Use(self, node: ir.Use):
        stdlib_path = ir.STDLIB_PATH / node.path
        if stdlib_path.exists():
            if self.file.path.stem == stdlib_path.stem:
                return node
            
            if (py_file := stdlib_path / f'{node.path}.py').exists():
                self.use_py(py_file, node.path)
            
            if (gem_file := stdlib_path / f'{node.path}.gem').exists():
                self.use_gem(gem_file, node.path)
        
        return node
    
    def visit_Return(self, node: ir.Return):
        value = self.visit(node.value)
        self.builder.ret(value)
    
    def visit_Int(self, node: ir.Int):
        return lir.Constant(self.visit(node.type), node.value)

    def visit_Float(self, node: ir.Float):
        return lir.Constant(self.visit(node.type), node.value)
    
    def visit_StringLiteral(self, node: ir.StringLiteral):
        return create_string_constant(self.module, node.value)
    
    def visit_Bool(self, node: ir.Bool):
        return lir.Constant(self.visit(node.type), node.value)

    def visit_Id(self, node: ir.Id):
        symbol = cast(ir.Symbol, self.scope.symbol_table.get(node.name))
        value = self.builder.load(symbol.value, node.name)
        # if node.name in self.params:
        #     param = self.params[node.name]
        #     if isinstance(param.type, ir.ReferenceType):
        #         value = self.builder.load(value, node.name)
        
        return value
    
    def visit_Bracketed(self, node: ir.Bracketed):
        return self.visit(node.value)

    def visit_Ternary(self, node: ir.Ternary):
        return self.builder.select(self.visit(node.cond), self.visit(node.true), self.visit(node.false), 'ternary')
    
    def handle_intrinsics(self, node: ir.Call, args: list[Any]):
        match node.callee:
            case 'panic':
                exit = self.c_registry.get('exit')
                puts = self.c_registry.get('puts')
                
                self.builder.call(puts, [args[0]])
                self.builder.call(exit, [llint(1)])
                return self.builder.unreachable()
            case '__buffer':
                const = args[0]
                if not isinstance(const, lir.Constant):
                    node.pos.comptime_error(self.file, 'Expected integer constant for __buffer')
                
                size = const.constant
                return create_static_buffer(self.module, lir.IntType(8), size, '__buffer', self.builder)
            case '__create_string':
                return create_struct_value(self.builder, self.string_type, args, 'string')
            case '__format_int':
                snprintf = self.c_registry.get('snprintf')
                if 'int_fmt' in self.module.globals:
                    fmt = self.module.get_global('int_fmt')
                else:
                    fmt = create_string_constant(self.module, '%d', 'int_fmt', self.builder)
                
                return self.builder.call(snprintf, [args[0], args[1], fmt, args[2]], '__format_int')
            case '__format_float':
                snprintf = self.c_registry.get('snprintf')
                if 'float_fmt' in self.module.globals:
                    fmt = self.module.get_global('float_fmt')
                else:
                    fmt = create_string_constant(self.module, '%f', 'float_fmt', self.builder)
                
                return self.builder.call(snprintf, [args[0], args[1], fmt, args[2]], '__format_float')
            case 'string.ptr':
                string = args[0]
                if isinstance(getattr(string, 'type'), lir.PointerType):
                    return get_allocated_struct_field_value(self.builder, string, 0, 'string.ptr')
                
                return get_struct_field(self.builder, string, 0, 'string.ptr')
            case '__null_terminate':
                ptr, position = args
                last_char_ptr = self.builder.gep(ptr, [position], True, 'last_char_ptr')
                return self.builder.store(NULL_BYTE(), last_char_ptr)
            case '__stdin':
                acrt_iob_func = self.c_registry.get('__acrt_iob_func')
                return self.builder.call(acrt_iob_func, [llint(0)], '__stdin')
            case '__print_pointer_no_newline':
                printf = self.c_registry.get('printf')
                
                string_fmt_name = 'string_fmt'
                if string_fmt_name in self.module.globals:
                    string_fmt = self.module.get_global(string_fmt_name)
                else:
                    string_fmt = create_string_constant(self.module, '%s', string_fmt_name)
                
                return self.builder.call(printf, [string_fmt, args[0]])
            case '__is_null':
                ptr = args[0]
                return self.builder.icmp_signed('==', ptr, NULL(), '__is_null')
            case '__oom_msg':
                out_of_memory_msg_name = '__oom_str'
                if out_of_memory_msg_name in self.module.globals:
                    return lir.Constant.gep(self.module.get_global(out_of_memory_msg_name), [zero(32), zero(32)])
                else:
                    return create_string_constant(self.module, 'out of memory', out_of_memory_msg_name)
            case 'string.length':
                string = args[0]
                if isinstance(getattr(string, 'type'), lir.PointerType):
                    return get_allocated_struct_field_value(self.builder, string, 1, 'string.length')
                
                return get_struct_field(self.builder, string, 1, 'string.length')
            case '__null':
                return NULL()
            case 'int.+.int':
                return self.builder.add(args[0], args[1], 'int.+.int')
            case 'int.-.int':
                return self.builder.sub(args[0], args[1], 'int.-.int')
            case 'int.*.int':
                return self.builder.mul(args[0], args[1], 'int.*.int')
            case 'int./.int':
                return self.builder.sdiv(args[0], args[1], 'int./.int')
            case 'int.%.int':
                return self.builder.srem(args[0], args[1], 'int.%.int')
            case 'int.==.int':
                return self.builder.icmp_signed('==', args[0], args[1], 'int.==.int')
            case 'int.!=.int':
                return self.builder.icmp_signed('!=', args[0], args[1], 'int.!=.int')
            case 'int.>.int':
                return self.builder.icmp_signed('>', args[0], args[1], 'int.>.int')
            case 'int.<.int':
                return self.builder.icmp_signed('<', args[0], args[1], 'int.<.int')
            case 'int.>=.int':
                return self.builder.icmp_signed('>=', args[0], args[1], 'int.>=.int')
            case 'int.<=.int':
                return self.builder.icmp_signed('<=', args[0], args[1], 'int.<=.int')
            case 'float.+.float':
                return self.builder.fadd(args[0], args[1], 'float.+.float')
            case 'float.-.float':
                return self.builder.fsub(args[0], args[1], 'float.-.float')
            case 'float.*.float':
                return self.builder.fmul(args[0], args[1], 'float.*.float')
            case 'float./.float':
                return self.builder.fdiv(args[0], args[1], 'float./.float')
            case 'float.%.float':
                return self.builder.frem(args[0], args[1], 'float.%.float')
            case 'float.==.float':
                return self.builder.fcmp_ordered('==', args[0], args[1], 'float.==.float')
            case 'float.!=.float':
                return self.builder.fcmp_ordered('!=', args[0], args[1], 'float.!=.float')
            case 'float.>.float':
                return self.builder.fcmp_ordered('>', args[0], args[1], 'float.>.float')
            case 'float.<.float':
                return self.builder.fcmp_ordered('<', args[0], args[1], 'float.<.float')
            case 'float.>=.float':
                return self.builder.fcmp_ordered('>=', args[0], args[1], 'float.>=.float')
            case 'float.<=.float':
                return self.builder.fcmp_ordered('<=', args[0], args[1], 'float.<=.float')
            case 'bool.==.bool':
                return self.builder.icmp_signed('==', args[0], args[1], 'bool.==.bool')
            case 'bool.!=.bool':
                return self.builder.icmp_signed('!=', args[0], args[1], 'bool.!=.bool')
            case 'bool.&&.bool':
                return self.builder.and_(args[0], args[1], 'bool.&&.bool')
            case 'bool.||.bool':
                return self.builder.or_(args[0], args[1], 'bool.||.bool')
            case '!.bool':
                return self.builder.not_(args[0], '!.bool')
    
    def visit_Call(self, node: ir.Call):
        args = [self.visit(arg) for arg in node.args]
        if (result := self.handle_intrinsics(node, args)) is not None:
            return result
        
        symbol = self.scope.symbol_table.get(node.callee)
        assert symbol is not None
        
        func = symbol.value
        assert isinstance(func, lir.Function), f'function {node.callee} is not defined or is generic'
        
        return self.builder.call(func, args, node.callee)
    
    def visit_Ref(self, node: ir.Ref):
        symbol = self.scope.symbol_table.get(node.name)
        assert symbol is not None
        
        return symbol.value
