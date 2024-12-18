from FileHandler import FileHandler
from LL1Generator import LL1Generator
from Lexer import Lexer
from NonTerminalEnum import NonTerminalEnum
from Processors.InvalidProcessor import InvalidProcessor
from Processors.NumberProcessor import NumberProcessor
from Processors.StringProcessor import StringProcessor
from Processors.IdentifierAndKeywordProcessor import IdentifierAndKeywordProcessor
from Processors.IgnoreProcessor import IgnoreProcessor
from Processors.OperatorProcessor import OperatorProcessor
from TokenEnum import TokenEnum
from TokenInfo import TokenInfo
from SymbolTable import SymbolTable
from collections import defaultdict
from semanticAction import ActionEnum, SemanticAction
from syntaxTree import NodoArbol, generar_arbol_sintactico, generar_arbol_sintactico_terminal


def matriz_default():
    return defaultdict(lambda: None) # Any non-defined cell will return None

NT = NonTerminalEnum
T = TokenEnum
Action =ActionEnum
tabla_ll1 = defaultdict(matriz_default)


# Definir las producciones de la gramática
P = defaultdict(list)

P[NT.S] = [[NT.FN, Action.CS, NT.S], []]

P[NT.FN]=[
    [NT.TR, Action.PT, T.IDENTIFIER, Action.PI, T.ABRIR_PARENTESIS, NT.P, T.CERRAR_PARENTESIS, NT.FN_, Action.ES]]

P[NT.TR]=[
    [T.VOID],
    [NT.T]]

P[NT.P]=[
    [NT.T, Action.PT, T.IDENTIFIER, Action.SP, NT.P_],
    []]

P[NT.P_]=[
    [T.COMA, Action.PT, T.IDENTIFIER, Action.SP, NT.P_],
    []]

P[NT.FN_]=[
    [Action.DP, T.PUNTO_COMA],
    [ Action.DF,T.ABRIR_LLAVE, NT.B_, T.CERRAR_LLAVE, Action.HR]]

P[NT.B_]=[
    [NT.B, NT.B_],
    []]

P[NT.B]=[
    [NT.ID],
    [NT.D],
    [NT.R],
    [NT.I],
    [NT.WH],
    [NT.SW]]

P[NT.D]=[[NT.T, Action.PTV, NT.V, Action.RVD, T.PUNTO_COMA]]

P[NT.T]=[
    [T.INT], 
    [T.CHAR], 
    [T.FLOAT]]

P[NT.V]=[[T.IDENTIFIER, Action.PV, NT.A_, NT.V_]]

P[NT.V_]=[[T.COMA, T.IDENTIFIER, Action.PV, NT.A_, NT.V_], []]

P[NT.A_]=[[], [T.ASIGNACION, NT.E, Action.ATL]]

P[NT.ID]=[[Action.VL,T.IDENTIFIER, Action.PV, NT.ID_]]

P[NT.ID_]=[[NT.C, T.PUNTO_COMA], [NT.A]]

P[NT.A]=[[T.ASIGNACION, NT.E, Action.ATL, T.PUNTO_COMA]]

P[NT.E]=[[NT.TE, NT.E_]]

P[NT.E_]=[
    [], 
    [T.SUMA, NT.TE, Action.RS, NT.E_], 
    [T.RESTA, NT.TE,Action.RR, NT.E_]]

P[NT.TE]=[[NT.F, NT.TE_]]

P[NT.TE_]=[
    [],
    [T.MULTIPLICACION, NT.F, Action.RM, NT.TE_],
    [T.DIVISION, NT.F, Action.RD, NT.TE_]]

P[NT.F]=[
    [T.IDENTIFIER, Action.PTE, NT.F_],
    [T.ABRIR_PARENTESIS, NT.E, T.CERRAR_PARENTESIS],
    [T.NUMERIC_CONSTANT, Action.PTE],
    [T.CHAR_LITERAL, Action.PTE,]]

P[NT.F_]=[
    [NT.C],
    [ Action.PTWV]]

P[NT.L]=[[NT.E, NT.OP, NT.E]]

