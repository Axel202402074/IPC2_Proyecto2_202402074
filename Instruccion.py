class Instruccion:
    def __init__(self, tiempo, dron, accion):
        self.tiempo = tiempo
        self.dron = dron
        self.accion = accion

    def __str__(self):
        return f"[{self.tiempo}s] {self.dron.nombre}: {self.accion}"
