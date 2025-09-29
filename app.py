from flask import Flask, render_template, request, redirect, url_for, send_file
import os

from lector_xml import cargar_configuracion
from generador_xml import generar_salida
from generador_html import generar_reporte_html
from generador_grafico import graficar_lista, graficar_instrucciones

app = Flask(__name__)

invernaderos = None


@app.route("/", methods=["GET", "POST"])
def index():
    global invernaderos
    print("DEBUG: invernaderos =", invernaderos)  # <-- Aquí sí es válido
    primer_inv = None
    tiene_invernaderos = False
    seleccionado = None

    if invernaderos and invernaderos.primero:
        tiene_invernaderos = True
        # Si el usuario seleccionó un invernadero, búscalo
        if request.method == "POST":
            nombre_inv = request.form.get("invernadero")
            actual = invernaderos.primero
            while actual:
                if actual.dato.nombre == nombre_inv:
                    seleccionado = actual.dato
                    break
                actual = actual.siguiente
        # Si no, muestra el primero
        if not seleccionado:
            seleccionado = invernaderos.primero.dato

    return render_template("index.html", invernaderos=invernaderos, primer_inv=seleccionado, tiene_invernaderos=tiene_invernaderos)

@app.route("/cargar", methods=["POST"])
def cargar():
    global invernaderos
    archivo = request.files["archivo"]
    if archivo:
        archivo.save("entrada.xml")
        invernaderos = cargar_configuracion("entrada.xml")
        print("Invernaderos cargados:", invernaderos)
    return redirect(url_for("index"))


@app.route("/graficar_instrucciones", methods=["POST"])
def graficar_instrucciones_route():
    global invernaderos
    if not invernaderos:
        return redirect(url_for("index"))

    inv_nombre = request.form.get("invernadero")
    plan_nombre = request.form.get("plan")
    tiempo_max = int(request.form.get("tiempo"))

    # Buscar invernadero
    actual_inv = invernaderos.primero
    while actual_inv and actual_inv.dato.nombre != inv_nombre:
        actual_inv = actual_inv.siguiente
    if not actual_inv:
        return redirect(url_for("index"))
    inv = actual_inv.dato

    # Buscar plan
    actual_plan = inv.planes.primero
    while actual_plan and actual_plan.dato.nombre != plan_nombre:
        actual_plan = actual_plan.siguiente
    if not actual_plan:
        return redirect(url_for("index"))
    plan = actual_plan.dato

    # Generar gráfica
    filename = f"cola_{inv_nombre}_{plan_nombre}_t{tiempo_max}"
    graficar_instrucciones(plan, tiempo_max, nombre_archivo=filename)

    return send_file(filename + ".png", mimetype="image/png")

@app.route("/ayuda")
def ayuda():
    return render_template("ayuda.html")

if __name__ == "__main__":
    app.run(debug=True)