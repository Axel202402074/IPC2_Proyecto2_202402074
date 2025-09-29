from lector_xml import cargar_configuracion
from generador_xml import generar_salida
from generador_html import generar_reporte_html
from generador_grafico import graficar_instrucciones

def main():
    # Cargar archivo
    invernaderos = cargar_configuracion("entrada.xml")
    print("Archivo de entrada cargado")

    # Generar salida y reporte
    generar_salida(invernaderos, "salida.xml")
    generar_reporte_html(invernaderos, "ReporteInvernaderos.html")
    print("Archivos generados: salida.xml y ReporteInvernaderos.html")

    # Graficar instrucciones de un plan en tiempo t
    inv = invernaderos.primero.dato
    plan = inv.planes.primero.dato
    graficar_instrucciones(plan, tiempo_max=3, nombre_archivo="cola_t3")

if __name__ == "__main__":
    main()
