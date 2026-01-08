from contextlib import contextmanager
from typing import Any, TypeVar
from dataclasses import fields
from logging import warning
from abc import ABC

from gem.ir import File, Node, Program, Scope, Type


NodeType = TypeVar('NodeType', bound=Node)

class CompilerPass(ABC):
    def __init__(self, file: File):
        self.file = file
    
    @contextmanager
    def child_scope(self):
        old_scope = self.scope
        self.scope = self.scope.make_child()
        yield
        self.scope = old_scope
    
    @property
    def scope(self):
        return self.file.scope
    
    @scope.setter
    def scope(self, value: Scope):
        self.file.scope = value
    
    @classmethod
    def run(cls, file: File, program: Program) -> Any:
        self = cls(file)
        return self.visit(program)
    
    def visit(self, node: NodeType) -> NodeType | Any:
        method_name = f'visit_{type(node).__name__}'
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return method(node)
        elif isinstance(node, Node):
            return self.visit_children(node)
        else:
            return node
    
    def visit_children(self, node: NodeType) -> NodeType | Any:
        node_fields = {}
        for field in fields(node):
            if not field.init:
                continue
            
            value = getattr(node, field.name)
            if isinstance(value, Node):
                node_fields[field.name] = self.visit(value)
            elif isinstance(value, list):
                node_fields[field.name] = [self.visit(element) for element in value]
            else:
                node_fields[field.name] = value
        
        return node.__class__(**node_fields)
