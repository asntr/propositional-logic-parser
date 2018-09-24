import ply.yacc as yacc

from lexer import tokens

from operations import *


def p_sentence(p):
    ''' sentence : equivalence_sentence '''
    p[0] = p[1]


def p_equivalence_sentence(p):
    ''' equivalence_sentence : implication_sentence EQUIVALENCE equivalence_sentence
                 | implication_sentence
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Operation(equivalence, p[1], p[3])


def p_implication_sentence(p):
    ''' implication_sentence : conjunctive_sentence IMPLICATION implication_sentence
                | conjunctive_sentence
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Operation(implication, p[1], p[3])


def p_conjunctive_sentence(p):
    ''' conjunctive_sentence : disjunctive_sentence CONJUNCTION conjunctive_sentence
                   | disjunctive_sentence
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Operation(conjunction, p[1], p[3])


def p_disjunctive_sentence(p):
    ''' disjunctive_sentence : negate_sentence DISJUNCTION disjunctive_sentence
                   | negate_sentence
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Operation(disjunction, p[1], p[3])


def p_negate_sentence(p):
    ''' negate_sentence : NEGATION negate_sentence
              | grouping_sentence
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Operation(negation, p[2])


def p_grouping_sentence(p):
    ''' grouping_sentence : LPAREN sentence RPAREN
                | atomic_sentence
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_atomic_sentence(p):
    ''' atomic_sentence : TRUE
                | FALSE
                | VARIABLE
    '''
    if isinstance(p[1], bool):
        p[0] = Constant(p[1])
    else:
        p[0] = Variable(p[1])


def p_error(p):
    raise TypeError('Unknown text at %r' % (p.value,))

start = 'sentence'

parser = yacc.yacc()
