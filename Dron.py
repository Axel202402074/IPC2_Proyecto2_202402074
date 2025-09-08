class Drone:
    def __init__(self, id, nombre, hilera, posicion, agua_usada, fertilizante_usado):
        self.id = id
        self.nombre = nombre
        self.hilera = hilera
        self.posicion = posicion
        self.agua_usada = agua_usada
        self.fertilizante_usado = fertilizante_usado

    def fly(self, nueva_posicion):
        self.posicion = nueva_posicion
        print(f"Drone {self.id} está volando a {self.posicion}")

    def land(self):
        print(f"Drone {self.id} ha aterrizado en {self.posicion}")

    def get_info(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "hilera": self.hilera,
            "posicion": self.posicion,
            "agua_usada": self.agua_usada,
            "fertilizante_usado": self.fertilizante_usado
        }