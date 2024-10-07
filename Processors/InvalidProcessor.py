from Processors.BaseVerification import BaseTokenProcessor
import re
from TokenEnum import TokenEnum
from TokenInfo import TokenInfo

#Ignora los espacios, saltos en linea y comentarios
class InvalidProcessor(BaseTokenProcessor):
        
    def __is_blank(self, word: str) -> bool:
        return re.match(r'.*[\s|//|/*]$', word)
    
    def __init__(self) -> None:
        super().__init__()

    def analize(self, code: str, position: int) -> str:
        i = position # Posicion actual al entrar
        
        while not self.__is_blank(code[position:i+1]) and i < len(code): # Continuar hasta espacio o salto de linea 
            i+=1 
    
        return TokenInfo(TokenEnum.INVALID_TOKEN, position, i-1, code[position:i],)