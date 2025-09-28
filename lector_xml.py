import xml.etree.ElementTree as ET
from Invernadero import Invernadero
from Hilera import Hilera
from Planta import Planta
from Dron import Dron
from Riego import Plan_Riego
from ListaSimpleEnlazada import ListaSimpleEnlazada
from MapaDrones import MapaDrones

def cargar_configuracion(ruta_xml):
    tree = ET.parse(ruta_xml)
    root = tree.getroot()

    todos_los_drones = MapaDrones()
    lista_drones_elem = root.find("listaDrones")
    if lista_drones_elem is not None:
        for dron_elem in lista_drones_elem.findall("dron"):
            id_dron = int(dron_elem.get("id"))
            nombre = dron_elem.get("nombre")
            todos_los_drones.agregar(id_dron, nombre)

    invernaderos = ListaSimpleEnlazada()

    lista_inv_elem = root.find("listaInvernaderos")
    if lista_inv_elem is None:
        return invernaderos

    for inv_elem in lista_inv_elem.findall("invernadero"):
        nombre_inv = inv_elem.get("nombre")
        inv = Invernadero(nombre_inv)

        num_hileras_elem = inv_elem.find("numeroHileras")
        plantas_x_hilera_elem = inv_elem.find("plantasXhilera")
        
        num_hileras = int(num_hileras_elem.text.strip()) if num_hileras_elem is not None else 0
        plantas_x_hilera = int(plantas_x_hilera_elem.text.strip()) if plantas_x_hilera_elem is not None else 0

        for i in range(1, num_hileras + 1):
            hilera = Hilera(i)
            inv.hileras.agregar(hilera)

        lista_plantas_elem = inv_elem.find("listaPlantas")
        if lista_plantas_elem is not None:
            for planta_elem in lista_plantas_elem.findall("planta"):
                hilera_num = int(planta_elem.get("hilera"))
                posicion = int(planta_elem.get("posicion"))
                litros = float(planta_elem.get("litrosAgua"))
                gramos = float(planta_elem.get("gramosFertilizante"))
                tipo = planta_elem.text.strip() if planta_elem.text else "Desconocido"
                
                planta = Planta(hilera_num, posicion, litros, gramos, tipo)
                
                actual_hilera = inv.hileras.primero
                while actual_hilera:
                    if actual_hilera.dato.numero == hilera_num:
                        actual_hilera.dato.agregar_planta(planta)
                        break
                    actual_hilera = actual_hilera.siguiente

        asignacion_elem = inv_elem.find("asignacionDrones")
        if asignacion_elem is not None:
            for dron_elem in asignacion_elem.findall("dron"):
                id_dron = int(dron_elem.get("id"))
                hilera = int(dron_elem.get("hilera"))
                
                nombre_dron = todos_los_drones.obtener(id_dron, f"DR{id_dron:02d}")
                dron = Dron(id_dron, nombre_dron, hilera)
                inv.drones.agregar(dron)

        planes_elem = inv_elem.find("planesRiego")
        if planes_elem is not None:
            for plan_elem in planes_elem.findall("plan"):
                nombre_plan = plan_elem.get("nombre")
                secuencia = plan_elem.text.strip() if plan_elem.text else ""
                
                plan = Plan_Riego(nombre_plan)
                plan.secuencia_str = secuencia
                
                inv.planes.agregar(plan)

        invernaderos.agregar(inv)

    return invernaderos