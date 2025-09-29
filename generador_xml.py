import xml.etree.ElementTree as ET

import xml.etree.ElementTree as ET

def generar_salida(invernaderos, ruta_salida="salida.xml"):
    root = ET.Element("datosSalida")
    lista_invernaderos_elem = ET.SubElement(root, "listaInvernaderos")

    # Recorremos todos los invernaderos
    actual_inv = invernaderos.primero
    while actual_inv:
        inv = actual_inv.dato
        invernadero_elem = ET.SubElement(lista_invernaderos_elem, "invernadero", nombre=inv.nombre)

        lista_planes_elem = ET.SubElement(invernadero_elem, "listaPlanes")

        actual_plan = inv.planes.primero
        while actual_plan:
            plan = actual_plan.dato
            plan_elem = ET.SubElement(lista_planes_elem, "plan", nombre=plan.nombre)

            # 🔹 Usamos el cálculo real del plan
            resultados = plan.calcular_resultados()

            ET.SubElement(plan_elem, "tiempoOptimoSegundos").text = str(resultados["tiempo_optimo"])
            ET.SubElement(plan_elem, "aguaRequeridaLitros").text = str(resultados["agua_total"])
            ET.SubElement(plan_elem, "fertilizanteRequeridoGramos").text = str(resultados["fertilizante_total"])

            eficiencia_elem = ET.SubElement(plan_elem, "eficienciaDronesRegadores")

            for dron, consumos in resultados["consumo_por_dron"].items():
                ET.SubElement(
                    eficiencia_elem,
                    "dron",
                    nombre=dron,
                    litrosAgua=str(consumos["agua"]),
                    gramosFertilizante=str(consumos["fertilizante"])
                )

            instrucciones_elem = ET.SubElement(plan_elem, "instrucciones")

            # 🔹 Guardamos todas las instrucciones en orden
            actual_instr = plan.secuencia.primero
            while actual_instr:
                instr = actual_instr.dato
                tiempo_elem = ET.SubElement(instrucciones_elem, "tiempo", segundos=str(instr.tiempo))
                if instr.planta:
                    ET.SubElement(
                        tiempo_elem,
                        "dron",
                        nombre=instr.dron,
                        accion=f"{instr.accion} ({instr.planta})"
                    )
                else:
                    ET.SubElement(
                        tiempo_elem,
                        "dron",
                        nombre=instr.dron,
                        accion=instr.accion
                    )
                actual_instr = actual_instr.siguiente

            actual_plan = actual_plan.siguiente

        actual_inv = actual_inv.siguiente

    tree = ET.ElementTree(root)
    tree.write(ruta_salida, encoding="utf-8", xml_declaration=True)
    print(f"Archivo de salida generado en: {ruta_salida}")

    # Nodo raíz
    root = ET.Element("datosSalida")
    lista_invernaderos_elem = ET.SubElement(root, "listaInvernaderos")

    # Recorrer todos los invernaderos cargados
    actual_inv = invernaderos.primero
    while actual_inv:
        inv = actual_inv.dato
        invernadero_elem = ET.SubElement(lista_invernaderos_elem, "invernadero", nombre=inv.nombre)

        lista_planes_elem = ET.SubElement(invernadero_elem, "listaPlanes")

        actual_plan = inv.planes.primero
        while actual_plan:
            plan = actual_plan.dato

            plan_elem = ET.SubElement(lista_planes_elem, "plan", nombre=plan.nombre)

            # ⚠️ Por ahora datos ficticios de prueba
            ET.SubElement(plan_elem, "tiempoOptimoSegundos").text = str(10)
            ET.SubElement(plan_elem, "aguaRequeridaLitros").text = str(5)
            ET.SubElement(plan_elem, "fertilizanteRequeridoGramos").text = str(500)

            eficiencia_elem = ET.SubElement(plan_elem, "eficienciaDronesRegadores")

            actual_dron = inv.drones.primero
            while actual_dron:
                dron = actual_dron.dato
                ET.SubElement(
                    eficiencia_elem,
                    "dron",
                    nombre=dron.nombre,
                    litrosAgua=str(dron.agua_usada),
                    gramosFertilizante=str(dron.fertilizante_usado)
                )
                actual_dron = actual_dron.siguiente

            instrucciones_elem = ET.SubElement(plan_elem, "instrucciones")

            # ⚠️ Datos ficticios de instrucciones
            tiempo1 = ET.SubElement(instrucciones_elem, "tiempo", segundos="1")
            ET.SubElement(tiempo1, "dron", nombre="DR01", accion="Adelante (H1P1)")

            tiempo2 = ET.SubElement(instrucciones_elem, "tiempo", segundos="2")
            ET.SubElement(tiempo2, "dron", nombre="DR01", accion="Regar")

            actual_plan = actual_plan.siguiente

        actual_inv = actual_inv.siguiente

    # Guardar archivo
    tree = ET.ElementTree(root)
    tree.write(ruta_salida, encoding="utf-8", xml_declaration=True)
    print(f"Archivo de salida generado en: {ruta_salida}")

