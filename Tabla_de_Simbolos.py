import re

# Definición de palabras reservadas, operadores y otros tokens del lenguaje C++
palabras_reservadas = [
    'int', 'float', 'double', 'char', 'bool', 'if', 'else', 'while', 'for', 'return', 'break', 'continue', 'class', 'struct', 'void'
]

# Expresiones regulares para los diferentes tipos de tokens
token_specification = [
    ('PALABRA_RESERVADA', r'\b(?:' + '|'.join(palabras_reservadas) + r')\b'),  # Palabras reservadas (keywords)
    ('COMENTARIO', r'//.*|/\*[\s\S]*?\*/'),       # Comentarios
    ('IDENTIFICADOR', r'[a-zA-Z_][a-zA-Z_0-9]*'),  # Identificadores
    ('NUMERO', r'\d+(\.\d*)?'),                   # Números enteros o decimales
    ('OPERADOR', r'[+\-*/%]=?|==|!=|<=|>=|&&|\|\||[+\-*/%]'),  # Operadores aritméticos, de comparación, lógicos, etc.
    ('ASIGNACION', r'='),                         # Operador de asignación
    ('SIMBOLO_INICIO_FIN', r'[{}()\[\];,]'),                 # Símbolos de bloques y separación
    ('CADENA', r'"(?:\\.|[^\\"])*"'),             # Cadenas de caracteres
    ('ESPACIO', r'[ \t\n]+'),                     # Espacios y tabulaciones
    ('DESCONOCIDO', r'.')                         # Cualquier otro caracter no reconocido
]

# Compilación de las expresiones regulares
tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)



# Función principal del tokenizador
def tokenizar(codigo_fuente):
    tokens = []
    for match in re.finditer(tok_regex, codigo_fuente):
        tipo_token = match.lastgroup
        valor_token = match.group(tipo_token)
        
        if tipo_token == 'ESPACIO' or tipo_token == 'COMENTARIO':
            # Ignorar espacios y comentarios
            continue
        elif tipo_token == 'DESCONOCIDO':
            print(f"Error: Token desconocido '{valor_token}' en el código.")
            tokens.append(("TOKEN_DESCONOCIDO", valor_token))
        else:
            tokens.append((tipo_token, valor_token))
            construir_tabla_simbolos(tipo_token, valor_token)
            

    
    return tokens

tabla_simbolos = {}
id_counter = 0  
contador_ambitos = 0  
ambito_actual = 'global'

def construir_tabla_simbolos(tipo_token, valor_token):
    global id_counter, contador_ambitos, ambito_actual

    if valor_token == '{':
        if contador_ambitos == 0:
            ambito_actual = 'local'
        contador_ambitos += 1
    elif valor_token == '}':
        contador_ambitos -= 1
        if contador_ambitos == 0:
            ambito_actual = 'global'

    id_actual = id_counter
    id_counter += 1

    # Almacena la información de la palabra reservada
    tabla_simbolos[id_actual] = {
        'tipo': tipo_token,
        'ambito': ambito_actual,
        'valor': valor_token
            }
        
    return


# Ejemplo de código en C++ para tokenizar
codigo_cpp = '''
int main() {
    int a = 5;               // Declaración de una variable entera
    int b = 10;              // Declaración de otra variable entera
    int suma;                // Declaración de una variable para almacenar la suma

    // Sumar a y b
    suma = a + b;           // Asignación de la suma

    // Estructura condicional
    if (suma > 10) {
        int resultado = 1;  // Se asigna un valor si la suma es mayor que 10
    } else {
        int resultado = 0;  // Se asigna un valor si la suma es 10 o menor
    }

    // Bucle for
    for (int i = 0; i < 5; i++) {
        a += i;             // Incrementar a con el índice del bucle
    }

    // Bucle while
    int contador = 0;
    while (contador < 3) {
        contador++;         // Incrementar el contador
    }

    return 0;               // Fin del programa
}

'''

# Tokenizamos el código
tokens_encontrados = tokenizar(codigo_cpp)


# Mostramos la tabla de símbolos con los detalles adicionales
print("\nTabla de Símbolos:")
print(f"{'ID':<5} {'Tipo':<20} {'Ámbito':<10} {'Valor'}")
print("=" * 55)  # Línea de separación

for key, value in tabla_simbolos.items():
    print(f" {key:<5} {value['tipo']:<20} {value['ambito']:<10} {value['valor']} ")
print("=" * 55)  # Línea de separación