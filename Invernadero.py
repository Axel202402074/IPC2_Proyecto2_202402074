from ListaSimpleEnlazada import ListaSimpleEnlazada


class Invernadero:
    def __init__(self, nombre):
        self.nombre = nombre
        self.hileras = ListaSimpleEnlazada()
        self.drones = ListaSimpleEnlazada()
        self.planes = ListaSimpleEnlazada()

    def __str__(self):
        return f"Invernadero {self.nombre}"