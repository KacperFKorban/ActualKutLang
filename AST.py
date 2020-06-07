from enum import Enum

class Node(object):
    def accept(self, visitor):
        return visitor.visit(self)

class Root(Node):
    def __init__(self, children, lineno):
        self.lineno = lineno
        self.children = children
    def __str__(self):
        return f"Root({str(self.children)})"
    def __repr__(self):
        return self.__str__()

class BinOperation(Node):
    def __init__(self, leftOperand, operator, rightOperand, lineno):
        self.lineno = lineno
        self.leftOperand = leftOperand
        self.rightOperand = rightOperand
        self.operator = operator
    def __str__(self):
        return f"BinOperation({str(self.leftOperand)}, {str(self.operator)}, {str(self.rightOperand)})"
    def __repr__(self):
        return self.__str__()

class Assignment(Node):
    def __init__(self, id, value, lineno):
        self.lineno = lineno
        self.id = id
        self.value = value
    def __str__(self):
        return f"Assignment({self.id}, {str(self.value)})"
    def __repr__(self):
        return self.__str__()

class Variable(Node):
    def __init__(self, id, lineno):
        self.lineno = lineno
        self.id = id
    def __str__(self):
        return f"Variable({self.id})"
    def __repr__(self):
        return self.__str__()

class If(Node):
    def __init__(self, cond, statements, elses, lineno):
        self.lineno = lineno
        self.cond = cond
        self.statements = statements
        self.elses = elses
    def __str__(self):
        return f"If({self.cond}, {self.statements}, {self.elses})"
    def __repr__(self):
        return self.__str__()

class While(Node):
    def __init__(self, cond, statements, lineno):
        self.lineno = lineno
        self.cond = cond
        self.statements = statements
    def __str__(self):
        return f"While({self.cond}, {self.statements})"
    def __repr__(self):
        return self.__str__()

class For(Node):
    def __init__(self, assignment, statements, lineno):
        self.lineno = lineno
        self.assignment = assignment
        self.statements = statements
    def __str__(self):
        return f"For({self.assignment}, {self.statements})"
    def __repr__(self):
        return self.__str__()

class Def(Node):
    def __init__(self, args, body, lineno):
        self.args = args
        self.body = body
        self.lineno = lineno
    def __str__(self):
        return f"Def({self.args}, {self.body})"
    def __repr__(self):
        return self.__str__()

class DefCall(Node):
    def __init__(self, name, args, lineno):
        self.name = name
        self.args = args
        self.lineno = lineno
    def __str__(self):
        return f"DefCall({self.name}, {self.args})"
    def __repr__(self):
        return self.__str__()

class Print(Node):
    def __init__(self, expressions, lineno):
        self.lineno = lineno
        self.expressions = expressions
    def __str__(self):
        return f"Print({self.expressions})"
    def __repr__(self):
        return self.__str__()

class Break(Node):
    def __init__(self, lineno):
        self.lineno = lineno
        pass
    def __str__(self):
        return f"Break"
    def __repr__(self):
        return self.__str__()

class Continue(Node):
    def __init__(self, lineno):
        self.lineno = lineno
        pass
    def __str__(self):
        return f"Continue"
    def __repr__(self):
        return self.__str__()

class Return(Node):
    def __init__(self, value, lineno):
        self.lineno = lineno
        self.value = value
    def __str__(self):
        return f"Return({self.value})"
    def __repr__(self):
        return self.__str__()

class IntNum(Node):
    def __init__(self, value, lineno):
        self.lineno = lineno
        self.value = value
    def __str__(self):
        return f"IntNum({self.value})"
    def __repr__(self):
        return self.__str__()

class FloatNum(Node):
    def __init__(self, value, lineno):
        self.lineno = lineno
        self.value = value
    def __str__(self):
        return f"FloatNum({self.value})"
    def __repr__(self):
        return self.__str__()

class Numbers(Node):
    def __init__(self, value, lineno):
        self.lineno = lineno
        self.value = value
    def __str__(self):
        return f"Numbers({self.value})"
    def __repr__(self):
        return self.__str__()

class String(Node):
    def __init__(self, value, lineno):
        self.lineno = lineno
        self.value = value
    def __str__(self):
        return f"String({self.value})"
    def __repr__(self):
        return self.__str__()

class Matrix(Node):
    def __init__(self, value, lineno):
        self.lineno = lineno
        self.value = value
    def __str__(self):
        return f"Matrix({self.value})"
    def __repr__(self):
        return self.__str__()

class Zeros(Node):
    def __init__(self, value, lineno):
        self.lineno = lineno
        self.value = value
    def __str__(self):
        return f"Zeros({self.value})"
    def __repr__(self):
        return self.__str__()

class Ones(Node):
    def __init__(self, value, lineno):
        self.lineno = lineno
        self.value = value
    def __str__(self):
        return f"Ones({self.value})"
    def __repr__(self):
        return self.__str__()

class Eye(Node):
    def __init__(self, value, lineno):
        self.lineno = lineno
        self.value = value
    def __str__(self):
        return f"Eye({self.value})"
    def __repr__(self):
        return self.__str__()

class Range(Node):
    def __init__(self, start, end, lineno):
        self.lineno = lineno
        self.start = start
        self.end = end
    def __str__(self):
        return f"Range({self.start}, {self.end})"
    def __repr__(self):
        return self.__str__()

class UnaryMinus(Node):
    def __init__(self, value, lineno):
        self.lineno = lineno
        self.value = value
    def __str__(self):
        return f"UnaryMinus({self.value})"
    def __repr__(self):
        return self.__str__()

class MatrixTranspose(Node):
    def __init__(self, value, lineno):
        self.lineno = lineno
        self.value = value
    def __str__(self):
        return f"MatrixTranspose({self.value})"
    def __repr__(self):
        return self.__str__()

class MatrixCellGetter(Node):
    def __init__(self, id, rownum, colnum, lineno):
        self.lineno = lineno
        self.id = id
        self.rownum = rownum
        self.colnum = colnum
    def __str__(self):
        return f"MatrixCellGetter({self.id}, {self.rownum}, {self.colnum})"
    def __repr__(self):
        return self.__str__()

class Statements(Node):
    def __init__(self, values, lineno):
        self.lineno = lineno
        self.values = values
    def __str__(self):
        return f"Statements({self.values})"
    def __repr__(self):
        return self.__str__()

class Expressions(Node):
    def __init__(self, values, lineno):
        self.lineno = lineno
        self.values = values
    def __str__(self):
        return f"Expressions({self.values})"
    def __repr__(self):
        return self.__str__()

class BinOperator(Enum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    ADDASSIGN = '+='
    SUBASSIGN = '-='
    MULASSIGN = '*='
    DIVASSIGN = '/='
    DOTADD = '.+'
    DOTSUB = '.-'
    DOTMUL = '.*'
    DOTDIV = './'
    EQ = '=='
    NOTEQ = '!='
    GT = '>'
    LT = '<'
    GTEQ = '>='
    LTEQ = '<='
    def __str__(self):
        return self.value

class Error(Node):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f"Error({self.value})"
    def __repr__(self):
        return self.__str__()