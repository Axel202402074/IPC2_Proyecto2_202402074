from graphviz import Digraph

def graficar_lista(lista, nombre_archivo="lista.png", titulo="Lista Simple Enlazada"):
    dot = Digraph(comment=titulo)
    dot.attr(rankdir="LR", size="8")

    actual = lista.primero
    idx = 0
    while actual:
        nodo_name = f"n{idx}"
        dot.node(nodo_name, str(actual.dato))
        if actual.siguiente:
            dot.edge(nodo_name, f"n{idx+1}")
        actual = actual.siguiente
        idx += 1

    dot.render(nombre_archivo, format="png", cleanup=True)
    print(f"Gráfico generado: {nombre_archivo}.png")


def graficar_instrucciones(plan, tiempo_max, nombre_archivo="cola_instrucciones.png"):
    dot = Digraph(comment=f"Instrucciones hasta {tiempo_max}s")
    dot.attr(rankdir="LR", size="8")

    actual = plan.secuencia.primero
    idx = 0
    while actual:
        instr = actual.dato
        if instr.tiempo <= tiempo_max:
            nodo_name = f"n{idx}"
            etiqueta = f"{instr.tiempo}s\\n{instr.dron}\\n{instr.accion}"
            if instr.planta:
                etiqueta += f" ({instr.planta})"
            dot.node(nodo_name, etiqueta, shape="box")
            if actual.siguiente and actual.siguiente.dato.tiempo <= tiempo_max:
                dot.edge(nodo_name, f"n{idx+1}")
        actual = actual.siguiente
        idx += 1

    dot.render(nombre_archivo, format="png", cleanup=True)
    print(f"Gráfico generado: {nombre_archivo}.png")