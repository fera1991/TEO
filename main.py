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
from syntaxTree import NodoArbol, generar_arbol_sintactico, generar_arbol_sintactico_terminal


def matriz_default():
    return defaultdict(lambda: None) # Any non-defined cell will return None

NT = NonTerminalEnum
T = TokenEnum
tabla_ll1 = defaultdict(matriz_default)


# Definir las producciones de la gramática
P = defaultdict(list)

P[NT.S] = [[NT.FN, NT.S], []]

P[NT.FN]=[[NT.TR, T.IDENTIFIER, T.ABRIR_PARENTESIS, NT.P, T.CERRAR_PARENTESIS, NT.FN_]]

P[NT.TR]=[[T.VOID],[NT.T]]

P[NT.P]=[[NT.T, T.IDENTIFIER, NT.P_], []]

P[NT.P_]=[[T.COMA, NT.T, T.IDENTIFIER, NT.P_],[]]

P[NT.FN_]=[[T.PUNTO_COMA],[T.ABRIR_LLAVE, NT.B_, T.CERRAR_LLAVE]]

P[NT.B_]=[[NT.B, NT.B_], []]

P[NT.B]=[[NT.ID],[NT.D],[NT.R],[NT.I],[NT.WH],[NT.SW]]

P[NT.D]=[[NT.T, NT.V, T.PUNTO_COMA]]

P[NT.T]=[[T.INT], [T.CHAR], [T.FLOAT]]

P[NT.V]=[[T.IDENTIFIER, NT.A_, NT.V_]]

P[NT.V_]=[[T.COMA, T.IDENTIFIER, NT.A_, NT.V_], []]

P[NT.A_]=[[], [T.ASIGNACION, NT.E]]

P[NT.ID]=[[T.IDENTIFIER, NT.ID_]]

P[NT.ID_]=[[NT.C, T.PUNTO_COMA], [NT.A]]

P[NT.A]=[[T.ASIGNACION, NT.E, T.PUNTO_COMA]]

P[NT.E]=[[NT.TE, NT.E_]]

P[NT.E_]=[[], [T.SUMA, NT.TE, NT.E_], [T.RESTA, NT.TE, NT.E_]]

P[NT.TE]=[[NT.F, NT.TE_]]

P[NT.TE_]=[[], [T.MULTIPLICACION, NT.F, NT.TE_], [T.DIVISION, NT.F, NT.TE_]]

P[NT.F]=[[T.IDENTIFIER, NT.F_], [T.ABRIR_PARENTESIS, NT.E, T.CERRAR_PARENTESIS], [T.NUMERIC_CONSTANT], [T.CHAR_LITERAL]]

P[NT.F_]=[[NT.C], []]

P[NT.L]=[[NT.E, NT.OP, NT.E]]

P[NT.OP]=[[T.IGUALDAD], [T.MAYOR_QUE], [T.MENOR_QUE]]

P[NT.C]=[[T.ABRIR_PARENTESIS, NT.APL, T.CERRAR_PARENTESIS]]

P[NT.APL]=[[NT.E, NT.APL_], []]

P[NT.APL_]=[[], [T.COMA, NT.E, NT.APL_]]

P[NT.R]=[[T.RETURN, NT.R_, T.PUNTO_COMA]]

P[NT.R_]=[[NT.E], []]

P[NT.I]=[[T.IF, T.ABRIR_PARENTESIS, NT.L, T.CERRAR_PARENTESIS, T.ABRIR_LLAVE, NT.B_, T.CERRAR_LLAVE, NT.I_]]

P[NT.I_]=[[NT.ELSE], []]

P[NT.ELSE]=[[T.ELSE, NT.ELSE_]]

P[NT.ELSE_]=[[T.ABRIR_LLAVE, NT.B_, T.CERRAR_LLAVE], [T.IF, T.ABRIR_PARENTESIS, NT.L, T.CERRAR_PARENTESIS, T.ABRIR_LLAVE, NT.B_, T.CERRAR_LLAVE, NT.I_]]
# TODO: Revisar despues si realmente ocupa B en lugar de B_

P[NT.WH]=[[T.WHILE, T.ABRIR_PARENTESIS, NT.L, T.CERRAR_PARENTESIS, T.ABRIR_LLAVE, NT.B_, T.CERRAR_LLAVE]]

P[NT.SW]=[[ T.SWITCH, T.ABRIR_PARENTESIS, NT.E, T.CERRAR_PARENTESIS, T.ABRIR_LLAVE, NT.CS, T.CERRAR_LLAVE]]

P[NT.CS]=[[NT.CA_LIST, NT.CA_LIST_], [NT.DT]]

P[NT.CA_LIST_]=[[], [NT.DT]]

P[NT.CA_LIST]=[[NT.CA, NT.CA_]]

P[NT.CA_]=[[NT.CA_LIST],[]]

P[NT.CA]=[[T.CASE, NT.E, T.DOS_PUNTOS, NT.B_, NT.BK]]

P[NT.DT]=[[T.DEFAULT, T.DOS_PUNTOS, NT.B_, NT.BK]]

P[NT.BK]=[[T.BREAK, T.PUNTO_COMA], []]

stack = [T.EOF, NT.S]

generator = LL1Generator()
tabla_ll1 = generator.generar_tabla(P, True)

errores = set()
from sync_sets import sync_sets

def miParser(lexer: Lexer, symbol_table: SymbolTable):
    
    tok: TokenInfo = lexer.tokenInfo()
    x=stack[-1] #primer elemento de der a izq

    raiz = NodoArbol("S")  # Cambiar "S" por el no terminal inicial de tu gramática
    nodos_pila = [raiz]  # Pila paralela para construir el árbol

    while True:    
        if x == tok.get_token() and x == T.EOF:
            if not errores: 
                print("Cadena reconocida exitosamente") 
                generar_arbol_sintactico(raiz) 
            return
        else:
            if x == tok.get_token() and x != T.EOF:
                stack.pop()
                nodos_pila.pop()  # Obtener el nodo correspondiente en la pila paralela
                x=stack[-1]
                tok=lexer.tokenInfo()             
            if isinstance(x, TokenEnum) and x != tok.get_token():
                error_msg = f"Error: se esperaba {x.name} en línea {tok.get_line()}, posición {tok.get_initial_position()}" 
                if error_msg not in errores:
                    errores.add(error_msg)
                    #print(error_msg) 

                sync_set = sync_sets
                #print(f"Iniciando Modo Pánico para TokenEnum {x.name}. Conjunto de sincronización: {[t.name for t in sync_set]}")

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

            if not isinstance(x, TokenEnum): #es no terminal
                #print("van entrar a la tabla:")
                #print(string_celda(x))
                #print(tok.get_token().value)
                celda=buscar_en_tabla(x,tok.get_token())                            
                if  celda is None:
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
                        nuevo_nodo = NodoArbol(simbolo.name)
                        nodo_actual.agregar_hijo(nuevo_nodo)  # Agregamos cada nuevo nodo al nodo actual
                        nuevos_nodos.append(nuevo_nodo)
                    nodos_pila.extend(reversed(nuevos_nodos))  # Agregamos nuevos nodos a la pila paralela en orden correcto      
    

def string_celda(c):
    return c.value if isinstance(c, TokenEnum) else c.name

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

