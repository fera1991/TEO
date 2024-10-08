from enum import StrEnum


class TokenEnum(StrEnum):

    # Token identificador
    IDENTIFIER = "id"
    NUMERIC_CONSTANT = "num"
    STRING_LITERAL = "string"
    CHAR_LITERAL = "charzcter"
    INVALID_TOKEN = "invalid"

    # Palabras reservadas
    INT = 'int'
    FLOAT = 'float'
    DOUBLE = 'double'
    CHAR = 'char'
    BOOL = 'bool'
    IF = 'if'
    ELSE = 'else'
    WHILE = 'while'
    FOR = 'for'
    RETURN = 'return'
    BREAK = 'break'
    CONTINUE = 'continue'
    CLASS = 'class'
    STRUCT = 'struct'
    VOID = 'void'
    
    SWITCH = 'switch'
    CASE = 'case'
    PUBLIC = 'public'
    PRIVATE = 'private'
    PROTECTED = 'protected'
    VIRTUAL = 'virtual'
    CONST = 'const'
    STATIC = 'static'
    LONG = 'long'
    SHORT = 'short'
    TRUE = 'true'
    FALSE = 'false'
    NULLPTR = 'nullptr'

    # Operadores aritméticos
    SUMA = '+'
    RESTA = '-'
    ASTERISCO = '*' # Se usa para multiplicación y punteros
    DIVISION = '/'
    MODULO = '%'
    INCREMENTO = '++'
    DECREMENTO = '--'
    
    # Asignación
    ASIGNACION = '='
    MAS_IGUAL = '+='
    MENOS_IGUAL = '-='
    POR_IGUAL = '*='
    DIVIDIDO_IGUAL = '/='
    MODULO_IGUAL = '%='

    # Operadores de Comparación
    IGUALDAD = '=='
    DIFERENTE = '!='
    MAYOR_QUE = '>'
    MENOR_QUE = '<'
    MAYOR_O_IGUAL = '>='
    MENOR_O_IGUAL = '<='
    
    # Operadores lógicos
    AND_LOGICO = '&&'
    OR_LOGICO = '||'
    NOT_LOGICO = '!'
    
    # Operadores bit a bit
    AMPERSAND = '&' # And. Se usa tambien en punteros
    BARRA_VERTICAL = '|' # OR
    CIRCUNFLEJO = '^' # XOR
    TILDE = '~' # NOT o COMPLEMENTO
    DESPLAZAMIENTO_IZQ = '<<'
    DESPLAZAMIENTO_DER = '>>'

    # Operadores condicionales
    TERNARIO = '?'
    DOS_PUNTOS = ':' # Usado tambien en la herencia de clases
        
    # Operadores de acceso a miembros
    PUNTO = '.'
    FLECHA = '->'

    # Operador coma
    COMA = ','
    
    RESOLUCION_AMBITO = '::'

    # Inicio y fin de bloque
    ABRIR_LLAVE = '{'
    CERRAR_LLAVE = '}'
    ABRIR_PARENTESIS = '('
    CERRAR_PARENTESIS = ')'
    ABRIR_CORCHETE = '['
    CERRAR_CORCHETE = ']'
    PUNTO_COMA = ';'

    # Otros tokens -- No se usaron
    COMILLA_SIMPLE = '\''
    COMILLA_DOBLE = '"'
    DIAGONAL_INVERTIDA = '\\'
    DIAGONAL = '/'
    COMENTARIO_SIMPLE = '//'
    COMENTARIO_MULTILINEA_INICIO = '/*'
    COMENTARIO_MULTILINEA_FIN = '*/'


    
    