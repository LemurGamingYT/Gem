from antlr4.error.ErrorListener import ErrorListener as ANTLRErrorListener
from antlr4 import InputStream, CommonTokenStream
from antlr4.Token import CommonToken

from gem.parser.GemVisitor import GemVisitor
from gem.parser.GemParser import GemParser
from gem.parser.GemLexer import GemLexer
from gem import ir


class ErrorListener(ANTLRErrorListener):
    def __init__(self, scope: ir.Scope):
        self.scope = scope
    
    def syntaxError(self, recognizer, offendingSymbol: CommonToken, line: int, column: int, msg, e):
        pos = ir.Position(line, column)
        pos.comptime_error(self.scope, f'invalid syntax \'{offendingSymbol.text}\'')

class IRBuilder(GemVisitor):
    def __init__(self, scope: ir.Scope):
        self.scope = scope
    
    def pos(self, ctx):
        return ir.Position(ctx.start.line, ctx.start.column)
    
    def build(self):
        lexer = GemLexer(InputStream(self.scope.src))
        parser = GemParser(CommonTokenStream(lexer))
        parser.removeErrorListeners()
        parser.addErrorListener(ErrorListener(self.scope))
        return self.visitProgram(parser.program())
    
    def visitProgram(self, ctx):
        return ir.Program(
            self.pos(ctx), self.scope.type_map.get('any'), [self.visit(stmt) for stmt in ctx.stmt()]
        )
    
    def visitType(self, ctx):
        return ir.Type(self.pos(ctx), ctx.getText(), ctx.getText())
    
    def visitArgs(self, ctx):
        return [self.visitArg(arg) for arg in ctx.arg()] if ctx is not None else []
    
    def visitArg(self, ctx):
        value = self.visit(ctx.expr())
        return ir.Arg(self.pos(ctx), value.type, value)
    
    def visitReturn(self, ctx):
        expr = self.visit(ctx.expr())
        return ir.Return(self.pos(ctx), expr.type, expr)
    
    def visitBreak(self, ctx):
        return ir.Break(self.pos(ctx), self.scope.type_map.get('any'))
    
    def visitContinue(self, ctx):
        return ir.Continue(self.pos(ctx), self.scope.type_map.get('any'))
    
    def visitBody(self, ctx):
        return ir.Body(
            self.pos(ctx), self.scope.type_map.get('any'),
            [self.visit(stmt) for stmt in ctx.bodyStmts()]
        )
    
    def visitParams(self, ctx):
        return [self.visitParam(param) for param in ctx.param()] if ctx is not None else []
    
    def visitParam(self, ctx):
        return ir.Param(
            self.pos(ctx), self.visitType(ctx.type_()), ctx.ID().getText(),
            ctx.MUTABLE() is not None
        )
    
    def visitReturnArrow(self, ctx: GemParser.ReturnArrowContext):
        return self.visitType(ctx.type_()) if ctx is not None else self.scope.type_map.get('nil')
    
    def visitFuncName(self, ctx: GemParser.FuncNameContext):
        func_name = ctx.ID().getText() if ctx.ID() is not None else 'new'
        extend_type = self.visitType(ctx.type_()) if ctx.type_() is not None else None
        return func_name, extend_type
    
    # def visitExternStmt(self, ctx: GemParser.ExternStmtContext):
    #     return_type = self.visitReturnArrow(ctx.returnArrow())
    #     func_name, extend_type = self.visitFuncName(ctx.funcName())
    #     return ir.Function(
    #         self.pos(ctx), return_type, func_name,
    #         self.visitParams(ctx.params()), None,
    #         flags=ir.FunctionFlags(extern=True),
    #         extend_type=extend_type
    #     )
    
    def visitFuncAssign(self, ctx):
        return_type = self.visitReturnArrow(ctx.returnArrow())
        func_name, extend_type = self.visitFuncName(ctx.funcName())
        return ir.Function(
            self.pos(ctx), return_type, func_name,
            self.visitParams(ctx.params()), self.visitBody(ctx.body()),
            flags=ir.FunctionFlags(),
            extend_type=extend_type
        )
    
    def visitVarAssign(self, ctx):
        return ir.Variable(
            self.pos(ctx), self.scope.type_map.get('any'), ctx.ID().getText(), self.visit(ctx.expr()),
            ctx.MUTABLE() is not None, ctx.op.text if ctx.op is not None else None
        )
    
    def visitIfStmt(self, ctx):
        return ir.If(
            self.pos(ctx), self.scope.type_map.get('any'), self.visit(ctx.expr()),
            self.visitBody(ctx.body()), self.visitElseStmt(ctx.elseStmt()),
            [self.visitElseifStmt(elseif) for elseif in ctx.elseifStmt()]
        )
    
    def visitElseStmt(self, ctx):
        return self.visitBody(ctx.body()) if ctx is not None else None
    
    def visitElseifStmt(self, ctx):
        return ir.Elseif(
            self.pos(ctx), self.scope.type_map.get('any'),
            self.visit(ctx.expr()), self.visitBody(ctx.body())
        )
    
    def visitWhileStmt(self, ctx):
        return ir.While(
            self.pos(ctx), self.scope.type_map.get('any'), self.visit(ctx.expr()),
            self.visitBody(ctx.body())
        )
    
    def visitUseStmt(self, ctx):
        return ir.Use(self.pos(ctx), self.scope.type_map.get('any'), ctx.STRING().getText()[1:-1])
    
    def visitInt(self, ctx):
        return ir.Int(self.pos(ctx), self.scope.type_map.get('int'), int(ctx.getText()))
    
    def visitFloat(self, ctx):
        return ir.Float(self.pos(ctx), self.scope.type_map.get('float'), float(ctx.getText()))
    
    def visitString(self, ctx):
        return ir.String(self.pos(ctx), self.scope.type_map.get('string'), ctx.getText()[1:-1])
    
    def visitBool(self, ctx):
        return ir.Bool(self.pos(ctx), self.scope.type_map.get('bool'), ctx.getText() == 'true')
    
    def visitId(self, ctx):
        return ir.Id(self.pos(ctx), self.scope.type_map.get('any'), ctx.getText())
    
    def visitCall(self, ctx):
        return ir.Call(
            self.pos(ctx), self.scope.type_map.get('any'), ctx.ID().getText(), self.visitArgs(ctx.args())
        )
    
    def visitParen(self, ctx):
        expr = self.visit(ctx.expr())
        return ir.Bracketed(self.pos(ctx), expr.type, expr)
    
    def visitCast(self, ctx):
        return ir.Cast(self.pos(ctx), self.visitType(ctx.type_()), self.visit(ctx.expr()))
    
    def visitAttr(self, ctx):
        return ir.Attribute(
            self.pos(ctx), self.scope.type_map.get('any'), self.visit(ctx.expr()), ctx.ID().getText(),
            self.visitArgs(ctx.args()) if ctx.LPAREN() is not None else None
        )
    
    def visitTernary(self, ctx):
        return ir.Ternary(
            self.pos(ctx), self.scope.type_map.get('any'), self.visit(ctx.expr(1)),
            self.visit(ctx.expr(0)), self.visit(ctx.expr(2))
        )
    
    def visitNew(self, ctx):
        return ir.New(
            self.pos(ctx), self.scope.type_map.get('any'), self.visitType(ctx.type_()),
            self.visitArgs(ctx.args())
        )
    
    def visitOperation(self, ctx):
        pos = self.pos(ctx)
        op = ctx.op.text
        if isinstance(ctx.expr(), list):
            left, right = self.visit(ctx.expr(0)), self.visit(ctx.expr(1))
            return ir.Operation(pos, self.scope.type_map.get('any'), op, left, right)
        else:
            left = self.visit(ctx.expr())
            return ir.UnaryOperation(pos, self.scope.type_map.get('any'), op, left)
    
    def visitAddition(self, ctx):
        return self.visitOperation(ctx)
    
    def visitMultiplication(self, ctx):
        return self.visitOperation(ctx)
    
    def visitRelational(self, ctx):
        return self.visitOperation(ctx)
    
    def visitLogical(self, ctx):
        return self.visitOperation(ctx)
    
    def visitUnary(self, ctx):
        return self.visitOperation(ctx)
