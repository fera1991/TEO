from Processors.BaseVerification import BaseTokenProcessor
import re
from TokenEnum import TokenEnum
from TokenInfo import TokenInfo

#Ignora los espacios, saltos en linea y comentarios
class EOFProcessor(BaseTokenProcessor):
    

    def analize(self, code: str, line: int, position: int) -> str:
        i = position # Posicion actual al entrar

        return TokenInfo(TokenEnum.EOF, line, position, i, TokenEnum.EOF)