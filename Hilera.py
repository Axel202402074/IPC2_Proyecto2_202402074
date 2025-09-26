from ListaSimpleEnlazada import ListaSimpleEnlazada


class Hilera:
    def __init__(self, numero):
        self.numero = numero
        self.plantas = ListaSimpleEnlazada()  # Usamos nuestra lista propia

    def agregar_planta(self, planta):
        self.plantas.agregar(planta)
