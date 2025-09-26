from ListaSimpleEnlazada import Nodo

class Cola:
    def __init__(self):
        self.frente = None   # primer elemento
        self.final = None    # último elemento
        self.longitud = 0

    def esta_vacia(self):
        return self.frente is None

    def encolar(self, dato):
        """Agrega un nuevo dato al final de la cola"""
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self.frente = nuevo
            self.final = nuevo
        else:
            self.final.siguiente = nuevo
            self.final = nuevo
        self.longitud += 1

    def desencolar(self):
        """Elimina y devuelve el primer dato de la cola"""
        if self.esta_vacia():
            return None
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        if self.frente is None:  # si quitamos el último
            self.final = None
        self.longitud -= 1
        return dato

    def ver_frente(self):
        """Devuelve el dato al frente sin eliminarlo"""
        if self.esta_vacia():
            return None
        return self.frente.dato

    def recorrer(self):
        """Recorre e imprime todos los elementos de la cola"""
        actual = self.frente
        while actual:
            print(actual.dato)
            actual = actual.siguiente