P[NT.OP]=[
    [T.IGUALDAD],
    [T.MAYOR_QUE],
    [T.MENOR_QUE]]

P[NT.C]=[
    [T.ABRIR_PARENTESIS, Action.IPL, NT.APL, T.CERRAR_PARENTESIS, Action.PTWF]]

P[NT.APL]=[
    [NT.E, Action.PPP, NT.APL_],
    []]

P[NT.APL_]=[
    [T.COMA, NT.E, Action.PPP, NT.APL_],
    []]

P[NT.R]=[[T.RETURN, NT.R_, Action.CRT, T.PUNTO_COMA]]

P[NT.R_]=[[NT.E], []]

P[NT.I]=[[T.IF, T.ABRIR_PARENTESIS, NT.L, T.CERRAR_PARENTESIS, T.ABRIR_LLAVE, NT.B_, T.CERRAR_LLAVE, NT.I_]]

P[NT.I_]=[
    [NT.ELSE],
    []]

P[NT.ELSE]=[[T.ELSE, NT.ELSE_]]

P[NT.ELSE_]=[
    [T.ABRIR_LLAVE, NT.B_, T.CERRAR_LLAVE],
    [T.IF, T.ABRIR_PARENTESIS, NT.L, T.CERRAR_PARENTESIS, T.ABRIR_LLAVE, NT.B_, T.CERRAR_LLAVE, NT.I_]]

P[NT.WH]=[[T.WHILE, T.ABRIR_PARENTESIS, NT.L, T.CERRAR_PARENTESIS, T.ABRIR_LLAVE, NT.B_, T.CERRAR_LLAVE]]

P[NT.SW]=[[ T.SWITCH, T.ABRIR_PARENTESIS, NT.E, T.CERRAR_PARENTESIS, T.ABRIR_LLAVE, NT.CS, T.CERRAR_LLAVE]]

P[NT.CS]=[
    [NT.CA_LIST, NT.CA_LIST_],
    [NT.DT]]

P[NT.CA_LIST_]=[
    [],
    [NT.DT]]

P[NT.CA_LIST]=[[NT.CA, NT.CA_]]

P[NT.CA_]=[[NT.CA_LIST],[]]

P[NT.CA]=[[T.CASE, NT.E, T.DOS_PUNTOS, NT.B_, NT.BK]]

P[NT.DT]=[[T.DEFAULT, T.DOS_PUNTOS, NT.B_, NT.BK]]

P[NT.BK]=[
    [T.BREAK, T.PUNTO_COMA],
    []]

stack = [T.EOF, NT.S]


generator = LL1Generator()
tabla_ll1 = generator.generar_tabla(P, True)

errores = set()
from sync_sets import sync_sets
sinc = generator. generar_conjunto_sinc(P, True)

