from operations import *
from itertools import combinations


TRUE = frozenset({Constant(True)})
FALSE = frozenset({Constant(False)})


def get_variables(root):
    if not root or isinstance(root, Constant):
        return set()
    if isinstance(root, Operation):
        res = set()
        for arg in root.args:
            res = res.union(get_variables(arg))
        return res
    if isinstance(root, Variable):
        return {root.name}


def implication_to_disjunction(root):
    root.op = disjunction
    left = root.args[0]
    neg_left = Operation(negation, left)
    root.args[0] = neg_left


def equivalence_to_conjuction(root):
    root.op = conjunction
    left = root.args[0]
    right = root.args[1]
    neg_left = Operation(negation, left)
    neg_right = Operation(negation, right)
    new_left = Operation(disjunction, neg_left.copy(), right.copy())
    new_right = Operation(disjunction, left.copy(), neg_right.copy())
    root.args[0] = new_left
    root.args[1] = new_right


def __normalize(root):
    if not isinstance(root, Operation):
        return
    if root.op == implication:
        implication_to_disjunction(root)
    if root.op == equivalence:
        equivalence_to_conjuction(root)
    for child in root.args:
        __normalize(child)


def normalize(root):
    res = root.copy()
    __normalize(res)
    return res


def apply_de_morgan(root):
    child = root.args[0]
    root.op = disjunction if child.op == conjunction else conjunction
    root.args = [None, None]
    left_negation = Operation(negation, child.args[0])
    right_negation = Operation(negation, child.args[1])
    root.args[0] = left_negation
    root.args[1] = right_negation


def remove_negations(root):
    if not isinstance(root, Operation):
        return root.copy()
    if root.op != negation:
        return Operation(root.op, *(remove_negations(child) for child in root.args))
    child = root.args[0]
    if not isinstance(child, Operation):
        if isinstance(child, Constant):
            return ~child
        return root.copy()
    if child.op != negation:
        res = root.copy()
        apply_de_morgan(res)
        root = remove_negations(res)
    else:
        # double negation law
        root = child.args[0]
        root = remove_negations(root)
    return root


def apply_distributive_rules(root):
    changes = 0

    def _apply_distributive_rules(root):
        nonlocal changes
        if not isinstance(root, Operation):
            return root.copy()
        if root.op != disjunction:
            return Operation(root.op, *(_apply_distributive_rules(child) for child in root.args))
        left = root.args[0]
        right = root.args[1]
        if isinstance(right, Operation) and right.op == conjunction:
            right_left = right.args[0]
            right_right = right.args[1]
            new_left = Operation(disjunction, left.copy(), right_left.copy())
            new_right = Operation(disjunction, left.copy(), right_right.copy())
            res = Operation(conjunction, new_left, new_right)
            changes += 1
            return _apply_distributive_rules(res)
        elif isinstance(left, Operation) and left.op == conjunction:
            res = Operation(root.op, *reversed(root.args))
            return _apply_distributive_rules(res)
        else:
            return Operation(root.op, *(_apply_distributive_rules(child) for child in root.args))

    root = _apply_distributive_rules(root)
    while changes > 0:
        changes = 0
        root = _apply_distributive_rules(root)
    return root


def combine_disjunctions(root):
    if isinstance(root, Constant) or isinstance(root, Variable) or isinstance(root, Operation) and root.op == negation:
        return {root}
    if isinstance(root, Operation) and root.op == disjunction:
        res = set()
        for arg in root.args:
            res = res.union(combine_disjunctions(arg))
        return res
    raise TypeError


def simplify_disjunction(d):
    res = d.copy()
    for el in d:
        if ~el in d or (isinstance(el, Constant) and el == Constant(True)):
            return {Constant(True)}
        if isinstance(el, Constant) and el == Constant(False) and len(d) > 1:
            res.remove(el)
    return res


def extract_disjunctions(root):
    if isinstance(root, Operation) and root.op != negation:
        if root.op == conjunction:
            res = set()
            for arg in root.args:
                res = res.union(extract_disjunctions(arg))
            return res
        if root.op == disjunction:
            return {frozenset(simplify_disjunction(combine_disjunctions(root)))}
    if isinstance(root, Variable) or isinstance(root, Constant) or isinstance(root, Operation) :
        return {frozenset({root})}


def get_cnf(syntax_tree):
    disjuncts = extract_disjunctions(syntax_tree)
    res = disjuncts.copy()
    for el in disjuncts:
        if el == FALSE:
            return {FALSE}
        if el == TRUE and len(disjuncts) > 1:
            res.remove(TRUE)
    return res


def print_cnf(cnf):
    disjunctions_reprs = []
    for disjunction_ in cnf:
        if len(disjunction_) > 1:
            full_repr = ' \\/ '.join([str(el) for el in disjunction_])
            disjunctions_reprs.append(
                f"({full_repr})"
            )
        else:
            disjunctions_reprs.append(str(next(iter(disjunction_))))
    print(' /\\ '.join(disjunctions_reprs))


def transform_to_cnf(syntax_tree, debug=False):
    if not isinstance(syntax_tree, Operation):
        cnf = {frozenset({syntax_tree.copy()})}
    else:
        # 0. Convert implications and equivalences
        syntax_tree = normalize(syntax_tree)
        if debug:
            print(f'After removing implications and equivalences: {syntax_tree}')
        # 1. Remove unnecessary negations
        syntax_tree = remove_negations(syntax_tree)
        if debug:
            print(f'After removing negations: {syntax_tree}')
        # 2. Apply distributive rules
        syntax_tree = apply_distributive_rules(syntax_tree)
        if debug:
            print(f'After applying distributive rules: {syntax_tree}')
        # 3. Eliminate constants. Extract set of disjunctions.
        cnf = get_cnf(syntax_tree)
    if debug:
        print('Cnf: ', end='')
        print_cnf(cnf)
    return cnf


def try_to_resolve(l, r):
    for el in l:
        if ~el in r:
            lset, rset = set(l), set(r)
            lset.remove(el)
            rset.remove(~el)
            yield frozenset(lset.union(rset))


def resolution_method(cnf):
    if cnf == {TRUE}:
        return True
    if cnf == {FALSE}:
        return False
    list_of_disjunctions = list(cnf)
    visited = set()
    diff = len(list_of_disjunctions)
    while diff > 0:
        diff = 0
        for (i, ldisjunction), (j, rdisjunction) in combinations(enumerate(list_of_disjunctions.copy()), 2):
            if (i, j) not in visited:
                visited.add((i, j))
                for resolvent in try_to_resolve(ldisjunction, rdisjunction):
                    if not resolvent:
                        return False
                    if resolvent not in list_of_disjunctions:
                        list_of_disjunctions.append(resolvent)
                        diff += 1
    return True
