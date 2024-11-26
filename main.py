from FileHandler import FileHandler
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

tabla_ll1[NT.S][T.VOID] = [NT.FN, NT.S]
tabla_ll1[NT.S][T.INT] = [NT.FN, NT.S]
tabla_ll1[NT.S][T.CHAR] = [NT.FN, NT.S]
tabla_ll1[NT.S][T.FLOAT] = [NT.FN, NT.S]
tabla_ll1[NT.S][T.EOF] = [] # palabra vacia

tabla_ll1[NT.FN][T.VOID]=[NT.TR, T.IDENTIFIER, T.ABRIR_PARENTESIS, NT.P, T.CERRAR_PARENTESIS, NT.FN_]
tabla_ll1[NT.FN][T.INT]=[NT.TR, T.IDENTIFIER, T.ABRIR_PARENTESIS, NT.P, T.CERRAR_PARENTESIS, NT.FN_]
tabla_ll1[NT.FN][T.CHAR]=[NT.TR, T.IDENTIFIER, T.ABRIR_PARENTESIS, NT.P, T.CERRAR_PARENTESIS, NT.FN_]
tabla_ll1[NT.FN][T.FLOAT]=[NT.TR, T.IDENTIFIER, T.ABRIR_PARENTESIS, NT.P, T.CERRAR_PARENTESIS, NT.FN_]

tabla_ll1[NT.TR][T.VOID]=[T.VOID]
tabla_ll1[NT.TR][T.INT]=[NT.T]
tabla_ll1[NT.TR][T.CHAR]=[NT.T]
tabla_ll1[NT.TR][T.FLOAT]=[NT.T]

tabla_ll1[NT.P][T.CERRAR_PARENTESIS]=[] # palabra vacia
tabla_ll1[NT.P][T.INT]=[NT.T, T.IDENTIFIER, NT.P_]
tabla_ll1[NT.P][T.CHAR]=[NT.T, T.IDENTIFIER, NT.P_]
tabla_ll1[NT.P][T.FLOAT]=[NT.T, T.IDENTIFIER, NT.P_]

tabla_ll1[NT.P_][T.CERRAR_PARENTESIS]=[] # palabra vacia
tabla_ll1[NT.P_][T.COMA]=[T.COMA, NT.T, T.IDENTIFIER, NT.P_]

tabla_ll1[NT.FN_][T.PUNTO_COMA]=[T.PUNTO_COMA]
tabla_ll1[NT.FN_][T.ABRIR_LLAVE]=[T.ABRIR_LLAVE, NT.B_, T.CERRAR_LLAVE]

tabla_ll1[NT.B_][T.IDENTIFIER]=[NT.B, NT.B_]
tabla_ll1[NT.B_][T.CERRAR_LLAVE]=[] # PALABRA VACIA
tabla_ll1[NT.B_][T.INT]=[NT.B, NT.B_]
tabla_ll1[NT.B_][T.CHAR]=[NT.B, NT.B_]
tabla_ll1[NT.B_][T.FLOAT]=[NT.B, NT.B_]
tabla_ll1[NT.B_][T.RETURN]=[NT.B, NT.B_]
tabla_ll1[NT.B_][T.IF]=[NT.B, NT.B_]
tabla_ll1[NT.B_][T.WHILE]=[NT.B, NT.B_]
tabla_ll1[NT.B_][T.SWITCH]=[NT.B, NT.B_]

tabla_ll1[NT.B][T.IDENTIFIER]=[NT.ID]
tabla_ll1[NT.B][T.INT]=[NT.D]
tabla_ll1[NT.B][T.CHAR]=[NT.D]
tabla_ll1[NT.B][T.FLOAT]=[NT.D]
tabla_ll1[NT.B][T.RETURN]=[NT.R]
tabla_ll1[NT.B][T.IF]=[NT.I]
tabla_ll1[NT.B][T.WHILE]=[NT.WH]
tabla_ll1[NT.B][T.SWITCH]=[NT.SW]

tabla_ll1[NT.D][T.INT]=[NT.T, NT.V, T.PUNTO_COMA]
tabla_ll1[NT.D][T.CHAR]=[NT.T, NT.V, T.PUNTO_COMA]
tabla_ll1[NT.D][T.FLOAT]=[NT.T, NT.V, T.PUNTO_COMA]

