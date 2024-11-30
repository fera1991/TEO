from enum import StrEnum

from SymbolTable import Symbol, SymbolTable, identificadorEnum
from TokenEnum import TokenEnum
from TokenInfo import TokenInfo
from expresionHandler import Expresion, ExpressionHandler


class ActionEnum(StrEnum):
    CS= 'clear semantics props'
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
    RSF='resolver switch flow' # Sirve para ver si todas las bifurcaciones del switch llegan a un return

    PTV='Push Type of Var' # PT + añadir una lista vacia a la pila para las variables
    VL= 'var list' # lista vacia paa 1 var
    PV='Push var to list'
    RVD='Resolve var declaration'
    ATL='Assign to list'

    # Manejo de identificadores y expresiones
    PTE='Push token expresion'
    IPL='Init paramas list'
    PPP='Push Param Expression'
    PTWV='Previus Token was a Variable'
    PTWF='Previus Token was a Function'
    
    # Operaciones aritmeticas
    RS= 'resolver suma'
    RR= 'resolver resta'
    RD= 'resolver division'
    RM= 'resolver multiplicación'

A= ActionEnum

class Parameter():
    type: TokenInfo
    name: TokenInfo

    def __init__(self, type, name):
        self.name = name
        self.type = type

class SemanticAction():
    actionStack = []
    semanticStack = []
    scopeStack = []
    returnStack = []
    symbolTable: SymbolTable
    tokenActual: TokenInfo
    insideSwitch: bool

    def __init__(self, symbolTable: SymbolTable):

        self.symbolTable = symbolTable
        self.insideSwitch = False
        self.returnStack: list = []
        self.modoSeguro = False
        self.errores = False
        self.semanticStack: list = ["Stack's bottom"]
        self.expHandler = ExpressionHandler(self.symbolTable, self.semanticStack, self.scopeStack, self.error)
    
    def addAction(self, action: ActionEnum):
        self.actionStack.append(action)

    def error(self, token: TokenInfo, msg: str):

        if isinstance(token, Symbol):
            line = token.linea
            position = token.inicio
        else:
            line = token.line
            position = token.initial_position
        self.errores = True
        print("Error semantico en linea: ", line,", posición: ",position)
        print(msg)

    def setCurrentToken( self, tk: TokenEnum):
        self.tokenActual = tk

    def execute(self, action: ActionEnum):

        semanticStack = self.semanticStack
        scopeStack = self.scopeStack
        t = self.tokenActual
        expHandler = self.expHandler
        symbolTable = self.symbolTable
        
        if action == A.CS:
            self.semanticStack.clear()
            self.semanticStack.append("Stack's botton")
            self.insideSwitch = False
            self.returnStack.clear()
            self.scopeStack.clear()
            self.semanticStack.append('global')
            self.symbolTable.returnToGlobal()
            self.modoSeguro = False
        
        if self.modoSeguro:
            return

        elif action == A.PI:
            semanticStack.append(t)

        elif action == A.PT:
            semanticStack.append(t)

        elif action == A.SP: # save parameter as object in the stack
            id = self.tokenActual.value
            type = semanticStack.pop()
            parameter = Parameter(type, id)
            semanticStack.append(parameter)

        
        elif action == A.DP: # declare prototype
            self.declarePrototype()
        
        elif action == A.DF:    
            self.declareFunction()
        
        elif action == A.ES:
            self.symbolTable.exitScope()
        
        elif action == A.CRT:
            self.checkReturn()
        elif action == A.HR:
            self.hasReturn()
        elif action == A.PTE:
            expHandler.addTokenExpression(t)
        elif action == A.IPL:
            expHandler.initParamasList()
        elif action == A.PPP:
            expHandler.pushParamasExpression(t)
        elif action == A.PTWV:
            expHandler.prevTokenWasVar()
        elif action == A.PTWF:
            expHandler.prevTokenWasFunction()
        elif action == A.RS:
            expHandler.resolveSum()
        elif action == A.RR:
            expHandler.resolveResta()
        elif action == A.RM:
            expHandler.resolveMul()
        elif action == A.RD:
            expHandler.resolveDiv()
        elif action == A.VL:
            semanticStack.append([]) # lista para var
        elif action == A.PTV:
            semanticStack.append(t)
            semanticStack.append([]) # lista para las variables
        elif action == A.PV:
            lista = semanticStack.pop() # recuperar lista
            lista.append((t, None))
            semanticStack.append(lista)
        elif action == A.ATL:
            e=semanticStack.pop()
            lista = semanticStack.pop()
            for var, v in lista:
                if v is None:
                    v = e
                else:
                    break
            semanticStack.append(lista)

        elif action == A.RVD:
            lista = semanticStack.pop()
            type = semanticStack.pop()
            for var, value in lista:
                var: TokenInfo
                v = symbolTable.findSymbol(var.value)
                if v is not None:
                    self.error(var, f"Identificador {var.value} ya ha sido declarado en este ambito")
                else:
                    symbolTable.defineVariable(var.value, type, var.initial_position, var.line, value)

        
    def declarePrototype(self):
            
        semanticStack = self.semanticStack
        symbolTable = self.symbolTable
        t = self.tokenActual
        parameters = []
        while isinstance(semanticStack[-1], Parameter):
            parameters.append(semanticStack.pop())

        name = semanticStack.pop()
        type = semanticStack.pop()
        

        id = symbolTable.findSymbol(name.token.value)
        if id is not None:
            same = id.tipo_valor == type
            arguments = len(id.parametros) != 0 # Si es 0, ponerlo falso porque no entrara al bucle

            if len(id.parametros) != len(parameters):
                arguments = False
            
            for i, (defined_type, param) in enumerate(zip(id.parametros, parameters)):
                if param.token != defined_type:
                    arguments = False

            if not same:
                self.error(type, f"{name.value} fue declarado, pero como tipo {id.tipo.value} en lugar de {type.value}")
            if not arguments:
                self.error(name, f"{name.value} no coincide con los parametros declarados en el prototipo")
            if not same or not arguments:
                symbolTable.createScope() # Independiente del resultado, despues habra un ES: Exit Scope, asi que lo creamos aqui para evitar problemas
                return
        
        if id is None: # No se habia declarado antes
            # If wasnt problems, create scope and insert parameter(now includings identifiexrs) in it
            symbolTable.defineFunction(name.value, type.token, name.initial_position, name.line, True)
            symbolTable.createScope()
            for p in parameters:
                symbolTable.addParameter(name.value, p.type.token) # Todavia no inluir los parametros como variables hasta definicion completa


    def declareFunction(self):
    
        semanticStack = self.semanticStack
        symbolTable = self.symbolTable
        scopeStack = self.scopeStack
        returnStack = self.returnStack
        t = self.tokenActual

        parameters: list[Parameter] = []
        while isinstance(semanticStack[-1], Parameter):
            parameters.append(semanticStack.pop())

        name: TokenInfo = semanticStack.pop()
        type: TokenInfo = semanticStack.pop()


        id = symbolTable.findSymbol(name.token.value)
        if id is not None:
            isPrototype = id.tipo = identificadorEnum.PROTOTYPE
            same = id.tipo_valor == type
            arguments = len(id.parametros) != 0 # Si es 0, ponerlo falso porque no entrara al bucle

            if len(id.parametros) != len(parameters):
                arguments = False
            
            for i, (defined_type, param) in enumerate(zip(id.parametros, parameters)):
                if param.token != defined_type:
                    arguments = False

            if not isPrototype:
                self.error(name, f"Redefinicion de identificador {name.value} como funcion de tipo {type.value}")
                symbolTable.createScope() # Independiente del resultado, despues habra un ES: Exit Scope, asi que lo creamos aqui para evitar problemas
                return
            if not same:
                self.error(type, f"{name.value} fue declarado, pero como tipo {id.tipo.value} en lugar de {type.value}")
            if not arguments:
                self.error(name, f"{name.value} no coincide con los parametros declarados en el prototipo")
            if not same or not arguments:
                symbolTable.createScope() # Independiente del resultado, despues habra un ES: Exit Scope, asi que lo creamos aqui para evitar problemas
                return
        if id is None: # No se habia declarado ni como prototipo
            symbolTable.defineFunction(name.value, type.token, name.initial_position, name.line, False)
        else: # Si llega hasta aqui, si se habia declarado como protipo
            symbolTable.updateFunctionType(name.value)

        # If wasnt problems, create scope and insert parameter(now includings identifiers) in it
        symbolTable.createScope()
        for p in parameters:
            symbolTable.addParameter(name.value, p.type.token)
            symbolTable.defineVariable(name.value, p.type.token, name.initial_position ,name.line)

        self.returnStack.clear() # Clear out return stack for new function body definition
        self.returnStack.append(type) # save return type
        self.returnStack.append(False) # Mark that the function still doesnt have a return
 
    def checkReturn(self):
        semanticStack = self.semanticStack
        scopeStack = self.scopeStack
        insideCase = self.insideSwitch
        returnStack = self.returnStack

        r:TokenInfo = returnStack[0]
        self.semanticStack.append(Expresion(None, 0, 12, 32, 89))
        e = self.semanticStack.pop()
        if(r.token == TokenEnum.VOID and e.type != None):
            self.error(e, "La funcion fue declarada como void, pero retorna una expresión")

        if not self.expHandler.compatibleType(r.token, e):
            s = f"Error, la función fue declarada como tipo {r.value}, pero "
            s += "no retorna ninguna expresión" if e.type == None else f"retorna una expresion de tipo {e.type}"
            self.error(e, s)

        r = returnStack.pop() # See if current flow already has a return

        returnStack.append( r if r else True) # Mark return in flow

        if insideCase:
            returnStack.append(False) # Inside a switch, a return also acts as a break, splitting the case flow
            # So, the next case/default still doent have a return

    def hasReturn(self):
        r = self.returnStack.pop()
        if not isinstance(r, bool):
            if not r:
                # TODO verificaar que este bien mostrar el mensaje en el token actual
                self.error(self.tokenActual ,"La funcion debe tener un return al final de cada camino antes de terminar")

    def createFlow(self):
        self.returnStack.append(False)

    def createFlowInSwitch(self):
        self.returnStack.append(self.tokenActual())
        self.createFlow()
    
    def breakFlow(self):
        if self.returnStack[-1] == True: # A return was used before in the same flow
            self.error(self.tokenActual, "Codigo inalcanzable: break despues de return")
            return
        
        if self.insideSwitch:
            self.returnStack.append(False) # Inside a switch, a break splits the case flow


    def checkPreviusCaseReturn(self):
        r = self.returnStack[-1] # Get gurrent flow, if previus case has a return, this will be true
        if r:
            self.createFlow()

    def resolveSwicthFlow(self):
        r=self.returnStack.pop()
        allFlowHasReturn = True
        while( not isinstance(r, TokenInfo) or r.token != TokenEnum.SWITCH):
            allFlowHasReturn = allFlowHasReturn and r
            r=self.returnStack.pop()
        
        r=self.returnStack.pop() # Now get main flow
        self.returnStack.append( r or allFlowHasReturn) # Mark if main flow already has a main return or all flows in switch ends with return
                