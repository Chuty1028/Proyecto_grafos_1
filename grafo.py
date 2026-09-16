import pandas as pd
import networkx as nx

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
