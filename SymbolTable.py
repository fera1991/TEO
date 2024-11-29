class SymbolTable:
    def __init__(self):
        self.symbol_table = {}
        self.id_counter = 0  # Contador para generar IDs únicos para cada símbolo
        self.scope_counter = 0  # Contador para gestionar el ámbito (nivel de anidación)
        self.local_scope_id = 0  # Identificador único para cada ámbito local
        self.current_scope = 'global'  # Definir el ámbito inicial como 'global'
        self.previous_tokens = []  # Para llevar un registro de los últimos tokens procesados
        self.errors = []  # Lista para almacenar los errores encontrados
        self.in_declaration = False # Indicador de multiple declaracion.
        self.in_declaration_asig = False # Indicador de multiple declaracion.
        self.type_declaration = '' # tipo de multiple declaracion.
        self.in_function_declaration = False  # Indicador de declaración de funciones
        self.id_function = 0
        self.save_scope = ''

    def process_token(self, token_type, token_value, token_initial_position, token_final_position, token_line_position):
        self.previous_tokens.append((token_type, token_value))

        # Manejo de ámbitos
        if token_value == '{':
            if self.scope_counter == 0:
                self.current_scope = f'local_{self.local_scope_id}'
            self.scope_counter += 1
        elif token_value == '}':
            self.scope_counter -= 1
            if self.scope_counter == 0:
                self.current_scope = 'global'
                

        tipo_real = None
        tipo = 'variable'
        valor = None

        if self.in_function_declaration and token_type == "ABRIR_LLAVE":
            self.symbol_table[self.id_function]['tipo'] = 'función'
            self.in_function_declaration = False
        if self.in_function_declaration and token_type == "PUNTO_COMA":
            self.local_scope_id -= 1
            self.in_function_declaration = False

        if token_type == "COMA":
            self.in_declaration_asig = False
        if token_type == "ASIGNACION":
            self.in_declaration_asig = True
        
        if token_type == 'PUNTO_COMA' or token_value in ['int', 'char', 'float'] or token_value == ')' :
            self.in_declaration = False

        if token_type == 'IDENTIFIER' and self.in_declaration == True and self.in_declaration_asig == False:
            id = self.id_counter
            self.id_counter += 1
            self.symbol_table[id] = {
                        'nombre': token_value,
                        'tipo': tipo,
                        'ambito': self.current_scope,
                        'inicio': token_initial_position,
                        'usos': 0,
                        'parametros': [],
                        'linea': token_line_position,
                        'tipo_valor': self.type_declaration,
                        'valor': valor
                    }

        # Procesamiento de identificadores
        if token_type == 'IDENTIFIER':
            if len(self.previous_tokens) > 1 and self.previous_tokens[-2][1] in ['int', 'float', 'char', 'void']:
                for symbol_id, symbol_data in self.symbol_table.items():
                    if symbol_data['nombre'] == token_value and symbol_data['ambito'] == self.current_scope:
                        # Verificar si es una función prototipo
                        if symbol_data['tipo'] == 'función_prototipo':
                                # Permitir la declaración si aún no se ha utilizado como función completa
                                if symbol_data['usos'] == 0:
                                    # Actualizar la tabla de símbolos para reflejar que ahora se ha utilizado como función completa
                                    symbol_data['usos'] = 1
                                    symbol_data['tipo'] = 'función'  # Actualizar el tipo a 'función' completa
                                else:
                                    # Error: ya se ha declarado como función completa
                                    error_message = f"Error: En la línea '{token_line_position}', la función '{token_value}' ya ha sido declarada como completa en el ámbito global."
                                    self.errors.append(error_message)
                                    return
                        else:
                            # Error: La variable ya existe en el ámbito y no es una función prototipo
                            error_message = f"Error: En la línea '{token_line_position}', la variable '{token_value}' ya está declarada en su ámbito."
                            self.errors.append(error_message)
                            return

                current_id = self.id_counter
                self.id_counter += 1

                if len(self.previous_tokens) > 1:
                    prev_token_value = self.previous_tokens[-2]
                    if prev_token_value[1] in ['int', 'float', 'char', 'void']:
                        if 'local' in self.current_scope:
                            self.in_declaration = True
                            self.type_declaration = prev_token_value[1]
                        tipo_real = prev_token_value[1]
                    else:
                        return
                        # Si estamos en la declaración de una función, agregar los parámetros
                if self.in_function_declaration:
                    # Primero, verificamos si el parámetro ya está en la lista de parámetros de la función
                    parametros = self.symbol_table[self.id_function]['parametros']
                    
                    # Verificar si ya existe un parámetro con el mismo nombre
                    parametro_existente = any(param['nombre'] == token_value for param in parametros)
                    
                    if not parametro_existente:
                        # Si no existe, agregamos el nuevo parámetro
                        self.symbol_table[self.id_function]['parametros'].append({
                            'nombre': token_value,
                            'tipo': tipo_real,
                            'ambito': self.current_scope  # Si es necesario agregar el ámbito
                        })

                else:
                    if tipo_real is not None:
                        self.symbol_table[current_id] = {
                            'nombre': token_value,
                            'tipo': tipo,
                            'ambito': self.current_scope,
                            'inicio': token_initial_position,
                            'usos': 0,
                            'parametros': [],
                            'linea': token_line_position,
                            'tipo_valor': tipo_real,
                            'valor': valor
                        }
                
            else:
                symbol_id, symbol_data = self.find_symbol(token_value)
                if symbol_id is None:
                    error_message = f"Error: En la linea '{token_line_position}', La variable '{token_value}' no está declarada en su ámbito."
                    self.errors.append(error_message)
                    return

       
        if token_value == '(':
            # Verificar si el token anterior es un identificador
            if len(self.previous_tokens) > 1 and self.previous_tokens[-2][0] == 'IDENTIFIER':
                # Obtener el nombre del identificador del token anterior
                previous_identifier = self.previous_tokens[-2][1]
                # Buscar si es el último símbolo registrado en la tabla de símbolos
                for symbol_id, symbol_data in self.symbol_table.items():
                    if symbol_data['nombre'] == previous_identifier and symbol_data['ambito'] == self.current_scope:
                        # Actualizar el tipo del símbolo a 'función'
                        self.symbol_table[symbol_id]['tipo'] = 'función_prototipo'
                        self.symbol_table[symbol_id]['ambito'] = 'global'
                        self.id_function = symbol_id
                        # Cambiar el ámbito actual a 'local'
                        self.local_scope_id += 1
                        self.current_scope = f"local_{self.local_scope_id}"
                        self.in_function_declaration = True 
                        break


        if len(self.previous_tokens) >= 2:
            second_last_token = self.previous_tokens[-2]
            if second_last_token[1] == '=':
                last_identifier_token = self.previous_tokens[-3]
                identifier_name = last_identifier_token[1]

                symbol_id, symbol_data = self.find_symbol(identifier_name)
                if symbol_id is not None:
                    valor = token_value
                    self.update_symbol(symbol_id, valor)
                    #print("Variable:", symbol_id, "Valor agregado: ", valor )

        if len(self.previous_tokens) > 3:
            self.previous_tokens.pop(0)

    def update_symbol(self, symbol_id, new_value): 
            if symbol_id in self.symbol_table:
                if self.symbol_table[symbol_id]['ambito'] == self.current_scope:
                    self.symbol_table[symbol_id]['valor'] = new_value
                    #print(f"Valor actualizado para el identificador '{self.symbol_table[symbol_id]['nombre']}' "
                    #      f"en el ámbito '{self.current_scope}': {new_value}")
                else:
                    error_message = f"Error: El identificador '{self.symbol_table[symbol_id]['nombre']}' no pertenece al ámbito actual ('{self.current_scope}'). No se puede actualizar."
                    self.errors.append(error_message)
                    print(error_message)
            else:
                error_message = f"Error: Identificador con ID {symbol_id} no encontrado."
                self.errors.append(error_message)
                print(error_message)


    def find_symbol_by_id(self, symbol_id):
        if symbol_id in self.symbol_table:
            return self.symbol_table[symbol_id]
        else:
            error_message = f"Error: Identificador con ID {symbol_id} no encontrado."
            self.errors.append(error_message)
            return error_message

    def find_symbol(self, symbol_name):
        # Primero, buscar en la función actual utilizando self.id_function
        if self.id_function in self.symbol_table:
            function_data = self.symbol_table[self.id_function]
            
            # Si la función tiene parámetros, buscar en esos parámetros
            if 'parametros' in function_data:
                for param in function_data['parametros']:
                    if param['nombre'] == symbol_name:
                        return self.id_function, param

        # Si no se encuentra en la función actual, buscar en el ámbito local
        for symbol_id, symbol_data in self.symbol_table.items():
            if symbol_data['nombre'] == symbol_name and symbol_data['ambito'] == self.current_scope:
                return symbol_id, symbol_data

        # Si no se encuentra en el ámbito local, buscar en el ámbito global
        if self.current_scope != "global":
            for symbol_id, symbol_data in self.symbol_table.items():
                if symbol_data['nombre'] == symbol_name and symbol_data['ambito'] == "global":
                    return symbol_id, symbol_data

        # Si no se encuentra en ningún ámbito ni en los parámetros, retornar None
        return None, None


    def delete_symbol(self, symbol_id):
        if symbol_id in self.symbol_table:
            deleted_symbol = self.symbol_table.pop(symbol_id)
            print(f"Identificador '{deleted_symbol['nombre']}' eliminado.")
        else:
            error_message = f"Error: Identificador con ID {symbol_id} no encontrado."
            self.errors.append(error_message)
            print(error_message)

    def print_symbol_table(self):
        print("\nTabla de Símbolos:")
        print(f"{'ID':<5} {'Nombre':<25} {'Tipo':<20} {'Ámbito':<10} {'Linea':<5} {'Posición':<10} {'Usos':<8} {'parametros':<15} {'Tipo Valor':<15} {'Valor'}")
        print("=" * 115)
        for symbol_id, symbol_data in self.symbol_table.items():
            # Verifica si 'parametros' es una lista vacía, si es así, lo deja vacío, si no, lo convierte en una cadena
            if symbol_data['parametros']:
                parametros = ", ".join([param['tipo'] for param in symbol_data['parametros'] if isinstance(param, dict)])
            else:
                parametros = ""
            
            print(f"{symbol_id:<5} {symbol_data['nombre']:<25} {symbol_data['tipo']:<20} "
                f"{symbol_data['ambito']:<12} {symbol_data['linea']:<5} {symbol_data['inicio']:<10} {symbol_data['usos']:<8} "
                f"{parametros:<15} {symbol_data['tipo_valor']:<15} {symbol_data['valor']}")
            print("-" * 115)
        print("=" * 115)

    def print_errors(self):
        print("\nErrores encontrados:")
        if not self.errors:
            print("No se encontraron errores.")
        else:
            for error in self.errors:
                print(f"- {error}")
