def generar_reporte_html(invernaderos, archivo="ReporteInvernaderos.html"):
    html = """
    <html>
    <head>
        <title>Reporte de Invernaderos</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1, h2, h3 { color: darkgreen; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
            th, td { border: 1px solid #555; padding: 8px; text-align: center; }
            th { background-color: #eee; }
        </style>
    </head>
    <body>
    <h1>Reporte de Invernaderos</h1>
    """

    actual_inv = invernaderos.primero
    while actual_inv:
        inv = actual_inv.dato
        html += f"<h2>{inv.nombre}</h2>"

        actual_plan = inv.planes.primero
        while actual_plan:
            plan = actual_plan.dato
            resultados = plan.calcular_resultados()

            html += f"<h3>Plan: {plan.nombre}</h3>"

            # 🔹 Resumen general del plan
            html += "<h4>Resumen del Plan</h4>"
            html += "<table><tr><th>Tiempo Óptimo (s)</th><th>Agua Total (L)</th><th>Fertilizante Total (g)</th></tr>"
            html += f"<tr><td>{resultados['tiempo_optimo']}</td><td>{resultados['agua_total']}</td><td>{resultados['fertilizante_total']}</td></tr></table>"

            # 🔹 Tabla 1: Asignación de drones
            html += "<h4>Asignación de Drones</h4>"
            html += "<table><tr><th>Hilera</th><th>Dron</th></tr>"
            actual_dron = inv.drones.primero
            while actual_dron:
                dron = actual_dron.dato
                html += f"<tr><td>{dron.hilera}</td><td>{dron.nombre}</td></tr>"
                actual_dron = actual_dron.siguiente
            html += "</table>"

            # 🔹 Tabla 2: Instrucciones reales
            html += "<h4>Instrucciones</h4>"
            html += "<table><tr><th>Tiempo (s)</th><th>Dron</th><th>Acción</th></tr>"
            actual_instr = plan.secuencia.primero
            while actual_instr:
                instr = actual_instr.dato
                if instr.planta:
                    html += f"<tr><td>{instr.tiempo}</td><td>{instr.dron}</td><td>{instr.accion} ({instr.planta})</td></tr>"
                else:
                    html += f"<tr><td>{instr.tiempo}</td><td>{instr.dron}</td><td>{instr.accion}</td></tr>"
                actual_instr = actual_instr.siguiente
            html += "</table>"

            # 🔹 Tabla 3: Consumo por dron
            html += "<h4>Consumo por Dron</h4>"
            html += "<table><tr><th>Dron</th><th>Agua Usada (L)</th><th>Fertilizante Usado (g)</th></tr>"
            for dron, consumos in resultados["consumo_por_dron"].items():
                html += f"<tr><td>{dron}</td><td>{consumos['agua']}</td><td>{consumos['fertilizante']}</td></tr>"
            html += "</table>"

            actual_plan = actual_plan.siguiente

        actual_inv = actual_inv.siguiente

    html += "</body></html>"

    with open(archivo, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Reporte HTML generado: {archivo}")

    html = """
    <html>
    <head>
        <title>Reporte de Invernaderos</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1, h2, h3 { color: darkgreen; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
            th, td { border: 1px solid #555; padding: 8px; text-align: center; }
            th { background-color: #eee; }
        </style>
    </head>
    <body>
    <h1>Reporte de Invernaderos</h1>
    """

    actual_inv = invernaderos.primero
    while actual_inv:
        inv = actual_inv.dato
        html += f"<h2>{inv.nombre}</h2>"

        actual_plan = inv.planes.primero
        while actual_plan:
            plan = actual_plan.dato
            html += f"<h3>Plan: {plan.nombre}</h3>"

            # Tabla 1: Asignación de drones
            html += "<h4>Asignación de Drones</h4>"
            html += "<table><tr><th>Hilera</th><th>Dron</th></tr>"
            actual_dron = inv.drones.primero
            while actual_dron:
                dron = actual_dron.dato
                html += f"<tr><td>{dron.hilera}</td><td>{dron.nombre}</td></tr>"
                actual_dron = actual_dron.siguiente
            html += "</table>"

            # Tabla 2: Instrucciones (por ahora ficticias)
            html += "<h4>Instrucciones</h4>"
            html += "<table><tr><th>Tiempo (s)</th><th>Dron</th><th>Acción</th></tr>"
            html += "<tr><td>1</td><td>DR01</td><td>Adelante (H1P1)</td></tr>"
            html += "<tr><td>2</td><td>DR01</td><td>Regar</td></tr>"
            html += "</table>"

            # Estadísticas (por ahora ficticias)
            html += "<h4>Estadísticas</h4>"
            html += "<table><tr><th>Total Agua (L)</th><th>Total Fertilizante (g)</th></tr>"
            html += "<tr><td>5</td><td>500</td></tr></table>"

            actual_plan = actual_plan.siguiente

        actual_inv = actual_inv.siguiente

    html += "</body></html>"

    with open(archivo, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Reporte HTML generado: {archivo}")
