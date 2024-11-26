from graphviz import Digraph

class NodoArbol:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    # Función para imprimir el árbol de manera legible en la terminal
    def imprimir_arbol_terminal(self, nivel=0):
        print("  " * nivel + f"└── {self.valor}")
        for hijo in self.hijos:
            hijo.imprimir_arbol_terminal(nivel + 1)


# Función para generar y guardar el árbol sintáctico
def generar_arbol_sintactico(raiz):
    dot = Digraph()

    def recorrer_nodo(nodo):
        dot.node(str(id(nodo)), nodo.valor)  # Agregar nodo al grafo
        for hijo in nodo.hijos:
            dot.node(str(id(hijo)), hijo.valor)
            dot.edge(str(id(nodo)), str(id(hijo)))  # Crear aristas entre nodos
            recorrer_nodo(hijo)

    recorrer_nodo(raiz)
    dot.render('arbol_sintactico', format='png', cleanup=True)
    print("Árbol sintáctico generado como 'arbol_sintactico.png'.")

def generar_arbol_sintactico_terminal(raiz):
    print("Árbol sintáctico en formato de texto:")
    raiz.imprimir_arbol_terminal()  # Inicia la impresión desde la raíz
