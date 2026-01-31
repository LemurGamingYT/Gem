from typing import cast

from gem.passes import CompilerPass
from gem import ir


class NodeExpansionPass(CompilerPass):
    """Gem's attribute gets, sets, method calls, operations, etc are all actually just functions. This pass expands the
    those nodes out into their function calls."""
    
    def visit_Program(self, node: ir.Program):
        nodes = []
        for stmt in node.nodes:
            nodes.append(self.visit(stmt))
        
        return ir.Program(node.pos, nodes)
    
    def visit_Body(self, node: ir.Body):
        nodes = []
        for stmt in node.nodes:
            nodes.append(self.visit(stmt))
        
        return ir.Body(node.pos, node.type, nodes)
    
    def visit_Function(self, node: ir.Function):
        overloads = [self.visit(overload) for overload in node.overloads]
        func = ir.Function(node.pos, node.ret_type, node.name, node.params, node.body, overloads, node.flags)
        
        self.scope.symbol_table.add(ir.Symbol(func.name, self.scope.type_map.get('function'), func, self.file))
        
        body = node.body
        if body is not None:
            with self.child_scope():
                for param in node.params:
                    self.scope.symbol_table.add(ir.Symbol(
                        param.name, param.type, param, self.file, is_mutable=param.is_mutable
                    ))
                
                func.body = self.visit(body)
        
        return func
    
    def visit_Variable(self, node: ir.Variable):
        value = self.visit(node.value)
        if self.scope.symbol_table.has(node.name):
            return self.visit(ir.Assignment(node.pos, value.type, node.name, value, node.op))
        
        self.scope.symbol_table.add(ir.Symbol(node.name, value.type, value, self.file, is_mutable=node.is_mutable))
        return ir.Variable(node.pos, value.type, node.name, value, node.is_mutable)
    
    def visit_Assignment(self, node: ir.Assignment):
        symbol = cast(ir.Symbol, self.scope.symbol_table.get(node.name))
        if symbol.is_mutable:
            node.pos.comptime_error(symbol.source, f'\'{node.name}\' is not mutable')
        
        value = node.value
        if node.op is not None:
            value = self.visit(ir.Operation(
                node.pos, node.type, node.op, ir.Id(node.value.pos, node.type, node.name),
                value
            ))
        
        symbol.value = value
        return ir.Assignment(node.pos, node.type, node.name, value)
    
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
    
    def visit_Bracketed(self, node: ir.Bracketed):
        value = self.visit(node.value)
        return ir.Bracketed(node.pos, value.type, value)
    
    def visit_Ternary(self, node: ir.Ternary):
        cond = self.visit(node.cond)
        true = self.visit(node.true)
        false = self.visit(node.false)
        return ir.Ternary(node.pos, true.type, cond, true, false)
    
    def visit_Call(self, node: ir.Call):
        return ir.Call(node.pos, node.type, node.callee, [self.visit(arg) for arg in node.args])
    
    def visit_Operation(self, node: ir.Operation):
        left = self.visit(node.left)
        right = self.visit(node.right)
        left_type, right_type = left.type, right.type
        callee = f'{left_type}.{node.op}.{right_type}'
        if not self.scope.symbol_table.has(callee):
            node.pos.comptime_error(self.file, f'invalid operation \'{node.op}\' for types \'{left_type}\' and \'{right_type}\'')
        
        return self.visit(ir.Call(node.pos, left_type, callee, [left.to_arg(), right.to_arg()]))
    
    def visit_UnaryOperation(self, node: ir.UnaryOperation):
        value = self.visit(node.value)
        value_type = value.type
        callee = f'{node.op}.{value_type}'
        if not self.scope.symbol_table.has(callee):
            node.pos.comptime_error(self.file, f'invalid operation \'{node.op}\' on type \'{value_type}\'')
        
        return self.visit(ir.Call(node.pos, value_type, callee, [value.to_arg()]))
    
    def visit_Attribute(self, node: ir.Attribute):
        value = self.visit(node.value)
        value_type = value.type
        if isinstance(value_type, ir.ReferenceType):
            value_type = value_type.type
        
        callee = f'{value_type}.{node.attr}'
        args = [value.to_arg()] + (node.args or [])
        symbol = self.scope.symbol_table.get(callee)
        if symbol is None:
            node.pos.comptime_error(self.file, f'no attribute \'{node.attr}\' for type \'{value.type}\'')
        
        func = cast(ir.Function, symbol.value)
        if func.flags.static:
            args = args[1:]
        
        return self.visit(ir.Call(node.pos, func.type, callee, args))
    
    def visit_New(self, node: ir.New):
        new_type = self.visit(node.new_type)
        callee = f'{new_type}.new'
        symbol = self.scope.symbol_table.get(callee)
        if symbol is None:
            node.pos.comptime_error(self.file, f'no constructor for type \'{new_type}\'')
        
        return self.visit(ir.Attribute(
            node.pos, new_type, ir.Id(node.new_type.pos, new_type, str(new_type)), 'new', node.args
        ))
