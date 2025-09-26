import xml.etree.ElementTree as ET
from Invernadero import Invernadero
from Hilera import Hilera
from Planta import Planta
from Dron import Dron
from Riego import Plan_Riego
from ListaSimpleEnlazada import ListaSimpleEnlazada

def cargar_configuracion(ruta_xml):
    tree = ET.parse(ruta_xml)
    root = tree.getroot()

    invernaderos = ListaSimpleEnlazada()

    # Recorrer lista de invernaderos
    for inv_elem in root.find("listaInvernaderos"):
        nombre_inv = inv_elem.get("nombre")
        invernadero = Invernadero(nombre_inv)

        # Leer número de hileras y plantas por hilera
        num_hileras = int(inv_elem.find("numeroHileras").text)
        plantas_x_hilera = int(inv_elem.find("plantasXhilera").text)

        # Crear hileras
        for i in range(1, num_hileras + 1):
            hilera = Hilera(i)
            invernadero.hileras.agregar(hilera)

        # Leer plantas
        for planta_elem in inv_elem.find("listaPlantas"):
            hilera = int(planta_elem.get("hilera"))
            posicion = int(planta_elem.get("posicion"))
            litros = int(planta_elem.get("litrosAgua"))
            gramos = int(planta_elem.get("gramosFertilizante"))
            tipo = planta_elem.text.strip()

            planta = Planta(hilera, posicion, litros, gramos, tipo)

            # Agregar a la hilera correspondiente
            hilera_obj = invernadero.hileras.obtener(hilera - 1)
            hilera_obj.agregar_planta(planta)

        # Leer asignación de drones
        for dron_elem in inv_elem.find("asignacionDrones"):
            id_dron = int(dron_elem.get("id"))
            hilera = int(dron_elem.get("hilera"))
            nombre = f"DR{id_dron:02d}"
            dron = Dron(id_dron, nombre, hilera)
            invernadero.drones.agregar(dron)

        # Leer planes de riego
        for plan_elem in inv_elem.find("planesRiego"):
            nombre_plan = plan_elem.get("nombre")
            secuencia = plan_elem.text.strip().split(", ")
            plan = Plan_Riego(nombre_plan)

            for instruccion in secuencia:
                plan.agregar_instruccion(instruccion)

            invernadero.planes.agregar(plan)

        # Agregar invernadero a la lista general
        invernaderos.agregar(invernadero)

    return invernaderos
