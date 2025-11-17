from typing import override

from llvmlite import ir as lir

from gem.codegen_utils import create_static_buffer, create_string_constant, llint, create_struct_value
from gem.lib import function, DefinitionContext, Class
from gem import ir


class int(Class):
    @override
    def init(self):
        BUF_SIZE = 16
        
        @function(self, self.scope.type_map.get('string'), [
            ir.Param(ir.Position.zero(), self.type, 'self')
        ], flags=ir.FunctionFlags(method=True))
        def to_string(ctx: DefinitionContext):
            self = ctx.arg_value(0)
            
            snprintf = ctx.c_registry.get('snprintf')
            
            buf = create_static_buffer(ctx.module, lir.IntType(8), BUF_SIZE, 'buf', ctx.builder)
            if 'int_fmt' in ctx.module.globals:
                fmt = ctx.module.get_global('int_fmt')
            else:
                fmt = create_string_constant(ctx.module, '%d', 'int_fmt')
            
            written = ctx.builder.call(snprintf, [buf, llint(BUF_SIZE), fmt, self], 'written')
            return create_struct_value(
                ctx.builder, ctx.type(ctx.scope.type_map.get('string')), [buf, written], 'string'
            )
        
        @function(self, self.type, [
            ir.Param(ir.Position.zero(), self.type, 'a'), ir.Param(ir.Position.zero(), self.type, 'b')
        ], override_name=f'{self.type}.+.{self.type}')
        def add(ctx: DefinitionContext):
            a = ctx.arg_value(0)
            b = ctx.arg_value(1)
            return ctx.builder.add(a, b, 'add')
