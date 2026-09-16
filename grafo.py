import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Leemos el archivo que ya dejó listo limpieza.py:
# solo los pases completados de los 3 partidos de fase de grupos
tabla_pases = pd.read_csv("pases_limpios.csv")

# GRAFO DIRIGIDO: un pase tiene dirección, sale del que lo da y llega
# al que lo recibe. Al ser dirigido podemos separar a los jugadores que
# reparten juego de los que solo lo reciben.
# SIN PESO: una flecha de A hacia B significa "A le completó al menos
# un pase a B durante la fase de grupos". No nos importa cuántas veces,
# sino con cuántos compañeros distintos logra conectarse cada jugador.
grafo_pases = nx.DiGraph()

# Recorremos pase por pase y conectamos al que lo dio con el que lo recibió.
# Los nodos son el NOMBRE del jugador (no un id), para que el grafo se
# pueda leer directamente al exponerlo.
for indice, pase in tabla_pases.iterrows():
    jugador_que_pasa = pase["jugador_nombre"]
    jugador_que_recibe = pase["receptor_nombre"]
    # add_edge no repite conexiones: si esa pareja ya estaba, no agrega otra flecha
    grafo_pases.add_edge(jugador_que_pasa, jugador_que_recibe)

# Revisamos que el grafo se haya armado bien
cantidad_jugadores = grafo_pases.number_of_nodes()
cantidad_conexiones = grafo_pases.number_of_edges()

print("Jugadores en el grafo (nodos):", cantidad_jugadores)
print("Conexiones distintas entre jugadores (aristas):", cantidad_conexiones)
print()
print("Lista de jugadores:")
for jugador in sorted(grafo_pases.nodes()):
    print(" -", jugador)

# VISUALIZACION

# El grado de un nodo es con cuantos companeros distintos esta conectado.
# Lo usamos para el tamano del circulo: mientras mas conectado esta un
# jugador, mas grande se ve en el dibujo.
grados_por_jugador = dict(grafo_pases.degree())
tamanos_de_nodos = [grados_por_jugador[jugador] * 70 for jugador in grafo_pases.nodes()]

# spring_layout acomoda los nodos solo: los jugadores que se pasan entre
# ellos quedan cerca y los que casi no se conectan quedan en la orilla.
# La semilla (seed) hace que el dibujo salga siempre igual cada vez que corremos.
posiciones_de_nodos = nx.spring_layout(grafo_pases, seed=7, k=1.5)

plt.figure(figsize=(14, 10))

# Como el grafo es dirigido, la punta de la flecha tiene que verse bien:
#   connectionstyle curva un poco cada arista, asi el pase de ida y el de
#     vuelta entre dos jugadores no quedan encimados en la misma linea recta
#   node_size le avisa a networkx que tan grande es cada circulo, para que
#     la punta se detenga en la orilla del nodo y no quede escondida debajo
nx.draw_networkx_edges(
    grafo_pases,
    posiciones_de_nodos,
    edge_color="gray",
    alpha=0.4,
    width=0.8,
    arrowsize=14,
    arrowstyle="-|>",
    connectionstyle="arc3,rad=0.12",
    node_size=tamanos_de_nodos,
)

# circulos de los jugadores
nx.draw_networkx_nodes(
    grafo_pases,
    posiciones_de_nodos,
    node_size=tamanos_de_nodos,
    node_color="#f58282",
    alpha=0.9,
)

# nombre de cada jugador encima de su circulo
nx.draw_networkx_labels(
    grafo_pases,
    posiciones_de_nodos,
    font_size=9,
    font_weight="bold",
)

plt.title("Croacia - Grafo de pases completados en fase de grupos (Qatar 2022)", fontsize=14)
plt.axis("off")
plt.tight_layout()

# Guardamos la imagen
plt.savefig("grafo_croacia.png", dpi=150)
plt.show()
