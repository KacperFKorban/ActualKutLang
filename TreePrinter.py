from __future__ import print_function
import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.Node)
    def printIndent(self, indent=0):
        for i in range(indent):
            print('|  ', end='')

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Root)
    def printTree(self, indent=0):
        for c in self.children:
            self.printIndent(indent)
            c.printTree()

    @addToClass(AST.BinOperation)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print(self.operator)
        self.leftOperand.printTree(indent+1)
        self.rightOperand.printTree(indent+1)
    
    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print('=')
        self.id.printTree(indent+1)
        self.value.printTree(indent+1)

    @addToClass(AST.Assignment)
    def printTreeWithoutOperator(self, indent=0):
        self.id.printTree(indent)
        self.value.printTree(indent)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print(self.id)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print('IF')
        self.cond.printTree(indent+1)
        self.printIndent(indent)
        print('THEN')
        self.statements.printTree(indent+1)
        if self.elses is not None:
            self.printIndent(indent)
            print('ELSE')
            self.elses.printTree(indent+1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print('WHILE')
        self.cond.printTree(indent+1)
        self.statements.printTree(indent+1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print('FOR')
        self.assignment.printTreeWithoutOperator(indent+1)
        self.statements.printTree(indent+1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print('PRINT')
        self.expressions.printTree(indent+1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print('BREAK')

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print('CONTINUE')

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print('RETURN')
        self.value.printTree(indent+1)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print(self.value)

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print(self.value)

    @addToClass(AST.Numbers)
    def printTree(self, indent=0):
        for n in self.value:
            n.printTree(indent)

    @addToClass(AST.String)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print('STRING')
        print(self.value)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print('VECTOR')
        for row in self.value:
            self.printIndent(indent+1)
            print('VECTOR')
            for v in row:
                v.printTree(indent+2)

    @addToClass(AST.Zeros)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print('zeros')
        self.value.printTree(indent+1)

    @addToClass(AST.Ones)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print('ones')
        self.value.printTree(indent+1)

    @addToClass(AST.Eye)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print('eye')
        self.value.printTree(indent+1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print('RANGE')
        self.start.printTree(indent+1)
        self.end.printTree(indent+1)

    @addToClass(AST.UnaryMinus)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print('-')
        self.value.printTree(indent+1)

    @addToClass(AST.MatrixTranspose)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print("TRANSPOSE")
        self.value.printTree(indent+1)

    @addToClass(AST.MatrixCellGetter)
    def printTree(self, indent=0):
        self.printIndent(indent)
        print("REF")
        self.printIndent(indent+1)
        print(self.id)
        self.printIndent(indent+1)
        print(self.rownum)
        self.printIndent(indent+1)
        print(self.colnum)

    @addToClass(AST.Statements)
    def printTree(self, indent=0):
        for c in self.values:
            c.printTree(indent)

    @addToClass(AST.Expressions)
    def printTree(self, indent=0):
        for c in self.values:
            c.printTree(indent)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        print(self.value)