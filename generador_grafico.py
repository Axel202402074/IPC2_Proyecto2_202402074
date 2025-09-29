from graphviz import Digraph

def graficar_lista(lista, nombre_archivo="lista", titulo="Lista Simple Enlazada"):
    """
    Genera un gráfico de una lista simple enlazada usando Graphviz.
    
    Args:
        lista: Objeto ListaSimpleEnlazada a graficar
        nombre_archivo: Nombre base del archivo (sin extensión)
        titulo: Título del gráfico
    """
    dot = Digraph(comment=titulo)
    dot.attr(rankdir="LR", size="10,5")
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue')
    
    actual = lista.primero
    idx = 0
    
    while actual:
        nodo_name = f"n{idx}"
        # Convertir el dato a string de forma segura
        dato_str = str(actual.dato)
        dot.node(nodo_name, dato_str)
        
        if actual.siguiente:
            dot.edge(nodo_name, f"n{idx+1}")
        
        actual = actual.siguiente
        idx += 1
    
    # Renderizar y generar el archivo
    dot.render(nombre_archivo, format="png", cleanup=True)
    print(f" Gráfico generado: {nombre_archivo}.png")


def graficar_instrucciones(plan, tiempo_max, nombre_archivo="cola_instrucciones"):
    """
    Genera un gráfico de las instrucciones de un plan hasta un tiempo máximo.
    
    Args:
        plan: Objeto Plan_Riego con las instrucciones
        tiempo_max: Tiempo máximo en segundos a incluir
        nombre_archivo: Nombre base del archivo (sin extensión)
    """
    dot = Digraph(comment=f"Instrucciones hasta {tiempo_max}s")
    dot.attr(rankdir="LR", size="12,6")
    dot.attr('node', shape='box', style='filled')
    
    actual = plan.secuencia.primero
    idx = 0
    contador = 0
    ultimo_nodo = None
    
    while actual:
        instr = actual.dato
        
        # Solo incluir instrucciones dentro del tiempo máximo
        if instr.tiempo <= tiempo_max:
            nodo_name = f"n{idx}"
            
            # Crear etiqueta con información de la instrucción
            etiqueta = f" {instr.tiempo}s\\n {instr.dron}\\n"
            
            # Determinar color según la acción
            accion_lower = instr.accion.lower()
            if "regar" in accion_lower:
                color = "lightblue"
                etiqueta += " Regar"
            elif "fertilizar" in accion_lower:
                color = "lightgreen"
                etiqueta += " Fertilizar"
            elif "adelante" in accion_lower or "mover" in accion_lower:
                color = "lightyellow"
                etiqueta += f" {instr.accion}"
            elif "girar" in accion_lower or "rotar" in accion_lower:
                color = "lightcoral"
                etiqueta += f" {instr.accion}"
            else:
                color = "lightgray"
                etiqueta += instr.accion
            
            # Agregar información de planta si existe
            if instr.planta:
                etiqueta += f"\\n {instr.planta}"
            
            # Crear nodo
            dot.node(nodo_name, etiqueta, fillcolor=color)
            
            # Crear arista con el nodo anterior
            if ultimo_nodo is not None:
                dot.edge(ultimo_nodo, nodo_name)
            
            ultimo_nodo = nodo_name
            contador += 1
            idx += 1
        
        actual = actual.siguiente
    
    # Renderizar y generar el archivo
    if contador > 0:
        dot.render(nombre_archivo, format="png", cleanup=True)
        print(f" Gráfico generado: {nombre_archivo}.png (Total: {contador} instrucciones)")
    else:
        print(f" No hay instrucciones dentro del tiempo máximo de {tiempo_max}s")


def graficar_cola(cola, nombre_archivo="cola", titulo="Cola"):
    """
    Genera un gráfico de una cola usando Graphviz.
    
    Args:
        cola: Objeto Cola a graficar
        nombre_archivo: Nombre base del archivo (sin extensión)
        titulo: Título del gráfico
    """
    dot = Digraph(comment=titulo)
    dot.attr(rankdir="LR", size="10,5")
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightyellow')
    
    actual = cola.frente
    idx = 0
    
    while actual:
        nodo_name = f"n{idx}"
        dato_str = str(actual.dato)
        dot.node(nodo_name, dato_str)
        
        if actual.siguiente:
            dot.edge(nodo_name, f"n{idx+1}")
        
        actual = actual.siguiente
        idx += 1
    
    # Renderizar y generar el archivo
    dot.render(nombre_archivo, format="png", cleanup=True)
    print(f" Gráfico generado: {nombre_archivo}.png")