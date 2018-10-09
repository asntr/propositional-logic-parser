class Operation:

    def __init__(self, op, *args):
        self.op = op
        self.args = list(args)
        self.num = len(args)

    def compute(self):
        return self.op(*map(lambda x: x.compute(), self.args))

    def __repr__(self):
        if len(self.args) == 1:
            return self.op.__doc__ + repr(self.args[0])
        else:
            return f'({self.args[0]} {self.op.__doc__} {self.args[1]})'

    def __hash__(self):
        res = hash(self.op)
        for arg in self.args:
            res ^= hash(arg)
        return res

    def __eq__(self, other):
        return self.op == other.op and self.args == other.args

    def __invert__(self):
        if self.op == negation:
            return self.args[0].copy()
        return Operation(negation, self)

    def copy(self):
        return Operation(self.op, *map(lambda x: x.copy(), self.args))


class Constant:

    def __init__(self, value):
        self.value = bool(value)

    def compute(self):
        return self.value

    def __repr__(self):
        return str(int(self.value))

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __invert__(self):
        return Constant(not self.value)

    def copy(self):
        return Constant(self.value)


class Variable:
    assigns = {}

    def __init__(self, name):
        self.name = name

    def compute(self):
        return bool(self.assigns[self.name])

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __invert__(self):
        return Operation(negation, self)

    def copy(self):
        return Variable(self.name)


def assign_values(names, values):
    Variable.assigns = dict(zip(names, values))


def conjunction(a, b):
    '/\\'
    return a and b


def disjunction(a, b):
    '\\/'
    return a or b


def implication(a, b):
    '->'
    return not a or b


def equivalence(a, b):
    '<->'
    return a == b


def negation(a):
    '~'
    return not a
