from typing import Any, cast
from copy import deepcopy
from abc import ABC

from gem.ir import Node, Scope


def run_pass(pass_class: type['CompilerPass'], node: Node, scope: Scope):
    return pass_class(scope).run_on(node)


class CompilerPass(ABC):
    def __init__(self, scope: Scope):
        self.scope = scope
    
    def run_on(self, node: Node):
        method_name = f'run_on_{node.__class__.__name__}'
        if hasattr(self, method_name):
            method = getattr(self, method_name, None)
            if method is None or not callable(method):
                node.pos.comptime_error(self.scope, 'unknown node type')
            
            res = cast(Any, method)(node)
            if res is not None:
                return res
        
        return self.run_on_children(node)

    def run_on_children(self, node: Node):
        def recursive_run_on_children(node):
            if not isinstance(node, Node):
                return node
            
            for k, v in node.__dict__.items():
                if k == 'parent':
                    continue

                if isinstance(v, Node):
                    setattr(node, k, self.run_on(v))
                elif isinstance(v, list):
                    setattr(node, k, [self.run_on(item) for item in v])
                elif isinstance(v, dict):
                    setattr(node, k, {self.run_on(k): self.run_on(v) for k, v in v.items()})
            
            return node

        new_node = deepcopy(node)
        recursive_run_on_children(new_node)
        return new_node
