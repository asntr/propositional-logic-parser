from parser import parser
from tools import resolution_method, transform_to_cnf


def main():
    formula = input()
    syntax_tree = parser.parse(formula)
    cnf = transform_to_cnf(syntax_tree, debug=True)
    answer = 'yes' if resolution_method(cnf) else 'no'
    print(f'Q: Is the given formula satisfiable?\nA: {answer}')

if __name__ == '__main__':
    main()
