from typing import override

from gem.codegen_utils import create_struct_value, NULL_BYTE, get_struct_field, llint
from gem.lib import function, DefinitionContext, Class
from gem import ir


class string(Class):
    @override
    def init(self):
        @function(self, self.type, [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('pointer'), 'ptr'),
            ir.Param(ir.Position.zero(), self.scope.type_map.get('int'), 'length')
        ], flags=ir.FunctionFlags(static=True, method=True))
        def new(ctx: DefinitionContext):
            ptr = ctx.arg_value(0)
            length = ctx.arg_value(1)
            
            memcpy = ctx.c_registry.get('memcpy')
            
            ptr_copy = ctx.call('gem_alloc', [ir.Arg(ctx.pos, ctx.scope.type_map.get('int'), length)])
            ctx.builder.call(memcpy, [ptr_copy, ptr, length, llint(0, 1)])
            
            last_char_ptr = ctx.builder.gep(ptr_copy, [llint(length)])
            ctx.builder.store(NULL_BYTE(), last_char_ptr)
            
            return create_struct_value(ctx.builder, ctx.type(self.type), [ptr_copy, length], 'string')
        
        @function(self, self.scope.type_map.get('nil'), [
            ir.Param(ir.Position.zero(), self.type, 'self')
        ], flags=ir.FunctionFlags(method=True))
        def destroy(ctx: DefinitionContext):
            self = ctx.arg_value(0)
            
            ptr = get_struct_field(ctx.builder, self, 0, 'ptr')
            ctx.call('gem_free', [ir.Arg(ctx.pos, ctx.scope.type_map.get('pointer'), ptr)])
        
        @function(self, self.type, [
            ir.Param(ir.Position.zero(), self.type, 'self')
        ], flags=ir.FunctionFlags(method=True))
        def to_string(ctx: DefinitionContext):
            return ctx.arg_value(0)
