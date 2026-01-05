from typing import cast

from gem.passes import CompilerPass
from gem import ir


class GenericsResolverPass(CompilerPass):
    def visit_Program(self, node: ir.Program):
        return ir.Program(node.pos, [self.visit(stmt) for stmt in node.nodes])
    
    def visit_Body(self, node: ir.Body):
        return ir.Body(node.pos, node.type, [self.visit(stmt) for stmt in node.nodes])
    
    def visit_GenericFunction(self, node: ir.Function, callsite: ir.Call):
        generic_map = node.create_generic_map(callsite.args)
        ret_type = node.replace_generic(node.ret_type, generic_map)
        extend_type = node.replace_generic(node.extend_type, generic_map) if node.extend_type is not None else None
        params = [
            ir.Param(param.pos, node.replace_generic(param.type, generic_map), param.name, param.is_mutable)
            for param in node.params
        ]
        
        func_name = node.name
        generic_map_str = '<' + ', '.join(str(type) for type in generic_map) + '>'
        func_name += generic_map_str
        
        func = ir.Function(
            node.pos, ret_type, func_name, params, node.body, node.overloads, node.flags, extend_type
        )
        
        if func.body is not None:
            with self.child_scope():
                for param in params:
                    self.scope.symbol_table.add(ir.Symbol(
                        param.name, param.type, param, self.file, is_mutable=param.is_mutable
                    ))
                
                func.body = self.visit(func.body)
        
        symbol = self.scope.symbol_table.get(node.name)
        if symbol is None:
            node.pos.comptime_error(self.file, f'generic function \'{node.name}\' does not exist')
        
        # TODO: place at the bottom of the function's original source code file
        node.overloads.append(func)
        self.scope.symbol_table.add(ir.Symbol(func.name, self.scope.type_map.get('function'), func, symbol.source))
        return func
    
    def visit_Function(self, node: ir.Function, callsite: ir.Call | None = None):
        if node.is_generic:
            if callsite is None:
                self.scope.symbol_table.add(ir.Symbol(node.name, self.scope.type_map.get('function'), node, self.file))
                return node
            else:
                return self.visit_GenericFunction(node, callsite)
        
        if node.body is not None:
            with self.child_scope():
                for param in node.params:
                    self.scope.symbol_table.add(ir.Symbol(
                        param.name, param.type, param, self.file, is_mutable=param.is_mutable
                    ))
                
                node.body = self.visit(node.body)
        
        return node
    
    def visit_Call(self, node: ir.Call):
        symbol = self.scope.symbol_table.get(node.callee)
        if symbol is None:
            node.pos.comptime_error(self.file, f'unknown function \'{node.callee}\'')
        
        func = cast(ir.Function, symbol.value)
        if func.is_generic:
            func = self.visit_Function(func, node)
        
        return func.call(node.pos, node.args)
