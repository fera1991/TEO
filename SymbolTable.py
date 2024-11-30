from enum import StrEnum
from TokenEnum import TokenEnum

class identificadorEnum(StrEnum):
    FUNCTION = 'funcion'
    PROTOTYPE = 'prototipo de funcion'
    VAR = 'variable'

class Symbol:
    def __init__(self, nombre: str, tipo: identificadorEnum, ambito: str, inicio: int, 
                 linea: int, tipo_valor: TokenEnum, valor=None):
        self.nombre = nombre
        self.tipo = tipo
        self.ambito = ambito
        self.inicio = inicio
        self.usos = 0
        self.parametros: list[TokenEnum] = []
        self.linea = linea
        self.tipo_valor = tipo_valor
        self.valor = valor

class SymbolTable:
    def __init__(self):
        self.symbol_table: dict[tuple[str, str], Symbol] = {}  # Key is (nombre, ambito)
        self.scope_counter = 0
        self.current_scope = 'global'
        self.scope_stack = ['global']

    def _check_exists(self, nombre: str, ambito: str) -> bool:
        """
        Check if a symbol already exists in the given scope
        """
        return (nombre, ambito) in self.symbol_table

    def defineVariable(self, nombre: str, tipo_valor: TokenEnum, inicio: int, linea: int, valor=None) -> bool:
        """
        Define a variable symbol
        Returns True if successful, False if symbol already exists in current scope
        """
        if self._check_exists(nombre, self.current_scope):
            return False
        
        new_symbol = Symbol(
            nombre=nombre,
            tipo=identificadorEnum.VAR,
            ambito=self.current_scope,
            inicio=inicio,
            linea=linea,
            tipo_valor=tipo_valor,
            valor=valor
        )
        
        self.symbol_table[(nombre, self.current_scope)] = new_symbol
        return True

    def defineFunction(self, nombre: str, tipo_valor: TokenEnum, inicio: int, linea: int, 
                      is_prototype: bool = False) -> bool:
        """
        Define a function or prototype symbol
        Returns True if successful, False if symbol already exists in global scope
        """
        if self._check_exists(nombre, 'global'):
            symbol = self.symbol_table[(nombre, 'global')]
            # Allow prototype to be converted to function
            if is_prototype or symbol.tipo != identificadorEnum.PROTOTYPE:
                return False
        
        new_symbol = Symbol(
            nombre=nombre,
            tipo=identificadorEnum.PROTOTYPE if is_prototype else identificadorEnum.FUNCTION,
            ambito='global',  # Functions are always global
            inicio=inicio,
            linea=linea,
            tipo_valor=tipo_valor,
            valor=None
        )
        
        self.symbol_table[(nombre, 'global')] = new_symbol
        return True

    def addParameter(self, function_name: str, param_type: TokenEnum) -> bool:
        """
        Add a parameter type to a function symbol
        """
        if not self._check_exists(function_name, 'global'):
            return False
            
        symbol = self.symbol_table[(function_name, 'global')]
        if symbol.tipo in [identificadorEnum.FUNCTION, identificadorEnum.PROTOTYPE]:
            symbol.parametros.append(param_type)
            return True
        return False

    def updateFunctionType(self, function_name: str) -> bool:
        """
        Update a function from prototype to full function
        """
        if not self._check_exists(function_name, 'global'):
            return False
            
        symbol = self.symbol_table[(function_name, 'global')]
        if symbol.tipo == identificadorEnum.PROTOTYPE:
            symbol.tipo = identificadorEnum.FUNCTION
            return True
        return False

    def updateValue(self, nombre: str, new_value) -> bool:
        """
        Update the value of a symbol in current scope
        """
        if self._check_exists(nombre, self.current_scope):
            self.symbol_table[(nombre, self.current_scope)].valor = new_value
            return True
        return False

    def findSymbol(self, nombre: str) -> Symbol:
        """
        Search for a symbol starting from current scope up through parent scopes
        """
        for scope in reversed(self.scope_stack):
            if self._check_exists(nombre, scope):
                return self.symbol_table[(nombre, scope)]
        return None

    def createScope(self):
        """
        Create a new scope nested within the current scope.
        """
        self.scope_counter += 1
        new_scope = f'local_{self.scope_counter}'
        self.current_scope = new_scope
        self.scope_stack.append(new_scope)

    def exitScope(self):
        """
        Exit current scope and return to parent scope.
        Returns False if already in global scope, True if successfully exited.
        """
        if self.current_scope == 'global':
            return False
            
        self.scope_stack.pop()
        self.current_scope = self.scope_stack[-1]
        return True

    def returnToGlobal(self):
        """
        Return to global scope regardless of current scope depth.
        """
        self.scope_stack = ['global']
        self.current_scope = 'global'
        
    def print_symbol_table(self):
        """
        Print the symbol table in the specified format.
        """
        print("\nTabla de Símbolos:")
        print(f"{'ID':<5} {'Nombre':<25} {'Tipo':<20} {'Ámbito':<10} {'Linea':<5} {'Posición':<10} {'Usos':<8} {'parametros':<15} {'Tipo Valor':<15} {'Valor'}")
        print("=" * 115)
        
        for symbol_id, symbol in self.symbol_table.items():
            symbol_dict = symbol.to_dict()
            parametros = ", ".join([f"{p['nombre']}:{p['tipo']}" for p in symbol_dict['parametros']]) if symbol_dict['parametros'] else ""
            
            print(f"{symbol_id:<5} {symbol_dict['nombre']:<25} {symbol_dict['tipo']:<20} "
                  f"{symbol_dict['ambito']:<12} {symbol_dict['linea']:<5} {symbol_dict['inicio']:<10} "
                  f"{symbol_dict['usos']:<8} {parametros:<15} {symbol_dict['tipo_valor']:<15} "
                  f"{symbol_dict['valor']}")
            print("-" * 115)
        print("=" * 115)