tabla_ll1[NT.T][T.INT]=[T.INT]
tabla_ll1[NT.T][T.CHAR]=[T.CHAR]
tabla_ll1[NT.T][T.FLOAT]=[T.FLOAT]

tabla_ll1[NT.V][T.IDENTIFIER]=[T.IDENTIFIER, NT.A_, NT.V_]

tabla_ll1[NT.V_][T.COMA]=[T.COMA, T.IDENTIFIER, NT.A_, NT.V_]
tabla_ll1[NT.V_][T.PUNTO_COMA]=[] # PALABRA VACIA

tabla_ll1[NT.A_][T.COMA]=[] # PALABRA VACIA
tabla_ll1[NT.A_][T.PUNTO_COMA]=[] # PALABRA VACIA
tabla_ll1[NT.A_][T.ASIGNACION]=[T.ASIGNACION, NT.E]

tabla_ll1[NT.ID][T.IDENTIFIER]=[T.IDENTIFIER, NT.ID_]

tabla_ll1[NT.ID_][T.IDENTIFIER]=[NT.C]
tabla_ll1[NT.ID_][T.ASIGNACION]=[NT.A]

tabla_ll1[NT.A][T.ASIGNACION]=[T.ASIGNACION, NT.E, T.PUNTO_COMA]

tabla_ll1[NT.E][T.IDENTIFIER]=[NT.TE, NT.E_]
tabla_ll1[NT.E][T.ABRIR_PARENTESIS]=[NT.TE, NT.E_]
tabla_ll1[NT.E][T.NUMERIC_CONSTANT]=[NT.TE, NT.E_]
tabla_ll1[NT.E][T.CHAR_LITERAL]=[NT.TE, NT.E_]

tabla_ll1[NT.E_][T.CERRAR_PARENTESIS]=[] # PALABRA VACIA
tabla_ll1[NT.E_][T.COMA]=[] # PALABRA VACIA
tabla_ll1[NT.E_][T.PUNTO_COMA]=[] # PALABRA VACIA
tabla_ll1[NT.E_][T.SUMA]=[T.SUMA, NT.TE, NT.E_]
tabla_ll1[NT.E_][T.RESTA]=[T.RESTA, NT.TE, NT.E_]
tabla_ll1[NT.E_][T.IGUALDAD]=[] # PALABRA VACIA
tabla_ll1[NT.E_][T.MAYOR_QUE]=[] # PALABRA VACIA
tabla_ll1[NT.E_][T.MENOR_QUE]=[] # PALABRA VACIA
tabla_ll1[NT.E_][T.DOS_PUNTOS]=[] # PALABRA VACIA

tabla_ll1[NT.TE][T.IDENTIFIER]=[NT.F, NT.TE_]
tabla_ll1[NT.TE][T.ABRIR_PARENTESIS]=[NT.F, NT.TE_]
tabla_ll1[NT.TE][T.NUMERIC_CONSTANT]=[NT.F, NT.TE_]
tabla_ll1[NT.TE][T.CHAR_LITERAL]=[NT.F, NT.TE_]

tabla_ll1[NT.TE_][T.CERRAR_PARENTESIS]=[] # PALABRA VACIA
tabla_ll1[NT.TE_][T.COMA]=[] # PALABRA VACIA
tabla_ll1[NT.TE_][T.PUNTO_COMA]=[] # PALABRA VACIA
tabla_ll1[NT.TE_][T.SUMA]=[] # PALABRA VACIA
tabla_ll1[NT.TE_][T.RESTA]=[] # PALABRA VACIA
tabla_ll1[NT.TE_][T.MULTIPLICACION]=[T.MULTIPLICACION, NT.F, NT.TE_]
tabla_ll1[NT.TE_][T.DIVISION]=[T.DIVISION, NT.F, NT.TE_]
tabla_ll1[NT.TE_][T.IGUALDAD]=[] # PALABRA VACIA
tabla_ll1[NT.TE_][T.MAYOR_QUE]=[] # PALABRA VACIA
tabla_ll1[NT.TE_][T.MENOR_QUE]=[] # PALABRA VACIA
tabla_ll1[NT.TE_][T.DOS_PUNTOS]=[] # PALABRA VACIA

