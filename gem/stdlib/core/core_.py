from typing import override

from gem.lib import function, DefinitionContext, Lib, UnknownFunctionError
from gem.stdlib.core.allocator import allocator
from gem.codegen_utils import get_struct_field
from gem.stdlib.core.string import string
from gem.stdlib.core.float import float
from gem.stdlib.core.int import int
from gem import ir


class core(Lib):
    @override
    def init(self):
        self.add(allocator)
        self.add(string)
        self.add(float)
        self.add(int)
        
        @function(self, self.scope.type_map.get('nil'), [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('any'), 'value')
        ], override_name='print')
        def _print(ctx: DefinitionContext):
            value = ctx.arg(0)
            value_type = value.type
            
            puts = ctx.c_registry.get('puts')
            
            try:
                to_string = ctx.call(f'{value_type}.to_string', [value])
            except UnknownFunctionError:
                value.pos.comptime_error(self.scope, f'no cast to string for type \'{value_type}\'')
            
            to_string_ptr = get_struct_field(ctx.builder, to_string, 0, 'ptr')
            ctx.builder.call(puts, [to_string_ptr])
