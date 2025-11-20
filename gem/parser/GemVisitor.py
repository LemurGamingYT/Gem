# Generated from gem/Gem.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .GemParser import GemParser
else:
    from GemParser import GemParser

# This class defines a complete generic visitor for a parse tree produced by GemParser.

class GemVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by GemParser#program.
    def visitProgram(self, ctx:GemParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#arg.
    def visitArg(self, ctx:GemParser.ArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#args.
    def visitArgs(self, ctx:GemParser.ArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#param.
    def visitParam(self, ctx:GemParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#params.
    def visitParams(self, ctx:GemParser.ParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#genericParam.
    def visitGenericParam(self, ctx:GemParser.GenericParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#genericParams.
    def visitGenericParams(self, ctx:GemParser.GenericParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#type.
    def visitType(self, ctx:GemParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#stmt.
    def visitStmt(self, ctx:GemParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#bodyStmt.
    def visitBodyStmt(self, ctx:GemParser.BodyStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#return.
    def visitReturn(self, ctx:GemParser.ReturnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#break.
    def visitBreak(self, ctx:GemParser.BreakContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#continue.
    def visitContinue(self, ctx:GemParser.ContinueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#body.
    def visitBody(self, ctx:GemParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#returnArrow.
    def visitReturnArrow(self, ctx:GemParser.ReturnArrowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#funcName.
    def visitFuncName(self, ctx:GemParser.FuncNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#ifStmt.
    def visitIfStmt(self, ctx:GemParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#elseifStmt.
    def visitElseifStmt(self, ctx:GemParser.ElseifStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#elseStmt.
    def visitElseStmt(self, ctx:GemParser.ElseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#whileStmt.
    def visitWhileStmt(self, ctx:GemParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#useStmt.
    def visitUseStmt(self, ctx:GemParser.UseStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#funcAssign.
    def visitFuncAssign(self, ctx:GemParser.FuncAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#varAssign.
    def visitVarAssign(self, ctx:GemParser.VarAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#new.
    def visitNew(self, ctx:GemParser.NewContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#string.
    def visitString(self, ctx:GemParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#bool.
    def visitBool(self, ctx:GemParser.BoolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#unary.
    def visitUnary(self, ctx:GemParser.UnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#float.
    def visitFloat(self, ctx:GemParser.FloatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#int.
    def visitInt(self, ctx:GemParser.IntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#logical.
    def visitLogical(self, ctx:GemParser.LogicalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#call.
    def visitCall(self, ctx:GemParser.CallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#cast.
    def visitCast(self, ctx:GemParser.CastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#paren.
    def visitParen(self, ctx:GemParser.ParenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#relational.
    def visitRelational(self, ctx:GemParser.RelationalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#id.
    def visitId(self, ctx:GemParser.IdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#multiplication.
    def visitMultiplication(self, ctx:GemParser.MultiplicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#attr.
    def visitAttr(self, ctx:GemParser.AttrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#ternary.
    def visitTernary(self, ctx:GemParser.TernaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GemParser#addition.
    def visitAddition(self, ctx:GemParser.AdditionContext):
        return self.visitChildren(ctx)



del GemParser