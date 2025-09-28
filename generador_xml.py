import xml.etree.ElementTree as ET
from ListaSimpleEnlazada import ListaSimpleEnlazada

class InstruccionesPorTiempo:
    def __init__(self, tiempo):
        self.tiempo = tiempo
        self.instrucciones = ListaSimpleEnlazada()
    
    def agregar_instruccion(self, instruccion):
        self.instrucciones.agregar(instruccion)

def generar_salida(invernaderos, ruta_salida="salida.xml"):
    root = ET.Element("datosSalida")
    lista_invernaderos_elem = ET.SubElement(root, "listaInvernaderos")

    actual_inv = invernaderos.primero
    while actual_inv:
        inv = actual_inv.dato
        invernadero_elem = ET.SubElement(
            lista_invernaderos_elem, 
            "invernadero", 
            nombre=inv.nombre
        )

        lista_planes_elem = ET.SubElement(invernadero_elem, "listaPlanes")

        actual_plan = inv.planes.primero
        while actual_plan:
            plan = actual_plan.dato
            plan_elem = ET.SubElement(lista_planes_elem, "plan", nombre=plan.nombre)

            resultados = plan.calcular_resultados()

            ET.SubElement(plan_elem, "tiempoOptimoSegundos").text = str(resultados["tiempo_optimo"])
            ET.SubElement(plan_elem, "aguaRequeridaLitros").text = str(int(resultados["agua_total"]))
            ET.SubElement(plan_elem, "fertilizanteRequeridoGramos").text = str(int(resultados["fertilizante_total"]))

            eficiencia_elem = ET.SubElement(plan_elem, "eficienciaDronesRegadores")
            
            consumo_drones = resultados["consumo_por_dron"]
            for dron_nombre, consumo_obj in consumo_drones.items():
                ET.SubElement(
                    eficiencia_elem,
                    "dron",
                    nombre=dron_nombre,
                    litrosAgua=str(int(consumo_obj.agua)),
                    gramosFertilizante=str(int(consumo_obj.fertilizante))
                )

            instrucciones_elem = ET.SubElement(plan_elem, "instrucciones")

            tiempos_dict = ListaSimpleEnlazada()
            
            actual_instr = plan.secuencia.primero
            while actual_instr:
                instr = actual_instr.dato
                tiempo = instr.tiempo
                
                encontrado = None
                actual_tiempo = tiempos_dict.primero
                while actual_tiempo:
                    if actual_tiempo.dato.tiempo == tiempo:
                        encontrado = actual_tiempo.dato
                        break
                    actual_tiempo = actual_tiempo.siguiente
                
                if encontrado is None:
                    nuevo_tiempo = InstruccionesPorTiempo(tiempo)
                    nuevo_tiempo.agregar_instruccion(instr)
                    tiempos_dict.agregar(nuevo_tiempo)
                else:
                    encontrado.agregar_instruccion(instr)
                
                actual_instr = actual_instr.siguiente

            actual_tiempo = tiempos_dict.primero
            while actual_tiempo:
                tiempo_obj = actual_tiempo.dato
                tiempo_elem = ET.SubElement(
                    instrucciones_elem, 
                    "tiempo", 
                    segundos=str(tiempo_obj.tiempo)
                )
                
                actual_instr2 = tiempo_obj.instrucciones.primero
                while actual_instr2:
                    instr = actual_instr2.dato
                    accion_texto = instr.accion
                    
                    ET.SubElement(
                        tiempo_elem,
                        "dron",
                        nombre=instr.dron,
                        accion=accion_texto
                    )
                    actual_instr2 = actual_instr2.siguiente
                
                actual_tiempo = actual_tiempo.siguiente

            actual_plan = actual_plan.siguiente

        actual_inv = actual_inv.siguiente

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(ruta_salida, encoding="utf-8", xml_declaration=True)
    print(f"Archivo de salida generado en: {ruta_salida}")