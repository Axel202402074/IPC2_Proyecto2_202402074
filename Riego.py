from ListaSimpleEnlazada import ListaSimpleEnlazada

class Plan_Riego:
    def __init__(self, nombre):
        self.nombre = nombre
        self.secuencia = ListaSimpleEnlazada()  # lista de instrucciones

    def agregar_instruccion(self, instruccion):
        self.secuencia.insertar(instruccion)

    def calcular_resultados(self):
        tiempo_optimo = 0
        agua_total = 0
        fertilizante_total = 0
        consumo_por_dron = {}

        actual = self.secuencia.primero
        while actual:
            instruccion = actual.dato
            tiempo_optimo = max(tiempo_optimo, instruccion.tiempo)

            if instruccion.accion.lower() == "regar" and instruccion.planta:
                agua_total += instruccion.planta.litros_agua
                consumo_por_dron.setdefault(instruccion.dron, {"agua": 0, "fertilizante": 0})
                consumo_por_dron[instruccion.dron]["agua"] += instruccion.planta.litros_agua

            elif instruccion.accion.lower() == "fertilizar" and instruccion.planta:
                fertilizante_total += instruccion.planta.gramos_fertilizante
                consumo_por_dron.setdefault(instruccion.dron, {"agua": 0, "fertilizante": 0})
                consumo_por_dron[instruccion.dron]["fertilizante"] += instruccion.planta.gramos_fertilizante

            actual = actual.siguiente

        return {
            "tiempo_optimo": tiempo_optimo,
            "agua_total": agua_total,
            "fertilizante_total": fertilizante_total,
            "consumo_por_dron": consumo_por_dron
        }
