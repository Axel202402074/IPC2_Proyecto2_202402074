from ListaSimpleEnlazada import Nodo
from graphviz import Digraph


class Cola:
    def __init__(self):
        self.frente = None
        self.final = None
        self.longitud = 0

    def esta_vacia(self):
        return self.frente is None

    def encolar(self, dato):
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self.frente = nuevo
            self.final = nuevo
        else:
            self.final.siguiente = nuevo
            self.final = nuevo
        self.longitud += 1

    def desencolar(self):
        if self.esta_vacia():
            return None
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        self.longitud -= 1
        return dato

    def ver_frente(self):
        if self.esta_vacia():
            return None
        return self.frente.dato

    def recorrer(self):
        actual = self.frente
        while actual:
            print(actual.dato)
            actual = actual.siguiente

    def __iter__(self):
        actual = self.frente
        while actual:
            yield actual.dato
            actual = actual.siguiente


def graficar_lista(lista, nombre_archivo="lista", titulo="Lista Simple Enlazada"):
    dot = Digraph(comment=titulo)
    dot.attr(rankdir="LR", size="8")

    actual = lista.primero
    idx = 0
    while actual:
        nodo_name = f"n{idx}"
        dot.node(nodo_name, str(actual.dato))
        if actual.siguiente:
            dot.edge(nodo_name, f"n{idx+1}")
        actual = actual.siguiente
        idx += 1

    dot.render(nombre_archivo, format="png", cleanup=True)
    print(f"Gráfico generado: {nombre_archivo}.png")


def graficar_cola(cola, nombre_archivo="cola", titulo="Cola"):
    dot = Digraph(comment=titulo)
    dot.attr(rankdir="LR", size="8")

    actual = cola.frente
    idx = 0
    while actual:
        nodo_name = f"n{idx}"
        dot.node(nodo_name, str(actual.dato))
        if actual.siguiente:
            dot.edge(nodo_name, f"n{idx+1}")
        actual = actual.siguiente
        idx += 1

    dot.render(nombre_archivo, format="png", cleanup=True)
    print(f"Gráfico generado: {nombre_archivo}.png")