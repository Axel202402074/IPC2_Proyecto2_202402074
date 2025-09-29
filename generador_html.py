def generar_reporte_html(invernaderos, archivo="ReporteInvernaderos.html"):
    """
    Genera un reporte HTML completo con todos los invernaderos, 
    planes, instrucciones y estadísticas.
    """
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reporte de Invernaderos</title>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { 
                color: #2d5016;
                text-align: center;
                border-bottom: 3px solid #4a7c2c;
                padding-bottom: 15px;
            }
            h2 { 
                color: #4a7c2c;
                margin-top: 30px;
                border-left: 5px solid #4a7c2c;
                padding-left: 15px;
            }
            h3 { 
                color: #5a8c34;
                margin-top: 25px;
            }
            h4 {
                color: #6b9d44;
                margin-top: 20px;
                margin-bottom: 10px;
            }
            table { 
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 25px;
                background-color: white;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            th, td { 
                border: 1px solid #ddd;
                padding: 12px;
                text-align: center;
            }
            th { 
                background-color: #4a7c2c;
                color: white;
                font-weight: bold;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            tr:hover {
                background-color: #f0f8e8;
            }
            .resumen {
                background-color: #e8f5e9;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            .resumen table th {
                background-color: #2d5016;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1> Reporte de Invernaderos</h1>
    """

    # Recorrer todos los invernaderos
    actual_inv = invernaderos.primero
    while actual_inv:
        inv = actual_inv.dato
        html += f"<h2>Invernadero: {inv.nombre}</h2>"

        # Recorrer todos los planes del invernadero
        actual_plan = inv.planes.primero
        while actual_plan:
            plan = actual_plan.dato
            
            # Calcular resultados del plan
            resultados = plan.calcular_resultados()

            html += f"<h3> Plan: {plan.nombre}</h3>"

            # Resumen general del plan
            html += '<div class="resumen">'
            html += "<h4>Resumen del Plan</h4>"
            html += "<table>"
            html += "<tr><th>Tiempo Óptimo (s)</th><th>Agua Total (L)</th><th>Fertilizante Total (g)</th></tr>"
            html += f"<tr><td><strong>{resultados['tiempo_optimo']}</strong></td>"
            html += f"<td><strong>{resultados['agua_total']}</strong></td>"
            html += f"<td><strong>{resultados['fertilizante_total']}</strong></td></tr>"
            html += "</table>"
            html += '</div>'

            # Tabla 1: Asignación de drones
            html += "<h4> Asignación de Drones</h4>"
            html += "<table><tr><th>Hilera</th><th>Dron</th></tr>"
            actual_dron = inv.drones.primero
            while actual_dron:
                dron = actual_dron.dato
                html += f"<tr><td>Hilera {dron.hilera}</td><td>{dron.nombre}</td></tr>"
                actual_dron = actual_dron.siguiente
            html += "</table>"

            # Tabla 2: Instrucciones ejecutadas
            html += "<h4> Instrucciones Ejecutadas</h4>"
            html += "<table><tr><th>Tiempo (s)</th><th>Dron</th><th>Acción</th></tr>"
            actual_instr = plan.secuencia.primero
            while actual_instr:
                instr = actual_instr.dato
                accion_texto = f"{instr.accion} ({instr.planta})" if instr.planta else instr.accion
                html += f"<tr><td>{instr.tiempo}</td><td>{instr.dron}</td><td>{accion_texto}</td></tr>"
                actual_instr = actual_instr.siguiente
            html += "</table>"

            # Tabla 3: Consumo por dron
            html += "<h4> Consumo por Dron</h4>"
            html += "<table><tr><th>Dron</th><th>Agua Usada (L)</th><th>Fertilizante Usado (g)</th></tr>"
            for dron, consumos in resultados["consumo_por_dron"].items():
                html += f"<tr><td><strong>{dron}</strong></td>"
                html += f"<td>{consumos['agua']}</td>"
                html += f"<td>{consumos['fertilizante']}</td></tr>"
            html += "</table>"

            actual_plan = actual_plan.siguiente

        actual_inv = actual_inv.siguiente

    html += """
        </div>
    </body>
    </html>
    """

    # Guardar archivo HTML
    with open(archivo, "w", encoding="utf-8") as f:
        f.write(html)

    print(f" Reporte HTML generado: {archivo}")