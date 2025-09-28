from ListaSimpleEnlazada import ListaSimpleEnlazada
from MapaDrones import MapaDrones, ConsumoDron


class Plan_Riego:
    def __init__(self, nombre):
        self.nombre = nombre
        self.secuencia = ListaSimpleEnlazada()
        self.secuencia_str = ""

    def agregar_instruccion(self, instruccion):
        self.secuencia.insertar(instruccion)

    def ordenar_instrucciones(self):
        if self.secuencia.longitud <= 1:
            return
        
        cambio = True
        while cambio:
            cambio = False
            actual = self.secuencia.primero
            while actual and actual.siguiente:
                if actual.dato.tiempo > actual.siguiente.dato.tiempo:
                    temp = actual.dato
                    actual.dato = actual.siguiente.dato
                    actual.siguiente.dato = temp
                    cambio = True
                elif actual.dato.tiempo == actual.siguiente.dato.tiempo:
                    if actual.dato.dron > actual.siguiente.dato.dron:
                        temp = actual.dato
                        actual.dato = actual.siguiente.dato
                        actual.siguiente.dato = temp
                        cambio = True
                actual = actual.siguiente

    def calcular_resultados(self):
        tiempo_optimo = 0
        agua_total = 0.0
        fertilizante_total = 0.0
        consumo_por_dron = MapaDrones()

        actual = self.secuencia.primero
        while actual:
            instruccion = actual.dato
            
            tiempo_optimo = max(tiempo_optimo, instruccion.tiempo)

            if instruccion.planta:
                if not consumo_por_dron.contiene(instruccion.dron):
                    consumo_por_dron.agregar(instruccion.dron, ConsumoDron())

                accion_lower = instruccion.accion.lower()
                
                if "regar" in accion_lower:
                    consumo = consumo_por_dron.obtener(instruccion.dron)
                    
                    agua = instruccion.planta.litros_agua
                    agua_total += agua
                    consumo.agua += agua
                    
                    fertilizante = instruccion.planta.gramos_fertilizante
                    fertilizante_total += fertilizante
                    consumo.fertilizante += fertilizante

            actual = actual.siguiente

        return {
            "tiempo_optimo": tiempo_optimo,
            "agua_total": round(agua_total, 2),
            "fertilizante_total": round(fertilizante_total, 2),
            "consumo_por_dron": consumo_por_dron
        }

    def obtener_instrucciones_en_tiempo(self, tiempo):
        instrucciones = ListaSimpleEnlazada()
        actual = self.secuencia.primero
        while actual:
            if actual.dato.tiempo == tiempo:
                instrucciones.agregar(actual.dato)
            actual = actual.siguiente
        return instrucciones

    def __str__(self):
        return f"Plan de Riego: {self.nombre} ({self.secuencia.longitud} instrucciones)"