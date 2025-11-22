from typing import Any, TypeVar
from logging import warning
from abc import ABC

from gem.ir import File, Node, Program, Scope


NodeType = TypeVar('NodeType', bound=Node)

class CompilerPass(ABC):
    def __init__(self, file: File):
        self.file = file
    
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
        else:
            warning(f'No method {method_name}, returning unchanged node')
            return node
