import xml.etree.ElementTree as ET
from Invernadero import Invernadero
from Hilera import Hilera
from Planta import Planta
from Dron import Dron
from Riego import Plan_Riego
from Instruccion import Instruccion
from ListaSimpleEnlazada import ListaSimpleEnlazada

def cargar_configuracion(ruta_xml):
    tree = ET.parse(ruta_xml)
    root = tree.getroot()

    invernaderos = ListaSimpleEnlazada()

    for inv_elem in root.findall("invernadero"):
        nombre_inv = inv_elem.get("nombre")
        inv = Invernadero(nombre_inv)

        # Hileras
        for hilera_elem in inv_elem.findall("hilera"):
            numero = hilera_elem.get("numero")
            hilera = Hilera(numero)

            for planta_elem in hilera_elem.findall("planta"):
                posicion = planta_elem.get("posicion")
                litros = float(planta_elem.get("litrosAgua"))
                gramos = float(planta_elem.get("gramosFertilizante"))
                tipo = planta_elem.get("tipo")
                planta = Planta(numero, posicion, litros, gramos, tipo)
                hilera.agregar_planta(planta)

            inv.hileras.insertar(hilera)

        # Drones
        for dron_elem in inv_elem.findall("dron"):
            id_dron = dron_elem.get("id")
            nombre_dron = dron_elem.get("nombre")
            hilera_asignada = dron_elem.get("hilera")
            dron = Dron(id_dron, nombre_dron, hilera_asignada)
            inv.drones.insertar(dron)

        # Planes de riego
        for plan_elem in inv_elem.findall("planRiego"):
            nombre_plan = plan_elem.get("nombre")
            plan = Plan_Riego(nombre_plan)

            tiempo = 1
            for instr_elem in plan_elem.findall("instruccion"):
                dron_nombre = instr_elem.get("dron")
                accion = instr_elem.get("accion")
                hilera = instr_elem.get("hilera")
                posicion = instr_elem.get("posicion")

                planta = None
                if hilera and posicion:
                    # Buscar planta en las hileras
                    actual_hilera = inv.hileras.primero
                    while actual_hilera:
                        if actual_hilera.dato.numero == hilera:
                            actual_planta = actual_hilera.dato.plantas.primero
                            while actual_planta:
                                if actual_planta.dato.posicion == posicion:
                                    planta = actual_planta.dato
                                    break
                                actual_planta = actual_planta.siguiente
                        actual_hilera = actual_hilera.siguiente

                instruccion = Instruccion(tiempo, dron_nombre, accion, planta)
                plan.agregar_instruccion(instruccion)
                tiempo += 1

            inv.planes.insertar(plan)

        invernaderos.insertar(inv)

    return invernaderos
