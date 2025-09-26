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
