from gem.lib import Lib, DefinitionContext, builtin
from gem import ir


class core(Lib):
    def init(self):
        @builtin(self, self.scope.type_map.get('int'), [
            ir.Param(ir.Position.zero(), self.scope.type_map.get('int'), 'a'),
            ir.Param(ir.Position.zero(), self.scope.type_map.get('int'), 'b')
        ])
        def test_add(ctx: DefinitionContext):
            a = ctx.arg_value(0)
            b = ctx.arg_value(1)
            return ctx.builder.add(a, b, 'sum')
