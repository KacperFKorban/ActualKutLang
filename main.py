import sys
import scanner
import parser
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker, Success
import Interpreter

def run(filename, output=True):
    file = open(filename, "r")
    prsr = parser.parser
    text = file.read()
    ast = prsr.parse(text, lexer=scanner.lexer)
    # if ast is not None:
    #     ast.printTree()
    #     print()
    
    typeChecker = TypeChecker()
    checkRes = typeChecker.visit(ast)
    if output:
        print(checkRes)

    if isinstance(checkRes, Success):
        return ast.accept(Interpreter.Interpreter(output))

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
        run(filename)
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)
    