from contextlib import contextmanager
from importlib import import_module
from logging import info
from typing import cast

from llvmlite import ir as lir, binding as llvm

from gem.c_registry import CRegistry
from gem.passes import CompilerPass
from gem import ir
from gem.codegen_utils import (
    NULL, create_static_buffer, create_struct_value, define_identified_type, create_string_constant, llint, get_struct_field
)


class CodeGenerationPass(CompilerPass):
    def __init__(self, file: ir.File):
        super().__init__(file)
        
        self.module = lir.Module(file.path.stem, lir.Context())
        self.module.triple = llvm.get_default_triple()
        
        self.c_registry = CRegistry(self.module, self.scope)
        
        self.builder = lir.IRBuilder()
        
        self.codegen_types = {}
        
        self.string_type = define_identified_type('string', [
            lir.PointerType(lir.IntType(8)),
            lir.IntType(32)
        ], self.module.context)
        
        self.while_merge_block = None
        self.while_test_block = None
    
    @contextmanager
    def child_scope(self, builder: lir.IRBuilder):
        old_builder = self.builder
        old_scope = self.scope
        self.builder = builder
        self.scope = self.scope.make_child()
        yield
        self.builder = old_builder
        self.scope = old_scope
    
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
            case _:
                if node.type in self.codegen_types:
                    return self.codegen_types[node.type]
                
                node.pos.comptime_error(self.file, f'unknown type \'{node.type}\'')
    
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
            
            self.scope.symbol_table.add(ir.Symbol(node.name, self.scope.type_map.get('function'), node))
            return node
        
        ret_type = self.visit(node.ret_type)
        func_type = lir.FunctionType(ret_type, [self.visit(param) for param in node.params])
        func = lir.Function(self.module, func_type, node.name)
        for i, param in enumerate(node.params):
            func.args[i].name = f'{param.name}_param'
        
        if node.flags.extern:
            func.linkage = 'external'
        
        self.scope.symbol_table.add(ir.Symbol(node.name, self.scope.type_map.get('function'), func))
        if node.body is not None:
            builder = lir.IRBuilder(func.append_basic_block('entry'))
            with self.child_scope(builder):
                for i, param in enumerate(node.params):
                    ptr = self.builder.alloca(self.visit(param.type), name=f'{param.name}_ptr')
                    self.builder.store(func.args[i], ptr)
                    
                    self.scope.symbol_table.add(ir.Symbol(param.name, param.type, ptr, param.is_mutable))
                
                self.visit(node.body)
                
                if ret_type == lir.VoidType() and not cast(lir.Block, self.builder.block).is_terminated:
                    self.builder.ret_void()
        
        return func
    
    def visit_Variable(self, node: ir.Variable):
        value = self.visit(node.value)
        ptr = self.builder.alloca(value.type, name=f'{node.name}_ptr')
        self.builder.store(value, ptr)
        self.scope.symbol_table.add(ir.Symbol(node.name, value.type, ptr, node.is_mutable))
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
    
    def visit_Use(self, node: ir.Use):
        stdlib_path = ir.STDLIB_PATH / node.path
        if stdlib_path.exists():
            if self.file.path.stem == stdlib_path.stem:
                return node
            
            if (stdlib_path / f'{node.path}.py').exists():
                py_module = import_module(f'gem.stdlib.{node.path}.{node.path}')
                instance = getattr(py_module, node.path)(self.scope)
                instance.add_to_scope()
                
                info(f'Imported python library {node.path}')
            
            if (gem_file := stdlib_path / f'{node.path}.gem').exists():
                from gem import compile_to_obj
                
                file = ir.File(gem_file, ir.Scope(), self.file.options)
                obj_file = compile_to_obj(file)
                
                for symbol in file.scope.symbol_table.symbols.values():
                    func = symbol.value
                    if isinstance(func, lir.Function):
                        new_func = lir.Function(self.module, func.function_type, func.name)
                        new_func.linkage = 'external'
                
                self.file.codegen_data.object_files.append(obj_file)
                self.scope.merge(file.scope)
                
                info(f'Imported gem library {node.path}')
        
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
        return self.builder.load(symbol.value, node.name)
    
    def visit_Bracketed(self, node: ir.Bracketed):
        return self.visit(node.value)

    def visit_Ternary(self, node: ir.Ternary):
        return self.builder.select(self.visit(node.cond), self.visit(node.true), self.visit(node.false), 'ternary')
    
    def handle_intrinsics(self, node: ir.Call, args: list[lir.Value]):
        match node.callee:
            case 'panic':
                exit = self.c_registry.get('exit')
                puts = self.c_registry.get('puts')
                
                ptr = get_struct_field(self.builder, args[0], 0, 'ptr')
                self.builder.call(puts, [ptr])
                self.builder.call(exit, [llint(1)])
                return self.builder.unreachable()
            case '__is_null':
                return self.builder.icmp_signed('==', args[0], NULL(), '__is_null')
            case '__buffer':
                const = args[0]
                if not isinstance(const, lir.Constant):
                    node.pos.comptime_error(self.file, 'Expected integer constant for __buffer')
                
                size = const.constant
                return create_static_buffer(self.module, lir.IntType(8), size, '__buffer', self.builder)
            case '__create_string':
                return create_struct_value(self.builder, self.string_type, args, 'string')
            case '__alloc':
                malloc = self.c_registry.get('malloc')
                puts = self.c_registry.get('puts')
                exit = self.c_registry.get('exit')
                
                ptr = self.builder.call(malloc, args, '__alloc')
                is_null = self.builder.icmp_signed('==', ptr, NULL(), '__alloc_ptr')
                with self.builder.if_then(is_null, False):
                    error = create_string_constant(self.module, 'out of memory', '__alloc_error')
                    self.builder.call(puts, [error])
                    self.builder.call(exit, [llint(1)])
                    self.builder.unreachable()
                
                return ptr
            case '__free':
                free = self.c_registry.get('free')
                return self.builder.call(free, args)
            case '__memcpy':
                memcpy = self.c_registry.get('memcpy')
                return self.builder.call(memcpy, args, '__memcpy')
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
            case '__print_pointer':
                puts = self.c_registry.get('puts')
                return self.builder.call(puts, args, '__print_pointer')
            case 'int.+.int':
                return self.builder.add(args[0], args[1], 'int.+.int')
            case 'float.+.float':
                return self.builder.fadd(args[0], args[1], 'float.+.float')
            case 'string.ptr':
                return get_struct_field(self.builder, args[0], 0, 'string.ptr')
    
    def visit_Call(self, node: ir.Call):
        args = [cast(lir.Value, self.visit(arg)) for arg in node.args]
        if (result := self.handle_intrinsics(node, args)) is not None:
            return result
        
        symbol = self.scope.symbol_table.get(node.callee)
        assert symbol is not None
        
        func = symbol.value
        if isinstance(func, ir.Function):
            func = self.visit(func)
        
        return self.builder.call(func, args, node.callee)
    
    def visit_Attribute(self, node: ir.Attribute):
        value = self.visit(node.value)
        match node.value.type.type, node.attr:
            case 'string', 'ptr':
                return get_struct_field(self.builder, cast(lir.Value, value), 0, 'string.ptr')
            case _:
                raise NotImplementedError(f'Unsupported attribute access: {value.type.type}.{node.attr}')
