from graphviz import Digraph

def graficar_lista(lista, nombre_archivo="lista", titulo="Lista Simple Enlazada"):
    dot = Digraph(comment=titulo)
    
    num_elementos = lista.longitud
    ancho = max(12, num_elementos * 2)
    
    dot.attr(rankdir="LR", size=f"{ancho},8")
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue', 
            fontsize='12', width='1.5', height='0.8')
    
    actual = lista.primero
    idx = 0
    
    while actual:
        nodo_name = f"n{idx}"
        dato_str = str(actual.dato)
        dot.node(nodo_name, dato_str)
        
        if actual.siguiente:
            dot.edge(nodo_name, f"n{idx+1}")
        
        actual = actual.siguiente
        idx += 1
    
    dot.render(nombre_archivo, format="png", cleanup=True, dpi='300')
    print(f"Grafico generado: {nombre_archivo}.png")


def graficar_instrucciones(plan, tiempo_max, nombre_archivo="cola_instrucciones"):
    # Contar instrucciones 
    actual = plan.secuencia.primero
    contador_previo = 0
    while actual:
        if actual.dato.tiempo <= tiempo_max:
            contador_previo += 1
        actual = actual.siguiente
        
    ancho = max(15, contador_previo * 2.5)
    alto = max(8, contador_previo * 0.3)
    
    dot = Digraph(comment=f"Instrucciones hasta {tiempo_max}s")
    dot.attr(rankdir="LR", size=f"{ancho},{alto}")
    dot.attr('node', shape='box', style='filled', fontsize='11', 
            width='2', height='1')
    dot.attr('graph', dpi='300', nodesep='0.5', ranksep='1')
    
    actual = plan.secuencia.primero
    idx = 0
    contador = 0
    ultimo_nodo = None
    
    while actual:
        instr = actual.dato
        
        if instr.tiempo <= tiempo_max:
            nodo_name = f"n{idx}"
            
            etiqueta = f"T:{instr.tiempo}s\\n{instr.dron}\\n"
            
            accion_lower = instr.accion.lower()
            if "regar" in accion_lower:
                color = "lightblue"
                etiqueta += "Regar"
            elif "fertilizar" in accion_lower:
                color = "lightgreen"
                etiqueta += "Fertilizar"
            elif "adelante" in accion_lower or "mover" in accion_lower:
                color = "lightyellow"
                etiqueta += f"{instr.accion}"
            elif "atras" in accion_lower:
                color = "lightcoral"
                etiqueta += f"{instr.accion}"
            elif "esperar" in accion_lower:
                color = "lightgray"
                etiqueta += "Esperar"
            else:
                color = "white"
                etiqueta += instr.accion
            
            if instr.planta:
                etiqueta += f"\\n{instr.planta}"
            
            dot.node(nodo_name, etiqueta, fillcolor=color)
            
            if ultimo_nodo is not None:
                dot.edge(ultimo_nodo, nodo_name)
            
            ultimo_nodo = nodo_name
            contador += 1
            idx += 1
        
        actual = actual.siguiente
    
    if contador > 0:
        dot.render(nombre_archivo, format="png", cleanup=True)
        print(f"Grafico generado: {nombre_archivo}.png (Total: {contador} instrucciones)")
    else:
        print(f"No hay instrucciones dentro del tiempo maximo de {tiempo_max}s")


def graficar_cola(cola, nombre_archivo="cola", titulo="Cola"):
    num_elementos = cola.longitud
    ancho = max(12, num_elementos * 2)
    
    dot = Digraph(comment=titulo)
    dot.attr(rankdir="LR", size=f"{ancho},8")
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightyellow',
            fontsize='12', width='1.5', height='0.8')
    dot.attr('graph', dpi='300')
    
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
    
    dot.render(nombre_archivo, format="png", cleanup=True)
    print(f"Grafico generado: {nombre_archivo}.png")