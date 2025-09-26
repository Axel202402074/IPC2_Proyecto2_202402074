from lector_xml import cargar_configuracion
from generador_html import generar_reporte_html

# Cargar archivo de entrada
invernaderos = cargar_configuracion("entrada.xml")

# Generar reporte HTML
generar_reporte_html(invernaderos, "ReporteInvernaderos.html")
