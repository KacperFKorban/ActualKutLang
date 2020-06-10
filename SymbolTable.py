class VariableSymbol(object):

    def __init__(self, name, type):
        self.name = name
        self.type = type
        
class Type:
    def __eq__(self, obj):
        return type(self) is type(obj)
    
class String(Type):
    def __repr__(self):
        return "String"

class Numeric(Type):
    pass

class Boolean(Type):
    def __repr__(self):
        return "Boolean" 

class Scalar(Numeric):
    pass

class Integer(Scalar):
    def __repr__(self):
        return "Integer"
    pass
    
class Float(Scalar):
    def __repr__(self):
        return "Float"
    pass

class Matrix(Numeric):
    def __init__(self, n, m, type):
        self.type = type
        self.n = n
        self.m = m
    def __repr__(self):
        return f"Matrix({self.n}, {self.m}, {self.type})"
    def equals(self, other):
        return isinstance(other, Matrix) and self.n == other.n and self.m == other.m
    def getCommonType(self, other):
        if isinstance(other, Matrix):
            return Float() if self.type == Float() or other.type == Float() else Integer()

class Range(Type):
    def __repr__(self):
        return "Range"

class Def(Type):
    def __init__(self, args, res):
        self.args = args
        self.res = res
    def __repr__(self):
        return f"Def({self.args}, {self.res})"

class SymbolTable(object):

    def __init__(self):
        self.parent = None
        self.scope = {}

    def set(self, symbol):
        if self.get(symbol.name) is None:
            self.scope[symbol.name] = symbol
        else:
            self.update_up(symbol)

    def put(self, symbol):
        self.scope[symbol.name] = symbol

    def update_up(self, symbol):
        if self.scope.get(symbol.name) is not None:
            self.put(symbol)
        else:
            self.parent.update_up(symbol)

    def get(self, name):
        if self.scope.__contains__(name):
            return self.scope[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            return None

    def getType(self, name):
        return self.get(name).type if self.get(name) else None
