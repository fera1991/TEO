from typing import Optional
from Processors.BaseVerification import BaseTokenProcessor
from TokenEnum import TokenEnum
from TokenInfo import TokenInfo

class OperatorProcessor(BaseTokenProcessor):
    __single_symbol_operators = list[TokenEnum]
    __double_symbol_operators = list[TokenEnum]

    def __init__(self, operators_token) -> None:
        super().__init__()
        self.__single_symbol_operators = [token for token in operators_token if len(token) == 1]
        self.__double_symbol_operators = [token for token in operators_token if len(token) == 2]

    
    def __find_operator(self,  word: str) -> Optional[TokenEnum]:

        if word =="":
            return None
        
        for operator in self.__double_symbol_operators: # Buscar primero en los operadores de dos simbolos
            if word == operator.value:
                return operator
        
        for operator in self.__single_symbol_operators: # verificar 
            if word == operator.value:
                return operator
        
        return None
    
    def analize(self, code: str, line: int, initial_position: int) -> str:
        i = initial_position

        for operator in self.__double_symbol_operators: # Buscar primero en los operadores de dos simbolos
            if code[i:i+2] == operator.value:
                return TokenInfo(operator, line, i, i+1)
            
        for operator in self.__single_symbol_operators: # verificar 
            if code[i:i+1] == operator.value:
                return TokenInfo(operator, line, initial_position, i)
        
        return self.next(code, line, initial_position)