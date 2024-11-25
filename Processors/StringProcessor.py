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
    
    def __valid_scape(self, word: str) -> bool:
        return re.match(r'^\\([nrtvba\'"\\0?]|x[0-9A-Fa-f]{2}|[0-7]{1,3})', word)
    
    def __is_one_char(self, word: str) -> bool:
        return re.match(r"^'([^'\\]|\\[nrtvba'\"\\0?]|\\x[0-9A-Fa-f]{2}|\\[0-7]{1,3})'" , word)
    
    def __init__(self) -> None:
        super().__init__()

    def analize(self, code: str, line: int, position: int) -> str:
        i = position # Posicion actual al entrar
        length = len(code)

        if(i>=length):
            return self.next(code, line, i)

        incomplete_string: bool = False
        invalid_scape_flag: bool = False
        too_long_char_flag: bool = False
        double_quote_flag: bool = self.__is_double_quote(code[i])
        single_quote_flag: bool = self.__is_single_quote(code[i])

        if( not single_quote_flag and not double_quote_flag) or i>=length: #Si no empieza con " ni ' pasar al siguiente eslabon
            return self.next(code, line, position)
               
        while double_quote_flag:
            i+=1
            if(self.__is_next_line(code[i:]) or i>=len(code)): # Si encuentra salto lina o final del archivo, esta incompleto
                incomplete_string = True
                double_quote_flag = False
                i-=1 # No incluir caracter de fin de linea
                break

            if(self.__is_double_quote(code[i])):
                break # Si ya encontro la otra comilla salir del bucle
            
            if(code[i] == '\\'): # Dado que "cadena\ncadena" se cambia por "cadena\\ncadena"
                scape = self.__valid_scape(code[i:])
                if scape:
                    i+=scape.end()-1 # si es un scape valido, saltarlo para evitar errores con //" o //n
                else:
                    invalid_scape_flag = True # de lo contrario marcar como invalido

        while single_quote_flag:
            i+=1
            if(self.__is_next_line(code[i:]) or i>=len(code)): # Si encuentra salto lina o final del archivo, esta incompleto
                incomplete_string = True
                single_quote_flag = False
                i-=1
                break

            if(self.__is_single_quote(code[i])):
                char = self.__is_one_char(code[i:])
                if not self.__is_one_char(code[position:i+1]): # Verificar que entre comillas solo sea un char
                    too_long_char_flag = True

                break # Si ya encontro la otra comilla salir del bucle

            if(code[i] == '\\'): # Dado que "cadena\ncadena" se cambia por "cadena\\ncadena"
                scape = self.__valid_scape(code[i:])
                if scape:
                    i+=scape.end()-1 # si es un scape valido, saltarlo para evitar errores con //" o //n
            
        if incomplete_string or invalid_scape_flag or too_long_char_flag: # si paro por salto de linea, char muy largo o secuencia invalida
            return TokenInfo( TokenEnum.INVALID_TOKEN, line, position, i, code[position:i+1])
        elif single_quote_flag:
            return TokenInfo(TokenEnum.CHAR_LITERAL, line, position, i, code[position:i+1])
            
        return TokenInfo(TokenEnum.STRING_LITERAL, line, position, i, code[position:i+1])