from Instruccion import Instruccion
from ListaSimpleEnlazada import ListaSimpleEnlazada
from MapaDrones import MapaDrones

class ItemSecuencia:
    def __init__(self, hilera, posicion):
        self.hilera = hilera
        self.posicion = posicion

class TareaDron:
    def __init__(self, dron, planta, posicion_destino):
        self.dron = dron
        self.planta = planta
        self.posicion_destino = posicion_destino
        self.posicion_actual = 0
        self.estado = "esperando"

class GeneradorInstrucciones:
    def __init__(self, invernadero):
        self.invernadero = invernadero
        self.posiciones_drones = MapaDrones()
        self.tiempo_global = 0
        
    def generar_plan(self, plan_riego, secuencia_str):
        secuencia = self._parsear_secuencia(secuencia_str)
        
        actual_dron = self.invernadero.drones.primero
        while actual_dron:
            dron = actual_dron.dato
            self.posiciones_drones.agregar(dron.nombre, 0)
            actual_dron = actual_dron.siguiente
        
        tareas_por_dron = MapaDrones()
        actual_dron = self.invernadero.drones.primero
        while actual_dron:
            dron = actual_dron.dato
            tareas_por_dron.agregar(dron.nombre, ListaSimpleEnlazada())
            actual_dron = actual_dron.siguiente
        
        actual_item = secuencia.primero
        while actual_item:
            item = actual_item.dato
            dron = self._obtener_dron_por_hilera(item.hilera)
            if dron:
                planta = self._obtener_planta(item.hilera, item.posicion)
                if planta:
                    tarea = TareaDron(dron, planta, item.posicion)
                    cola_tareas = tareas_por_dron.obtener(dron.nombre)
                    cola_tareas.agregar(tarea)
            actual_item = actual_item.siguiente
        
        self._procesar_tareas_paralelo(plan_riego, tareas_por_dron)
        
        plan_riego.ordenar_instrucciones()
        return plan_riego
    
    def _procesar_tareas_paralelo(self, plan_riego, tareas_por_dron):
        indices_tareas = MapaDrones()
        tareas_actuales = MapaDrones()
        
        actual_dron = self.invernadero.drones.primero
        while actual_dron:
            dron = actual_dron.dato
            nombre = dron.nombre
            cola = tareas_por_dron.obtener(nombre)
            indices_tareas.agregar(nombre, cola.primero if cola else None)
            tareas_actuales.agregar(nombre, None)
            actual_dron = actual_dron.siguiente
        
        todas_finalizadas = False
        
        while not todas_finalizadas:
            self.tiempo_global += 1
            
            actual_dron = self.invernadero.drones.primero
            while actual_dron:
                dron = actual_dron.dato
                nombre = dron.nombre
                
                tarea_actual = tareas_actuales.obtener(nombre)
                if tarea_actual is None:
                    indice = indices_tareas.obtener(nombre)
                    if indice is not None:
                        tarea_actual = indice.dato
                        tarea_actual.posicion_actual = self.posiciones_drones.obtener(nombre)
                        tareas_actuales.agregar(nombre, tarea_actual)
                        indices_tareas.agregar(nombre, indice.siguiente)
                
                tarea = tareas_actuales.obtener(nombre)
                
                if tarea is None:
                    instruccion = Instruccion(self.tiempo_global, nombre, "Esperar", None)
                    plan_riego.agregar_instruccion(instruccion)
                
                elif tarea.posicion_actual < tarea.posicion_destino:
                    tarea.posicion_actual += 1
                    instruccion = Instruccion(
                        self.tiempo_global,
                        nombre,
                        f"Adelante (H{dron.hilera}P{tarea.posicion_actual})",
                        None
                    )
                    plan_riego.agregar_instruccion(instruccion)
                    self.posiciones_drones.agregar(nombre, tarea.posicion_actual)
                
                elif tarea.posicion_actual > tarea.posicion_destino:
                    tarea.posicion_actual -= 1
                    instruccion = Instruccion(
                        self.tiempo_global,
                        nombre,
                        f"Atras (H{dron.hilera}P{tarea.posicion_actual})",
                        None
                    )
                    plan_riego.agregar_instruccion(instruccion)
                    self.posiciones_drones.agregar(nombre, tarea.posicion_actual)
                
                else:
                    instruccion = Instruccion(
                        self.tiempo_global,
                        nombre,
                        "Regar",
                        tarea.planta
                    )
                    plan_riego.agregar_instruccion(instruccion)
                    tareas_actuales.agregar(nombre, None)
                
                actual_dron = actual_dron.siguiente
            
            todas_finalizadas = True
            actual_dron = self.invernadero.drones.primero
            while actual_dron:
                nombre = actual_dron.dato.nombre
                if tareas_actuales.obtener(nombre) is not None or indices_tareas.obtener(nombre) is not None:
                    todas_finalizadas = False
                    break
                actual_dron = actual_dron.siguiente
    
    def _parsear_secuencia(self, secuencia_str):
        secuencia = ListaSimpleEnlazada()
        items = secuencia_str.split(',')
        for item in items:
            item = item.strip()
            partes = item.split('-')
            if len(partes) == 2:
                hilera = int(partes[0].replace('H', ''))
                posicion = int(partes[1].replace('P', ''))
                secuencia.agregar(ItemSecuencia(hilera, posicion))
        return secuencia
    
    def _obtener_dron_por_hilera(self, hilera_num):
        actual_dron = self.invernadero.drones.primero
        while actual_dron:
            dron = actual_dron.dato
            if dron.hilera == hilera_num:
                return dron
            actual_dron = actual_dron.siguiente
        return None
    
    def _obtener_planta(self, hilera_num, posicion_num):
        actual_hilera = self.invernadero.hileras.primero
        while actual_hilera:
            hilera = actual_hilera.dato
            if hilera.numero == hilera_num:
                actual_planta = hilera.plantas.primero
                while actual_planta:
                    planta = actual_planta.dato
                    if planta.posicion == posicion_num:
                        return planta
                    actual_planta = actual_planta.siguiente
            actual_hilera = actual_hilera.siguiente
        return None