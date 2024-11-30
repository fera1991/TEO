from collections import defaultdict
from NonTerminalEnum import NonTerminalEnum
from TokenEnum import TokenEnum
from semanticAction import ActionEnum

class LL1Generator():

    First = []
    Follow = []
    tabla_ll1 = []
    def __init__(self):

        self.First = defaultdict(lambda: None)
        self.Follow = defaultdict(lambda: None)
        self.tabla_ll1 = defaultdict(lambda: defaultdict(lambda: None))
        pass

# Función para calcular el conjunto FIRST con control de recursión
            
    def stringProd(self, p):
        s = ""
        if p == []:
            s+="' ' "

        for e in p:
            if isinstance(e, TokenEnum):
                s += e.value
            elif isinstance(e, ActionEnum):
                s += "#" + e.name
            else:
                s += e.name
            s+=" "
        return s

    def stringTer(self, c):
        s=""
        for e in c:
            s += "'' " if e == None else e.value + " "
        return s 
    
    def calcular_first(self, symbol, P, visitados):
        if symbol in visitados:
            return set()  # Evitar recursión infinita

        visitados.add(symbol)  # Marcar el símbolo como visitado

        first_set = set()

        if isinstance(symbol, TokenEnum):  # Si es un terminal
            first_set.add(symbol)
        else:  # Si es un no terminal
            for produccion in P[symbol]:
                if not produccion:  # Si la producción es vacía, agregamos None al FIRST
                    first_set.add(None)
                else:
                    for simbolo in produccion:
                        first_set |= self.calcular_first(simbolo, P, visitados)
                        # Si no es vacío, no seguimos con los siguientes símbolos
                        if None not in self.calcular_first(simbolo, P, visitados):  
                            break

        visitados.remove(symbol)  # Eliminar del conjunto de visitados una vez procesado
        self.First[symbol] = first_set
        return first_set

    def calcular_follow(self, symbol, P, follow_sets, start_symbol):
        # Si el símbolo es el inicial, añadir EOF
        if symbol == start_symbol:
            follow_sets[symbol].add(TokenEnum.EOF)

        # Recorrer todas las producciones
        for non_terminal, producciones in P.items():
            for produccion in producciones:
                for i, current_symbol in enumerate(produccion):
                    if current_symbol == symbol:
                        # Caso 2: Hay símbolos después
                        if i + 1 < len(produccion):
                            siguiente = produccion[i + 1]
                            first_siguiente = self.calcular_first(siguiente, P, set())
                            follow_sets[symbol] |= (first_siguiente - {None})  # Agregar FIRST(B) sin None
                            
                            # Si FIRST(B) contiene None, agregar FOLLOW del no terminal
                            if None in first_siguiente:
                                follow_sets[symbol] |= follow_sets[non_terminal]
                        
                        # Caso 3: Es el último símbolo
                        if i + 1 == len(produccion):
                            follow_sets[symbol] |= follow_sets[non_terminal]
            self.Follow[symbol]=follow_sets[symbol]

        return follow_sets

    def llenar_tabla_ll1(self, P, first_sets, follow_sets):
        # Inicializar la tabla LL(1) como un diccionario bidimensional
        self.tabla_ll1 = defaultdict(lambda: defaultdict(lambda: None))

        for non_terminal, producciones in P.items():
            for produccion in producciones:
                # Obtener el conjunto FIRST de la producción
                first_produccion = set()
                for simbolo in produccion:
                    if isinstance(simbolo, (TokenEnum, NonTerminalEnum)):
                        first_produccion |= first_sets[simbolo]
                        if None not in first_sets[simbolo]:  # Parar si no contiene vacío
                            break
                else:
                    first_produccion.add(None)  # Agregar vacío si todos los símbolos lo tienen

                # 1. Agregar producción para los terminales en FIRST
                for terminal in first_produccion:
                    if terminal is not None:  # Saltar vacío
                        if self.tabla_ll1[non_terminal][terminal]:
                            print(f"Conflicto en TABLA[{non_terminal}][{terminal}]")
                        self.tabla_ll1[non_terminal][terminal] = produccion

                # 2. Agregar producción para los terminales en FOLLOW si FIRST contiene vacío
                if None in first_produccion:
                    for terminal in follow_sets[non_terminal]:
                        if self.tabla_ll1[non_terminal][terminal]:
                            print(f"Conflicto en TABLA[{non_terminal}][{terminal}]")
                        self.tabla_ll1[non_terminal][terminal] = produccion

        return self.tabla_ll1
    
    def generar_conjunto_sinc(self, P, doPrint=False):
        # Inicializar conjuntos FIRST y FOLLOW
        self.First = defaultdict(lambda: None)
        self.Follow = defaultdict(lambda: None)

        # Filtrar producciones (sin anotaciones semánticas)
        P_filtered = self.filtrar_producciones(P) 

        # Calcular FIRST para todos los símbolos
        first_sets = defaultdict(set)
        for symbol in list(P_filtered.keys()) + list(TokenEnum):
            first_sets[symbol] = self.calcular_first(symbol, P_filtered, set())

        # Calcular FOLLOW para todos los no terminales
        follow_sets = defaultdict(set)
        for non_terminal in P_filtered:
            self.calcular_follow(non_terminal, P_filtered, follow_sets, NonTerminalEnum.S)

        # Calcular el conjunto SINC
        sinc_sets = defaultdict(set)
        for nt, productions in P_filtered.items():
            for production in productions:
                if not production:  # Producción epsilon
                    sinc_sets[nt].update(follow_sets[nt])
                else:
                    first_symbols = set()
                    for symbol in production:
                        if isinstance(symbol, NonTerminalEnum):  # Si es un No Terminal
                            first_symbols.update(first_sets[symbol])
                            if "" not in first_sets[symbol]:  # Detenerse si epsilon no está en FIRST
                                break
                        elif isinstance(symbol, TokenEnum):  # Si es un Terminal
                            first_symbols.add(symbol)
                            break
                    else:
                        # Si todos los símbolos producen epsilon
                        first_symbols.update(follow_sets[nt])

                    sinc_sets[nt].update(first_symbols)

        # Mostrar el conjunto SINC si se solicita
        if doPrint:
            for nt in NonTerminalEnum:
                if sinc_sets[nt]:
                    print(f"SINC de {nt.name}: {self.stringTer(sinc_sets[nt])}")
            print()

        return sinc_sets

    def filtrar_producciones(self, P):
        nueva_P = defaultdict(list)
        
        for no_terminal, producciones in P.items():
            for produccion in producciones:
                # Filtrar elementos que no sean sintácticos
                nueva_produccion = [
                    simbolo for simbolo in produccion
                    if isinstance(simbolo, (NonTerminalEnum, TokenEnum))
                ]
                # Agregar la producción filtrada al nuevo conjunto
                nueva_P[no_terminal].append(nueva_produccion)
        
        return nueva_P

    def generar_tabla(self, P, doPrint = False):
        
        self.First = defaultdict(lambda: None)
        self.Follow = defaultdict(lambda: None)

        P_filtered = self.filtrar_producciones(P) # Produccione sin anotaciones semanticas, solo terminales y no terminales

        # Calcular FIRST para todos los símbolos
        first_sets = defaultdict(set)
        for symbol in list(P_filtered.keys()) + list(TokenEnum):
            first_sets[symbol] = self.calcular_first(symbol, P_filtered, set())

        # Calcular FOLLOW para todos los no terminales
        follow_sets = defaultdict(set)
        for non_terminal in P_filtered:
            self.calcular_follow(non_terminal, P_filtered, follow_sets, NonTerminalEnum.S)

        # Llenar la tabla LL(1)
        P = self.llenar_tabla_ll1(P, first_sets, follow_sets)

        # Mostrar la tabla de resultados
        if doPrint:
            for n in NonTerminalEnum:
                if self.First[n] != None:
                    print(f"First de {n.name}: {self.stringTer( self.First[n] )}")

            print()

            for n in NonTerminalEnum:
                if self.Follow[n] != None:
                    print(f"Follow de {n.name}: {self.stringTer( self.Follow[n] )}")
            print()

            for non_terminal, row in P.items():
                for terminal, produccion in row.items():

                    print(f"TABLA[{non_terminal.name}][{terminal.value}] = {non_terminal.name} -> ", end="")
                    s=self.stringProd(produccion)
                    print(s)
                print()

        return self.tabla_ll1