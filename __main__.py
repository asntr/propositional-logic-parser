from parser import parser
from tools import resolution_method, transform_to_cnf
from operations import assign_values
import argparse


def get_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--debug', default=True)

    return arg_parser.parse_args()


def main():
    args = get_args()
    formula = input()
    syntax_tree = parser.parse(formula)
    cnf = transform_to_cnf(syntax_tree, debug=args.debug)
    answer = 'Yes' if resolution_method(cnf) else 'No'
    print(f'Q: Is the given formula satisfiable?\nA: {answer}')

if __name__ == '__main__':
    main()
