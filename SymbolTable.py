class SymbolTable:
    def __init__(self):
        # Inicializar la tabla de símbolos y las variables necesarias para su gestión
        self.symbol_table = {}
        self.id_counter = 0  # Contador para generar IDs únicos para cada símbolo
        self.scope_counter = 0  # Contador para gestionar el ámbito (nivel de anidación)
        self.current_scope = 'global'  # Definir el ámbito inicial como 'global'

    def process_token(self, token_type, token_value, token_initial_position, token_final_position):
        # Si se encuentra una llave de apertura, se entra en un nuevo ámbito
        if token_value == '{':
            if self.scope_counter == 0:
                self.current_scope = 'local'  # El ámbito cambia a local si es el primer bloque
            self.scope_counter += 1

        # Si se encuentra una llave de cierre, se sale del ámbito actual
        elif token_value == '}':
            self.scope_counter -= 1
            if self.scope_counter == 0:
                self.current_scope = 'global'  # Se regresa al ámbito global

        # Asigna un ID único a cada símbolo
        current_id = self.id_counter
        self.id_counter += 1

        # Almacena el símbolo en la tabla de símbolos
        self.symbol_table[current_id] = {
            'tipo': token_type,          # Tipo de token (e.g., palabra clave, identificador)
            'ambito': self.current_scope, # Ámbito del símbolo
            'posicion_inicial': token_initial_position, # Posicion inicial del símbolo
            'posicion_final': token_final_position, # Posicion final del símbolo
            'valor': token_value          # Valor asociado al token
        }

    def get_symbol_table(self):
        """Devuelve la tabla de símbolos completa."""
        return self.symbol_table

    def print_symbol_table(self):
        print("\nTabla de Símbolos:")
        print(f"{'ID':<5} {'Tipo':<20} {'Ámbito':<10} {'Inicio':<8} {'Fin':<8}  {'Valor'}")
        print("=" * 65)  # Línea de separación
        
        for symbol_id, symbol_data in self.symbol_table.items():
            print(f"{symbol_id:<5} {symbol_data['tipo']:<20} {symbol_data['ambito']:<10} {symbol_data['posicion_inicial']:<8} {symbol_data['posicion_final']:<8} {symbol_data['valor']}")
        print("=" * 65)  # Línea de separación
       
