import scanner
import ply.yacc as yacc
from enum import Enum
from AST import *

tokens = scanner.tokens

errors = None

precedence = (
   ("right", '='),
   ("left", 'EQ', 'GT', 'LT', 'GTEQ', 'LTEQ'),
   ("left", '+', '-', 'DOTADD', 'DOTSUB'),
   ("left", '*', '/', 'DOTMUL', 'DOTDIV'),
   ("right", "'", '-')
)

def p_error(p):
    if p:
        print(Error("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value)))
        while parser.token():
            pass
        parser.restart()
    else:
        print(Error('End of input'))

def p_start(p):
    """start : statements"""
    p[0] = Root(p[1], p.lineno(1))

def p_statement_instruction(p):
    """statement : instruction"""
    p[0] = p[1]

def p_instruction_if(p):
    """instruction : IF '(' expression ')' statement
                   | IF '(' expression ')' statement ELSE statement"""
    if len(p)>6:
        p[0] = If(p[3], p[5], p[7], p.lineno(1))
    else:
        p[0] = If(p[3], p[5], None, p.lineno(1))

def p_instruction_while(p):
    """instruction : WHILE '(' expression ')' statement"""
    p[0] = While(p[3], p[5], p.lineno(1))

def p_expression_return(p):
    """expression : RETURN expression"""
    p[0] = Return(p[2], p.lineno(1))

def p_instruction_def(p):
    """expression : '(' args ')' ARROW statement"""
    p[0] = Def(p[2], p[5], p.lineno(4))

def p_instruction_for(p):
    """instruction : FOR ID '=' range statement"""
    p[0] = For(Assignment(Variable(p[2], p.lineno(2)), p[4], p.lineno(3)), p[5], p.lineno(1))

def p_args(p):
    """args : ID
            | args ',' ID"""
    if len(p)>2:
        p[0] = p[1] + [Variable(p[3], p.lineno(3))]
    else:
        p[0] = [Variable(p[1], p.lineno(1))]

def p_statements(p):
    """statements : statement
                  | statements statement"""
    if len(p)>2:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement_expression(p):
    """statement : expression ';'"""
    p[0] = p[1]

def p_statement_statements(p):
    """statement : '{' statements '}'"""
    p[0] = Statements(p[2], p.lineno(1))

def p_statement_print(p):
    """statement : PRINT expressions ';'"""
    p[0] = Print(Expressions(p[2], p.lineno(1)), p.lineno(1))

def p_expressions(p):
    """expressions : expression
                   | expressions ',' expression"""
    if len(p)>2:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_mexpression_minit(p):
    """expression : '[' minit ']'
                  | '[' ']'"""
    if len(p)>3:
        p[0] = Matrix(p[2], p.lineno(1))
    else:
        p[0] = Matrix([[]], p.lineno(1))

def p_minit(p):
    """minit : mrow ';'
             | mrow
             | '[' mrow ']' ','
             | '[' mrow ']'
             | mrow ';' minit
             | '[' mrow ']' ',' minit"""
    if len(p)==2 or len(p)==3:
        p[0] = [p[1]]
    elif (len(p)==4 or len(p)==5) and p[1]=='[':
        p[0] = [p[2]]
    elif len(p)==6:
        p[0] = [p[2]] + p[5]
    else:
        p[0] = [p[1]] + p[3]
        

def p_mrow(p):
    """mrow : number
            | number ',' mrow"""
    if len(p)>2:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_number_intnum(p):
    """number : INTNUM"""
    p[0] = IntNum(p[1], p.lineno(1))

def p_number_floatnum(p):
    """number : FLOATNUM"""
    p[0] = FloatNum(p[1], p.lineno(1))

def p_expression_assignment(p):
    """expression : assignable '=' expression"""
    p[0] = Assignment(p[1], p[3], p.lineno(2))

def p_expression_unaryminus(p):
    """expression : '-' expression"""
    p[0] = UnaryMinus(p[2], p.lineno(1))

def p_expression_matrixtranspose(p):
    """expression : expression \"'\""""
    p[0] = MatrixTranspose(p[1], p.lineno(2))

def p_expression_fancy_assign(p):
    """expression : assignable ADDASSIGN expression
                  | assignable SUBASSIGN expression
                  | assignable MULASSIGN expression
                  | assignable DIVASSIGN expression"""
    if p[2] == '+=':
        op = BinOperator.ADDASSIGN
    elif p[2] == '-=':
        op = BinOperator.SUBASSIGN
    elif p[2] == '*=':
        op = BinOperator.MULASSIGN
    else:
        op = BinOperator.DIVASSIGN
    p[0] = BinOperation(p[1], op, p[3], p.lineno(2))

def p_expression_sum(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression DOTADD expression
                  | expression DOTSUB expression"""
    if p[2] == '+':
        op = BinOperator.ADD
    elif p[2] == '-':
        op = BinOperator.SUB
    elif p[2] == '.+':
        op = BinOperator.DOTADD
    else:
        op = BinOperator.DOTSUB
    p[0] = BinOperation(p[1], op, p[3], p.lineno(2))

def p_expression_mul(p):
    """expression : expression '*' expression
                  | expression '/' expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression"""
    if p[2] == '*':
        op = BinOperator.MUL
    elif p[2] == '/':
        op = BinOperator.DIV
    elif p[2] == '.*':
        op = BinOperator.DOTMUL
    else:
        op = BinOperator.DOTDIV
    p[0] = BinOperation(p[1], op, p[3], p.lineno(2))

def p_expression_cond(p):
    """expression : expression EQ expression
                  | expression NOTEQ expression
                  | expression GT expression
                  | expression LT expression
                  | expression GTEQ expression
                  | expression LTEQ expression"""
    if p[2] == '==':
        op = BinOperator.EQ
    elif p[2] == '!=':
        op = BinOperator.NOTEQ
    elif p[2] == '>':
        op = BinOperator.GT
    elif p[2] == '<':
        op = BinOperator.LT
    elif p[2] == '>=':
        op = BinOperator.GTEQ
    else:
        op = BinOperator.LTEQ
    p[0] = BinOperation(p[1], op, p[3], p.lineno(2))

def p_numbers(p):
    """numbers : number
               | numbers ',' number"""
    if len(p) > 2:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_expression_function(p):
    """expression : ZEROS '(' numbers ')'
                  | ONES '(' numbers ')'
                  | EYE '(' numbers ')'
                  | ID '(' expressions ')'"""
    if p[1] == 'zeros':
        p[0] = Zeros(Numbers(p[3], p.lineno(3)), p.lineno(1))
    elif p[1] == 'ones':
        p[0] = Ones(Numbers(p[3], p.lineno(3)), p.lineno(1))
    elif p[1] == 'eye':
        p[0] = Eye(Numbers(p[3], p.lineno(3)), p.lineno(1))
    else:
        p[0] = DefCall(p[1], Expressions(p[3], p.lineno(3)), p.lineno(1))

def p_expression_number(p):
    """expression : number"""
    p[0] = p[1]

def p_expression_string(p):
    """expression : STRING"""
    p[0] = String(p[1][1:-1], p.lineno(1))

def p_expression_assignable(p):
    """expression : assignable"""
    p[0] = p[1]

def p_expression_id(p):
    """assignable : ID"""
    p[0] = Variable(p[1], p.lineno(1))

def p_assignable_matrixcellgetter(p):
    """assignable : matrixcellgetter"""
    p[0] = p[1]

def p_matrixcellgetter(p):
    """matrixcellgetter : ID '[' expression ',' expression ']'"""
    p[0] = MatrixCellGetter(p[1], p[3], p[5], p.lineno(1))

def p_expression_group(p):
    """expression : '(' expression ')'"""
    p[0] = p[2]

def p_expression_break(p):
    """expression : BREAK"""
    p[0] = Break(p.lineno(1))

def p_expression_continue(p):
    """expression : CONTINUE"""
    p[0] = Continue(p.lineno(1))

def p_expression_range(p):
    """expression : range"""
    p[0] = p[1]

def p_range(p):
    """range : expression ':' expression"""
    p[0] = Range(p[1], p[3], p.lineno(1))

parser = yacc.yacc()
