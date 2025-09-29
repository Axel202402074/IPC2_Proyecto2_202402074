class Instruccion:
    def __init__(self, tiempo, dron, accion, planta=None):
        self.tiempo = tiempo
        self.dron = dron
        self.accion = accion
        self.planta = planta  # Puede ser None si no aplica

    def __str__(self):
        if self.planta:
            return f"[{self.tiempo}s] {self.dron}: {self.accion} ({self.planta})"
        else:
            return f"[{self.tiempo}s] {self.dron}: {self.accion}"
