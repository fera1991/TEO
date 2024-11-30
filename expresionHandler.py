from enum import StrEnum

from SymbolTable import Symbol, SymbolTable
from TokenEnum import TokenEnum
from TokenInfo import TokenInfo

class TypeEnum(StrEnum):
    NONE = 'vacio'
    INT = 'type int'
    FLOAT = 'type float'
    CHAR = 'type char'

T = TypeEnum

class Parameter():
    type: TokenInfo
    name: TokenInfo

    def __init__(self, type, name):
        self.name = name
        self.type = type

class Expresion():
    type: str
    value: str
    line: int
    initial_position: int
    final_position: int

    def __init__(self, t, v, l, ip, fp):
        self.line=l
        self.type=t
        self.value=v
        self.initial_position=ip
        self.final_position=fp

class ExpressionHandler():

    def __init__(self, symbolTable: SymbolTable, semanticStack, scopeStack, error):
        self.semanticStack = semanticStack
        self.symbolTable = symbolTable
        self.insideSwitch = False
        self.error = error
        self.scopeStack = scopeStack

    def converTypeToExpr(self, token: TokenEnum):
        
        if token == TokenEnum.VOID:
            return T.NONE
        if token == TokenEnum.INT:
            return T.INT
        if token == TokenEnum.FLOAT:
            return T.FLOAT
        if token == TokenEnum.CHAR:
            return T.CHAR
        
        print(f"Por alguna razon, {token}  no se pudo convertir a nada")
        return T.NONE
    
    def compatibleType(self, token, exp) -> bool:
        void=[T.NONE]
        int=[T.INT, T.FLOAT, T.CHAR]
        char = [T.CHAR, T.INT]
        float = [T.INT, T.FLOAT, T.CHAR]

        if token == TokenEnum.VOID and exp.type in void:
            return True
        if token == TokenEnum.INT and exp.type in int:
            return True
        if token == TokenEnum.FLOAT and exp.type in char:
            return True
        if token == TokenEnum.CHAR and exp.type in float:
            return True
        
        return False
    
    def operateTypes(self, op1, op2):
        type1=op1.type
        type2=op2.type
        if type1 == type2:
            return type1
        # Definir la jerarquía de tipos en orden ascendente
        type_hierarchy = [T.NONE, T.CHAR, T.INT, T.FLOAT]

        r = max(type1, type2, key=type_hierarchy.index)

        return r if r!=T.CHAR else T.INT # En una operacion aritemtica convertir siempre char en int
    
    def addTokenExpression(self, tk: TokenInfo):

        if tk.token == TokenEnum.NUMERIC_CONSTANT:
            if tk.value.isdigit():
                v=int(tk.value)
                self.semanticStack.append( Expresion(T.INT, v, tk.line, tk.initial_position, tk.final_position) )
                v=8
            else:
                try:
                    v = float(tk.value)
                    self.semanticStack.append( Expresion(T.FLOAT, v, tk.line, tk.initial_position, tk.final_position) )
                except ValueError:
                    print("El token NUMERIC_CONSTANT no se pudo convertir a numero")
        elif tk.token == TokenEnum.CHAR_LITERAL :
            self.semanticStack.append( Expresion(T.CHAR, 0, tk.line, tk.initial_position, tk.final_position) )

        elif tk.token == TokenEnum.IDENTIFIER:
            self.semanticStack.append(tk) # Por el momento guardar como token
    
    def initParamasList(self):
        self.semanticStack.append([]) # Cuando se llama, es porque viene una lista de parametros

    def pushParamasExpression(self, tk: TokenInfo):
        e = self.semanticStack.pop( ) # Sacar la ultima expresion añadida a la pila
        self.semanticStack[-1].append(e) # Añadir a la lista de parametros inicializada antes de entrar a la expresion

    def prevTokenWasVar(self):
        tk: TokenInfo = self.semanticStack.pop()
        id: Symbol = self.symbolTable.findSymbol(tk.value)
        exists = True

        if(id is None):
            self.error(tk, f"Se invoca la variable {tk.value}, pero no se declaro antes")

        self.semanticStack.append( Expresion(self.converTypeToExpr(tk.token), None, tk.line, tk.initial_position, tk.final_position)) # Ahora regresarla como expresión

    def prevTokenWasFunction(self):
    
        p = self.semanticStack.pop() # Sacar lista de parametros 
        ftk: TokenInfo = self.semanticStack.pop() # Sacar id funcion

        if not isinstance(ftk, TokenInfo):
            ftk = ftk[0][0]

        f: Symbol = self.symbolTable.findSymbol(ftk.value)

        if f is None:
            self.error(ftk, f"Referencia indefinida a función {ftk.value}")
            self.semanticStack.append( Expresion( TypeEnum.NONE, None, ftk.line, ftk.initial_position, ftk.final_position))
            return
    
        type = f.tipo_valor
        params = f.parametros
        Flag = True

        if type == TokenEnum.VOID:
            self.error(f, f"La funcion {ftk.value} esta declarada como void. No retorna ningun valor")
            Flag = False
        if len(params) != len(p):
            self.error(f, f"La cantidad de parametros no coincide con la definición de {ftk.value}")
        else:
            for i, ( t, p ) in enumerate( zip( params, p)):
                if not self.compatibleType(t, p): # Comparador el TokenEnum que representa el tipo del parametro, con la expresion que se le intenta pasar
                    self.error(p, f"Al parametro N° {i} de tipo: {t.value} se le intentanta asignar una expresion no compatible: {p.type}")
            
        # Si todo esta bien, puede añadirse la invocacion de la funcion como una expresion del tipo que retorna
        if Flag:
            self.semanticStack.append( Expresion(self.converTypeToExpr(type), None, ftk.line, ftk.initial_position, ftk.final_position)) # Ahora regresarla como expresión
        else:
            self.semanticStack.append( Expresion( TypeEnum.NONE, None, ftk.line, ftk.initial_position, ftk.final_position))

    def resolveSum(self):
        op1: Expresion = self.semanticStack.pop()
        op2: Expresion = self.semanticStack.pop()
        v = None
        typeResult = self.operateTypes(op1, op2)
        result = Expresion(typeResult, v, op1.line, op1.initial_position, op1.final_position)
        self.semanticStack.append(result)
    
    def resolveResta(self):
        op1: Expresion = self.semanticStack.pop()
        op2: Expresion = self.semanticStack.pop()
        v = None
        typeResult = self.operateTypes(op1, op2)        
        result = Expresion(typeResult, v, op1.line, op1.initial_position, op1.final_position)
        self.semanticStack.append(result)
    
    def resolveMul(self):
        op1: Expresion = self.semanticStack.pop()
        op2: Expresion = self.semanticStack.pop()
        v = None
        typeResult = self.operateTypes(op1, op2)
        result = Expresion(typeResult, v, op1.line, op1.initial_position, op1.final_position)
        self.semanticStack.append(result)
    
    def resolveDiv(self):
        op1: Expresion = self.semanticStack.pop()
        op2: Expresion = self.semanticStack.pop()
        v = None
        typeResult = self.operateTypes(op1, op2)        
        result = Expresion(typeResult, v, op1.line, op1.initial_position, op1.final_position)
        self.semanticStack.append(result)
