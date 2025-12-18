grammar Gem;

program: stmt* EOF;

arg: expr;
args: arg (COMMA arg)*;

param: MUTABLE? type ID;
params: param (COMMA param)*;

genericParam: ID;
genericParams: LT genericParam (COMMA genericParam)* GT;

type: ID | type AMPERSAND;

stmt
    : varAssign | funcAssign
    | whileStmt | ifStmt | useStmt | externStmt
    | expr
    ;

bodyStmts
    : stmt #bodyStmt
    | RETURN expr #return
    | BREAK #break
    | CONTINUE #continue
    ;

body: LBRACE bodyStmts* RBRACE;

returnArrow: RETURNS type;
funcName
    : extend_type=type DOT ID
    | extend_type=type DOT NEW
    | ID
    | NEW
    ;

ifStmt: IF expr body elseifStmt* elseStmt?;
elseifStmt: ELSE IF expr body;
elseStmt: ELSE body;
whileStmt: WHILE expr body;
useStmt: USE STRING;
externStmt: EXTERN ID;

funcAssign
    : FUNC funcName genericParams? LPAREN params? RPAREN returnArrow? body
    ;
varAssign
    : ID op=(ADD | SUB | MUL | DIV | MOD)? ASSIGN expr
    | MUTABLE? ID ASSIGN expr
    ;

expr
    : LPAREN type RPAREN expr #cast
    | ID LPAREN args? RPAREN #call
    | LPAREN expr RPAREN #paren
    | INT #int
    | FLOAT #float
    | STRING #string
    | BOOL #bool
    | ID #id
    | NEW type LPAREN args? RPAREN #new
    | expr IF expr ELSE expr #ternary
    | expr DOT ID (LPAREN args? RPAREN)? #attr
    | expr op=(MUL | DIV | MOD) expr #multiplication
    | expr op=(ADD | SUB) expr #addition
    | expr op=(EEQ | NEQ | GT | LT | GTE | LTE) expr #relational
    | expr op=(AND | OR) expr #logical
    | op=(NOT | SUB | ADD) expr #unary
    ;


// Basic keywords
IF: 'if';
USE: 'use';
NEW: 'new';
FUNC: 'fn';
ELSE: 'else';
MUTABLE: 'mut';
RETURN: 'return';
EXTERN: 'extern';

// Loop keywords
WHILE: 'while';
BREAK: 'break';
CONTINUE: 'continue';

APOSTROPHE: '\'';

INT: '-'? [0-9]+;
FLOAT: '-'? [0-9]* '.' [0-9]+;
STRING: '"' .*? '"' | APOSTROPHE .*? APOSTROPHE;
BOOL: 'true' | 'false';
ID: [a-zA-Z_][a-zA-Z_0-9]*;

ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
MOD: '%';
EEQ: '==';
NEQ: '!=';
GT: '>';
LT: '<';
GTE: '>=';
LTE: '<=';
AND: '&&';
OR: '||';
NOT: '!';

DOT: '.';
COMMA: ',';
ASSIGN: '=';
LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
RETURNS: '->';
AMPERSAND: '&';

COMMENT: '//' .*? '\n' -> skip;
MULTILINE_COMMENT: '/*' .*? '*/' -> skip;
WHITESPACE: [\t\r\n ]+ -> skip;
OTHER: .;
