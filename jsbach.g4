grammar jsbach;

root : (COMENTARI|def_methods)* EOF;

expr :    
      '#' expr                                      #SizeOfArray
    | expr (MUL|DIV) expr                           #MultDiv
    | expr ADD expr                                 #Suma
    | <assoc=right> expr SUB expr                   #Resta
    | expr MOD expr                                 #Mod
    | INT                                           #Valor
    | NAME_VARIABLE                                 #Var
    | BOOL                                          #BoolValue
    | STRING                                        #StringValue
    | (NAME_NOTE|NAME_NOTE_NO_NUMBER)               #Nota
    | '{' expr* '}'                                 #Array
    | '(' expr ')'                                  #EvalExprParentesis
    | expr '[' expr ']'                             #AccedeixIessimArray
    | expr CONCAT expr                              #ConcatArray
    ;

instr :
      statements
    | i_o_assig
    | call_method
    | instr_llistes
    | COMENTARI
    ;

instr_llistes :
      expr '<<' expr                                #AfageixElementArray
    | '8<' expr'[' expr ']'                         #EliminaIessimArray
    ;

i_o_assig :
      OUTPUT expr*                                  #Escriu
    | INPUT NAME_VARIABLE                           #LLegeix
    | NAME_VARIABLE ASSIG expr                      #Assig
    | PLAY expr                                     #ReproduirNota
    ;

def_methods :
      NAME_METHOD expr* IN_BLOCK instr* OUT_BLOCK      #DefMethod
    ;

call_method :
      NAME_METHOD expr*                             #CallMethod
    ;

statements :
      IF boolrule IN_BLOCK instr* OUT_BLOCK         #IfStatement
    | IF boolrule IN_BLOCK instr* OUT_BLOCK ELSE IN_BLOCK instr* OUT_BLOCK #IfElseStatement
    | WHILE boolrule IN_BLOCK instr* OUT_BLOCK      #While
    ;

boolrule : 
       expr EQ expr                                 #Equal
    |  expr GT expr                                 #More
    |  expr LT expr                                 #Less
    |  expr LE expr                                 #LessEqual
    |  expr GE expr                                 #GreaterEqual
    |  expr DIFF expr                               #Diff
    |  (NAME_VARIABLE|BOOL)                         #VarIf
    ;


// STATEMENTS
IF : 'if';
ELSE : 'else';
WHILE : 'while';
IN_BLOCK : '|:';
OUT_BLOCK : ':|';

// ESPECIFICACIONS
ASSIG : '<-';
INPUT : '<?>';
OUTPUT : '<!>';
PLAY : '<:>';

// TIPUS
INT : [0-9]+;
BOOL : 'true'|'false';
NAME_NOTE : [A-Z][0-9];
NAME_NOTE_NO_NUMBER : [A-Z];
STRING : '"'.*?'"';

// OPERADORS
CONCAT : ':';
ADD : '+' ;
SUB : '-';
MUL : '*';
DIV : '/';
MOD : '%';
LE : '<=';
GE : '>=';
GT : '>';
LT : '<';
EQ : '=';
DIFF : '/=';

// OTHERS
NAME_METHOD : [A-Z][a-zA-Z]*;
NAME_VARIABLE : [a-z][a-zA-Z]*;
COMENTARI : '~~~'.*?'~~~' -> skip;
WS : [ \n\r\t]+ -> skip ;