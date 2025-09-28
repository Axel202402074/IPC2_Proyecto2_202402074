def generar_reporte_html(invernaderos, archivo="ReporteInvernaderos.html"):
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Reporte de Invernaderos</title>
        <style>
            body { 
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f9f9f9;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border: 1px solid #ddd;
            }
            h1 { 
                font-size: 24px;
                border-bottom: 2px solid #333;
                padding-bottom: 10px;
            }
            h2 { 
                font-size: 20px;
                margin-top: 30px;
            }
            h3 { 
                font-size: 18px;
                margin-top: 20px;
            }
            table { 
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 20px;
                font-size: 14px;
            }
            th, td { 
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th { 
                background-color: #f0f0f0;
                font-weight: bold;
            }
            tr:nth-child(even) {
                background-color: #fafafa;
            }
            .seccion {
                background-color: #fafafa;
                padding: 15px;
                margin-bottom: 20px;
                border: 1px solid #e0e0e0;
            }
        </style>
    </head>
    <body>
        <div class="container">
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

            html += '<div class="seccion">'
            html += "<table>"
            html += "<tr><th>Dato</th><th>Valor</th></tr>"
            html += f"<tr><td>Tiempo Optimo</td><td>{resultados['tiempo_optimo']} segundos</td></tr>"
            html += f"<tr><td>Agua Total</td><td>{resultados['agua_total']} litros</td></tr>"
            html += f"<tr><td>Fertilizante Total</td><td>{resultados['fertilizante_total']} gramos</td></tr>"
            html += "</table>"
            html += '</div>'

            html += "<table>"
            html += "<tr><th>Dron</th><th>Agua (L)</th><th>Fertilizante (g)</th></tr>"
            consumo_drones = resultados["consumo_por_dron"]
            for dron_nombre, consumo_obj in consumo_drones.items():
                html += f"<tr><td>{dron_nombre}</td>"
                html += f"<td>{consumo_obj.agua}</td>"
                html += f"<td>{consumo_obj.fertilizante}</td></tr>"
            html += "</table>"

            actual_plan = actual_plan.siguiente

        actual_inv = actual_inv.siguiente

    html += """
        </div>
    </body>
    </html>
    """

    with open(archivo, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Reporte HTML generado: {archivo}")