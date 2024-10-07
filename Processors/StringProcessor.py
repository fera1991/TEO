from Processors.BaseVerification import BaseTokenProcessor
import re

from TokenEnum import TokenEnum
from TokenInfo import TokenInfo

#Ignora los espacios, saltos en linea y comentarios
class StringProcessor(BaseTokenProcessor):
        
    def __is_single_quote(self, word: str) -> bool:
        return re.match(r"^'.*", word)
    
    def __is_double_quote(self, word: str) -> bool:
        return re.match(r'^".*', word)
    
    def __is_next_line(self, word: str) -> bool:
        return re.match(r'^\r?\n.*', word)
    
    
    def __is_false_next_line(self, word: str) -> bool:
        return re.match(r'\\n.*', word)

    def __init__(self) -> None:
        super().__init__()

    def analize(self, code: str, position: int) -> str:
        i = position # Posicion actual al entrar
        length = len(code)

        incomplete_string: bool = False
        single_quote_flag: bool = self.__is_single_quote(code[i])
        double_quote_flag: bool = self.__is_double_quote(code[i])

        if( not single_quote_flag and not double_quote_flag): #Si no empieza con " ni ' pasar al siguiente eslabon
            return self.next(code, position)
        
        while single_quote_flag:
            i+=1            
            if(self.__is_next_line(code[i:])):
                incomplete_string = True
                single_quote_flag = False
                break

            if(self.__is_single_quote(code[i])): # Si ya encontro la otra comilla salir del bucle
                break
            
            if(self.__is_false_next_line(code[i:])):
                i+=2 # Si  es //n, saltar 2 adicional para no confundir con /n en la siguiente iteracion

        
        while double_quote_flag:
            i+=1
            if(self.__is_next_line(code[i:])):
                incomplete_string = True
                double_quote_flag = False
                break

            if(self.__is_double_quote(code[i])):
                break # Si ya encontro la otra comilla salir del bucle
            
            if(self.__is_false_next_line(code[i:])):
                i+=2 # Si  es //n, saltar 2 adicional para no confundir con /n en la siquiente iteracion
            
        if incomplete_string: # si paro por salto de linea, retornar token invalido
            return TokenInfo( TokenEnum.INVALID_TOKEN, position, i, code[position:i])
        
        return TokenInfo(TokenEnum.STRING, position, i, code[position:i+1])