import sys
from compiler import Compiler
from linter.basic_linter import BasicLinter
from lexer.lexer import MockLexer, RegexLexer, StateMachineLexer
from lexer.binary_tree import BinaryTree
from utils.tokens import TOKENS
from colorama import *

if __name__ == '__main__':
    init()
    if len(sys.argv) < 2:
        sys.exit('Usage: ' + sys.argv[0] + ' <filename>')
    code = ""
    with open(sys.argv[1]) as file:
        code = file.readlines()

    atoms_table = BinaryTree()
    for token in TOKENS:
        atoms_table.add_or_get(token)
    print(Fore.YELLOW + "Table of atoms:")
    atoms_table.print_elems('Atom code', 'Lexical atom', color=Fore.YELLOW)
    

    sym_table = BinaryTree()

    li = BasicLinter()
    le = StateMachineLexer(atoms_table, sym_table)
    c = Compiler(li, le)
    #try:
    c.compile(code)
    # except Exception as e:
    #     print(str(e))
