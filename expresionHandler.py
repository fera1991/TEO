from enum import StrEnum

from SymbolTable import SymbolTable
from TokenEnum import TokenEnum
from TokenInfo import TokenInfo


class actionEnum(StrEnum):
    PT= 'push type'
    PI= 'push identificator'
    SP= 'save parameter'
    DP= 'declare prototype'
    DF= 'declare function'
    ES= 'exit scope'
    # Sirven para checkear que una funcion siempre tenga un return apropiado, incluyendo las bifurcaciones
    CRT = 'check return type'
    HR='has return' # Si la funcion no es void, debe tener un return al final de cada camino
    CFS='create new flow for switxh'
    BF='break flow in switch'
    CPCR='check if prev case had return'
    RSF='resolver switch flow' # Sirve para ver si todas las bifurcaciones del switch llegan a un return'

A= actionEnum

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
    position: int

    def __init__(self, t, v, l, p):
        self.line=l
        self.type=t
        self.value=v
        self.position=p

class ExpressionHandler():
    semanticStack: []

    def __init__(self, symbolTable: SymbolTable, semanticStack, error):
        self.semanticStack = semanticStack
        self.symbolTable = symbolTable
        self.insideSwitch = False
        self.error = error

    def converTypeToExpr(self, token: TokenEnum):
        
        if token.type == TokenEnum.VOID:
            return T.NONE
        if token.type == TokenEnum.INT:
            return T.INT
        if token.type == TokenEnum.FLOAT:
            return T.FLOAT
        if token.type == TokenEnum.CHAR:
            return T.CHAR
        
        print(f"Por alguna razon, {token.name}  no se pudo convertir a nada")
        return T.NONE
    
    def compatibleType(self, token, exp) -> bool: # TODO hacer las otras
        void=[T.NONE]
        int=[T.INT, T.FLOAT, T.CHAR]
        char = [T.CHAR, T.INT]
        float = [T.INT, T.FLOAT, T.CHAR]

        if token.type == TokenEnum.VOID and exp.type in void:
            return True
        if token.type == TokenEnum.INT and exp.type in int:
            return True
        if token.type == TokenEnum.FLOAT and exp.type in char:
            return True
        if token.type == TokenEnum.CHAR and exp.type in float:
            return True
        
        return False
    
    def operateTypes(self, op1, op2):
        type1=op1.type
        type2=op2.type
        if type1 == type2:
            return type1
        # Definir la jerarquía de tipos en orden ascendente
        type_hierarchy = [T.CHAR, T.INT, T.FLOAT]

        r = max(type1, type2, key=type_hierarchy.index)

        return r if r!=T.CHAR else T.INT # En una operacion aritemtica convertir siempre char en int
    
    def addTokenExpression(self, tk: TokenInfo):

        if tk.token == TokenEnum.NUMERIC_CONSTANT:
            if tk.value.isdigit():
                v=int(tk.value)
                self.semanticStack.append( Expresion(T.INT, v, tk.line, tk.initial_position) )
            else:
                try:
                    v = float(tk.value)
                    self.semanticStack.append( Expresion(T.FLOAT, v, tk.line, tk.initial_position) )
                except ValueError:
                    print("El token NUMERIC_CONSTANT no se pudo convertir a numero")
        elif tk.token == TokenEnum.CHAR_LITERAL :
            self.semanticStack.append( Expresion(T.CHAR, 0, tk.line, tk.initial_position) )

        elif tk.token == TokenEnum.IDENTIFIER:
            self.semanticStack.append(tk) # Por el momento guardar como token
    
    def initParamasList(self):
        self.semanticStack.append([]) # Cuando se llama, es porque viene una lista de parametros

    def pushParamasExpression(self, tk: TokenInfo):
        e = self.semanticStack.pop( ) # Sacar la ultima expresion añadida a la pila
        self.semanticStack[-1].append(e) # Añadir a la lista de parametros inicializada antes de entrar a la expresion

    def prevTokenWasVar(self):
        tk = self.semanticStack.pop()
        # TODO buscar el identificador en la tabla de simbolos como variable
        type = "tipo de la variable segun la tabla"
        exists = True

        if(not exists):
            self.error(tk, f"Se invoca la variable {tk.value}, pero no se declaro antes")

        self.semanticStack.append( Expresion(self.converTypeToExpr(tk), None, tk.line, tk.initial_position)) # Ahora regresarla como expresión

    def prevTokenWasFunction(self):
    
        p = self.semanticStack.pop() # Sacar lista de parametros
        f = self.semanticStack.pop() # Sacar funcion

        # TODO buscar el identificador en la tabla de simbolos como funcion
        type = "tipo de la variable segun la tabla"
        params = ['tipo de los parametros de la funcion segun la tabla de simbolos']
        exists = True

        if not exists:
            self.error(f, f"Referencia indefinida a función {f.value}")
    

        if exists:
            if type == TokenEnum.VOID:
                self.error(f, f"LA funcion {f.value} esta declarada como void. No retorna ningun valor")
            if len(params) != len(p):
                self.error(f, f"La cantidad de parametros no coincide con la definición {f.value}")
            else:
                for i, ( t, p ) in enumerate( zip( params, p)):
                    if not self.compatibleType(t, p): # Comparador el TokenEnum que representa el tipo del parametro, con la expresion que se le intenta pasar
                        self.error(p, f"Al parametro N° {i} de tipo: {t.value} se le intentanta asignar una expresion no compatible: {p.type}")
            
        # Si todo esta bien, puede añadirse la invocaion de la funcion como una expresion del tipo que retorna
        # El 5 es arbitrario, ya que no creo usar el valor despues en este caso
        self.semanticStack.append( Expresion(self.converTypeToExpr(type), None, f.line, f.initial_position)) # Ahora regresarla como expresión

    def resolveSum(self):
        op1: Expresion = self.semanticStack.pop()
        op2: Expresion = self.semanticStack.pop()
        v = None
        typeResult = self.operateTypes(op1, op2)
        result = Expresion(typeResult, v, op1.line, op1.position)
        self.semanticStack.append(result)
    
    def resolveResta(self):
        op1: Expresion = self.semanticStack.pop()
        op2: Expresion = self.semanticStack.pop()
        v = None
        typeResult = self.operateTypes(op1, op2)        
        result = Expresion(typeResult, v, op1.line, op1.position)
        self.semanticStack.append(result)
    
    def resolveMul(self):
        op1: Expresion = self.semanticStack.pop()
        op2: Expresion = self.semanticStack.pop()
        v = None
        typeResult = self.operateTypes(op1, op2)
        result = Expresion(typeResult, v, op1.line, op1.position)
        self.semanticStack.append(result)
    
    def resolveDiv(self):
        op1: Expresion = self.semanticStack.pop()
        op2: Expresion = self.semanticStack.pop()
        v = None
        typeResult = self.operateTypes(op1, op2)        
        result = Expresion(typeResult, v, op1.line, op1.position)
        self.semanticStack.append(result)
