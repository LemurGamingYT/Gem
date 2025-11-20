from typing import Any, TypeVar
from logging import warning
from abc import ABC

from gem.ir import Node, Program, Scope


NodeType = TypeVar('NodeType', bound=Node)

class CompilerPass(ABC):
    def __init__(self, scope: Scope, options):
        self.scope = scope
        self.options = options
    
    @classmethod
    def run(cls, scope: Scope, options, program: Program) -> Any:
        self = cls(scope, options)
        return self.visit(program)
    
    def visit(self, node: NodeType) -> NodeType | Any:
        method_name = f'visit_{type(node).__name__}'
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return method(node)
        else:
            warning(f'No method {method_name}, returning unchanged node')
            return node
