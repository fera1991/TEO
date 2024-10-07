from Processors.BaseVerification import BaseTokenProcessor
from TokenEnum import TokenEnum
from TokenInfo import TokenInfo

class OperatorProcessor(BaseTokenProcessor):
    __token: TokenEnum
    __symbol: str

    def __init__(self, operator_symbol: str, operator_token: TokenEnum) -> None:
        super().__init__()
        self.__symbol = operator_symbol
        self.__token = operator_token

    
    def __init__(self, operator_token: TokenEnum) -> None:
        super().__init__()
        self.__symbol = operator_token.value
        self.__token = operator_token

    def analize(self, code: str, initial_position: int) -> str:
        i = initial_position + len(self.__symbol)

        if code[initial_position: i] == self.__symbol: #Comparar si encuentra el operador en la esa posicion
            return TokenInfo(self.__token, initial_position, i-1)
            
        return self.next(code, initial_position)