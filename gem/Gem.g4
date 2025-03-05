grammar Gem;

parse: stmt* EOF;

type: ID | type LBRACK RBRACK;

stmt
    : varAssign | funcAssign
    | whileStmt | ifStmt | useStmt | foreachStmt
    | expr
    ;

bodyStmt: stmt | RETURN expr | BREAK | CONTINUE;
body: LBRACE bodyStmt* RBRACE;

ifStmt: IF expr body elseifStmt* elseStmt?;
elseifStmt: ELSE IF expr body;
elseStmt: ELSE body;
whileStmt: WHILE expr body;
useStmt: USE STRING;
foreachStmt: FOR ID IN expr body;
// forToStmt: FOR ID ASSIGN expr TO expr body;

funcAssign
    : FUNC ID genericParams? LPAREN params? RPAREN (RETURNS ret_type=type)? body
    ;
varAssign
    : ID op=(ADD | SUB | MUL | DIV | MOD)? ASSIGN expr
    | CONST? ID ASSIGN expr
    ;

arg: expr;
args: arg (COMMA arg)*;

param: type ID;
params: param (COMMA param)*;

genericParams: LT ID (COMMA ID)* GT;

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
    | NEW type LBRACK INT? RBRACK #newArray
    | LBRACK args? RBRACK #arrayInit
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
CONST: 'const';
RETURN: 'return';

// Loop keywords
IN: 'in';
// TO: 'to';
FOR: 'for';
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
LBRACK: '[';
RBRACK: ']';
RETURNS: '->';

COMMENT: '//' .*? '\n' -> skip;
MULTILINE_COMMENT: '/*' .*? '*/' -> skip;
WHITESPACE: [\t\r\n ]+ -> skip;
OTHER: .;