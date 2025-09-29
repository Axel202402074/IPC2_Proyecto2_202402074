import xml.etree.ElementTree as ET

def generar_salida(invernaderos, ruta_salida="salida.xml"):
    """
    Genera el archivo XML de salida con los resultados de todos los planes.
    """
    # Nodo raíz
    root = ET.Element("datosSalida")
    lista_invernaderos_elem = ET.SubElement(root, "listaInvernaderos")

    # Recorrer todos los invernaderos usando la lista enlazada
    actual_inv = invernaderos.primero
    while actual_inv:
        inv = actual_inv.dato
        invernadero_elem = ET.SubElement(
            lista_invernaderos_elem, 
            "invernadero", 
            nombre=inv.nombre
        )

        lista_planes_elem = ET.SubElement(invernadero_elem, "listaPlanes")

        # Recorrer todos los planes del invernadero
        actual_plan = inv.planes.primero
        while actual_plan:
            plan = actual_plan.dato
            plan_elem = ET.SubElement(lista_planes_elem, "plan", nombre=plan.nombre)

            # Calcular resultados reales del plan
            resultados = plan.calcular_resultados()

            # Agregar datos calculados
            ET.SubElement(plan_elem, "tiempoOptimoSegundos").text = str(resultados["tiempo_optimo"])
            ET.SubElement(plan_elem, "aguaRequeridaLitros").text = str(resultados["agua_total"])
            ET.SubElement(plan_elem, "fertilizanteRequeridoGramos").text = str(resultados["fertilizante_total"])

            # Eficiencia por dron
            eficiencia_elem = ET.SubElement(plan_elem, "eficienciaDronesRegadores")
            
            for dron, consumos in resultados["consumo_por_dron"].items():
                ET.SubElement(
                    eficiencia_elem,
                    "dron",
                    nombre=dron,
                    litrosAgua=str(consumos["agua"]),
                    gramosFertilizante=str(consumos["fertilizante"])
                )

            # Instrucciones ejecutadas
            instrucciones_elem = ET.SubElement(plan_elem, "instrucciones")

            # Recorrer todas las instrucciones del plan
            actual_instr = plan.secuencia.primero
            while actual_instr:
                instr = actual_instr.dato
                tiempo_elem = ET.SubElement(
                    instrucciones_elem, 
                    "tiempo", 
                    segundos=str(instr.tiempo)
                )
                
                # Formatear la acción
                if instr.planta:
                    accion_texto = f"{instr.accion} ({instr.planta})"
                else:
                    accion_texto = instr.accion
                
                ET.SubElement(
                    tiempo_elem,
                    "dron",
                    nombre=instr.dron,
                    accion=accion_texto
                )
                
                actual_instr = actual_instr.siguiente

            actual_plan = actual_plan.siguiente

        actual_inv = actual_inv.siguiente

    # Guardar archivo XML
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")  # Formato legible (Python 3.9+)
    tree.write(ruta_salida, encoding="utf-8", xml_declaration=True)
    print(f"✅ Archivo de salida generado en: {ruta_salida}")