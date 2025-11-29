# Generated from gem/Gem.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,44,256,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,1,0,5,0,44,8,0,10,0,12,0,47,9,0,1,0,1,0,1,1,1,1,1,2,1,2,1,2,
        5,2,56,8,2,10,2,12,2,59,9,2,1,3,3,3,62,8,3,1,3,1,3,1,3,1,4,1,4,1,
        4,5,4,70,8,4,10,4,12,4,73,9,4,1,5,1,5,1,6,1,6,1,6,1,6,5,6,81,8,6,
        10,6,12,6,84,9,6,1,6,1,6,1,7,1,7,1,7,1,7,1,7,5,7,93,8,7,10,7,12,
        7,96,9,7,1,8,1,8,1,8,1,8,1,8,1,8,3,8,104,8,8,1,9,1,9,1,9,1,9,1,9,
        3,9,111,8,9,1,10,1,10,5,10,115,8,10,10,10,12,10,118,9,10,1,10,1,
        10,1,11,1,11,1,11,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,
        12,3,12,135,8,12,1,13,1,13,1,13,1,13,5,13,141,8,13,10,13,12,13,144,
        9,13,1,13,3,13,147,8,13,1,14,1,14,1,14,1,14,1,14,1,15,1,15,1,15,
        1,16,1,16,1,16,1,16,1,17,1,17,1,17,1,18,1,18,1,18,1,18,3,18,168,
        8,18,1,18,1,18,3,18,172,8,18,1,18,1,18,1,19,1,19,3,19,178,8,19,1,
        19,1,19,1,19,3,19,183,8,19,1,19,1,19,1,19,3,19,188,8,19,1,20,1,20,
        1,20,1,20,1,20,1,20,1,20,1,20,1,20,3,20,199,8,20,1,20,1,20,1,20,
        1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,3,20,215,
        8,20,1,20,1,20,1,20,1,20,3,20,221,8,20,1,20,1,20,1,20,1,20,1,20,
        1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,
        1,20,1,20,1,20,1,20,1,20,3,20,246,8,20,1,20,3,20,249,8,20,5,20,251,
        8,20,10,20,12,20,254,9,20,1,20,0,2,14,40,21,0,2,4,6,8,10,12,14,16,
        18,20,22,24,26,28,30,32,34,36,38,40,0,6,1,0,18,22,2,0,18,19,31,31,
        1,0,20,22,1,0,18,19,1,0,23,28,1,0,29,30,278,0,45,1,0,0,0,2,50,1,
        0,0,0,4,52,1,0,0,0,6,61,1,0,0,0,8,66,1,0,0,0,10,74,1,0,0,0,12,76,
        1,0,0,0,14,87,1,0,0,0,16,103,1,0,0,0,18,110,1,0,0,0,20,112,1,0,0,
        0,22,121,1,0,0,0,24,134,1,0,0,0,26,136,1,0,0,0,28,148,1,0,0,0,30,
        153,1,0,0,0,32,156,1,0,0,0,34,160,1,0,0,0,36,163,1,0,0,0,38,187,
        1,0,0,0,40,220,1,0,0,0,42,44,3,16,8,0,43,42,1,0,0,0,44,47,1,0,0,
        0,45,43,1,0,0,0,45,46,1,0,0,0,46,48,1,0,0,0,47,45,1,0,0,0,48,49,
        5,0,0,1,49,1,1,0,0,0,50,51,3,40,20,0,51,3,1,0,0,0,52,57,3,2,1,0,
        53,54,5,33,0,0,54,56,3,2,1,0,55,53,1,0,0,0,56,59,1,0,0,0,57,55,1,
        0,0,0,57,58,1,0,0,0,58,5,1,0,0,0,59,57,1,0,0,0,60,62,5,6,0,0,61,
        60,1,0,0,0,61,62,1,0,0,0,62,63,1,0,0,0,63,64,3,14,7,0,64,65,5,17,
        0,0,65,7,1,0,0,0,66,71,3,6,3,0,67,68,5,33,0,0,68,70,3,6,3,0,69,67,
        1,0,0,0,70,73,1,0,0,0,71,69,1,0,0,0,71,72,1,0,0,0,72,9,1,0,0,0,73,
        71,1,0,0,0,74,75,5,17,0,0,75,11,1,0,0,0,76,77,5,26,0,0,77,82,3,10,
        5,0,78,79,5,33,0,0,79,81,3,10,5,0,80,78,1,0,0,0,81,84,1,0,0,0,82,
        80,1,0,0,0,82,83,1,0,0,0,83,85,1,0,0,0,84,82,1,0,0,0,85,86,5,25,
        0,0,86,13,1,0,0,0,87,88,6,7,-1,0,88,89,5,17,0,0,89,94,1,0,0,0,90,
        91,10,1,0,0,91,93,5,40,0,0,92,90,1,0,0,0,93,96,1,0,0,0,94,92,1,0,
        0,0,94,95,1,0,0,0,95,15,1,0,0,0,96,94,1,0,0,0,97,104,3,38,19,0,98,
        104,3,36,18,0,99,104,3,32,16,0,100,104,3,26,13,0,101,104,3,34,17,
        0,102,104,3,40,20,0,103,97,1,0,0,0,103,98,1,0,0,0,103,99,1,0,0,0,
        103,100,1,0,0,0,103,101,1,0,0,0,103,102,1,0,0,0,104,17,1,0,0,0,105,
        111,3,16,8,0,106,107,5,7,0,0,107,111,3,40,20,0,108,111,5,10,0,0,
        109,111,5,11,0,0,110,105,1,0,0,0,110,106,1,0,0,0,110,108,1,0,0,0,
        110,109,1,0,0,0,111,19,1,0,0,0,112,116,5,37,0,0,113,115,3,18,9,0,
        114,113,1,0,0,0,115,118,1,0,0,0,116,114,1,0,0,0,116,117,1,0,0,0,
        117,119,1,0,0,0,118,116,1,0,0,0,119,120,5,38,0,0,120,21,1,0,0,0,
        121,122,5,39,0,0,122,123,3,14,7,0,123,23,1,0,0,0,124,125,3,14,7,
        0,125,126,5,32,0,0,126,127,5,17,0,0,127,135,1,0,0,0,128,129,3,14,
        7,0,129,130,5,32,0,0,130,131,5,3,0,0,131,135,1,0,0,0,132,135,5,17,
        0,0,133,135,5,3,0,0,134,124,1,0,0,0,134,128,1,0,0,0,134,132,1,0,
        0,0,134,133,1,0,0,0,135,25,1,0,0,0,136,137,5,1,0,0,137,138,3,40,
        20,0,138,142,3,20,10,0,139,141,3,28,14,0,140,139,1,0,0,0,141,144,
        1,0,0,0,142,140,1,0,0,0,142,143,1,0,0,0,143,146,1,0,0,0,144,142,
        1,0,0,0,145,147,3,30,15,0,146,145,1,0,0,0,146,147,1,0,0,0,147,27,
        1,0,0,0,148,149,5,5,0,0,149,150,5,1,0,0,150,151,3,40,20,0,151,152,
        3,20,10,0,152,29,1,0,0,0,153,154,5,5,0,0,154,155,3,20,10,0,155,31,
        1,0,0,0,156,157,5,9,0,0,157,158,3,40,20,0,158,159,3,20,10,0,159,
        33,1,0,0,0,160,161,5,2,0,0,161,162,5,15,0,0,162,35,1,0,0,0,163,164,
        5,4,0,0,164,165,3,24,12,0,165,167,5,35,0,0,166,168,3,8,4,0,167,166,
        1,0,0,0,167,168,1,0,0,0,168,169,1,0,0,0,169,171,5,36,0,0,170,172,
        3,22,11,0,171,170,1,0,0,0,171,172,1,0,0,0,172,173,1,0,0,0,173,174,
        3,20,10,0,174,37,1,0,0,0,175,177,5,17,0,0,176,178,7,0,0,0,177,176,
        1,0,0,0,177,178,1,0,0,0,178,179,1,0,0,0,179,180,5,34,0,0,180,188,
        3,40,20,0,181,183,5,6,0,0,182,181,1,0,0,0,182,183,1,0,0,0,183,184,
        1,0,0,0,184,185,5,17,0,0,185,186,5,34,0,0,186,188,3,40,20,0,187,
        175,1,0,0,0,187,182,1,0,0,0,188,39,1,0,0,0,189,190,6,20,-1,0,190,
        191,5,35,0,0,191,192,3,14,7,0,192,193,5,36,0,0,193,194,3,40,20,16,
        194,221,1,0,0,0,195,196,5,17,0,0,196,198,5,35,0,0,197,199,3,4,2,
        0,198,197,1,0,0,0,198,199,1,0,0,0,199,200,1,0,0,0,200,221,5,36,0,
        0,201,202,5,35,0,0,202,203,3,40,20,0,203,204,5,36,0,0,204,221,1,
        0,0,0,205,221,5,13,0,0,206,221,5,14,0,0,207,221,5,15,0,0,208,221,
        5,16,0,0,209,221,5,17,0,0,210,211,5,3,0,0,211,212,3,14,7,0,212,214,
        5,35,0,0,213,215,3,4,2,0,214,213,1,0,0,0,214,215,1,0,0,0,215,216,
        1,0,0,0,216,217,5,36,0,0,217,221,1,0,0,0,218,219,7,1,0,0,219,221,
        3,40,20,1,220,189,1,0,0,0,220,195,1,0,0,0,220,201,1,0,0,0,220,205,
        1,0,0,0,220,206,1,0,0,0,220,207,1,0,0,0,220,208,1,0,0,0,220,209,
        1,0,0,0,220,210,1,0,0,0,220,218,1,0,0,0,221,252,1,0,0,0,222,223,
        10,7,0,0,223,224,5,1,0,0,224,225,3,40,20,0,225,226,5,5,0,0,226,227,
        3,40,20,8,227,251,1,0,0,0,228,229,10,5,0,0,229,230,7,2,0,0,230,251,
        3,40,20,6,231,232,10,4,0,0,232,233,7,3,0,0,233,251,3,40,20,5,234,
        235,10,3,0,0,235,236,7,4,0,0,236,251,3,40,20,4,237,238,10,2,0,0,
        238,239,7,5,0,0,239,251,3,40,20,3,240,241,10,6,0,0,241,242,5,32,
        0,0,242,248,5,17,0,0,243,245,5,35,0,0,244,246,3,4,2,0,245,244,1,
        0,0,0,245,246,1,0,0,0,246,247,1,0,0,0,247,249,5,36,0,0,248,243,1,
        0,0,0,248,249,1,0,0,0,249,251,1,0,0,0,250,222,1,0,0,0,250,228,1,
        0,0,0,250,231,1,0,0,0,250,234,1,0,0,0,250,237,1,0,0,0,250,240,1,
        0,0,0,251,254,1,0,0,0,252,250,1,0,0,0,252,253,1,0,0,0,253,41,1,0,
        0,0,254,252,1,0,0,0,24,45,57,61,71,82,94,103,110,116,134,142,146,
        167,171,177,182,187,198,214,220,245,248,250,252
    ]

