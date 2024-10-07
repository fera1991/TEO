from FileHandler import FileHandler
from Processors.InvalidProcessor import InvalidProcessor
from Processors.NumberProcessor import NumberProcessor
from Processors.StringProcessor import StringProcessor
from Processors.IdentifierAndKeywordProcessor import IdentifierAndKeywordProcessor
from Processors.IgnoreProcessor import IgnoreProcessor
from Processors.OperatorProcessor import OperatorProcessor
from TokenEnum import TokenEnum
from TokenInfo import TokenInfo
from Processors.SymbolTableProcessor import SymbolTableProcessor

def build_processors_chain():

    keywords = [
    TokenEnum.INT,
    TokenEnum.FLOAT,
    TokenEnum.DOUBLE,
    TokenEnum.CHAR,
    TokenEnum.BOOL,
    TokenEnum.IF,
    TokenEnum.ELSE,
    TokenEnum.WHILE,
    TokenEnum.FOR,
    TokenEnum.RETURN,
    TokenEnum.BREAK,
    TokenEnum.CONTINUE,
    TokenEnum.CLASS,
    TokenEnum.STRUCT,
    TokenEnum.VOID
    ]

    ignore_processor = IgnoreProcessor()
    inde_and_key_processor = IdentifierAndKeywordProcessor(keywords)
    number_processor = NumberProcessor()
    string_processor = StringProcessor()
    invalid_processor = InvalidProcessor()

    (
        ignore_processor.set_next(inde_and_key_processor)
        .set_next( OperatorProcessor(TokenEnum.INCREMENTO) )
        .set_next( OperatorProcessor(TokenEnum.MAS_IGUAL) ) 
        .set_next( OperatorProcessor(TokenEnum.SUMA) )
        .set_next( OperatorProcessor(TokenEnum.DECREMENTO) )
        .set_next( OperatorProcessor(TokenEnum.MENOS_IGUAL) )
        .set_next( OperatorProcessor(TokenEnum.FLECHA) )
        .set_next( OperatorProcessor(TokenEnum.RESTA) )
        .set_next( OperatorProcessor(TokenEnum.POR_IGUAL) )
        .set_next( OperatorProcessor(TokenEnum.ASTERISCO) )
        .set_next( OperatorProcessor(TokenEnum.DIVIDIDO_IGUAL) )
        .set_next( OperatorProcessor(TokenEnum.DIVISION) )
        .set_next( OperatorProcessor(TokenEnum.MODULO_IGUAL) )
        .set_next( OperatorProcessor(TokenEnum.MODULO) )
        .set_next( OperatorProcessor(TokenEnum.IGUALDAD) )
        .set_next( OperatorProcessor(TokenEnum.ASIGNACION) )
        .set_next( OperatorProcessor(TokenEnum.DIFERENTE) )
        .set_next( OperatorProcessor(TokenEnum.NOT_LOGICO) )
        .set_next( OperatorProcessor(TokenEnum.MAYOR_O_IGUAL) )
        .set_next( OperatorProcessor(TokenEnum.DESPLAZAMIENTO_DER) )
        .set_next( OperatorProcessor(TokenEnum.MAYOR_QUE) )
        .set_next( OperatorProcessor(TokenEnum.MENOR_O_IGUAL) )
        .set_next( OperatorProcessor(TokenEnum.DESPLAZAMIENTO_IZQ) )
        .set_next( OperatorProcessor(TokenEnum.MENOR_QUE) )
        .set_next( OperatorProcessor(TokenEnum.AND_LOGICO) )
        .set_next( OperatorProcessor(TokenEnum.AMPERSAND) )
        .set_next( OperatorProcessor(TokenEnum.OR_LOGICO) )
        .set_next( OperatorProcessor(TokenEnum.BARRA_VERTICAL) )
        .set_next( OperatorProcessor(TokenEnum.CIRCUNFLEJO) )
        .set_next( OperatorProcessor(TokenEnum.TILDE) )
        .set_next( OperatorProcessor(TokenEnum.RESOLUCION_AMBITO) )
        .set_next( OperatorProcessor(TokenEnum.TERNARIO) )
        .set_next( OperatorProcessor(TokenEnum.DOS_PUNTOS) )
        .set_next( OperatorProcessor(TokenEnum.PUNTO) )        
        .set_next( OperatorProcessor(TokenEnum.COMA) )
        .set_next( OperatorProcessor(TokenEnum.ABRIR_LLAVE) )
        .set_next( OperatorProcessor(TokenEnum.CERRAR_LLAVE) )
        .set_next( OperatorProcessor(TokenEnum.ABRIR_PARENTESIS) )
        .set_next( OperatorProcessor(TokenEnum.CERRAR_PARENTESIS) )
        .set_next( OperatorProcessor(TokenEnum.ABRIR_CORCHETE) )
        .set_next( OperatorProcessor(TokenEnum.CERRAR_CORCHETE) )
        .set_next( OperatorProcessor(TokenEnum.PUNTO_COMA) )
        .set_next(number_processor)
        .set_next(string_processor)
        .set_next(invalid_processor)
    )

    return ignore_processor



def load_code():
    fh = FileHandler()
    
    filepath = input("Ingrese archivo con el codigo a tokenizar: ")
    code = fh.read_file(filepath)
    print("Archivo cargado exitosamente!")

    return code

def main():

    print("ANALIZADOR LEXICO\n")

    # Crear la tabla de símbolos
    symbol_table_processor = SymbolTableProcessor()
    
    codeString = load_code()
    processor_chain = build_processors_chain()

    print("Codigo a tokenizar:")

    print(codeString)

    position = 0
    token_list = []

    print("Generando tokens ...")
    while position < len(codeString):
        token_info: TokenInfo = processor_chain.analize(codeString, position)
        token_list.append( token_info)
        position = token_info.get_final_position() + 1
        
        # Procesar el token y añadirlo a la tabla de símbolos
        symbol_table_processor.process_token(token_info.get_token().name, token_info.get_value())
            
    
    print("\nLista de tokens generados:\n")
    print("////////////////////////////////////////////////////////////////////////")
    for token in token_list:
        token.print()
        print("------------------------------------------------------------------------")
    print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")

    # Imprimir la tabla de símbolos
    symbol_table_processor.print_symbol_table()


if __name__ == '__main__':
    main()