tabla_ll1[NT.F][T.IDENTIFIER]=[T.IDENTIFIER]
tabla_ll1[NT.F][T.ABRIR_PARENTESIS]=[T.ABRIR_PARENTESIS, NT.E, T.CERRAR_PARENTESIS]
tabla_ll1[NT.F][T.NUMERIC_CONSTANT]=[T.NUMERIC_CONSTANT]
tabla_ll1[NT.F][T.CHAR_LITERAL]=[T.CHAR_LITERAL]

tabla_ll1[NT.L][T.IDENTIFIER]=[NT.E, NT.OP, NT.E]
tabla_ll1[NT.L][T.ABRIR_PARENTESIS]=[NT.E, NT.OP, NT.E]
tabla_ll1[NT.L][T.NUMERIC_CONSTANT]=[NT.E, NT.OP, NT.E]
tabla_ll1[NT.L][T.CHAR_LITERAL]=[NT.E, NT.OP, NT.E]


tabla_ll1[NT.OP][T.IGUALDAD]=[T.IGUALDAD]
tabla_ll1[NT.OP][T.MAYOR_QUE]=[T.MAYOR_QUE]
tabla_ll1[NT.OP][T.MENOR_QUE]=[T.MENOR_QUE]

tabla_ll1[NT.C][T.IDENTIFIER]=[T.IDENTIFIER, T.ABRIR_PARENTESIS, NT.APL, T.CERRAR_PARENTESIS, T.PUNTO_COMA]

tabla_ll1[NT.APL][T.IDENTIFIER]=[NT.E, NT.APL_]
tabla_ll1[NT.APL][T.ABRIR_PARENTESIS]=[NT, NT.APL_]
tabla_ll1[NT.APL][T.CERRAR_PARENTESIS]=[] # PALABRA VACIA
tabla_ll1[NT.APL][T.NUMERIC_CONSTANT]=[NT.E, NT.APL_]
tabla_ll1[NT.APL][T.CHAR_LITERAL]=[NT.E, NT.APL_]

tabla_ll1[NT.APL_][T.CERRAR_PARENTESIS]=[] # PALABRA VACIA
tabla_ll1[NT.APL_][T.COMA]=[T.COMA, NT.E, NT.APL_]

tabla_ll1[NT.R][T.RETURN]=[T.RETURN, NT.E, T.PUNTO_COMA]

tabla_ll1[NT.I][T.IDENTIFIER]=[] # PALABRA VACIA
tabla_ll1[NT.I][T.IF]=[T.IF, T.ABRIR_PARENTESIS, NT.L, T.CERRAR_PARENTESIS, T.ABRIR_LLAVE, NT.B_, T.CERRAR_LLAVE, NT.I_]

tabla_ll1[NT.I_][T.CERRAR_LLAVE]=[] # PALABRA VACIA
tabla_ll1[NT.I_][T.INT]=[] # PALABRA VACIA
tabla_ll1[NT.I_][T.CHAR]=[] # PALABRA VACIA
tabla_ll1[NT.I_][T.FLOAT]=[] # PALABRA VACIA
tabla_ll1[NT.I_][T.RETURN]=[] # PALABRA VACIA
tabla_ll1[NT.I_][T.IF]=[] # PALABRA VACIA
tabla_ll1[NT.I_][T.ELSE]=[NT.ELSE]
tabla_ll1[NT.I_][T.WHILE]=[] # PALABRA VACIA
tabla_ll1[NT.I_][T.SWITCH]=[] # PALABRA VACIA
tabla_ll1[NT.I_][T.CASE]=[] # PALABRA VACIA
tabla_ll1[NT.I_][T.DEFAULT]=[] # PALABRA VACIA
tabla_ll1[NT.I_][T.BREAK]=[] # PALABRA VACIA

tabla_ll1[NT.ELSE][T.ELSE]=[T.ELSE, NT.ELSE_]

tabla_ll1[NT.ELSE_][T.ABRIR_LLAVE]=[T.ABRIR_LLAVE, NT.B_, T.CERRAR_LLAVE]
tabla_ll1[NT.ELSE_][T.IF]=[T.IF, T.ABRIR_PARENTESIS, NT.L, T.CERRAR_PARENTESIS, T.ABRIR_LLAVE, NT.B, T.CERRAR_LLAVE, NT.I_] # TODO: Revisar despues si realmente ocupa B en lugar de B_

