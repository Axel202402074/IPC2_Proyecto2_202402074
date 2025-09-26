class Dron:
    def __init__(self, id_dron, nombre, hilera=None):
        self.id_dron = id_dron
        self.nombre = nombre
        self.hilera = hilera
        self.agua_usada = 0
        self.fertilizante_usado = 0

    def __str__(self):
        return f"{self.nombre} (Hilera {self.hilera})"