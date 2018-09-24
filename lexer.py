import ply.lex as lex

tokens = (
    'VARIABLE',
    'TRUE',
    'FALSE',
    'CONJUNCTION',
    'DISJUNCTION',
    'IMPLICATION',
    'LPAREN',
    'RPAREN',
    'EQUIVALENCE',
    'NEGATION'
)


def t_VARIABLE(t):
    r'[a-zA-Z]'
    return t


def t_TRUE(t):
    r'1'
    t.value = True
    return t


def t_FALSE(t):
    r'0'
    t.value = False
    return t


def t_CONJUNCTION(t):
    r'/\\'
    return t


def t_DISJUNCTION(t):
    r'\\/'
    return t


def t_IMPLICATION(t):
    r'->'
    return t


def t_LPAREN(t):
    r'\('
    return t


def t_EQUIVALENCE(t):
    r'<->'
    return t


def t_RPAREN(t):
    r'\)'
    return t


def t_NEGATION(t):
    r'~'
    return t

t_ignore = ' \t\n'


def t_error(t):
    print(f'Illegal character "{t.value[0]}" at line {t.lineno}')
    t.lexer.skip(1)


lexer = lex.lex()
