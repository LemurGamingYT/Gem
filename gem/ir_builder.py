from typing import cast

from antlr4.error.ErrorListener import ErrorListener
from antlr4 import InputStream, CommonTokenStream
from antlr4.Token import CommonToken

from gem.parser import GemLexer, GemParser, GemVisitor
from gem.ir import (
    Position, Scope, Program, Constant, Call, Return, Function, Body, Param, Id, Bracketed, Variable,
    Attribute, Operation, Cast, If, While, Break, Continue, Ternary, Foreach
)


class GemErrorListener(ErrorListener):
    def __init__(self, scope: Scope):
        self.scope = scope

    def syntaxError(self, _, offendingSymbol: CommonToken, line: int, column: int, msg, e):
        pos = Position(line, column)
        pos.comptime_error(self.scope, f'invalid syntax \'{offendingSymbol.text}\'')


class GemIRBuilder(GemVisitor):
    def __init__(self, scope: Scope):
        self.scope = scope
    
    def pos(self, ctx: GemParser.ParseContext):
        return Position(ctx.start.line, ctx.start.column)
    
    def build(self):
        lexer = GemLexer(InputStream(self.scope.src))
        parser = GemParser(CommonTokenStream(lexer))
        parser.removeErrorListeners()
        parser.addErrorListener(GemErrorListener(self.scope))
        tree = parser.parse()
        return self.visitParse(tree)
    
    def visitParse(self, ctx: GemParser.ParseContext):
        return Program(
            self.pos(ctx), self.scope.get_type('nil'),
            [self.visitStmt(stmt) for stmt in ctx.stmt()]
        )
    
    def visitType(self, ctx: GemParser.TypeContext):
        type = self.scope.get_type(ctx.getText())
        if type is None:
            self.scope.pos.comptime_error(self.scope, f'unknown type \'{ctx.getText()}\'')
        
        return type
    
    def visitParams(self, ctx: GemParser.ParamsContext | None):
        return [self.visitParam(param) for param in ctx.param()] if ctx is not None else []
    
    def visitParam(self, ctx: GemParser.ParamContext) -> Param:
        return Param(
            self.pos(ctx), self.visitType(ctx.type_()),
            ctx.ID().getText()
        )
    
    def visitArgs(self, ctx: GemParser.ArgsContext | None):
        return [self.visitArg(arg) for arg in ctx.arg()] if ctx is not None else []
    
    def visitArg(self, ctx: GemParser.ArgContext):
        return self.visit(ctx.expr())
    
    def visitBodyStmt(self, ctx: GemParser.BodyStmtContext):
        if ctx.stmt():
            return self.visitStmt(ctx.stmt())
        elif ctx.RETURN():
            expr = self.visit(ctx.expr())
            return Return(self.pos(ctx), expr.type, expr)
        elif ctx.BREAK():
            return Break(self.pos(ctx), self.scope.get_type('nil'))
        elif ctx.CONTINUE():
            return Continue(self.pos(ctx), self.scope.get_type('nil'))
        
        raise NotImplementedError
    
    def visitBody(self, ctx: GemParser.BodyContext):
        self.scope = Scope(self.scope.file, self.pos(ctx), self.scope)
        nodes = [self.visitBodyStmt(stmt) for stmt in ctx.bodyStmt()]
        self.scope = cast(Scope, self.scope.parent)
        return Body(self.pos(ctx), self.scope.get_type('nil'), nodes)
    
    def visitIfStmt(self, ctx: GemParser.IfStmtContext):
        return If(
            self.pos(ctx), self.scope.get_type('nil'),
            self.visit(ctx.expr()), self.visitBody(ctx.body()),
            self.visitElseStmt(ctx.elseStmt()),
            [self.visitElseifStmt(elseif) for elseif in ctx.elseifStmt()]
        )

    def visitElseStmt(self, ctx: GemParser.ElseStmtContext | None):
        return self.visitBody(ctx.body()) if ctx is not None else None

    def visitElseifStmt(self, ctx: GemParser.ElseifStmtContext):
        return self.visit(ctx.expr()), self.visitBody(ctx.body())
    
    def visitWhileStmt(self, ctx: GemParser.WhileStmtContext):
        return While(
            self.pos(ctx), self.scope.get_type('nil'),
            self.visit(ctx.expr()), self.visitBody(ctx.body())
        )
    
    def visitForeachStmt(self, ctx: GemParser.ForeachStmtContext):
        var_name = ctx.ID().getText()
        body = self.visitBody(ctx.body())
        iterable = self.visit(ctx.expr())
        return Foreach(self.pos(ctx), self.scope.get_type('nil'), var_name, iterable, body)
    
    def visitGenericParams(self, ctx: GemParser.GenericParamsContext | None):
        return [param.getText() for param in ctx.ID()]\
            if ctx is not None else []
    
    def visitFuncAssign(self, ctx: GemParser.FuncAssignContext):
        pos = self.pos(ctx)
        name = ctx.ID().getText()
        ret_type = self.visitType(ctx.type_()) if ctx.type_() is not None else\
            self.scope.get_type('nil')
        params = self.visitParams(ctx.params())
        body = self.visitBody(ctx.body())
        generic_params = self.visitGenericParams(ctx.genericParams())
        return Function(pos, ret_type, name, params, body, generic_names=generic_params)
    
    def visitVarAssign(self, ctx: GemParser.VarAssignContext):
        pos = self.pos(ctx)
        name = ctx.ID().getText()
        expr = self.visit(ctx.expr())
        return Variable(
            pos, expr.type, name, expr, is_const=ctx.CONST() is not None,
            op=cast(CommonToken, ctx.op).text if ctx.op is not None else None
        )
    
    def visitInt(self, ctx: GemParser.IntContext):
        return Constant(self.pos(ctx), self.scope.get_type('int'), int(ctx.getText()))
    
    def visitFloat(self, ctx: GemParser.FloatContext):
        return Constant(self.pos(ctx), self.scope.get_type('float'), float(ctx.getText()))
    
    def visitString(self, ctx: GemParser.StringContext):
        return Constant(self.pos(ctx), self.scope.get_type('string'), ctx.getText())
    
    def visitBool(self, ctx: GemParser.BoolContext):
        return Constant(self.pos(ctx), self.scope.get_type('bool'), ctx.getText() == 'true')
    
    def visitId(self, ctx: GemParser.IdContext):
        return Id(self.pos(ctx), self.scope.get_type('any'), ctx.getText())
    
    def visitCall(self, ctx: GemParser.CallContext):
        return Call(
            self.pos(ctx), self.scope.get_type('any'), ctx.ID().getText(), self.visitArgs(ctx.args())
        )
    
    def visitParen(self, ctx: GemParser.ParenContext):
        expr = self.visit(ctx.expr())
        return Bracketed(self.pos(ctx), expr.type, expr)
    
    def visitAttr(self, ctx: GemParser.AttrContext):
        value = self.visit(ctx.expr())
        attr = ctx.ID().getText()
        args = self.visitArgs(ctx.args()) if ctx.LPAREN() is not None else None
        return Attribute(self.pos(ctx), self.scope.get_type('any'), value, attr, args)

    def visitCast(self, ctx: GemParser.CastContext):
        return Cast(self.pos(ctx), self.visitType(ctx.type_()), self.visit(ctx.expr()))
    
    def visitTernary(self, ctx: GemParser.TernaryContext):
        return Ternary(
            self.pos(ctx), self.scope.get_type('any'),
            self.visit(ctx.expr(1)), self.visit(ctx.expr(0)), self.visit(ctx.expr(2))
        )

    def visitOperation(self, ctx):
        op = ctx.op.text
        pos = self.pos(ctx)
        if isinstance(ctx.expr(), list):
            lhs = self.visit(ctx.expr(0))
            rhs = self.visit(ctx.expr(1))
        else:
            lhs = self.visit(ctx.expr())
            rhs = None
        
        return Operation(pos, self.scope.get_type('any'), op, lhs, rhs)

    def visitAddition(self, ctx: GemParser.AdditionContext):
        return self.visitOperation(ctx)
    
    def visitMultiplication(self, ctx: GemParser.MultiplicationContext):
        return self.visitOperation(ctx)
    
    def visitRelational(self, ctx: GemParser.RelationalContext):
        return self.visitOperation(ctx)
    
    def visitLogical(self, ctx: GemParser.LogicalContext):
        return self.visitOperation(ctx)
    
    def visitUnary(self, ctx: GemParser.UnaryContext):
        return self.visitOperation(ctx)
