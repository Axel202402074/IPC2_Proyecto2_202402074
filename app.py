from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os
from lector_xml import cargar_configuracion
from GeneradorInstrucciones import GeneradorInstrucciones
from generador_html import generar_reporte_html
from generador_xml import generar_salida
from generador_grafico import graficar_instrucciones
from ListaSimpleEnlazada import ListaSimpleEnlazada

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'archivos'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs('archivos', exist_ok=True)

invernaderos = None

@app.route('/')
def index():
    global invernaderos
    
    tiene_inv = invernaderos is not None and invernaderos.longitud > 0
    
    return render_template('index.html', 
                        tiene_invernaderos=tiene_inv,
                        invernaderos=invernaderos)

@app.route('/cargar', methods=['POST'])
def cargar():
    global invernaderos
    
    if 'archivo' not in request.files:
        return redirect(url_for('index'))
    
    archivo = request.files['archivo']
    
    if archivo.filename == '':
        return redirect(url_for('index'))
    
    if archivo and archivo.filename.endswith('.xml'):
        filename = secure_filename(archivo.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        archivo.save(filepath)
        
        invernaderos = cargar_configuracion(filepath)
        
    return redirect(url_for('index'))

@app.route('/simular', methods=['POST'])
def simular():
    global invernaderos
    
    if not invernaderos:
        return redirect(url_for('index'))
    
    # Procesar plan 
    inv_plan = request.form.get('invernadero_plan', '')
    if '|' in inv_plan:
        nombre_inv, nombre_plan = inv_plan.split('|', 1)
    else:
        nombre_inv = request.form.get('invernadero')
        nombre_plan = request.form.get('plan')
    
    invernadero = None
    actual_inv = invernaderos.primero
    while actual_inv:
        if actual_inv.dato.nombre == nombre_inv:
            invernadero = actual_inv.dato
            break
        actual_inv = actual_inv.siguiente
    
    if not invernadero:
        return redirect(url_for('index'))
    
    plan = None
    actual_plan = invernadero.planes.primero
    while actual_plan:
        if actual_plan.dato.nombre == nombre_plan:
            plan = actual_plan.dato
            break
        actual_plan = actual_plan.siguiente
    
    if not plan:
        return redirect(url_for('index'))
    
    generador = GeneradorInstrucciones(invernadero)
    plan.secuencia = ListaSimpleEnlazada()
    generador.generar_plan(plan, plan.secuencia_str)
    
    resultados = plan.calcular_resultados()
    
    return render_template('resultados.html',
                        tiene_invernaderos=True,
                        invernaderos=invernaderos,
                        resultados=resultados,
                        invernadero_actual=invernadero,
                        plan_actual=plan)

@app.route('/graficar', methods=['POST'])
def graficar():
    global invernaderos
    
    if not invernaderos:
        return redirect(url_for('index'))
    
    # Procesar formato "plan"
    inv_plan = request.form.get('invernadero_plan', '')
    if '|' in inv_plan:
        nombre_inv, nombre_plan = inv_plan.split('|', 1)
    else:
        nombre_inv = request.form.get('invernadero')
        nombre_plan = request.form.get('plan')
    
    tiempo = int(request.form.get('tiempo', 3))
    
    invernadero = None
    actual_inv = invernaderos.primero
    while actual_inv:
        if actual_inv.dato.nombre == nombre_inv:
            invernadero = actual_inv.dato
            break
        actual_inv = actual_inv.siguiente
    
    if not invernadero:
        return redirect(url_for('index'))
    
    plan = None
    actual_plan = invernadero.planes.primero
    while actual_plan:
        if actual_plan.dato.nombre == nombre_plan:
            plan = actual_plan.dato
            break
        actual_plan = actual_plan.siguiente
    
    if not plan:
        return redirect(url_for('index'))
    
    generador = GeneradorInstrucciones(invernadero)
    plan.secuencia = ListaSimpleEnlazada()
    generador.generar_plan(plan, plan.secuencia_str)
    
    ruta_grafico = os.path.join(app.config['UPLOAD_FOLDER'], f"grafico_{nombre_plan}.png")
    graficar_instrucciones(plan, tiempo, os.path.join(app.config['UPLOAD_FOLDER'], f"grafico_{nombre_plan}"))
    
    return send_file(ruta_grafico, mimetype='image/png')

@app.route('/generar_html')
def generar_html():
    global invernaderos
    
    if not invernaderos:
        return redirect(url_for('index'))
    
    actual_inv = invernaderos.primero
    while actual_inv:
        inv = actual_inv.dato
        actual_plan = inv.planes.primero
        while actual_plan:
            plan = actual_plan.dato
            generador = GeneradorInstrucciones(inv)
            plan.secuencia = ListaSimpleEnlazada()
            generador.generar_plan(plan, plan.secuencia_str)
            actual_plan = actual_plan.siguiente
        actual_inv = actual_inv.siguiente
    
    ruta_html = os.path.join(app.config['UPLOAD_FOLDER'], "ReporteInvernaderos.html")
    generar_reporte_html(invernaderos, ruta_html)
    
    return send_file(ruta_html)

@app.route('/generar_xml')
def generar_xml():
    global invernaderos
    
    if not invernaderos:
        return redirect(url_for('index'))
    
    actual_inv = invernaderos.primero
    while actual_inv:
        inv = actual_inv.dato
        actual_plan = inv.planes.primero
        while actual_plan:
            plan = actual_plan.dato
            generador = GeneradorInstrucciones(inv)
            plan.secuencia = ListaSimpleEnlazada()
            generador.generar_plan(plan, plan.secuencia_str)
            actual_plan = actual_plan.siguiente
        actual_inv = actual_inv.siguiente
    
    ruta_salida = os.path.join(app.config['UPLOAD_FOLDER'], "salida.xml")
    generar_salida(invernaderos, ruta_salida)
    
    return send_file(ruta_salida, as_attachment=True)

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

if __name__ == '__main__':
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    print("Servidor iniciado en: http://localhost:4000")
    print("Presiona CTRL+C para detener")
    
    app.run(debug=False, host='localhost', port=4000, use_reloader=False)