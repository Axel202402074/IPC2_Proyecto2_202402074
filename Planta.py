
class Planta:
    def __init__(self, hilera, posicion, litros_agua, gramos_fertilizante, tipo, nombre, altura):
        self.hilera = hilera
        self.posicion = posicion
        self.litros_agua = litros_agua
        self.gramos_fertilizante = gramos_fertilizante
        self.tipo = tipo
        self.nombre = nombre
        self.altura = altura


    def crecer(self, cm):
        self.altura += cm
        print(f"{self.nombre} ha crecido {cm} cm y ahora mide {self.altura} cm.")

    def describir(self):
        return f"{self.nombre} es una planta de tipo {self.tipo} y mide {self.altura} cm."