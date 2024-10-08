import re
from Processors.BaseVerification import BaseTokenProcessor
from TokenEnum import TokenEnum
from TokenInfo import TokenInfo

#Clase encargada de verificar identificadores y palabras clave
class NumberProcessor(BaseTokenProcessor):
    def __init__(self) -> None:
        super().__init__()


    def analize(self, code: str, position: int) -> TokenInfo:
        buffer: str = ""        
        r = re.compile(r'^(?!.*\n)\d+(\.\d*)?$')

        i=position

        while( i < len(code) and r.match(buffer +code[i])):
            buffer += code[i]
            i += 1
        
        if buffer=="":
            return self.next(code, position) # Si el buffer esta vacio significa que nunca cumplio, por lo que pasa la cadena
        
        return TokenInfo( TokenEnum.NUMERIC_CONSTANT, position, i-1, buffer) # Si no esta vacio, regresar token NUMERIC_CONSTANT
            
        