def miParser(lexer: Lexer, symbol_table: SymbolTable):
    
    tok: TokenInfo = lexer.tokenInfo()
    x=stack[-1] #primer elemento de der a izq

    raiz = NodoArbol("S")  # Cambiar "S" por el no terminal inicial de tu gramática
    nodos_pila = [raiz]  # Pila paralela para construir el árbol
    semacticAction = SemanticAction(symbol_table)

    while True:    
        if x == tok.get_token() and x == T.EOF:
            if not errores and not semacticAction.errores: 
                print("Cadena reconocida exitosamente") 
                generar_arbol_sintactico(raiz) 
            return
        else:
            if x == tok.get_token() and x != T.EOF:
                stack.pop()
                nodos_pila.pop()  # Obtener el nodo correspondiente en la pila paralela
                x=stack[-1]
                semacticAction.setCurrentToken(tok) # pasar el token al que las acciones se referiran
                tok=lexer.tokenInfo()             
            if isinstance(x, TokenEnum) and x != tok.get_token():
                print("Error: se esperaba ", tok.get_token())
                print("En Linea:", tok.get_line())
                print("En posición:", tok.get_initial_position())
                semacticAction.modoSeguro= True
                return 0;
            if isinstance(x, ActionEnum):
                semacticAction.execute(x)
                stack.pop()
                x=stack[-1]

            if isinstance(x, NonTerminalEnum): #es no terminal
                
                # print("van entrar a la tabla:")
                # print(string_celda(x))
                # print(tok.get_token().value)
                celda=buscar_en_tabla(x,tok.get_token())                            
                if  celda is None:
                    semacticAction.modoSeguro= True
                    if tok.get_token() == TokenEnum.INVALID_TOKEN:
                        error_msg = f"Error: Token desconocido {tok.get_value()} en línea {tok.get_line()}, posición {tok.get_initial_position()}"
                        if error_msg not in errores:
                            errores.add(error_msg)
                    else:
                        error_msg = f"Error: NO se esperaba {tok.get_token().name} en línea {tok.get_line()}, posición {tok.get_initial_position()}" 
                        if error_msg not in errores:
                            errores.add(error_msg)
                    #print(error_msg)

                    sync_set = sync_sets
                    #print(f"Iniciando Modo Pánico para NonTerminalEnum {x.name}. Conjunto de sincronización: {[t.name for t in sync_set]}")

                    while tok.get_token() not in sync_set and tok.get_token() != T.EOF:
                        #print(f"Descartando token '{tok.get_token().value}' (token: {tok.get_token().name}) en línea {tok.get_line()}, posición {tok.get_initial_position()}")
                        tok = lexer.tokenInfo()

                    if tok.get_token() in sync_set:
                        #print(f"Recuperado en el token '{tok.get_token().value}' (token: {tok.get_token().name}) en línea {tok.get_line()}, posición {tok.get_initial_position()}")
                        if stack:
                            stack.pop()
                            x = stack[-1] if stack else None
                        else:
                            print("Pila vacía durante la recuperación. Terminando análisis.")
                            return 0  # Salir del análisis si la pila está vacía
                    else:
                        #print("No se pudo recuperar. Fin del análisis.")
                        return 0
                    continue
                else:
                    stack.pop()
                    agregar_pila(celda)
                    #print_stack()
                    #print("------------")
                    x=stack[-1]

                    # Agregar nodos hijos al árbol sintáctico
                    nodo_actual = nodos_pila.pop()  # Nodo actual en la pila paralela
                    nuevos_nodos = []  # Lista temporal para los nodos hijos
                    for simbolo in celda:  # Procesamos en orden inverso para respetar la pila
                        if isinstance(simbolo, (TokenEnum, NonTerminalEnum)):
                            nuevo_nodo = NodoArbol(simbolo.name)
                            nodo_actual.agregar_hijo(nuevo_nodo)  # Agregamos cada nuevo nodo al nodo actual
                            nuevos_nodos.append(nuevo_nodo)
                    nodos_pila.extend(reversed(nuevos_nodos))  # Agregamos nuevos nodos a la pila paralela en orden correcto      
    

def string_celda(e):
    if isinstance(e, TokenEnum):
        s = e.value
    elif isinstance(e, ActionEnum):
        s = "#" + e.name
    else:
        s = e.name
    return s

def print_stack():
    for s in stack[:-1]:
        t = string_celda(s)
        print(t, end=", ")
    
    s = stack[-1]
    print(string_celda(s) )
    
def buscar_en_tabla(no_terminal, terminal):
    return tabla_ll1[no_terminal][terminal]

def agregar_pila(produccion):
    for elemento in reversed(produccion):
        stack.append(elemento)


def load_code():
    fh = FileHandler()
    filepath = "example.c"
    code = fh.read_file(filepath)
    print("Archivo cargado exitosamente!")

    return code

def main():
    
    # Crear la tabla de símbolos
    symbol_table= SymbolTable()
    lexer = Lexer(symbol_table)
    
    codeString = load_code()
    
    print("Codigo a tokenizar:")

    print(codeString)
    
    lexer.read(codeString)

    # Imprimir la tabla de símbolos
    symbol_table.print_symbol_table()

    miParser(lexer, symbol_table)

    if errores: 
        print("Errores detectados en la cadena:")
        errores_ordenados = sorted(errores, key=lambda e: int(e.split("línea")[1].split(",")[0].strip())) 
        for error in errores_ordenados: 
            print(error)

    print(len(codeString))


if __name__ == '__main__':
    main()

