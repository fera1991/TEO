# Función para calcular el conjunto FOLLOW
def calcular_follow(symbol, P, follow_sets, start_symbol, visitados):
    if symbol in visitados:
        return  # Evitar recursión infinita

    visitados.add(symbol)  # Marcar el símbolo como visitado

    # El símbolo de inicio siempre tiene el marcador EOF en FOLLOW
    if symbol == start_symbol:
        follow_sets[symbol].add(TokenEnum.EOF)

    # Recorrer todas las producciones de la gramática
    for non_terminal, producciones in P.items():
        for produccion in producciones:
            if symbol in produccion:  # Si el símbolo aparece en la producción
                index = produccion.index(symbol)
                siguiente = produccion[index + 1:]  # Lo que sigue después del símbolo

                if siguiente:  # Hay símbolos después del actual
                    # Calcular FIRST del resto de la producción
                    first_siguiente = set()
                    for s in siguiente:
                        first_siguiente |= calcular_first(s, P, set())
                        if None not in calcular_first(s, P, set()):
                            break
                    first_siguiente.discard(None)  # Excluir la cadena vacía
                    follow_sets[symbol] |= first_siguiente

                    # Si el FIRST del resto contiene None, agregar FOLLOW del no terminal
                    if None in first_siguiente:
                        follow_sets[symbol] |= follow_sets[non_terminal]
                else:  # No hay símbolos después, agregar FOLLOW del no terminal
                    follow_sets[symbol] |= follow_sets[non_terminal]