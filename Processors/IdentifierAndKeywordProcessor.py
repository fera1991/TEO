import re
from typing import Optional
from Processors.BaseVerification import BaseTokenProcessor
from TokenEnum import TokenEnum
from TokenInfo import TokenInfo

#Clase encargada de verificar identificadores y palabras clave
class IdentifierAndKeywordProcessor(BaseTokenProcessor):
    def __init__(self, keywords) -> None:
        super().__init__()
        self.keywords = keywords

    def __find_keyword(self,  word: str) -> Optional[TokenEnum]:

        if word =="":
            return None
        
        for keyword in self.keywords:
            if word == keyword.value:
                return keyword
        return None

    def analize(self, code: str, position: int) -> TokenInfo:
        buffer: str = ""
        r = re.compile(r'^(?!.*\n)(_|[aA-zZ])\w*$')
        i=position

        while(i < len(code) and r.match(buffer +code[i]) ):
            buffer += code[i]
            i += 1
        
        if buffer=="":
            return self.next(code, position) # Si el buffer esta vacio significa que nunca cumplio, por lo que pasa la cadena
        

        token = self.__find_keyword(buffer)

        if token: 
            return TokenInfo(token, position, i-1) # Si coincide con alguna palabra clave, regresar el token

        
        return TokenInfo( TokenEnum.IDENTIFIER, position, i-1, buffer) # Si no esta vacio ni es keyword, regresar token Identifier
            
        

