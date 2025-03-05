from typing import cast

from gem.passes import CompilerPass
from gem.ir import (
    Program, Function, Body, Return, Call, Id, Bracketed, CallContext, EnvItem, Variable, Attribute,
    Operation, Scope, Constant, Type, Param, Foreach, For, Increment, get_end_points
)


op_map = {'+': 'add', '-': 'sub', '*': 'mul', '/': 'div', '%': 'mod', '==': 'eq', '!=': 'neq',
          '<': 'lt', '<=': 'lte', '>': 'gt', '>=': 'gte', '&&': 'and', '||': 'or', '!': 'not'}

class GemAnalyser(CompilerPass):
    def run_on_Program(self, node: Program):
        nodes = [self.run_on(stmt) for stmt in node.stmts]
        return Program(node.pos, node.type, nodes)
    
    def run_on_Body(self, node: Body):
        self.scope = self.scope.make_child(node.pos)
        nodes = [self.run_on(stmt) for stmt in node.body]
        self.scope = cast(Scope, self.scope.parent)
        return Body(node.pos, node.type, nodes)
    
    def run_on_Function(self, node: Function):
        params = node.params.copy()
        is_main_function = node.name == 'main'

        i8_ptr = Type('i8**', 'i8**')
        if is_main_function:
            if len(node.params) > 0:
                node.pos.comptime_error(self.scope, 'main function cannot have parameters')
            
            params = [
                Param(node.pos, self.scope.get_type('int'), 'argc'),
                Param(node.pos, i8_ptr, 'argv')
            ]

        func = Function(node.pos, node.type, node.name, params, node.body)
        self.scope.set_env(EnvItem(node.name, node.type, func))
        for param in params:
            self.scope.set_env(EnvItem(param.name, param.type, param))

        body: Body | None = self.run_on(node.body) if node.body is not None else None
        if is_main_function and body is not None:
            body.body.insert(0, Call(node.pos, self.scope.get_type('nil'), 'geminit', [
                Id(node.pos, self.scope.get_type('int'), 'argc'),
                Id(node.pos, i8_ptr, 'argv')
            ]))

            for i, _ in get_end_points(body.body):
                body.body.insert(i, Call(node.pos, self.scope.get_type('nil'), 'gemexit', []))
        
        func.body = body
        for param in params:
            self.scope.remove_env(param.name)

        return func
    
    def run_on_Variable(self, node: Variable):
        value = self.run_on(node.value)
        if (item := self.scope.get_env(node.name)) is not None:
            if item.type != value.type:
                node.pos.comptime_error(self.scope, f'cannot assign {value.type} to {item.type}')
            
            if item.is_const:
                node.pos.comptime_error(self.scope, f'cannot assign to const \'{node.name}\'')
            
            if node.op is not None:
                value = self.run_on(Operation(
                    node.pos, item.type, node.op, Id(node.pos, item.type, node.name), value,
                    parent=value
                ))

            return Variable(node.pos, value.type, node.name, value, True, node.is_const, node.op)
        
        self.scope.set_env(EnvItem(node.name, value.type, value, node.is_const))
        return Variable(node.pos, value.type, node.name, value, False, node.is_const, node.op)
    
    def run_on_Return(self, node: Return):
        value = self.run_on(node.value)
        return Return(node.pos, value.type, value)
    
    def run_on_Foreach(self, node: Foreach):
        iterable = self.run_on(node.iterable)
        iter_name = self.scope.unique_name
        int_ty = self.scope.get_type('int')

        len_ctx = CallContext.from_name(node.pos, self.scope, f'{iterable.type}_length', [iterable])
        if len_ctx is None:
            node.pos.comptime_error(self.scope, f'cannot get length of {iterable.type}')
        
        iter_ctx = CallContext.from_name(node.pos, self.scope, f'iter_{iterable.type}', [
            iterable, Id(node.pos, int_ty, iter_name)
        ])
        if iter_ctx is None:
            node.pos.comptime_error(self.scope, f'cannot iterate over {iterable.type}')
        
        self.scope.set_env(EnvItem(node.var_name, iter_ctx.ret_type, iter_ctx.invoke()))
        body: Body = self.run_on(node.body)
        body.body.insert(0, Variable(node.pos, iter_ctx.ret_type, node.var_name, iter_ctx.invoke()))
        self.scope.remove_env(node.var_name)
        
        return For(
            node.pos, int_ty, iter_name, Constant(node.pos, int_ty, '0'),
            Operation(node.pos, int_ty, '<', Id(node.pos, int_ty, iter_name), len_ctx.invoke()),
            Increment(node.pos, int_ty, Id(node.pos, int_ty, iter_name)),
            body
        )
    
    def run_on_Call(self, node: Call):
        args = [self.run_on(arg) for arg in node.args]
        ctx = CallContext.from_name(node.pos, self.scope, node.name, args)
        if ctx is None:
            node.pos.comptime_error(self.scope, f'unknown function \'{node.name}\'')
        
        return ctx.invoke()

    def run_on_Id(self, node: Id):
        item = self.scope.get_env(node.name)
        type = self.scope.get_type(node.name)
        if item is None and type is None:
            node.pos.comptime_error(self.scope, f'unknown identifier \'{node.name}\'')
        
        return Id(node.pos, type or item.type, node.name)
    
    def run_on_Bracketed(self, node: Bracketed):
        value = self.run_on(node.value)
        return Bracketed(node.pos, value.type, value)
    
    def run_on_Attribute(self, node: Attribute):
        value = self.run_on(node.value)
        args = [value] + ([self.run_on(arg) for arg in node.args] if node.args is not None else [])
        ctx = CallContext.from_name(node.pos, self.scope, f'{value.type}_{node.attr}', args)
        if ctx is None:
            node.pos.comptime_error(self.scope, f'unknown attribute \'{node.attr}\'')
        
        func = ctx.func
        if func.flags.static:
            ctx.args = ctx.args[1:]
        
        return ctx.invoke()
    
    def run_on_Operation(self, node: Operation):
        lhs = self.run_on(node.lhs)
        rhs = self.run_on(node.rhs) if node.rhs is not None else None
        op_name = op_map[node.op]
        if rhs is None:
            call_name = f'{op_name}_{lhs.type}'
            args = [lhs]
            err_msg = f'invalid operand type \'{lhs.type}\' for operator \'{node.op}\''
        else:
            call_name = f'{lhs.type}_{op_name}_{rhs.type}'
            args = [lhs, rhs]
            err_msg = f'invalid operands type \'{lhs.type}\' and type \'{rhs.type}\' for operator'\
                f' \'{node.op}\''
        
        ctx = CallContext.from_name(node.pos, self.scope, call_name, args)
        if ctx is None:
            node.pos.comptime_error(self.scope, err_msg)
        
        return ctx.invoke()
    
    def run_on_Constant(self, node: Constant):
        return node
