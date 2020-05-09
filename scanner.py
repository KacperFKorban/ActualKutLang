import ply.lex as lex
import sys

reserved = {
    'if'       : 'IF',
    'else'     : 'ELSE',
    'while'    : 'WHILE',
    'for'      : 'FOR',
    'break'    : 'BREAK',
    'continue' : 'CONTINUE',
    'return'   : 'RETURN',
    'eye'      : 'EYE',
    'zeros'    : 'ZEROS',
    'ones'     : 'ONES',
    'print'    : 'PRINT'
}

tokens = [
    'COMMENT',
    'DOTADD',
    'DOTSUB',
    'DOTMUL',
    'DOTDIV',
    'ADDASSIGN',
    'SUBASSIGN',
    'MULASSIGN',
    'DIVASSIGN',
    'EQ',
    'NOTEQ',
    'LT',
    'GT',
    'LTEQ',
    'GTEQ',
    'ID',
    'INTNUM',
    'FLOATNUM',
    'STRING'
    ] + list(reserved.values())

literals = [
    '=',
    '(',
    ')',
    '[',
    ']',
    '{',
    '}',
    ':',
    "'",
    ',',
    ';',
    '+',
    '-',
    '*',
    '/'
    ]

t_EQ = r'=='
t_NOTEQ = r'!='
t_LT = r'<'
t_GT = r'>'
t_LTEQ = r'<='
t_GTEQ = r'>='

t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'

t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='

def t_FLOATNUM(t):
    r'[-+]?\d*\.\d+([eE][-+]?\d+)?|[-+]?\d+\.([eE][-+]?\d+)?|[-+]?\d+[eE][-+]?\d+'
    t.value = float(t.value)
    return t

def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

t_STRING = r'"[^"\\]*(?:\\.[^"\\]*)*"'

def t_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value,'ID')
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' in line {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()
