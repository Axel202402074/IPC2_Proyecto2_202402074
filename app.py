from flask import Flask, render_template, request, redirect, url_for, send_file
import os

from lector_xml import cargar_configuracion
from generador_xml import generar_salida
from generador_html import generar_reporte_html
from generador_grafico import graficar_lista

app = Flask(__name__)

invernaderos = None


@app.route("/")
def index():
    return render_template("index.html", invernaderos=invernaderos)


@app.route("/cargar", methods=["POST"])
def cargar():
    global invernaderos
    archivo = request.files["archivo"]
    if archivo:
        archivo.save("entrada.xml")
        invernaderos = cargar_configuracion("entrada.xml")
    return redirect(url_for("index"))


@app.route("/ver_plan", methods=["GET"])
def ver_plan():
    inv_nombre = request.args.get("invernadero")
    plan_nombre = request.args.get("plan")

    if not invernaderos:
        return redirect(url_for("index"))

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

    # Generar reporte HTML de ese plan específico
    generar_reporte_html(invernaderos, "ReporteInvernaderos.html")
    return send_file("ReporteInvernaderos.html", as_attachment=True)
