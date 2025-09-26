from ListaSimpleEnlazada import ListaSimpleEnlazada

class Plan_Riego:
    def __init__(self, nombre):
        self.nombre = nombre
        self.secuencia = ListaSimpleEnlazada()  # Secuencia de Hx-Py

    def agregar_instruccion(self, instruccion):
        self.secuencia.agregar(instruccion)