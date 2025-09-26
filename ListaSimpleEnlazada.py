class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaSimpleEnlazada:
    def __init__(self):
        self.primero = None
        self.longitud = 0

    def agregar(self, dato):
        nodo = Nodo(dato)
        if self.primero is None:
            self.primero = nodo
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nodo
        self.longitud += 1

    def obtener(self, indice):
        if indice < 0 or indice >= self.longitud:
            return None
        actual = self.primero
        for i in range(indice):
            actual = actual.siguiente
        return actual.dato

    def buscar_indice(self, id_buscar):
        # Busca el índice de un elemento por su id
        actual = self.primero
        indice = 0
        while actual:
            if hasattr(actual.dato, 'id') and actual.dato.id == id_buscar:
                return indice
            actual = actual.siguiente
            indice += 1
        return -1
    
    def recorrer(self):
        # Recorre e imprime todos los datos
        actual = self.primero
        while actual:
            print(actual.dato)
            actual = actual.siguiente

    def eliminar(self, indice):
        if indice < 0 or indice >= self.longitud:
            return None
        if indice == 0:
            eliminado = self.primero.dato
            self.primero = self.primero.siguiente
        else:
            anterior = self.primero
            for i in range(indice - 1):
                anterior = anterior.siguiente
            eliminado = anterior.siguiente.dato
            anterior.siguiente = anterior.siguiente.siguiente
        self.longitud -= 1
        return eliminado


