from enum import StrEnum

from SymbolTable import SymbolTable
from TokenEnum import TokenEnum
from TokenInfo import TokenInfo
from expresionHandler import ExpressionHandler


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
    RSF='resolver switch flow' # Sirve para ver si todas las bifurcaciones del switch llegan a un return

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

A= actionEnum

class Parameter():
    type: TokenInfo
    name: TokenInfo

    def __init__(self, type, name):
        self.name = name
        self.type = type

class semanticAction():
    actionStack: []
    semanticStack: []
    scopeStack: []
    returnStack: []
    symbolTable: SymbolTable
    tokenActual: TokenInfo
    insideSwitch: bool

    def __init__(self, symbolTable: SymbolTable):

        self.symbolTable = symbolTable
        self.insideSwitch = False
        self.expHandler = ExpressionHandler(self.symbolTable, self.semanticStack, self.scopeStack, self.error)
    
    def addAction(self, action: actionEnum):
        self.actionStack.append(action)

    def error(self, token: TokenInfo, msg: str):
        line = token.get_line
        position = token.get_initial_position()
        
        print("Error semantico en linea: "+line+", posición: "+position)
        print(msg)

    def compatibleType(token, exp) -> bool: # TODO hacer las otras
        void=[None]
        if token.type == TokenEnum.VOID and exp.type in void:
            return True

    def execute(self):

        action = self.actionStack[-1]
        semanticStack = self.semanticStack
        scopeStack = self.scopeStack
        t = self.tokenActual
        expHandler = self.expHandler
        
        if action == A.PI:
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
            scopeStack.pop() # Salir del ultimo ambito
        
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
            expHandler.prevTokenWasFunction()
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
        

    def declarePrototype(self):
            
        semanticStack = self.semanticStack
        scopeStack = self.scopeStack
        t = self.tokenActual
        parameters = []
        while isinstance(semanticAction[-1], Parameter):
            parameters.append(semanticStack.pop())

        name = semanticStack.pop()
        type = semanticStack.pop()
        exists =  False # TODO: search in symbolTable for function name, that return type

        if(exists):
            self.error( name, "Identificador:"+name.get_value()+" ya ha sido declarado en el ambito")
        else:
            # TODO insert in symbolTable function with identifier=name, that returns type and have selected parameters.
            # Mark as only prototype
            # also create scope for function, and push in scopeStack
            scopeStack.append("Scope de prototipo")

    def declareFunction(self):
    
        action = self.actionStack[-1]
        semanticStack = self.semanticStack
        scopeStack = self.scopeStack
        t = self.tokenActual

        parameters = []
        while isinstance(semanticAction[-1], Parameter):
            parameters.append(semanticStack.pop())

        name = semanticStack.pop()
        type = semanticStack.pop()

        exists =  True # TODO: search in symbolTable for function name, that return type

        if not exists:
            # TODO save identifier and type on symbol table
            SymbolTable
        else:
            same = True # TODO verify that have the same type as protype
            arguments = True # TODO verify that both have the same type and quantity of parameters. Identifiers doesnt matter

            if not same:
                self.error(type, name.value+ " fue declarado, pero como tipo x en lugar de "+type.value)
            if not arguments:
                self.error(type, name.value+ " no coincide con los parametros declarados en el prototipo")

        # If wasnt problems, create scope and insert parameter(now includings identifiers) in it

        scopeStack.append("scope de la función")

        self.returnStack = [] # Clear out return stack for new body definition
        self.returnStack.append(type) # save return type
 
    def checkReturn(self):
        action = self.actionStack[-1]
        semanticStack = self.semanticStack
        scopeStack = self.scopeStack
        insideCase = self.insideSwitch
        returnStack = self.returnStack

        r:TokenInfo = returnStack[0]
        e = self.semanticStack.pop()
        if(r.token == TokenEnum.VOID and e.type != None):
            self.error(e, "Error, la expresion fue declarada como void, pero retorna una expresión")

        if not self.compatibleType(r, e):
            s = f"Error, la función fue declarada como tipo {r.get_value}, pero "
            s += "no retorna ninguna expresión" if e.type == None else f"retorna una expresion de tipo {e.type}"
            self.error(e, s)

        r = returnStack.pop() # See if current flow already has a return

        returnStack.append( r if r else True) # Mark return in flow

        if insideCase:
            returnStack.append(False) # Inside a switch, a return also acts as a break, splitting the case flow
            # So, the next case/default still doent have a return

    def hasReturn(self):
        r = self.returnStack.pop()
        if not r:
            # TODO verificaar que este bien mostrar el mensaje en el token actual
            self.error(self.tokenActual ,"La funcion debe tener un return al final de cada camino")

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
                