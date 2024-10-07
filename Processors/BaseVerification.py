from abc import ABC, abstractmethod
from typing import Any

from TokenInfo import TokenInfo


#Clase abstracta que define los eslabones para una Chain of Responsability
class BaseTokenProcessor(ABC):
    __next_processor = None

    def __init__(self) -> None:
        super().__init__()
        self.__next_processor = None

    def set_next( self,  new_processor: 'BaseTokenProcessor') -> 'BaseTokenProcessor':
        self.__next_processor = new_processor
        return self.__next_processor #Regresar el ultimo elemento ingresado, para facilitar encadenamiento
    
    @abstractmethod
    def analize(self, code: str, position: int) -> TokenInfo:
        pass
    
    def next(self, code: str, position: int) -> TokenInfo:
        if self.__next_processor:
            return self.__next_processor.analize(code, position)

        return None #TODO: regresar token vacio