import sys
import scanner
import parser
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = parser.parser
    text = file.read()
    ast = parser.parse(text, lexer=scanner.lexer)
    # if ast is not None:
    #     ast.printTree()
    #     print()
    
    typeChecker = TypeChecker()   
    typeChecker.visit(ast)