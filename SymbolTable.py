class SymbolTable:
    def __init__(self):
        # Inicializar la tabla de símbolos y las variables necesarias para su gestión
        self.symbol_table = {}
        self.id_counter = 0  # Contador para generar IDs únicos para cada símbolo
        self.scope_counter = 0  # Contador para gestionar el ámbito (nivel de anidación)
        self.current_scope = 'global'  # Definir el ámbito inicial como 'global'
        self.previous_tokens = []  # Para llevar un registro de los últimos tokens procesados

    def process_token(self, token_type, token_value, token_initial_position, token_final_position, token_line_position):
        # Agregar el token actual a la lista de tokens previos
        self.previous_tokens.append((token_type, token_value))

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

        
        current_id = self.id_counter
        self.id_counter += 1

       
        tipo_real = 'None'

        if token_type == 'IDENTIFIER':
            if len(self.previous_tokens) > 1:
                prev_token_value = self.previous_tokens[-2]
                if prev_token_value[1] in ['void','int', 'float', 'double', 'char', 'bool', 'class', 'struct']:
                    tipo_real = prev_token_value[1] 
        elif token_type == 'NUMERIC_CONSTANT':
            
            if '.' in token_value:  
                if token_value.count('.') == 1: 
                    tipo_real = 'float' 
                else:
                    tipo_real = 'None'  
            else:
                tipo_real = 'int'  

        # Almacena el símbolo en la tabla normalmente
        self.symbol_table[current_id] = {
            'tipo': token_type,          
            'ambito': self.current_scope, 
            'posicion_inicial': token_initial_position, 
            'posicion_final': token_final_position, 
            'valor': token_value,
            'tipo_real': tipo_real,  # Almacena el tipo real como cadena
        }

        #Solo los últimos 3 tokens para evitar un uso excesivo de memoria
        if len(self.previous_tokens) > 3:
            self.previous_tokens.pop(0)

    def get_symbol_table(self):
        """Devuelve la tabla de símbolos completa."""
        return self.symbol_table

    def print_symbol_table(self):
        print("\nTabla de Símbolos:")
        print(f"{'ID':<5} {'Tipo':<20} {'Ámbito':<10} {'Inicio':<8} {'Fin':<8} {'Tipo valor':<15} {'Valor'}")
        print("=" * 80)  
        
        for symbol_id, symbol_data in self.symbol_table.items():
            print(f"{symbol_id:<5} {symbol_data['tipo']:<20} {symbol_data['ambito']:<10} {symbol_data['posicion_inicial']:<8} {symbol_data['posicion_final']:<8} {symbol_data['tipo_real']:<15} {symbol_data['valor']}")
            print("-" * 80)  
        print("=" * 80) 