tabla_ll1[NT.WH][T.WHILE]=[T.WHILE, T.ABRIR_PARENTESIS, NT.L, T.CERRAR_PARENTESIS, T.ABRIR_LLAVE, NT.B_, T.CERRAR_LLAVE]

tabla_ll1[NT.SW][T.SWITCH]=[T.ABRIR_PARENTESIS, NT.E, T.CERRAR_PARENTESIS, T.ABRIR_LLAVE, NT.CS, T.CERRAR_LLAVE]

tabla_ll1[NT.CS][T.CASE]=[NT.CA_LIST, NT.CA_LIST_]
tabla_ll1[NT.CS][T.DEFAULT]=[NT.DT]

tabla_ll1[NT.CA_LIST_][T.CERRAR_LLAVE]=[] # PALABRA VACIA
tabla_ll1[NT.CA_LIST_][T.DEFAULT]=[NT.DT]

tabla_ll1[NT.CA_LIST][T.CASE]=[NT.CA, NT.CA_]

tabla_ll1[NT.CA_][T.CERRAR_LLAVE]=[] # PALABRA VACIA
tabla_ll1[NT.CA_][T.CASE]=[NT.CA_LIST]
tabla_ll1[NT.CA_][T.DEFAULT]=[] # PALABRA VACIA

tabla_ll1[NT.CA][T.CASE]=[T.CASE, NT.E, T.DOS_PUNTOS, NT.B, NT.BK]

tabla_ll1[NT.DT][T.DEFAULT]=[T.DEFAULT, T.DOS_PUNTOS, NT.B, NT.BK] # PALABRA VACIA

tabla_ll1[NT.BK][T.CERRAR_LLAVE]=[] # PALABRA VACIA
tabla_ll1[NT.BK][T.CASE]=[] # PALABRA VACIA
tabla_ll1[NT.BK][T.DEFAULT]=[] # PALABRA VACIA
tabla_ll1[NT.BK][T.BREAK]=[T.BREAK, T.PUNTO_COMA]

stack = [T.EOF, NT.S]

def miParser(lexer: Lexer, symbol_table: SymbolTable):
    
    tok: TokenInfo = lexer.tokenInfo()
    x=stack[-1] #primer elemento de der a izq

    raiz = NodoArbol("S")  # Cambiar "S" por el no terminal inicial de tu gramática
    nodos_pila = [raiz]  # Pila paralela para construir el árbol

    while True:    
        if x == tok.get_token() and x == T.EOF:
            print("Cadena reconocida exitosamente")
            generar_arbol_sintactico(raiz)  # Generar y guardar el árbol sintáctico
            generar_arbol_sintactico_terminal(raiz)
            return #aceptar
        else:
            if x == tok.get_token() and x != T.EOF:
                stack.pop()
                nodo_actual = nodos_pila.pop()  # Obtener el nodo correspondiente en la pila paralela
                nodo_actual.agregar_hijo(NodoArbol(tok.get_token().name))  # Agregar el nodo terminal como hijo
                x=stack[-1]
                tok=lexer.tokenInfo()             
            if isinstance(x, TokenEnum) and x != tok.get_token():
                print("Error: se esperaba ", tok.get_token())
                return 0;
            if not isinstance(x, TokenEnum): #es no terminal
                print("van entrar a la tabla:")
                print(string_celda(x))
                print(tok.get_token().value)
                celda=buscar_en_tabla(x,tok.get_token())                            
                if  celda is None:
                    if tok.get_token() == TokenEnum.INVALID_TOKEN:
                        print("Error: Token desconocido: ", tok.get_value())
                        print("En Linea:", tok.get_line())
                        print("En posición:", tok.get_initial_position())
                    else:
                        print("Error: NO se esperaba", tok.get_token().name)
                        print("En Linea:", tok.get_line())
                        print("En posición:", tok.get_initial_position())
                    
                    return 0;
                else:
                    stack.pop()
                    agregar_pila(celda)
                    print_stack()
                    print("------------")
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

    print(len(codeString))


if __name__ == '__main__':
    main()

