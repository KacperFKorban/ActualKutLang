from AST import BinOperator
import AST
from SymbolTable import *

class NodeVisitor(object):

    def visit(self, node):
        if node is None:
            return NotAttempted()
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

class TypeCheckerResult:
    pass

class Success(TypeCheckerResult):
    def __init__(self, warns):
        self.warns = warns
    def __repr__(self):
        return f"SUCCESS\n{self.warns} warning{'s' if self.warns != 1 else ''} found"

class Failure(TypeCheckerResult):
    def __init__(self, errors, warns):
        self.errors = errors
        self.warns = warns
    def __repr__(self):
        return f"FAILED\n{self.errors} error{'s' if self.errors != 1 else ''} and {self.warns} warning{'s' if self.warns != 1 else ''} found"

class NotAttempted(TypeCheckerResult):
    def __repr__(self):
        return ""

class TypeChecker(NodeVisitor):

    def __init__(self):
        self.symbolTable = SymbolTable()
        self.loopsCount = 0
        self.errors = 0
        self.warns = 0

    def assign_op_dict(self):
        return {
            BinOperator.ADDASSIGN: BinOperator.ADD,
            BinOperator.SUBASSIGN: BinOperator.SUB,
            BinOperator.MULASSIGN: BinOperator.MUL,
            BinOperator.DIVASSIGN: BinOperator.DIV
        }

    def getTypeForBinOperation(self, op, arg1, arg2):
        if self.boolean_operators().__contains__(op):
            return self.check_boolean_operation(arg1, arg2)
        elif self.scalar_operators().__contains__(op):
            return self.check_numeric_bin_operation(op, arg1, arg2)
        elif self.matrix_operators().__contains__(op):
            return self.check_matrix_bin_operation(op, arg1, arg2)


    def boolean_operators(self):
        return [BinOperator.EQ, BinOperator.NOTEQ, BinOperator.GT, BinOperator.LT, BinOperator.GTEQ, BinOperator.LTEQ]

    def matrix_operators(self):
        return [BinOperator.DOTADD, BinOperator.DOTSUB, BinOperator.DOTMUL, BinOperator.DOTDIV]  

    def scalar_operators(self):
        return [BinOperator.ADD, BinOperator.SUB, BinOperator.MUL, BinOperator.DIV,
        BinOperator.ADDASSIGN, BinOperator.SUBASSIGN, BinOperator.MULASSIGN, BinOperator.DIVASSIGN]

    def assign_operators(self):
        return [BinOperator.ADDASSIGN, BinOperator.SUBASSIGN, BinOperator.MULASSIGN, BinOperator.DIVASSIGN]

    def check_boolean_operation(self, arg1, arg2):
        if isinstance(arg1, Scalar) and isinstance(arg2, Scalar):
            return Boolean()
        elif isinstance(arg1, Matrix) and isinstance(arg2, Matrix):
            return Boolean()
        elif isinstance(arg1, String) and isinstance(arg2, String):
            return Boolean()
        else:
            return None

    def check_numeric_bin_operation(self, op, arg1, arg2):
        if isinstance(arg1, Scalar) and isinstance(arg2, Scalar):
            return Float() if isinstance(arg1, Float) or isinstance(arg2, Float) else Integer()
        elif op == BinOperator.ADD or op == BinOperator.SUB or op == BinOperator.ADDASSIGN or op == BinOperator.SUBASSIGN:
            if isinstance(arg1, Matrix) and arg1.equals(arg2):
                return Matrix(arg1.n, arg1.m, arg1.getCommonType(arg2))
            elif op == BinOperator.ADD and isinstance(arg1, String) and isinstance(arg2, String):
                return String()
            else:
                return None
        elif op == BinOperator.MUL or op == BinOperator.MULASSIGN:
            if isinstance(arg1, Matrix) and isinstance(arg2, Matrix) and arg1.m == arg2.n:
                return Matrix(arg1.n, arg2.m, arg1.getCommonType(arg2))
            else:
                return None
        elif op == BinOperator.DIV or op == BinOperator.DIVASSIGN:
            if isinstance(arg1, Matrix) and isinstance(arg2, Matrix) and arg1.m == arg2.n and arg2.n == arg2.m:
                return Matrix(arg1.n, arg2.m, arg1.getCommonType(arg2))
            else:
                return None
        else:
            return None

    def check_matrix_bin_operation(self, op, arg1, arg2):
        if isinstance(arg1, Matrix) and isinstance(arg2, Matrix) and arg1.equals(arg2):
            return Matrix(arg1.n, arg1.m, arg1.getCommonType(arg2))
        elif (isinstance(arg1, Scalar) and isinstance(arg2, Matrix)) or (isinstance(arg1, Matrix) and isinstance(arg2, Scalar)):
            return arg1 if isinstance(arg1, Matrix) else arg2
        else:
            return None

    def new_scope(self):
        old_symbolTable = self.symbolTable
        self.symbolTable = SymbolTable()
        self.symbolTable.parent = old_symbolTable
    
    def pop_scope(self):
        self.symbolTable = self.symbolTable.parent

    def error(self, msg, lineno):
        self.errors += 1
        print(f"ERROR at line {lineno}: {msg}")

    def warn(self, msg, lineno):
        self.warns += 1
        print(f"WARN at line {lineno}: {msg}")

    def is_expressions(self, t, e):
        exprs = [
            AST.For,
            AST.Assignment,
            AST.If,
            AST.For,
            AST.While,
            AST.Print,
            AST.Statements,
            AST.Break,
            AST.Continue,
            AST.Return
        ]
        if exprs.__contains__(t):
            return False
        elif t == AST.BinOperation and self.assign_operators().__contains__(e.operator):
            return False
        else:
            return True

    def visit_Root(self, node):
        for c in node.children:
            t = self.visit(c)
            if self.is_expressions(type(c), c) and t is not None:
                self.warn(f"Unused expression of type {t}", c.lineno)
        if self.errors == 0:
            return Success(self.warns)
        else:
            return Failure(self.errors, self.warns)

    def visit_BinOperation(self, node):
        if self.assign_operators().__contains__(node.operator):
            desugarized = AST.Assignment(node.leftOperand, AST.BinOperation(node.leftOperand, self.assign_op_dict()[node.operator], node.rightOperand, node.lineno), node.lineno)
            return self.visit(desugarized)
        else:
            type1 = self.visit(node.leftOperand)
            type2 = self.visit(node.rightOperand)
            op    = node.operator
            res_type = self.getTypeForBinOperation(op, type1, type2)
            if res_type is None and type1 is not None and type2 is not None:
                self.error(f"Type mismatch for operation {op} found: {type1}, {type2}", node.lineno)
                return None
            else:
                return res_type

    def visit_Assignment(self, node):
        if isinstance(node.id, AST.Variable):
            id = node.id.id
            v_type = self.symbolTable.getType(id)
            type = self.visit(node.value)
            if type == Range():
                type = Integer()
            self.symbolTable.put(VariableSymbol(id, type))
            return type
        else:
            v_type = self.visit(node.id)
            type = self.visit(node.value)
            if type == Range():
                type = Integer()
            if not isinstance(type, Scalar):
                self.error(f"Cannot assign non scalar value to matrix element, but found {type}", node.lineno)
                return None
            return type

    def visit_Variable(self, node):
        v = self.symbolTable.get(node.id)
        if v is None:
            self.error(f"Call to variable {node.id} before assignment", node.lineno)
        else:
            return v.type
        
    def visit_If(self, node):
        c_type = self.visit(node.cond)
        self.new_scope()
        s_type = self.visit(node.statements)
        if self.is_expressions(type(node.statements), node.statements)  and s_type is not None:
            self.warn(f"Unused expression of type {s_type}", node.statements.lineno)
        self.pop_scope()
        if node.elses:
            self.new_scope()
            e_type = self.visit(node.elses)
            if self.is_expressions(type(node.elses), node.elses)  and e_type is not None:
                self.warn(f"Unused expression of type {e_type}", node.elses.lineno)
            self.pop_scope()
        if c_type != Boolean() and c_type is not None:
            self.error(f"If condition must be a Boolean, but found {c_type}", node.cond.lineno)

    def visit_While(self, node):
        self.loopsCount += 1
        self.new_scope()
        c_type = self.visit(node.cond)
        s_type = self.visit(node.statements)
        if self.is_expressions(type(node.statements), node.statements)  and s_type is not None:
            self.warn(f"Unused expression of type {s_type}", node.statements.lineno)
        self.pop_scope()
        self.loopsCount -= 1
        if c_type != Boolean() and c_type is not None:
            self.error(f"While condition must be a Boolean, {c_type}", node.cond.lineno)

    def visit_For(self, node):
        self.loopsCount += 1
        self.new_scope()
        a_type = self.visit(node.assignment)
        s_type = self.visit(node.statements)
        if self.is_expressions(type(node.statements), node.statements) and s_type is not None:
            self.warn(f"Unused expression of type {s_type}", node.statements.lineno)
        self.pop_scope()
        self.loopsCount -= 1
        
    def visit_Print(self, node):
        return None

    def visit_Break(self, node):
        if self.loopsCount == 0:
            self.error("Break statement can only be used in a loop", node.lineno)
        return None

    def visit_Continue(self, node):
        if self.loopsCount == 0:
            self.error("Continue statement can only be used in a loop", node.lineno)
        return None

    def visit_Return(self, node):
        return self.visit(node.value)

    def visit_FloatNum(self, node):
        return Float()
    
    def visit_IntNum(self, node):
        return Integer()

    def visit_Numbers(self, node):
        types = map(lambda x: self.visit(x), node.value)
        type = None
        for t in types:
            if type == Integer() or type == None:
                type = t
        return type


    def visit_String(self, node):
        return String()

    def visit_Matrix(self, node):
        oldsize = None
        type = None
        for row in node.value:
            newsize = len(row)
            if oldsize is not None and oldsize != newsize:
                self.error(f"Rows of matrix don't have equal lenghts, found rows of size {oldsize} and {newsize}", row[0].lineno)
            oldsize = len(row)
            for v in row:
                t = self.visit(v)
                if type and type != t and t != None and (not isinstance(type, Scalar) or not isinstance(t, Scalar)):
                    self.error(f"Mismatched types in matrix definition {type}, {t}", v.lineno)
                if type == Integer() or type == None:
                    type = t
        if type != Integer() and type != Float() and type != None:
            self.error(f"Matrixes can only contain Numeric values, but found {type}", node.lineno)
        if oldsize == 0 and len(node.value) == 1:
            return Matrix(0, 0, Integer())
        else:
            return Matrix(len(node.value), oldsize, type)

    def visit_Zeros(self, node):
        t = self.visit(node.value)
        if t != Integer():
            self.error(f"Zeros parameters should be Integers, but found {t}", node.lineno)
            return None
        vals = node.value.value if node.value.value is not None else []
        vals = list(map(lambda x: x.value, vals))
        if len(vals) != 1 and len(vals) != 2:
            self.error(f"Zeros must take one or two integer arguments, but found {len(vals)}", node.lineno)
        if len(vals) == 1:
            return Matrix(vals[0], vals[0], Integer())
        else:
            return Matrix(vals[0], vals[1], Integer())

    def visit_Ones(self, node):
        t = self.visit(node.value)
        if t != Integer():
            self.error(f"Ones parameters should be Integers, but found {t}", node.lineno)
            return None
        vals = node.value.value if node.value.value is not None else []
        vals = list(map(lambda x: x.value, vals))
        if len(vals) != 1 and len(vals) != 2:
            self.error(f"Ones must take one or two integer arguments, but found {len(vals)}", node.lineno)
        if len(vals) == 1:
            return Matrix(vals[0], vals[0], Integer())
        else:
            return Matrix(vals[0], vals[1], Integer())
    
    def visit_Eye(self, node):
        t = self.visit(node.value)
        if t != Integer():
            self.error(f"Eye parameters should be Integers, but found {t}", node.lineno)
            return None
        vals = node.value.value if node.value.value is not None else []
        vals = list(map(lambda x: x.value, vals))
        if len(vals) != 1 and len(vals) != 2:
            self.error(f"Eye must take one or two integer arguments, but found {len(vals)}", node.lineno)
        if len(vals) == 1:
            return Matrix(vals[0], vals[0], Integer())
        else:
            return Matrix(vals[0], vals[1], Integer())

    def visit_Range(self, node):
        exp1 = self.visit(node.start)
        exp2 = self.visit(node.end)
        if (exp1 != Integer() and exp1) or (exp2 != Integer() and exp2):
            self.error(f"Range takes only integers as parameters, but found {exp1} {exp2}", node.lineno)
        return Integer()

    def visit_UnaryMinus(self, node):
        type = self.visit(node.value)
        if not isinstance(type, Numeric) and type is not None:
            self.error(f"Unary minus takes as argument only numeric types, but found {type}", node.lineno)
        return type

    def visit_MatrixTranspose(self, node):
        m_type = self.visit(node.value)
        if not isinstance(m_type, Matrix) and m_type is not None:
            self.error(f"Matrix transposition can only be done on matrixes, but found {m_type}", node.lineno)
            return None
        elif m_type is None:
            return None
        else:
            return Matrix(m_type.m, m_type.n, m_type.type)

    def visit_MatrixCellGetter(self, node):
        m_type = self.symbolTable.getType(node.id)
        if not isinstance(m_type, Matrix) and m_type is not None:
            self.error(f"Matrix getter can only be used on a Matrix, but found {m_type}", node.lineno)
            return None
        elif m_type is None:
            return None
        else:
            return m_type.type

    def visit_Statements(self, node):
        for c in node.values:
            t = self.visit(c)
            if self.is_expressions(type(c), c):
                self.warn(f"Unused expression of type {t}", c.lineno)

    def visit_Expressions(self, node):
        for e in node.values:
            self.visit(e)
