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
