from enum import StrEnum


class TokenEnum(StrEnum):


    # Tipos de datos
    INT = 'int'
    CHAR = 'char'
    FLOAT = 'float'

    # Utilización de variables
    IDENTIFIER = "id"
    NUMERIC_CONSTANT = "num"
    STRING_LITERAL = "string"
    CHAR_LITERAL = "charzcter"
    INVALID_TOKEN = "invalid"
    EOF = "eof"

    # Condicional If- else
    IF = 'if'
    ELSE = 'else'

    # Declaración y definición de funciones
    RETURN = 'return'
    VOID = 'void'

    #Operadores aritmeticos
    SUMA = '+'
    RESTA = '-'
    MULTIPLICACION = '*'
    DIVISION = '/'

    # Instrucciones de iteración
    WHILE = 'while'

    # Asignación
    ASIGNACION = '='
    
    # Operadores de Comparación
    IGUALDAD = '=='
    MAYOR_QUE = '>'
    MENOR_QUE = '<'
    
    # Inicio y fin de bloque
    ABRIR_LLAVE = '{'
    CERRAR_LLAVE = '}'
    ABRIR_PARENTESIS = '('
    CERRAR_PARENTESIS = ')'
    ABRIR_CORCHETE = '['
    CERRAR_CORCHETE = ']'
    PUNTO_COMA = ';'

    # Operador coma
    COMA = ','

    # switch
    SWITCH = 'switch'
    BREAK = 'break'
    DEFAULT = "default"
    CONTINUE = 'continue'
    CASE = 'case'
    DOS_PUNTOS = ':'

# Sin usar
'''
    FOR = "for"
    DO = "do"
    STRUCT = 'struct'
    CONST = 'const'
    STATIC = 'static'
    LONG = 'long'
    SHORT = 'short'
    
    #Operadores aritmeticos
    MODULO = '%'
    INCREMENTO = '++'
    DECREMENTO = '--'

    # Asignación
    MAS_IGUAL = '+='
    MENOS_IGUAL = '-='
    POR_IGUAL = '*='
    DIVIDIDO_IGUAL = '/='
    MODULO_IGUAL = '%='

    # Operadores de Comparación
    DIFERENTE = '!='
    MAYOR_O_IGUAL = '>='
    MENOR_O_IGUAL = '<='
    
    
    # Operadores bit a bit
    AMPERSAND = '&' # And. Se usa tambien en punteros
    BARRA_VERTICAL = '|' # OR
    CIRCUNFLEJO = '^' # XOR
    TILDE = '~' # NOT o COMPLEMENTO
    DESPLAZAMIENTO_IZQ = '<<'
    DESPLAZAMIENTO_DER = '>>'

    # Operadores condicionales
    TERNARIO = '?'
        
    # Operadores de acceso a miembros
    PUNTO = '.'
    FLECHA = '->'  

    # Otros tokens -- No se usaron
    COMILLA_SIMPLE = '\''
    COMILLA_DOBLE = '"'
    DIAGONAL_INVERTIDA = '\\'
    DIAGONAL = '/'
    COMENTARIO_SIMPLE = '//'
    COMENTARIO_MULTILINEA_INICIO = '/*'
    COMENTARIO_MULTILINEA_FIN = '*/'


    
'''