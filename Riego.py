from ListaSimpleEnlazada import ListaSimpleEnlazada


class Plan_Riego:
    def __init__(self, nombre):
        self.nombre = nombre
        self.secuencia = ListaSimpleEnlazada()

    def agregar_instruccion(self, instruccion):
        self.secuencia.insertar(instruccion)

    def calcular_resultados(self):
        tiempo_optimo = 0
        agua_total = 0.0
        fertilizante_total = 0.0
        consumo_por_dron = {}

        actual = self.secuencia.primero
        while actual:
            instruccion = actual.dato
            
            tiempo_optimo = max(tiempo_optimo, instruccion.tiempo)

            if instruccion.planta:
                if instruccion.dron not in consumo_por_dron:
                    consumo_por_dron[instruccion.dron] = {"agua": 0.0, "fertilizante": 0.0}

                accion_lower = instruccion.accion.lower()
                
                if "regar" in accion_lower:
                    agua = instruccion.planta.litros_agua
                    agua_total += agua
                    consumo_por_dron[instruccion.dron]["agua"] += agua
                
                if "fertilizar" in accion_lower:
                    fertilizante = instruccion.planta.gramos_fertilizante
                    fertilizante_total += fertilizante
                    consumo_por_dron[instruccion.dron]["fertilizante"] += fertilizante

            actual = actual.siguiente

        return {
            "tiempo_optimo": tiempo_optimo,
            "agua_total": round(agua_total, 2),
            "fertilizante_total": round(fertilizante_total, 2),
            "consumo_por_dron": consumo_por_dron
        }

    def obtener_instrucciones_en_tiempo(self, tiempo):
        instrucciones = []
        actual = self.secuencia.primero
        while actual:
            if actual.dato.tiempo == tiempo:
                instrucciones.append(actual.dato)
            actual = actual.siguiente
        return instrucciones

    def __str__(self):
        return f"Plan de Riego: {self.nombre} ({self.secuencia.longitud} instrucciones)"