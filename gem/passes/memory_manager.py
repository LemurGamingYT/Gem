from contextlib import contextmanager
from dataclasses import dataclass
from logging import info
from typing import cast

from gem.passes import CompilerPass
from gem import ir


DONT_EXTRACT = (
    ir.Type, ir.Variable, ir.Assignment, ir.ReferenceType, ir.Ref, ir.If, ir.Elseif, ir.While, ir.Break, ir.Continue, ir.Id,
    ir.Return, ir.Function
)


@dataclass
class OwnedObject:
    """Represents an object on the stack that owns it's heap-allocated memory. If an object is owned,
it's memory is freed when the object is destroyed and guarantees that the object is the only reference
to the memory. If the object is moved, the memory is not freed until the moved object is destroyed."""

    node: ir.Node
    moved: bool = False

@dataclass
class RefObject:
    """Represents a reference counted object. This means that the object is referenced in other areas
of the code and has a shared ownership. The memory is freed when the last reference to the object is
destroyed."""

    node: ir.Node


class MemoryManager(CompilerPass):
    def __init__(self, scope):
        super().__init__(scope)

        self.can_extract = True
    
    @contextmanager
    def child_scope(self):
        old_scope = self.scope
        self.scope = self.scope.make_child()
        yield
        self.scope = old_scope
    
    @contextmanager
    def no_extract(self):
        self.can_extract = False
        yield
        self.can_extract = True

    def extract(self, node: ir.Node):
        var_name = self.scope.unique_name
        var = ir.Variable(node.pos, node.type, var_name, node)
        self.scope.body_nodes.append(var)

        info(f'Creating owned object: {var_name} of type {node.type}')

        self.scope.symbol_table.add(ir.Symbol(var_name, node.type, OwnedObject(node)))
        return ir.Id(node.pos, node.type, var_name)

    def destroy_owned_value(self, pos: ir.Position, symbol: ir.Symbol):
        destroy_symbol = self.scope.symbol_table.get(f'{symbol.type}.destroy')
        assert destroy_symbol is not None, f'Could not find destroy method for type {symbol.type}'

        destroy_func = destroy_symbol.value
        assert isinstance(destroy_func, ir.Function), f'Invalid destroy method for type {symbol.type}'

        return [ir.Call(pos, destroy_func.ret_type, destroy_func.name, [
            ir.Id(pos, symbol.type, symbol.name).to_ref().to_arg()
        ])]

    def decrement_ref_count(self, pos: ir.Position, symbol: ir.Symbol):
        raise NotImplementedError('decrement_ref_count')

    def end_of_scope(self, pos: ir.Position):
        self.scope.body_nodes.append(ir.Comment(pos, 'end of scope'))
        for symbol in self.scope.symbol_table.symbols.values():
            destroy_method = self.scope.symbol_table.get(f'{symbol.type}.destroy')
            if destroy_method is None:
                continue

            if isinstance(symbol.value, OwnedObject):
                if symbol.value.moved:
                    continue
                
                self.scope.body_nodes.extend(self.destroy_owned_value(pos, symbol))
            elif isinstance(symbol.value, RefObject):
                self.scope.body_nodes.extend(self.decrement_ref_count(pos, symbol))

    def extract_node(self, node: ir.Node):
        if isinstance(node, DONT_EXTRACT) or not self.can_extract:
            return node

        destroy_method = self.scope.symbol_table.get(f'{node.type}.destroy')
        if destroy_method is None:
            return node
        
        return self.extract(node)

    def visit(self, node) -> ir.Node:
        return self.extract_node(super().visit(node))

    def visit_Program(self, node: ir.Program):
        info('Running memory manager')
        return ir.Program(node.pos, [self.visit(stmt) for stmt in node.nodes])

    def visit_Body(self, node: ir.Body):
        with self.child_scope():
            has_returned = False
            for stmt in node.nodes:
                stmt = self.visit(stmt)
                if isinstance(stmt, ir.Return):
                    self.end_of_scope(stmt.pos)
                    has_returned = True
    
                self.scope.body_nodes.append(stmt)
            
            if not has_returned:
                pos = node.pos
                if len(node.nodes) > 0:
                    pos = node.nodes[-1].pos
                
                self.end_of_scope(pos)
    
            return ir.Body(node.pos, node.type, self.scope.body_nodes)

    def visit_Function(self, node: ir.Function):
        body = node.body
        if body is not None:
            old_scope = self.scope
            self.scope = self.scope.make_child()
            for param in node.params:
                self.scope.symbol_table.add(ir.Symbol(param.name, param.type, OwnedObject(param, True), param.is_mutable))
            
            body = self.visit_Body(body)
            
            self.scope = old_scope
        
        return ir.Function(node.pos, node.type, node.name, node.params, body, node.overloads, node.flags, node.extend_type)

    def visit_Variable(self, node: ir.Variable):
        # don't extract a variable's value (the variable owns it's value)
        value = self.visit(node.value)
        if isinstance(value, ir.Id):
            symbol = cast(ir.Symbol, self.scope.symbol_table.get(value.name))
            if isinstance(symbol.value, OwnedObject):
                info(f'Transfering ownership of {value.name} to {node.name}')
                symbol.value.moved = True
                self.scope.symbol_table.add(ir.Symbol(node.name, value.type, OwnedObject(value), node.is_mutable))
                return ir.Variable(node.pos, value.type, node.name, value, node.is_mutable, node.op)

        self.scope.symbol_table.add(ir.Symbol(node.name, value.type, OwnedObject(value), node.is_mutable))
        return ir.Variable(node.pos, value.type, node.name, value, node.is_mutable)
    
    def visit_Assignment(self, node: ir.Assignment):
        assign_symbol = self.scope.symbol_table.get(node.name)
        assert assign_symbol is not None, f'Assignment symbol {node.name} not found in symbol table'
        
        value = self.visit(node.value)
        if isinstance(value, ir.Id):
            symbol = cast(ir.Symbol, self.scope.symbol_table.get(value.name))
            if isinstance(symbol.value, OwnedObject):
                info(f'Transfering ownership of {value.name} to {node.name}')
                symbol.value.moved = True
                self.scope.symbol_table.add(ir.Symbol(node.name, value.type, OwnedObject(value), assign_symbol.is_mutable))
                return ir.Assignment(node.pos, value.type, node.name, value, node.op)
        
        self.scope.symbol_table.add(ir.Symbol(node.name, value.type, OwnedObject(value), assign_symbol.is_mutable))
        return ir.Assignment(node.pos, value.type, node.name, value, node.op)
    
    def visit_Elseif(self, node: ir.Elseif):
        cond = self.visit(node.cond)
        body = self.visit_Body(node.body)
        return ir.Elseif(node.pos, cond, body)
    
    def visit_If(self, node: ir.If):
        cond = self.visit(node.cond)
        body = self.visit_Body(node.body)
        
        else_body = node.else_body
        if else_body is not None:
            else_body = self.visit_Body(else_body)
        
        return ir.If(node.pos, cond, body, else_body, [
            self.visit_Elseif(elseif) for elseif in node.elseifs
        ])
    
    def visit_While(self, node: ir.While):
        cond = self.visit(node.cond)
        body = self.visit_Body(node.body)
        return ir.While(node.pos, cond, body)

    def visit_Return(self, node: ir.Return):
        value = self.visit(node.value)
        if isinstance(value, ir.Id):
            symbol = cast(ir.Symbol, self.scope.symbol_table.get(value.name))
            if isinstance(symbol.value, OwnedObject):
                symbol.value.moved = True
        
        return ir.Return(node.pos, value.type, value)
    
    def visit_Arg(self, node: ir.Arg):
        value = self.visit(node.value)
        return ir.Arg(node.pos, value.type, value)
        
    def visit_Call(self, node: ir.Call):
        return ir.Call(node.pos, node.type, node.callee, [self.visit_Arg(arg) for arg in node.args])