class GemParser ( Parser ):

    grammarFileName = "Gem.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'if'", "'use'", "'new'", "'fn'", "'else'", 
                     "'mut'", "'return'", "'extern'", "'while'", "'break'", 
                     "'continue'", "'''", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'+'", "'-'", "'*'", "'/'", 
                     "'%'", "'=='", "'!='", "'>'", "'<'", "'>='", "'<='", 
                     "'&&'", "'||'", "'!'", "'.'", "','", "'='", "'('", 
                     "')'", "'{'", "'}'", "'->'", "'&'" ]

    symbolicNames = [ "<INVALID>", "IF", "USE", "NEW", "FUNC", "ELSE", "MUTABLE", 
                      "RETURN", "EXTERN", "WHILE", "BREAK", "CONTINUE", 
                      "APOSTROPHE", "INT", "FLOAT", "STRING", "BOOL", "ID", 
                      "ADD", "SUB", "MUL", "DIV", "MOD", "EEQ", "NEQ", "GT", 
                      "LT", "GTE", "LTE", "AND", "OR", "NOT", "DOT", "COMMA", 
                      "ASSIGN", "LPAREN", "RPAREN", "LBRACE", "RBRACE", 
                      "RETURNS", "AMPERSAND", "COMMENT", "MULTILINE_COMMENT", 
                      "WHITESPACE", "OTHER" ]

    RULE_program = 0
    RULE_arg = 1
    RULE_args = 2
    RULE_param = 3
    RULE_params = 4
    RULE_genericParam = 5
    RULE_genericParams = 6
    RULE_type = 7
    RULE_stmt = 8
    RULE_bodyStmts = 9
    RULE_body = 10
    RULE_returnArrow = 11
    RULE_funcName = 12
    RULE_ifStmt = 13
    RULE_elseifStmt = 14
    RULE_elseStmt = 15
    RULE_whileStmt = 16
    RULE_useStmt = 17
    RULE_funcAssign = 18
    RULE_varAssign = 19
    RULE_expr = 20

    ruleNames =  [ "program", "arg", "args", "param", "params", "genericParam", 
                   "genericParams", "type", "stmt", "bodyStmts", "body", 
                   "returnArrow", "funcName", "ifStmt", "elseifStmt", "elseStmt", 
                   "whileStmt", "useStmt", "funcAssign", "varAssign", "expr" ]

    EOF = Token.EOF
    IF=1
    USE=2
    NEW=3
    FUNC=4
    ELSE=5
    MUTABLE=6
    RETURN=7
    EXTERN=8
    WHILE=9
    BREAK=10
    CONTINUE=11
    APOSTROPHE=12
    INT=13
    FLOAT=14
    STRING=15
    BOOL=16
    ID=17
    ADD=18
    SUB=19
    MUL=20
    DIV=21
    MOD=22
    EEQ=23
    NEQ=24
    GT=25
    LT=26
    GTE=27
    LTE=28
    AND=29
    OR=30
    NOT=31
    DOT=32
    COMMA=33
    ASSIGN=34
    LPAREN=35
    RPAREN=36
    LBRACE=37
    RBRACE=38
    RETURNS=39
    AMPERSAND=40
    COMMENT=41
    MULTILINE_COMMENT=42
    WHITESPACE=43
    OTHER=44

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(GemParser.EOF, 0)

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GemParser.StmtContext)
            else:
                return self.getTypedRuleContext(GemParser.StmtContext,i)


        def getRuleIndex(self):
            return GemParser.RULE_program

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = GemParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 36508263006) != 0):
                self.state = 42
                self.stmt()
                self.state = 47
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 48
            self.match(GemParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(GemParser.ExprContext,0)


        def getRuleIndex(self):
            return GemParser.RULE_arg

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArg" ):
                return visitor.visitArg(self)
            else:
                return visitor.visitChildren(self)




    def arg(self):

        localctx = GemParser.ArgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_arg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 50
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arg(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GemParser.ArgContext)
            else:
                return self.getTypedRuleContext(GemParser.ArgContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(GemParser.COMMA)
            else:
                return self.getToken(GemParser.COMMA, i)

        def getRuleIndex(self):
            return GemParser.RULE_args

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgs" ):
                return visitor.visitArgs(self)
            else:
                return visitor.visitChildren(self)




    def args(self):

        localctx = GemParser.ArgsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_args)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 52
            self.arg()
            self.state = 57
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==33:
                self.state = 53
                self.match(GemParser.COMMA)
                self.state = 54
                self.arg()
                self.state = 59
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self):
            return self.getTypedRuleContext(GemParser.TypeContext,0)


        def ID(self):
            return self.getToken(GemParser.ID, 0)

        def MUTABLE(self):
            return self.getToken(GemParser.MUTABLE, 0)

        def getRuleIndex(self):
            return GemParser.RULE_param

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParam" ):
                return visitor.visitParam(self)
            else:
                return visitor.visitChildren(self)




    def param(self):

        localctx = GemParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 61
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==6:
                self.state = 60
                self.match(GemParser.MUTABLE)


            self.state = 63
            self.type_(0)
            self.state = 64
            self.match(GemParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GemParser.ParamContext)
            else:
                return self.getTypedRuleContext(GemParser.ParamContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(GemParser.COMMA)
            else:
                return self.getToken(GemParser.COMMA, i)

        def getRuleIndex(self):
            return GemParser.RULE_params

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParams" ):
                return visitor.visitParams(self)
            else:
                return visitor.visitChildren(self)




    def params(self):

        localctx = GemParser.ParamsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_params)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.param()
            self.state = 71
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==33:
                self.state = 67
                self.match(GemParser.COMMA)
                self.state = 68
                self.param()
                self.state = 73
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GenericParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(GemParser.ID, 0)

        def getRuleIndex(self):
            return GemParser.RULE_genericParam

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGenericParam" ):
                return visitor.visitGenericParam(self)
            else:
                return visitor.visitChildren(self)




    def genericParam(self):

        localctx = GemParser.GenericParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_genericParam)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 74
            self.match(GemParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GenericParamsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LT(self):
            return self.getToken(GemParser.LT, 0)

        def genericParam(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GemParser.GenericParamContext)
            else:
                return self.getTypedRuleContext(GemParser.GenericParamContext,i)


        def GT(self):
            return self.getToken(GemParser.GT, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(GemParser.COMMA)
            else:
                return self.getToken(GemParser.COMMA, i)

        def getRuleIndex(self):
            return GemParser.RULE_genericParams

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGenericParams" ):
                return visitor.visitGenericParams(self)
            else:
                return visitor.visitChildren(self)




    def genericParams(self):

        localctx = GemParser.GenericParamsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_genericParams)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 76
            self.match(GemParser.LT)
            self.state = 77
            self.genericParam()
            self.state = 82
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==33:
                self.state = 78
                self.match(GemParser.COMMA)
                self.state = 79
                self.genericParam()
                self.state = 84
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 85
            self.match(GemParser.GT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(GemParser.ID, 0)

        def type_(self):
            return self.getTypedRuleContext(GemParser.TypeContext,0)


        def AMPERSAND(self):
            return self.getToken(GemParser.AMPERSAND, 0)

        def getRuleIndex(self):
            return GemParser.RULE_type

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitType" ):
                return visitor.visitType(self)
            else:
                return visitor.visitChildren(self)



    def type_(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = GemParser.TypeContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 14
        self.enterRecursionRule(localctx, 14, self.RULE_type, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 88
            self.match(GemParser.ID)
            self._ctx.stop = self._input.LT(-1)
            self.state = 94
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = GemParser.TypeContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_type)
                    self.state = 90
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 91
                    self.match(GemParser.AMPERSAND) 
                self.state = 96
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class StmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varAssign(self):
            return self.getTypedRuleContext(GemParser.VarAssignContext,0)


        def funcAssign(self):
            return self.getTypedRuleContext(GemParser.FuncAssignContext,0)


        def whileStmt(self):
            return self.getTypedRuleContext(GemParser.WhileStmtContext,0)


        def ifStmt(self):
            return self.getTypedRuleContext(GemParser.IfStmtContext,0)


        def useStmt(self):
            return self.getTypedRuleContext(GemParser.UseStmtContext,0)


        def expr(self):
            return self.getTypedRuleContext(GemParser.ExprContext,0)


        def getRuleIndex(self):
            return GemParser.RULE_stmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStmt" ):
                return visitor.visitStmt(self)
            else:
                return visitor.visitChildren(self)




    def stmt(self):

        localctx = GemParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_stmt)
        try:
            self.state = 103
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 97
                self.varAssign()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 98
                self.funcAssign()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 99
                self.whileStmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 100
                self.ifStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 101
                self.useStmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 102
                self.expr(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BodyStmtsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return GemParser.RULE_bodyStmts

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class BreakContext(BodyStmtsContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.BodyStmtsContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BREAK(self):
            return self.getToken(GemParser.BREAK, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBreak" ):
                return visitor.visitBreak(self)
            else:
                return visitor.visitChildren(self)


    class BodyStmtContext(BodyStmtsContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.BodyStmtsContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def stmt(self):
            return self.getTypedRuleContext(GemParser.StmtContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBodyStmt" ):
                return visitor.visitBodyStmt(self)
            else:
                return visitor.visitChildren(self)


    class ContinueContext(BodyStmtsContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.BodyStmtsContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def CONTINUE(self):
            return self.getToken(GemParser.CONTINUE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContinue" ):
                return visitor.visitContinue(self)
            else:
                return visitor.visitChildren(self)


    class ReturnContext(BodyStmtsContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.BodyStmtsContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def RETURN(self):
            return self.getToken(GemParser.RETURN, 0)
        def expr(self):
            return self.getTypedRuleContext(GemParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturn" ):
                return visitor.visitReturn(self)
            else:
                return visitor.visitChildren(self)



    def bodyStmts(self):

        localctx = GemParser.BodyStmtsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_bodyStmts)
        try:
            self.state = 110
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2, 3, 4, 6, 9, 13, 14, 15, 16, 17, 18, 19, 31, 35]:
                localctx = GemParser.BodyStmtContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 105
                self.stmt()
                pass
            elif token in [7]:
                localctx = GemParser.ReturnContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 106
                self.match(GemParser.RETURN)
                self.state = 107
                self.expr(0)
                pass
            elif token in [10]:
                localctx = GemParser.BreakContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 108
                self.match(GemParser.BREAK)
                pass
            elif token in [11]:
                localctx = GemParser.ContinueContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 109
                self.match(GemParser.CONTINUE)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACE(self):
            return self.getToken(GemParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(GemParser.RBRACE, 0)

        def bodyStmts(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GemParser.BodyStmtsContext)
            else:
                return self.getTypedRuleContext(GemParser.BodyStmtsContext,i)


        def getRuleIndex(self):
            return GemParser.RULE_body

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBody" ):
                return visitor.visitBody(self)
            else:
                return visitor.visitChildren(self)




    def body(self):

        localctx = GemParser.BodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_body)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 112
            self.match(GemParser.LBRACE)
            self.state = 116
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 36508266206) != 0):
                self.state = 113
                self.bodyStmts()
                self.state = 118
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 119
            self.match(GemParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReturnArrowContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURNS(self):
            return self.getToken(GemParser.RETURNS, 0)

        def type_(self):
            return self.getTypedRuleContext(GemParser.TypeContext,0)


        def getRuleIndex(self):
            return GemParser.RULE_returnArrow

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnArrow" ):
                return visitor.visitReturnArrow(self)
            else:
                return visitor.visitChildren(self)




    def returnArrow(self):

        localctx = GemParser.ReturnArrowContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_returnArrow)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 121
            self.match(GemParser.RETURNS)
            self.state = 122
            self.type_(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FuncNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.extend_type = None # TypeContext

        def DOT(self):
            return self.getToken(GemParser.DOT, 0)

        def ID(self):
            return self.getToken(GemParser.ID, 0)

        def type_(self):
            return self.getTypedRuleContext(GemParser.TypeContext,0)


        def NEW(self):
            return self.getToken(GemParser.NEW, 0)

        def getRuleIndex(self):
            return GemParser.RULE_funcName

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFuncName" ):
                return visitor.visitFuncName(self)
            else:
                return visitor.visitChildren(self)




    def funcName(self):

        localctx = GemParser.FuncNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_funcName)
        try:
            self.state = 134
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 124
                localctx.extend_type = self.type_(0)
                self.state = 125
                self.match(GemParser.DOT)
                self.state = 126
                self.match(GemParser.ID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 128
                localctx.extend_type = self.type_(0)
                self.state = 129
                self.match(GemParser.DOT)
                self.state = 130
                self.match(GemParser.NEW)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 132
                self.match(GemParser.ID)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 133
                self.match(GemParser.NEW)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(GemParser.IF, 0)

        def expr(self):
            return self.getTypedRuleContext(GemParser.ExprContext,0)


        def body(self):
            return self.getTypedRuleContext(GemParser.BodyContext,0)


        def elseifStmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GemParser.ElseifStmtContext)
            else:
                return self.getTypedRuleContext(GemParser.ElseifStmtContext,i)


        def elseStmt(self):
            return self.getTypedRuleContext(GemParser.ElseStmtContext,0)


        def getRuleIndex(self):
            return GemParser.RULE_ifStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStmt" ):
                return visitor.visitIfStmt(self)
            else:
                return visitor.visitChildren(self)




    def ifStmt(self):

        localctx = GemParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_ifStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 136
            self.match(GemParser.IF)
            self.state = 137
            self.expr(0)
            self.state = 138
            self.body()
            self.state = 142
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 139
                    self.elseifStmt() 
                self.state = 144
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,10,self._ctx)

            self.state = 146
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==5:
                self.state = 145
                self.elseStmt()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElseifStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ELSE(self):
            return self.getToken(GemParser.ELSE, 0)

        def IF(self):
            return self.getToken(GemParser.IF, 0)

        def expr(self):
            return self.getTypedRuleContext(GemParser.ExprContext,0)


        def body(self):
            return self.getTypedRuleContext(GemParser.BodyContext,0)


        def getRuleIndex(self):
            return GemParser.RULE_elseifStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElseifStmt" ):
                return visitor.visitElseifStmt(self)
            else:
                return visitor.visitChildren(self)




    def elseifStmt(self):

        localctx = GemParser.ElseifStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_elseifStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 148
            self.match(GemParser.ELSE)
            self.state = 149
            self.match(GemParser.IF)
            self.state = 150
            self.expr(0)
            self.state = 151
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElseStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ELSE(self):
            return self.getToken(GemParser.ELSE, 0)

        def body(self):
            return self.getTypedRuleContext(GemParser.BodyContext,0)


        def getRuleIndex(self):
            return GemParser.RULE_elseStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElseStmt" ):
                return visitor.visitElseStmt(self)
            else:
                return visitor.visitChildren(self)




    def elseStmt(self):

        localctx = GemParser.ElseStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_elseStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 153
            self.match(GemParser.ELSE)
            self.state = 154
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhileStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHILE(self):
            return self.getToken(GemParser.WHILE, 0)

        def expr(self):
            return self.getTypedRuleContext(GemParser.ExprContext,0)


        def body(self):
            return self.getTypedRuleContext(GemParser.BodyContext,0)


        def getRuleIndex(self):
            return GemParser.RULE_whileStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStmt" ):
                return visitor.visitWhileStmt(self)
            else:
                return visitor.visitChildren(self)




    def whileStmt(self):

        localctx = GemParser.WhileStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_whileStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 156
            self.match(GemParser.WHILE)
            self.state = 157
            self.expr(0)
            self.state = 158
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UseStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def USE(self):
            return self.getToken(GemParser.USE, 0)

        def STRING(self):
            return self.getToken(GemParser.STRING, 0)

        def getRuleIndex(self):
            return GemParser.RULE_useStmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUseStmt" ):
                return visitor.visitUseStmt(self)
            else:
                return visitor.visitChildren(self)




    def useStmt(self):

        localctx = GemParser.UseStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_useStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 160
            self.match(GemParser.USE)
            self.state = 161
            self.match(GemParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FuncAssignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FUNC(self):
            return self.getToken(GemParser.FUNC, 0)

        def funcName(self):
            return self.getTypedRuleContext(GemParser.FuncNameContext,0)


        def LPAREN(self):
            return self.getToken(GemParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(GemParser.RPAREN, 0)

        def body(self):
            return self.getTypedRuleContext(GemParser.BodyContext,0)


        def params(self):
            return self.getTypedRuleContext(GemParser.ParamsContext,0)


        def returnArrow(self):
            return self.getTypedRuleContext(GemParser.ReturnArrowContext,0)


        def getRuleIndex(self):
            return GemParser.RULE_funcAssign

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFuncAssign" ):
                return visitor.visitFuncAssign(self)
            else:
                return visitor.visitChildren(self)




    def funcAssign(self):

        localctx = GemParser.FuncAssignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_funcAssign)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 163
            self.match(GemParser.FUNC)
            self.state = 164
            self.funcName()
            self.state = 165
            self.match(GemParser.LPAREN)
            self.state = 167
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==6 or _la==17:
                self.state = 166
                self.params()


            self.state = 169
            self.match(GemParser.RPAREN)
            self.state = 171
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==39:
                self.state = 170
                self.returnArrow()


            self.state = 173
            self.body()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarAssignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.op = None # Token

        def ID(self):
            return self.getToken(GemParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(GemParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(GemParser.ExprContext,0)


        def ADD(self):
            return self.getToken(GemParser.ADD, 0)

        def SUB(self):
            return self.getToken(GemParser.SUB, 0)

        def MUL(self):
            return self.getToken(GemParser.MUL, 0)

        def DIV(self):
            return self.getToken(GemParser.DIV, 0)

        def MOD(self):
            return self.getToken(GemParser.MOD, 0)

        def MUTABLE(self):
            return self.getToken(GemParser.MUTABLE, 0)

        def getRuleIndex(self):
            return GemParser.RULE_varAssign

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarAssign" ):
                return visitor.visitVarAssign(self)
            else:
                return visitor.visitChildren(self)




    def varAssign(self):

        localctx = GemParser.VarAssignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_varAssign)
        self._la = 0 # Token type
        try:
            self.state = 187
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 175
                self.match(GemParser.ID)
                self.state = 177
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 8126464) != 0):
                    self.state = 176
                    localctx.op = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8126464) != 0)):
                        localctx.op = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()


                self.state = 179
                self.match(GemParser.ASSIGN)
                self.state = 180
                self.expr(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 182
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 181
                    self.match(GemParser.MUTABLE)


                self.state = 184
                self.match(GemParser.ID)
                self.state = 185
                self.match(GemParser.ASSIGN)
                self.state = 186
                self.expr(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return GemParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class NewContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NEW(self):
            return self.getToken(GemParser.NEW, 0)
        def type_(self):
            return self.getTypedRuleContext(GemParser.TypeContext,0)

        def LPAREN(self):
            return self.getToken(GemParser.LPAREN, 0)
        def RPAREN(self):
            return self.getToken(GemParser.RPAREN, 0)
        def args(self):
            return self.getTypedRuleContext(GemParser.ArgsContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNew" ):
                return visitor.visitNew(self)
            else:
                return visitor.visitChildren(self)


    class StringContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(GemParser.STRING, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString" ):
                return visitor.visitString(self)
            else:
                return visitor.visitChildren(self)


    class BoolContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BOOL(self):
            return self.getToken(GemParser.BOOL, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBool" ):
                return visitor.visitBool(self)
            else:
                return visitor.visitChildren(self)


    class UnaryContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(GemParser.ExprContext,0)

        def NOT(self):
            return self.getToken(GemParser.NOT, 0)
        def SUB(self):
            return self.getToken(GemParser.SUB, 0)
        def ADD(self):
            return self.getToken(GemParser.ADD, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnary" ):
                return visitor.visitUnary(self)
            else:
                return visitor.visitChildren(self)


    class FloatContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def FLOAT(self):
            return self.getToken(GemParser.FLOAT, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFloat" ):
                return visitor.visitFloat(self)
            else:
                return visitor.visitChildren(self)


    class IntContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(GemParser.INT, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInt" ):
                return visitor.visitInt(self)
            else:
                return visitor.visitChildren(self)


    class LogicalContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GemParser.ExprContext)
            else:
                return self.getTypedRuleContext(GemParser.ExprContext,i)

        def AND(self):
            return self.getToken(GemParser.AND, 0)
        def OR(self):
            return self.getToken(GemParser.OR, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogical" ):
                return visitor.visitLogical(self)
            else:
                return visitor.visitChildren(self)


    class CallContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(GemParser.ID, 0)
        def LPAREN(self):
            return self.getToken(GemParser.LPAREN, 0)
        def RPAREN(self):
            return self.getToken(GemParser.RPAREN, 0)
        def args(self):
            return self.getTypedRuleContext(GemParser.ArgsContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCall" ):
                return visitor.visitCall(self)
            else:
                return visitor.visitChildren(self)


    class CastContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(GemParser.LPAREN, 0)
        def type_(self):
            return self.getTypedRuleContext(GemParser.TypeContext,0)

        def RPAREN(self):
            return self.getToken(GemParser.RPAREN, 0)
        def expr(self):
            return self.getTypedRuleContext(GemParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCast" ):
                return visitor.visitCast(self)
            else:
                return visitor.visitChildren(self)


    class ParenContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(GemParser.LPAREN, 0)
        def expr(self):
            return self.getTypedRuleContext(GemParser.ExprContext,0)

        def RPAREN(self):
            return self.getToken(GemParser.RPAREN, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParen" ):
                return visitor.visitParen(self)
            else:
                return visitor.visitChildren(self)


    class RelationalContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GemParser.ExprContext)
            else:
                return self.getTypedRuleContext(GemParser.ExprContext,i)

        def EEQ(self):
            return self.getToken(GemParser.EEQ, 0)
        def NEQ(self):
            return self.getToken(GemParser.NEQ, 0)
        def GT(self):
            return self.getToken(GemParser.GT, 0)
        def LT(self):
            return self.getToken(GemParser.LT, 0)
        def GTE(self):
            return self.getToken(GemParser.GTE, 0)
        def LTE(self):
            return self.getToken(GemParser.LTE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelational" ):
                return visitor.visitRelational(self)
            else:
                return visitor.visitChildren(self)


    class IdContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(GemParser.ID, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitId" ):
                return visitor.visitId(self)
            else:
                return visitor.visitChildren(self)


    class MultiplicationContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GemParser.ExprContext)
            else:
                return self.getTypedRuleContext(GemParser.ExprContext,i)

        def MUL(self):
            return self.getToken(GemParser.MUL, 0)
        def DIV(self):
            return self.getToken(GemParser.DIV, 0)
        def MOD(self):
            return self.getToken(GemParser.MOD, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplication" ):
                return visitor.visitMultiplication(self)
            else:
                return visitor.visitChildren(self)


    class AttrContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(GemParser.ExprContext,0)

        def DOT(self):
            return self.getToken(GemParser.DOT, 0)
        def ID(self):
            return self.getToken(GemParser.ID, 0)
        def LPAREN(self):
            return self.getToken(GemParser.LPAREN, 0)
        def RPAREN(self):
            return self.getToken(GemParser.RPAREN, 0)
        def args(self):
            return self.getTypedRuleContext(GemParser.ArgsContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAttr" ):
                return visitor.visitAttr(self)
            else:
                return visitor.visitChildren(self)


    class TernaryContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GemParser.ExprContext)
            else:
                return self.getTypedRuleContext(GemParser.ExprContext,i)

        def IF(self):
            return self.getToken(GemParser.IF, 0)
        def ELSE(self):
            return self.getToken(GemParser.ELSE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTernary" ):
                return visitor.visitTernary(self)
            else:
                return visitor.visitChildren(self)


    class AdditionContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a GemParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GemParser.ExprContext)
            else:
                return self.getTypedRuleContext(GemParser.ExprContext,i)

        def ADD(self):
            return self.getToken(GemParser.ADD, 0)
        def SUB(self):
            return self.getToken(GemParser.SUB, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddition" ):
                return visitor.visitAddition(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = GemParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 40
        self.enterRecursionRule(localctx, 40, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 220
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,19,self._ctx)
            if la_ == 1:
                localctx = GemParser.CastContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 190
                self.match(GemParser.LPAREN)
                self.state = 191
                self.type_(0)
                self.state = 192
                self.match(GemParser.RPAREN)
                self.state = 193
                self.expr(16)
                pass

            elif la_ == 2:
                localctx = GemParser.CallContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 195
                self.match(GemParser.ID)
                self.state = 196
                self.match(GemParser.LPAREN)
                self.state = 198
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 36508262408) != 0):
                    self.state = 197
                    self.args()


                self.state = 200
                self.match(GemParser.RPAREN)
                pass

            elif la_ == 3:
                localctx = GemParser.ParenContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 201
                self.match(GemParser.LPAREN)
                self.state = 202
                self.expr(0)
                self.state = 203
                self.match(GemParser.RPAREN)
                pass

            elif la_ == 4:
                localctx = GemParser.IntContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 205
                self.match(GemParser.INT)
                pass

            elif la_ == 5:
                localctx = GemParser.FloatContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 206
                self.match(GemParser.FLOAT)
                pass

            elif la_ == 6:
                localctx = GemParser.StringContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 207
                self.match(GemParser.STRING)
                pass

            elif la_ == 7:
                localctx = GemParser.BoolContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 208
                self.match(GemParser.BOOL)
                pass

            elif la_ == 8:
                localctx = GemParser.IdContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 209
                self.match(GemParser.ID)
                pass

            elif la_ == 9:
                localctx = GemParser.NewContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 210
                self.match(GemParser.NEW)
                self.state = 211
                self.type_(0)
                self.state = 212
                self.match(GemParser.LPAREN)
                self.state = 214
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 36508262408) != 0):
                    self.state = 213
                    self.args()


                self.state = 216
                self.match(GemParser.RPAREN)
                pass

            elif la_ == 10:
                localctx = GemParser.UnaryContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 218
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 2148270080) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 219
                self.expr(1)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 252
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,23,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 250
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,22,self._ctx)
                    if la_ == 1:
                        localctx = GemParser.TernaryContext(self, GemParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 222
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 223
                        self.match(GemParser.IF)
                        self.state = 224
                        self.expr(0)
                        self.state = 225
                        self.match(GemParser.ELSE)
                        self.state = 226
                        self.expr(8)
                        pass

                    elif la_ == 2:
                        localctx = GemParser.MultiplicationContext(self, GemParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 228
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 229
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 7340032) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 230
                        self.expr(6)
                        pass

                    elif la_ == 3:
                        localctx = GemParser.AdditionContext(self, GemParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 231
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 232
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==18 or _la==19):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 233
                        self.expr(5)
                        pass

                    elif la_ == 4:
                        localctx = GemParser.RelationalContext(self, GemParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 234
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 235
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 528482304) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 236
                        self.expr(4)
                        pass

                    elif la_ == 5:
                        localctx = GemParser.LogicalContext(self, GemParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 237
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 238
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==29 or _la==30):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 239
                        self.expr(3)
                        pass

                    elif la_ == 6:
                        localctx = GemParser.AttrContext(self, GemParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 240
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 241
                        self.match(GemParser.DOT)
                        self.state = 242
                        self.match(GemParser.ID)
                        self.state = 248
                        self._errHandler.sync(self)
                        la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
                        if la_ == 1:
                            self.state = 243
                            self.match(GemParser.LPAREN)
                            self.state = 245
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)
                            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 36508262408) != 0):
                                self.state = 244
                                self.args()


                            self.state = 247
                            self.match(GemParser.RPAREN)


                        pass

             
                self.state = 254
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,23,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[7] = self.type_sempred
        self._predicates[20] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def type_sempred(self, localctx:TypeContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 1)
         

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 1:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 6)
         




