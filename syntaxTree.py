import shutil  # Para verificar si Graphviz está en el sistema

# Intentar importar Graphviz
try:
    from graphviz import Digraph  # Intentar importar Graphviz
except ImportError:
    Digraph = None  # Si no está disponible, asignar None

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


# Función para generar y guardar el árbol sintáctico con Graphviz
def generar_arbol_sintactico(raiz):
    if Digraph is not None:  # Solo proceder si Graphviz está disponible
        dot = Digraph()

        def recorrer_nodo(nodo):
            dot.node(str(id(nodo)), nodo.valor)  # Agregar nodo al grafo
            for hijo in nodo.hijos:
                dot.node(str(id(hijo)), hijo.valor)
                dot.edge(str(id(nodo)), str(id(hijo)))  # Crear aristas entre nodos
                recorrer_nodo(hijo)

        recorrer_nodo(raiz)
        try:
            dot.render('arbol_sintactico', format='png', cleanup=True)
            print("Árbol sintáctico generado como 'arbol_sintactico.png'.")
        except Exception as e:
            print(f"Ocurrió un error al generar el árbol con Graphviz: {e}")
            print("Generando el árbol en formato de texto:")
            generar_arbol_sintactico_terminal(raiz)  # Si hubo error, usar la alternativa
    else:
        print("Graphviz no está disponible. Generando el árbol en formato de texto:")
        generar_arbol_sintactico_terminal(raiz)  # Generar árbol en terminal como alternativa


# Función alternativa para generar el árbol en la terminal
def generar_arbol_sintactico_terminal(raiz):
    print("Árbol sintáctico en formato de texto:")
    raiz.imprimir_arbol_terminal()  # Inicia la impresión desde la raíz
