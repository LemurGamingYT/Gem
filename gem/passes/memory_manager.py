from dataclasses import dataclass
from typing import cast

from gem.passes import CompilerPass
from gem.ir import (
    Node, Body, Return, Call, Id, Reference, Scope, Type, Position, Constant, Variable,
    Bracketed, Attribute, Operation, Cast, EnvItem
)


EXPRESSIONS = (Call, Constant, Id, Bracketed, Attribute, Operation, Cast)

@dataclass
class FreeItem:
    name: str
    type: Type
    value: Node

    def as_call(self, pos: Position, scope: Scope):
        method_name = f'free_{self.type.c_type}'
        return Call(pos, scope.get_type('nil'), method_name, [
            Reference(pos, self.type, Id(pos, self.type, self.name))
        ])
    
    def as_var(self, pos: Position):
        return Variable(pos, self.type, self.name, self.value, parent=self.value)
    
    def as_id(self, pos: Position):
        return Id(pos, self.type, self.name)


class MemoryManager(CompilerPass):
    def __init__(self, scope: Scope):
        super().__init__(scope)
    
    def free_func(self, type: Type):
        method_name = f'free_{type.c_type}'
        return self.scope.get_env(method_name)

    def run_on_Body(self, node: Body):
        self.scope = self.scope.make_child(node.pos)
        setattr(self.scope, 'prepend_nodes', [])
        setattr(self.scope, 'free_items', [])

        has_inserted = False
        nodes = []
        for stmt in node.body:
            stmt = self.run_on(stmt)
            if len((prepend_nodes := getattr(self.scope, 'prepend_nodes'))) > 0:
                nodes.extend(prepend_nodes)
                setattr(self.scope, 'prepend_nodes', [])
            
            if not isinstance(stmt, Return):
                nodes.append(stmt)
                continue

            for item in getattr(self.scope, 'free_items'):
                nodes.append(item.as_call(stmt.pos, self.scope))
            
            nodes.append(stmt)
            has_inserted = True
        
        if not has_inserted:
            for item in getattr(self.scope, 'free_items'):
                nodes.append(item.as_call(node.pos, self.scope))
        
        self.scope = cast(Scope, self.scope.parent)
        return Body(node.pos, node.type, nodes)
    
    def run_on_Variable(self, node: Variable):
        if self.free_func(node.type) is not None:
            self.scope.set_env(EnvItem(node.name, node.type, node.value))
            getattr(self.scope, 'free_items').append(FreeItem(node.name, node.type, node.value))
    
    def run_on(self, node: Node):
        node = super().run_on(node)
        if not isinstance(node, EXPRESSIONS):
            return node
        
        if self.free_func(node.type) is None:
            return node
        
        is_in_var = node.has_parent(Variable) is not None
        if is_in_var:
            return node
        
        is_in_return = node.has_parent(Return) is not None
        if is_in_return:
            return node
        
        item = FreeItem(self.scope.unique_name, node.type, node)

        # check if the value is an id with the same name as a variable, if so, return the variable
        # instead of creating a new variable with the same value as the variable
        for name in self.scope.env:
            if isinstance(node, Id) and node.name == name:
                return Id(node.pos, node.type, name)
            
            for child in node.get_descendants():
                if isinstance(child, Id) and child.name == name:
                    return node
        
        for descendant in node.get_descendants():
            if isinstance(descendant, Id) and descendant.name == item.name:
                return descendant
        
        getattr(self.scope, 'free_items').append(item)
        getattr(self.scope, 'prepend_nodes').append(item.as_var(node.pos))
        return item.as_id(node.pos)
