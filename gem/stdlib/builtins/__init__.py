from gem.ir import Scope, Position, CallContext, Call, Attribute, Constant, function


def setup(scope: Scope, pos: Position):
    @function(pos, scope, [('value', scope.get_type('any'))], scope.get_type('nil'))
    def _print(ctx: CallContext):
        ctx.scope.include('stdio.h')
        to_string = Attribute(
            ctx.pos, ctx.scope.get_type('string_lit'), ctx.call('to_string', [ctx.get_arg('value')]),
            'buf', None
        )

        fmt = Constant(ctx.pos, ctx.scope.get_type('string_lit'), r'"%s\n"')
        return Call(ctx.pos, ctx.scope.get_type('nil'), 'printf', [fmt, to_string])

    @function(pos, scope, [('value', scope.get_type('any'))], scope.get_type('string'))
    def _to_string(ctx: CallContext):
        value = ctx.get_arg('value')
        return ctx.call(f'{value.type}_to_string', [value])
