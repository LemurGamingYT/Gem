from gem.passes import CompilerPass
from gem.ir import (
    Program, Function, Body, Return, Call, Constant, Id, Bracketed, Param, Variable, Attribute,
    Operation, Reference, Cast, If, While, Break, Continue, Ternary, Foreach, For, Increment,
    Decrement
)


class GemCodeGeneration(CompilerPass):
    def run_on_Program(self, node: Program):
        stmts_str = '\n'.join(self.run_on(stmt) for stmt in node.stmts) + '\n'
        return f'{self.scope.includes_str}\n{self.scope.toplevel_str}\n{stmts_str}'
    
    def run_on_Param(self, node: Param):
        return f'{node.type.c_type} {node.name}'
    
    def run_on_Function(self, node: Function):
        params_str = ', '.join(self.run_on(param) for param in node.params)
        if node.body is not None:
            body = f' {{\n{self.run_on(node.body)}\n}}'
        else:
            body = ';'

        if len(node.params) == 0:
            params_str = 'void'
        
        return f'{node.type.c_type} {node.name}({params_str}){body}\n'
    
    def run_on_Variable(self, node: Variable):
        value = self.run_on(node.value)
        if node.is_assignment:
            return f'{node.name} = {value}'
        
        return f'{node.type.c_type} {node.name} = {value}'
    
    def run_on_Body(self, node: Body):
        nodes = [self.run_on(stmt) for stmt in node.body]
        return '\n'.join(node + ';' for node in nodes)
    
    def run_on_Foreach(self, _: Foreach):
        raise NotImplementedError
    
    def run_on_For(self, node: For):
        start = self.run_on(node.start)
        end = self.run_on(node.end)
        step = self.run_on(node.step)
        body = self.run_on(node.body)
        return f"""for ({node.type.c_type} {node.var_name} = {start}; {end}; {step}) {{
{body}
}}"""

    def run_on_Return(self, node: Return):
        return f'return {self.run_on(node.value)}'
    
    def run_on_Constant(self, node: Constant):
        if str(node.type) == 'string':
            return f'make_string({node.value}, {len(node.value) - 2})'
        elif str(node.type) == 'bool':
            return 'true' if node.value else 'false'
        
        return str(node.value)
    
    def run_on_Id(self, node: Id):
        return node.name
    
    def run_on_Bracketed(self, node: Bracketed):
        return f'({self.run_on(node.value)})'
    
    def run_on_Call(self, node: Call):
        args_str = ', '.join(self.run_on(arg) for arg in node.args)
        return f'{node.name}({args_str})'
    
    def run_on_Attribute(self, node: Attribute):
        accessor = '->' if node.object_is_a_pointer else '.'
        args = f'({", ".join(self.run_on(arg) for arg in node.args)})' if node.args is not None else ''
        return f'{self.run_on(node.value)}{accessor}{node.attr}{args}'
    
    def run_on_Operation(self, node: Operation):
        return f'{self.run_on(node.lhs)} {node.op} {self.run_on(node.rhs)}'
    
    def run_on_Reference(self, node: Reference):
        return f'&{self.run_on(node.name)}'
    
    def run_on_Cast(self, node: Cast):
        return f'({node.type.c_type})({self.run_on(node.value)})'
    
    def run_on_If(self, node: If):
        else_str = ''
        if node.else_body is not None:
            else_str = f'else {{\n{self.run_on(node.else_body)}\n}}'
        
        elseifs_str = ''
        if len(node.elseifs) > 0:
            elseifs_str = '\n'.join(
                f'else if ({self.run_on(cond)}) {{\n{self.run_on(body)}\n}}'
                for cond, body in node.elseifs
            )
        
        return f'if ({self.run_on(node.cond)}) {{\n{self.run_on(node.body)}\n}}{elseifs_str}{else_str}'
    
    def run_on_While(self, node: While):
        return f'while ({self.run_on(node.cond)}) {{\n{self.run_on(node.body)}\n}}'
    
    def run_on_Break(self, _: Break):
        return 'break'
    
    def run_on_Continue(self, _: Continue):
        return 'continue'
    
    def run_on_Ternary(self, node: Ternary):
        return f'({self.run_on(node.cond)} ? {self.run_on(node.true)} : {self.run_on(node.false)})'

    def run_on_Increment(self, node: Increment):
        return f'{self.run_on(node.var)}++'

    def run_on_Decrement(self, node: Decrement):
        return f'{self.run_on(node.var)}--'
