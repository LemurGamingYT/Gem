from contextlib import contextmanager
from importlib import import_module
from typing import cast, Optional
from logging import info

from gem.passes import CompilerPass
from gem import ir


class AnalyserPass(CompilerPass):
    def __init__(self, file: ir.File):
        super().__init__(file)
        
        self.declare_intrinsic('panic', self.scope.type_map.get('nil'), [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('string'), 'msg')
        ])
        
        self.declare_intrinsic('__buffer', self.scope.type_map.get('pointer'), [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('int'), 'size')
        ])
        
        self.declare_intrinsic('__create_string', self.scope.type_map.get('string'), [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('pointer'), 'ptr'),
            ir.Param(ir.Position.zero(), self.scope.type_map.get('int'), 'length')
        ])
        
        self.declare_intrinsic('__alloc', self.scope.type_map.get('pointer'), [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('int'), 'size')
        ])
        
        self.declare_intrinsic('__free', self.scope.type_map.get('nil'), [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('pointer'), 'ptr')
        ])
        
        self.declare_intrinsic('__memcpy', self.scope.type_map.get('pointer'), [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('pointer'), 'dest'),
            ir.Param(ir.Position.zero(), self.scope.type_map.get('pointer'), 'src'),
            ir.Param(ir.Position.zero(), self.scope.type_map.get('int'), 'size'),
            ir.Param(ir.Position.zero(), self.scope.type_map.get('bool'), 'is_volatile')
        ])
        
        self.declare_intrinsic('__format_int', self.scope.type_map.get('int'), [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('pointer'), 'buf'),
            ir.Param(ir.Position.zero(), self.scope.type_map.get('int'), 'length'),
            ir.Param(ir.Position.zero(), self.scope.type_map.get('int'), 'i')
        ])
        
        self.declare_intrinsic('__format_float', self.scope.type_map.get('int'), [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('pointer'), 'buf'),
            ir.Param(ir.Position.zero(), self.scope.type_map.get('int'), 'length'),
            ir.Param(ir.Position.zero(), self.scope.type_map.get('float'), 'f')
        ])
        
        self.declare_intrinsic('__print_pointer', self.scope.type_map.get('nil'), [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('pointer'), 'ptr')
        ])
        
        self.declare_intrinsic('int.+.int', self.scope.type_map.get('int'), [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('int'), 'a'),
            ir.Param(ir.Position.zero(), self.scope.type_map.get('int'), 'b')
        ])
        
        self.declare_intrinsic('float.+.float', self.scope.type_map.get('float'), [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('float'), 'a'),
            ir.Param(ir.Position.zero(), self.scope.type_map.get('float'), 'b')
        ])
        
        self.declare_intrinsic('string.ptr', self.scope.type_map.get('pointer'), [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('string'), 'str')
        ])
        
        self.declare_intrinsic('__null_terminate', self.scope.type_map.get('nil'), [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('pointer'), 'ptr'),
            ir.Param(ir.Position.zero(), self.scope.type_map.get('int'), 'position')
        ])
        
    def declare_intrinsic(self, name: str, ret_type: ir.Type, params: list[ir.Param]):
        self.scope.symbol_table.add(ir.Symbol(name, self.scope.type_map.get('function'), ir.Function(
            ir.Position.zero(), ret_type, name, params
        )))
        
        info(f'Declared intrinsic {name}')
    
    @contextmanager
    def child_scope(self):
        old_scope = self.scope
        self.scope = self.scope.make_child()
        yield
        self.scope = old_scope
    
    def visit_Program(self, node: ir.Program):
        nodes = []
        for stmt in node.nodes:
            nodes.append(self.visit(stmt))
        
        return ir.Program(node.pos, nodes)
    
    def visit_Type(self, node: ir.Type):
        t = self.scope.type_map.get(node.type)
        if t is None:
            node.pos.comptime_error(self.file, f'unknown type \'{node.type}\'')
        
        return t
    
    def visit_ReferenceType(self, node: ir.ReferenceType):
        return ir.ReferenceType(self.visit(node.type))
    
    def visit_Arg(self, node: ir.Arg):
        value = self.visit(node.value)
        return ir.Arg(node.pos, value.type, value)
    
    def visit_Param(self, node: ir.Param):
        return ir.Param(node.pos, self.visit(node.type), node.name, node.is_mutable)
    
    def visit_Body(self, node: ir.Body):
        nodes = []
        for stmt in node.nodes:
            nodes.append(self.visit(stmt))
        
        return ir.Body(node.pos, node.type, nodes)
    
    def visit_Function(self, node: ir.Function, callsite: Optional[ir.Call] = None):
        if node.name in self.scope.symbol_table.symbols:
            node.pos.comptime_error(self.file, f'function \'{node.name}\' already defined')
        
        # if self.scope.parent is not None:
        #     node.pos.comptime_error(self.file, 'functions can only be defined at the top level')
        
        if node.is_generic and callsite is None:
            self.scope.symbol_table.add(ir.Symbol(node.name, self.scope.type_map.get('function'), node))
            return node
        
        generic_map = node.create_generic_map(callsite.args if callsite is not None else [])
        for name, typ in generic_map.items():
            self.scope.type_map.add_type(name, typ)
        
        ret_type = self.visit(node.ret_type)
        params = [self.visit(param) for param in node.params]
        overloads = [self.visit(overload) for overload in node.overloads]
        extend_type = self.visit(node.extend_type) if node.extend_type is not None else None
        flags = node.flags
        func_name = node.name
        if extend_type is not None:
            if func_name == 'new':
                flags.static = True
            
            func_name = f'{extend_type}.{func_name}'
        
        if node.is_generic:
            generics_str = ', '.join(str(type) for type in generic_map.values())
            func_name += f'<{generics_str}>'
        
        func = ir.Function(node.pos, ret_type, func_name, params, node.body, overloads, flags)
        
        self.scope.symbol_table.add(ir.Symbol(func.name, self.scope.type_map.get('function'), func))
        body = node.body
        if body is not None:
            with self.child_scope():
                info(f'Entering function {func.name}\'s body')
                for param in params:
                    self.scope.symbol_table.add(ir.Symbol(param.name, param.type, param, param.is_mutable))
                
                func.body = self.visit(body)
        
        if node.is_generic:
            node.overloads.append(func)
            return func
        
        return func
    
    def visit_Variable(self, node: ir.Variable):
        value = self.visit(node.value)
        if (symbol := self.scope.symbol_table.get(node.name)) is not None:
            return self.visit(ir.Assignment(node.pos, symbol.type, node.name, value, node.op))
        
        self.scope.symbol_table.add(ir.Symbol(node.name, value.type, value, node.is_mutable))
        return ir.Variable(node.pos, value.type, node.name, value, node.is_mutable)
    
    def visit_Assignment(self, node: ir.Assignment):
        symbol = cast(ir.Symbol, self.scope.symbol_table.get(node.name))
        if symbol.is_mutable:
            node.pos.comptime_error(self.file, f'\'{node.name}\' is not mutable')
        
        symbol.value = node.value
        return self
    
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
                from gem import parse
                
                file = ir.File(gem_file, ir.Scope(), self.file.options)
                program = parse(file)
                AnalyserPass.run(file, program)
                
                self.scope.merge(file.scope)
                
                info(f'Imported gem library {node.path}')
        
        return node
    
    def visit_Return(self, node: ir.Return):
        value = self.visit(node.value)
        return ir.Return(node.pos, value.type, value)
    
    def visit_Int(self, node: ir.Int):
        return ir.Int(node.pos, self.visit(node.type), node.value)
    
    def visit_Float(self, node: ir.Float):
        return ir.Float(node.pos, self.visit(node.type), node.value)
    
    def visit_String(self, node: ir.String):
        return self.visit(ir.Call(node.pos, self.visit(node.type), 'string.new', [
            ir.StringLiteral(node.pos, self.scope.type_map.get('pointer'), node.value).to_arg(),
            ir.Int(node.pos, self.scope.type_map.get('int'), len(node.value)).to_arg()
        ]))
    
    def visit_StringLiteral(self, node: ir.StringLiteral):
        return ir.StringLiteral(node.pos, self.scope.type_map.get('pointer'), node.value)
    
    def visit_Bool(self, node: ir.Bool):
        return ir.Bool(node.pos, self.visit(node.type), node.value)
    
    def visit_Id(self, node: ir.Id):
        symbol = self.scope.symbol_table.get(node.name)
        typ = self.scope.type_map.tryget(node.name)
        if symbol is None and typ is None:
            node.pos.comptime_error(self.file, f'unknown symbol \'{node.name}\'')
        
        return ir.Id(node.pos, symbol.type if symbol is not None else cast(ir.Type, typ), node.name)
    
    def visit_Bracketed(self, node: ir.Bracketed):
        value = self.visit(node.value)
        return ir.Bracketed(node.pos, value.type, value)
    
    def visit_Ternary(self, node: ir.Ternary):
        cond = self.visit(node.cond)
        true = self.visit(node.true)
        false = self.visit(node.false)
        if cond.type != self.scope.type_map.get('bool'):
            node.pos.comptime_error(self.file, f'expected type \'bool\' for condition, got \'{cond.type}\'')
        
        if true.type != false.type:
            node.pos.comptime_error(self.file, 'ternary branches must have the same type')
        
        return ir.Ternary(node.pos, true.type, cond, true, false)
    
    def fix_arg(self, arg: ir.Arg, param: ir.Param):
        if isinstance(param.type, ir.ReferenceType) and not isinstance(arg.type, ir.ReferenceType):
            if not isinstance(arg.value, ir.Id):
                arg.pos.comptime_error(self.file, 'attempt to get a reference to non-id')
            
            return self.visit(ir.Ref(arg.pos, arg.type, arg.value.name)).to_arg()
        
        return arg
    
    def visit_Call(self, node: ir.Call):
        symbol = self.scope.symbol_table.get(node.callee)
        if symbol is None:
            node.pos.comptime_error(self.file, f'unknown symbol \'{node.callee}\'')

        func = cast(ir.Function, symbol.value)
        args = [self.visit(arg) for arg in node.args]
        for overload in func.overloads + [func]:
            info(f'Checking if {overload.name}\'s arguments match')
            if not overload.match_params(args):
                continue
            
            new_args = [self.fix_arg(arg, param) for arg, param in zip(args, overload.params)]
            callsite = overload.call(node.pos, new_args)
            if overload.is_generic:
                overload = self.visit_Function(overload, callsite)
                callsite = overload.call(node.pos, new_args)
            
            return callsite
        
        node.pos.comptime_error(self.file, f'no matching overload for function \'{node.callee}\' with given arguments')
    
    def visit_Operation(self, node: ir.Operation):
        left = self.visit(node.left)
        right = self.visit(node.right)
        left_type, right_type = left.type, right.type
        callee = f'{left_type}.{node.op}.{right_type}'
        if callee not in self.scope.symbol_table.symbols:
            node.pos.comptime_error(self.file, f'invalid operation \'{node.op}\' for types \'{left_type}\' and \'{right_type}\'')
        
        return self.visit(ir.Call(node.pos, left_type, callee, [
            ir.Arg(node.pos, left_type, left), ir.Arg(node.pos, right_type, right
        )]))
    
    def visit_Attribute(self, node: ir.Attribute):
        value = self.visit(node.value)
        value_type = value.type
        if isinstance(value_type, ir.ReferenceType):
            value_type = value_type.type
        
        callee = f'{value_type}.{node.attr}'
        args = [value.to_arg()] + (node.args if node.args is not None else [])
        symbol = self.scope.symbol_table.get(callee)
        if symbol is None:
            node.pos.comptime_error(self.file, f'no attribute \'{node.attr}\' for type \'{value.type}\'')
        
        func = cast(ir.Function, symbol.value)
        if func.flags.static:
            args = args[1:]
        
        return self.visit(ir.Call(node.pos, value.type, callee, args))
    
    def visit_New(self, node: ir.New):
        new_type = self.visit_Type(node.new_type)
        callee = f'{new_type}.new'
        symbol = self.scope.symbol_table.get(callee)
        if symbol is None:
            node.pos.comptime_error(self.file, f'no constructor for type \'{new_type}\'')
        
        return self.visit(ir.Attribute(
            node.pos, new_type, ir.Id(node.new_type.pos, new_type, str(new_type)), 'new', node.args
        ))
    
    def visit_Ref(self, node: ir.Ref):
        symbol = self.scope.symbol_table.get(node.name)
        if symbol is None:
            node.pos.comptime_error(self.file, f'reference to {node.name} no longer exists')
        
        return ir.Ref(node.pos, self.visit(ir.ReferenceType(symbol.type)), node.name)
