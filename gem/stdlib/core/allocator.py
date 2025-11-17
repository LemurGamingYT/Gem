from typing import override

from gem.lib import function, DefinitionContext, Lib
from gem import ir


class allocator(Lib):
    @override
    def init(self):
        @function(self, self.scope.type_map.get('pointer'), [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('int'), 'size')
        ])
        def gem_alloc(ctx: DefinitionContext):
            size = ctx.arg_value(0)
            
            malloc = ctx.c_registry.get('malloc')
            ptr = ctx.builder.call(malloc, [size], 'ptr')
            # TODO: implement error handling for malloc failure
            
            return ptr
        
        @function(self, self.scope.type_map.get('nil'), [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('pointer'), 'ptr')
        ])
        def gem_free(ctx: DefinitionContext):
            ptr = ctx.arg_value(0)
            
            # TODO: prevent calling free on null pointer
            
            free = ctx.c_registry.get('free')
            ctx.builder.call(free, [ptr])
