from TokenEnum import TokenEnum


class TokenInfo:
    token: TokenEnum
    line: int
    initial_position: int
    final_position: int
    value: str

   
    def __init__(self, token: TokenEnum, line: int, init_position: int, final_position: int, value: str = None) -> None:
        if value:
            self.value = value
        else:
            self.value = token.value
        self.token = token
        self.line = line
        self.initial_position = init_position
        self.final_position = final_position
        
    
    def get_token(self) -> TokenEnum:
        return self.token
    
    def get_initial_position(self) -> str:
        return self.initial_position
    
    def get_final_position(self) -> str:
        return self.final_position
    
    def get_symbol(self) -> str:
        return self.token.value # El simbolo sera el mismo valor del operador
    
    def get_value(self) -> str:
        return self.value
    def get_line(self) -> str:
        return self.line
    
    def print(self):
        print("\nToken: " + self.token.name)
        print("Valor: " + str(self.value))
        print("Linea: " + str(self.line))
        print("Posición 1er caracter: " + str(self.initial_position))
        print("Posición ultimo caracter: " + str(self.final_position))