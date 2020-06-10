import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys
import operator
import copy
from AST import BinOperator
from TreePrinter import TreePrinter
import main

sys.setrecursionlimit(10000)

class BinOperationUtils():
    def __init__(self):
        self.assignment_operators = ['+=', '-=', '*=', '/=']
        self.operators = {
            '+': self.add,
            '-': self.sub,
            '*': self.mul,
            '/': self.div,
            '.+': self.dotadd,
            '.-': self.dotsub,
            '.*': self.dotmul,
            './': self.dotdiv,
            '==': self.eq,
            '!=': self.ne,
            '>': self.gt,
            '<': self.lt,
            '>=': self.ge,
            '<=': self.le
        }
    
    def shouldAssign(self, op):
        return op in self.assignment_operators

    def calculate(self, a, op, b):
        try:
            return self.operators[op](a,b)
        except:
            raise ArithmeticError()

    def add(self, a, b):
        if isinstance(a, list):
            return list(map(lambda l: list(map(lambda x: x[0]+x[1], list(zip(l[0], l[1])))), list(zip(a, b))))
        else:
            return a + b

    def sub(self, a, b):
        if isinstance(a, list):
            return list(map(lambda l: list(map(lambda x: x[0]-x[1], list(zip(l[0], l[1])))), list(zip(a, b))))
        else:
            return a - b

    def mul(self, a, b):
        if isinstance(a, list):
            resultMatrix = [ [0 for x in range(len(a))] for y in range(len(b[0])) ]
            for i in range(len(a)):
                for j in range(len(b[0])):
                    for k in range(len(b)):
                        resultMatrix[i][j] += a[i][k] * b[k][j]
            return resultMatrix
        else:
            return a * b

    def div(self, a, b):
        if isinstance(a, list):
            inverted = self.getMatrixInverse(b)
            return self.add(a, inverted)
        else:
            return a / b
    
    def getMatrixInverse(self, m):
        determinant = self.getMatrixDeterminant(m)
        if len(m) == 2:
            return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                    [-1*m[1][0]/determinant, m[0][0]/determinant]]

        cofactors = []
        for r in range(len(m)):
            cofactorRow = []
            for c in range(len(m)):
                minor = self.getMatrixMinor(m,r,c)
                cofactorRow.append(((-1)**(r+c)) * self.getMatrixDeterminant(minor))
            cofactors.append(cofactorRow)
        cofactors = self.transposeMatrix(cofactors)
        for r in range(len(cofactors)):
            for c in range(len(cofactors)):
                cofactors[r][c] = cofactors[r][c]/determinant
        return cofactors

    def transposeMatrix(self, m):
        return list(map(list,zip(*m)))

    def getMatrixMinor(self, m,i,j):
        return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

    def getMatrixDeterminant(self, m):
        if len(m) == 2:
            return m[0][0]*m[1][1]-m[0][1]*m[1][0]

        determinant = 0
        for c in range(len(m)):
            determinant += ((-1)**c)*m[0][c]*self.getMatrixDeterminant(self.getMatrixMinor(m,0,c))
        return determinant

    def dotadd(self, a, b):
        if isinstance(a, list) and not isinstance(b, list):
            return list(map(lambda l: list(map(lambda x: x + b, l)), a))
        elif not isinstance(a, list) and isinstance(b, list):
            return list(map(lambda l: list(map(lambda x: a + x, l)), b))
        else:
            return self.dotop(self.add, a, b)

    def dotsub(self, a, b):
        if isinstance(a, list) and not isinstance(b, list):
            return list(map(lambda l: list(map(lambda x: x - b, l)), a))
        elif not isinstance(a, list) and isinstance(b, list):
            return list(map(lambda l: list(map(lambda x: a - x, l)), b))
        else:
            return self.dotop(self.sub, a, b)

    def dotmul(self, a, b):
        if isinstance(a, list) and not isinstance(b, list):
            return list(map(lambda l: list(map(lambda x: x * b, l)), a))
        elif not isinstance(a, list) and isinstance(b, list):
            return list(map(lambda l: list(map(lambda x: a * x, l)), b))
        else:
            return self.dotop(self.mul, a, b)

    def dotdiv(self, a, b):
        if isinstance(a, list) and not isinstance(b, list):
            return list(map(lambda l: list(map(lambda x: x / b, l)), a))
        elif not isinstance(a, list) and isinstance(b, list):
            return list(map(lambda l: list(map(lambda x: a / x, l)), b))
        else:
            return self.dotop(self.div, a, b)

    def dotop(self, f, a, b):
        if len(a) == len(b) and ((len(a) == 0 or len(b) == 0) or (len(a[0]) == len(b[0]))):
            if len(a) == 0 or len(b) == 0:
                return [[]]
            res1 = copy.deepcopy(a)
            for i in range(len(a)):
                for j in range(len(a[i])):
                    res1[i][j] = f(a[i][j], b[i][j])
            return res1
        elif len(b[0]) == 1 or len(a[0]) == 1 or len(b) == 1 or len(a) == 1:
            if len(a[0]) == 1:
                changed = copy.deepcopy(a)
                for i in range(len(a)):
                    for j in range(len(b[0]) - 1):
                        changed[i].append(changed[i][0])
                return self.dotop(f,changed,b)
            elif len(b[0]) == 1:
                changed = copy.deepcopy(b)
                for i in range(len(b)):
                    for j in range(len(a[0]) - 1):
                        changed[i].append(changed[i][0])
                return self.dotop(f, a, changed)
            elif len(a) ==1:
                changed = copy.deepcopy(a)
                for i in range(len(b) - 1):
                    changed.append(a[0])
                return self.dotop(f, changed, b)
            else:
                changed = copy.deepcopy(b)
                for i in range(len(a) - 1):
                    changed.append(b[0])
                return self.dotop(f, a, changed)
        
    def eq(self, a, b):
        return a.__str__() == b.__str__()

    def ne(self, a, b):
        return a.__str__() != b.__str__()

    def gt(self, a, b):
        return a > b

    def lt(self, a, b):
        return a < b

    def ge(self, a, b):
        return a >= b

    def le(self, a, b):
        return a <= b

