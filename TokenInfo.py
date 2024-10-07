from TokenEnum import TokenEnum


class TokenInfo:
    __token: TokenEnum
    __initial_position: int
    __final_position: int
    __value: str

   
    def __init__(self, token: TokenEnum, init_position: int, final_position: int, value: str = None) -> None:
        if value:
            self.__value = value
        else:
            self.__value = token.value
        self.__token = token
        self.__initial_position = init_position
        self.__final_position = final_position
        
    
    def get_token(self) -> TokenEnum:
        return self.__token
    
    def get_initial_position(self) -> str:
        return self.__initial_position
    
    def get_final_position(self) -> str:
        return self.__final_position
    
    def get_symbol(self) -> str:
        return self.__token.value # El simbolo sera el mismo valor del operador
    
    def get_value(self) -> str:
        return self.__value
    
    def print(self):
        print("\nToken: " + self.__token.name)
        print("Valor: " + str(self.__value))
        print("Posición 1er caracter: " + str(self.__initial_position))
        print("Posición ultimo caracter: " + str(self.__final_position))