from ListaSimpleEnlazada import ListaSimpleEnlazada

class ParIdNombre:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor

class MapaDrones:
    def __init__(self):
        self.pares = ListaSimpleEnlazada()
    
    def agregar(self, clave, valor):
        actual = self.pares.primero
        while actual:
            if actual.dato.clave == clave:
                actual.dato.valor = valor
                return
            actual = actual.siguiente
        
        par = ParIdNombre(clave, valor)
        self.pares.agregar(par)
    
    def obtener(self, clave, valor_default=None):
        actual = self.pares.primero
        while actual:
            if actual.dato.clave == clave:
                return actual.dato.valor
            actual = actual.siguiente
        return valor_default
    
    def contiene(self, clave):
        actual = self.pares.primero
        while actual:
            if actual.dato.clave == clave:
                return True
            actual = actual.siguiente
        return False
    
    def obtener_claves(self):
        claves = ListaSimpleEnlazada()
        actual = self.pares.primero
        while actual:
            claves.agregar(actual.dato.clave)
            actual = actual.siguiente
        return claves
    
    def items(self):
        actual = self.pares.primero
        while actual:
            yield (actual.dato.clave, actual.dato.valor)
            actual = actual.siguiente


class ConsumoDron:
    def __init__(self):
        self.agua = 0.0
        self.fertilizante = 0.0