from Processors.BaseVerification import BaseTokenProcessor
import re

#Ignora los espacios, saltos en linea y comentarios
class IgnoreProcessor(BaseTokenProcessor):
        
    def __is_blank(self, word: str) -> bool:
        return re.match(r'^\s.', word)
    
    def __line_comment(self, word: str) -> bool:
        return re.match(r'^\/\/.*', word)
    
    def __comment_start(self, word: str) -> bool:
        return re.match(r'^\/\*.*', word)
    
    def __comment_end(self, word: str) -> bool:
        return re.match(r'^\*\/.*', word)
    
    def __is_next_line(self, word: str) -> bool:
        return re.match(r'^\r?\n.*', word)

    def __init__(self) -> None:
        super().__init__()

    def analize(self, code: str, position: int) -> str:
        i = position # Posicion actual al entrar
        length=len(code)
        
        while( (self.__is_blank(code[i:]) or self.__line_comment(code[i:]) or self.__comment_start(code[i:])) and i<length):

            while(self.__is_blank(code[i:]) and i<length): # Continuar hasta que no encuentre espacio ni salto de linea
                i+=1 
        
            if self.__line_comment(code[i:]): # En caso de comentario de linea //
                while(not self.__is_next_line(code[i:]) and i<length): # Continuar hasta salto de linea
                    i+=1 
            
            if self.__comment_start(code[i:]): # En caso de comentario de bloque /*
                while(not self.__comment_end(code[i:]) and i<length): # Continuar hasta cierre de comentario de bloque */
                    i+=1 
                i+=2 # Saltar */ al final

            
        return self.next(code, i) # Pasar la cadena con la posisión actualizada