

from Processors.BaseVerification import BaseTokenProcessor
from Processors.EOFProcessor import EOFProcessor
from Processors.IdentifierAndKeywordProcessor import IdentifierAndKeywordProcessor
from Processors.IgnoreProcessor import IgnoreProcessor
from Processors.InvalidProcessor import InvalidProcessor
from Processors.NumberProcessor import NumberProcessor
from Processors.OperatorProcessor import OperatorProcessor
from Processors.StringProcessor import StringProcessor
from SymbolTable import SymbolTable
from TokenEnum import TokenEnum
from TokenInfo import TokenInfo


class Lexer:

    __token_list = []
    __token_position: int = 0
    __processors_chain: BaseTokenProcessor
    __symbol_table: SymbolTable
        
    def build_processors_chain(self):

        keywords = [
        TokenEnum.INT,
        TokenEnum.CHAR,
        TokenEnum.FLOAT,
        TokenEnum.IF,
        TokenEnum.ELSE,
        TokenEnum.VOID,
        TokenEnum.RETURN,
        TokenEnum.WHILE,
        TokenEnum.SWITCH,
        TokenEnum.CASE,
        TokenEnum.BREAK,
        TokenEnum.DEFAULT
        ]

        operators = [
        TokenEnum.SUMA,
        TokenEnum.RESTA,
        TokenEnum.MULTIPLICACION, 
        TokenEnum.DIVISION, 
        TokenEnum.IGUALDAD, 
        TokenEnum.ASIGNACION, 
        TokenEnum.MAYOR_QUE, 
        TokenEnum.MENOR_QUE, 
        TokenEnum.COMA, 
        TokenEnum.ABRIR_LLAVE, 
        TokenEnum.CERRAR_LLAVE, 
        TokenEnum.ABRIR_PARENTESIS, 
        TokenEnum.CERRAR_PARENTESIS, 
        TokenEnum.ABRIR_CORCHETE, 
        TokenEnum.CERRAR_CORCHETE, 
        TokenEnum.PUNTO_COMA,
        TokenEnum.DOS_PUNTOS]

        ignore_processor = IgnoreProcessor()
        inde_and_key_processor = IdentifierAndKeywordProcessor(keywords)
        number_processor = NumberProcessor()
        string_processor = StringProcessor()
        invalid_processor = InvalidProcessor()
        eof_processor = EOFProcessor()

        (
            ignore_processor.set_next(inde_and_key_processor)
            .set_next( OperatorProcessor(operators))
            .set_next(number_processor)
            .set_next(string_processor)
            .set_next(invalid_processor)
            .set_next(eof_processor)
        )

        return ignore_processor

    def show_tokenList(self):
        print("\nLista de tokens generados:\n")
        print("////////////////////////////////////////////////////////////////////////")
        for token in self.__token_list:
            token.print()
            print("------------------------------------------------------------------------")
        print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")

    def __init__(self, symbolTable: SymbolTable):
        self.__token_list = []
        self.__token_position=0
        self.__symbol_table = symbolTable
        self.__processors_chain= self.build_processors_chain()

    def read(self, codeString: str):
        
        processor_chain = self.__processors_chain
        symbol_table = self.__symbol_table

        print("ANALIZADOR LEXICO\n")

        position = 0
        line = 1
        token_list = []

        print("Generando tokens ...")
        while True:
            token_info: TokenInfo = processor_chain.analize(codeString, line, position)
            token_list.append( token_info)
            position = token_info.get_final_position() + 1
            line = token_info.get_line()
            
            # Procesar el token y añadirlo a la tabla de símbolos
            symbol_table.process_token(token_info.get_token().name, token_info.get_value(), token_info.get_initial_position(), token_info.get_final_position(), token_info.get_line())

            if(token_info.get_token() == TokenEnum.EOF):
                break
        

        self.__token_list = token_list
        self.__token_position=0

    def tokenInfo(self) -> TokenInfo:
        t = self.__token_list[self.__token_position]
        self.__token_position += 1

        return t    

        