class Interpreter(object):

    def assign_op_dict(self):
        return {
            BinOperator.ADDASSIGN: BinOperator.ADD,
            BinOperator.SUBASSIGN: BinOperator.SUB,
            BinOperator.MULASSIGN: BinOperator.MUL,
            BinOperator.DIVASSIGN: BinOperator.DIV
        }

    def assign_operators(self):
        return [BinOperator.ADDASSIGN, BinOperator.SUBASSIGN, BinOperator.MULASSIGN, BinOperator.DIVASSIGN]

    def __init__(self, output = True):
        self.memory = MemoryStack()
        self.output = output

    binOpUtils = BinOperationUtils()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Root)
    def visit(self, node):
        try:
            for l in node.children:
                l.accept(self)
        except ReturnValueException as e:
            print(f"Program finished with value {e.value}")
        except Exception as e:
            
            print(f"Oops an error has occured: {type(e).__name__}")
        finally:
            return self.memory

    @when(AST.BinOperation)
    def visit(self, node):
        if self.assign_operators().__contains__(node.operator):
            desugarized = AST.Assignment(node.leftOperand, AST.BinOperation(node.leftOperand, self.assign_op_dict()[node.operator], node.rightOperand, node.lineno), node.lineno)
            return desugarized.accept(self)
        r1 = node.leftOperand.accept(self)
        r2 = node.rightOperand.accept(self)
        op = node.operator.value
        result = self.binOpUtils.calculate(r1, op, r2)
        return result

    @when(AST.Assignment)
    def visit(self, node):
        val = node.value.accept(self)
        if (isinstance(node.id, AST.MatrixCellGetter)):
            m = self.memory.get(node.id.id)
            m[node.id.rownum.accept(self)][node.id.colnum.accept(self)] = val
            self.memory.set(node.id.id, m)
        elif isinstance(node.value, AST.Def):
            self.memory.set(node.id.id, (val[0], copy.deepcopy(self.memory)))
            self.memory.set(node.id.id, (val[0], copy.deepcopy(self.memory)))
        else:
            self.memory.set(node.id.id, copy.deepcopy(val))
        return val

    @when(AST.Variable)
    def visit(self, node):
        return self.memory.get(node.id)

    @when(AST.If)
    def visit(self, node):
        self.memory.push(Memory())
        if node.cond.accept(self):
            node.statements.accept(self)
        elif node.elses is not None:
            node.elses.accept(self)
        self.memory.pop()
                
        
    @when(AST.While)
    def visit(self, node):
        self.memory.push(Memory())
        while node.cond.accept(self):
            try:
                node.statements.accept(self)
            except ContinueException:
                continue
            except BreakException:
                break
        self.memory.pop()
    
    @when(AST.For)
    def visit(self, node):
        self.memory.push(Memory())
        self.memory.insert(node.assignment.id.id, None)
        range = node.assignment.value.accept(self)
        for i in range:
            self.memory.set(node.assignment.id.id, i)
            try:
                node.statements.accept(self)
            except ContinueException:
                continue
            except BreakException:
                break
        self.memory.pop()

    @when(AST.Def)
    def visit(self, node):
        return (node, copy.deepcopy(self.memory))

    @when(AST.DefCall)
    def visit(self, node):
        try:
            func, mem = self.memory.get(node.name)
            args = node.args.accept(self)
            if (len(func.args) != len(args)):
                raise RuntimeError(f"Incompatible arguments for function call: {node.name}")
            else:
                prev = self.memory
                self.memory = copy.deepcopy(mem)
                self.memory.push(Memory())
                self.memory.set(node.name, (func, mem))
                for arg, val in zip(func.args, args):
                    self.memory.insert(arg.id, val)
                func.body.accept(self)
        except ReturnValueException as e:
            return e.value
        finally:
            self.memory = prev
        
    @when(AST.Print)
    def visit(self, node):
        exprs = node.expressions.accept(self)
        if self.output:
            print(*exprs, sep=', ')
    

    @when(AST.Break)
    def visit(self, node):
        raise BreakException()

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException()
    
    @when(AST.Return)
    def visit(self, node):
        raise ReturnValueException(node.value.accept(self))

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.Numbers)
    def visit(self, node):
        return [x.accept(self) for x in node.value]

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.Matrix)
    def visit(self, node):
        return list(map(lambda l: list(map(lambda x: x.accept(self), l)), node.value))

    @when(AST.Zeros)
    def visit(self, node):
        val = node.value.accept(self)
        if(len(val) == 1):
            return [ [ 0 for x in range(0,val[0]) ] for y in range(0,val[0]) ]
        else:
            return [ [ 0 for x in range(0,val[1]) ] for y in range(0,val[0]) ]

    @when(AST.Ones)
    def visit(self, node):
        val = node.value.accept(self)
        if(len(val) == 1):
            return [ [ 1 for x in range(0,val[0]) ] for y in range(0,val[0]) ]
        else:
            return [ [ 1 for x in range(0,val[1]) ] for y in range(0,val[0]) ]

    @when(AST.Eye)
    def visit(self, node):
        val = node.value.accept(self)
        if(len(val) == 1):
            return [ [ (1 if x == y else 0) for x in range(0,val[0]) ] for y in range(0,val[0]) ]
        else:
            return [ [ (1 if x == y else 0) for x in range(0,val[1]) ] for y in range(0,val[0]) ]

    @when(AST.Range)
    def visit(self, node):
        start = node.start.accept(self)
        end = node.end.accept(self)
        return range(start, end+1)

    @when(AST.UnaryMinus)
    def visit(self, node):
        v = node.value.accept(self)
        if isinstance(v, list):
            return list(map(lambda l: list(map(lambda x: -x, l)), v))
        else:
            return -v

    @when(AST.MatrixTranspose)
    def visit(self, node):
        val = node.value.accept(self)
        return self.binOpUtils.transposeMatrix(val)

    @when(AST.MatrixCellGetter)
    def visit(self, node):
        m = self.memory.get(node.id)
        return m[node.rownum.accept(self)][node.colnum.accept(self)]
        
    @when(AST.Statements)
    def visit(self, node):
        return [x.accept(self) for x in node.values]

    @when(AST.Expressions)
    def visit(self, node):
        return list(map(lambda x: x.accept(self), node.values))


