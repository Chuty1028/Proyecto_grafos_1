# "import" trae una libreria ya hecha. "pandas" lee csv y los maneja como
# tabla. "as pd" le pone apodo, para escribir pd en vez de pandas
import pandas as pd
# "networkx" es la libreria de grafos: guarda los nodos y las aristas. "as nx"
# el apodo, para escribir nx
import networkx as nx
# "matplotlib.pyplot" es la parte de matplotlib que dibuja, "as plt" el apodo.
# networkx calcula el grafo pero no lo pinta, por eso hacen falta las dos
import matplotlib.pyplot as plt

# PASO 1: LEER LOS DATOS

# "tabla_pases" es la variable donde guardamos, "=" mete adentro lo de la
# "pd.read_csv" es la funcion de pandas que abre un csv y lo vuelve
# tabla, y entre parentesis va el archivo que abre: pases_limpios.csv
tabla_pases = pd.read_csv("pases_limpios.csv")

# PASO 2: CREAR EL GRAFO VACIO

# "nx.DiGraph()" le pide a networkx un grafo nuevo y lo guarda en la variable
# "grafo_pases". "Di" viene de directed (dirigido): A->B no es lo mismo que
# B->A. Los parentesis vacios = nace sin nodos ni aristas, lo llenamos abajo
grafo_pases = nx.DiGraph()

# PASO 3: LLENAR EL GRAFO, PASE POR PASE

# "for" repite lo de adentro una vez por fila. "indice" guarda el numero de
# fila (0, 1, 2... no lo usamos). "pase" guarda la fila entera, o sea UN pase.
# "in" dice de donde saca los datos. "tabla_pases.iterrows()" es la funcion de
# pandas que va entregando las filas de una en una
for indice, pase in tabla_pases.iterrows():

    # "pase[...]" saca una columna de esa fila, entre corchetes el nombre de la
    # columna. "jugador_nombre" es el que DA el pase
    jugador_que_pasa = pase["jugador_nombre"]

    # lo mismo con la columna "receptor_nombre": el que RECIBE el pase
    jugador_que_recibe = pase["receptor_nombre"]

    # "add_edge(a, b)" agrega la arista (flecha) de a hacia b, "edge" es arista.
    # Si el jugador no existia lo crea como nodo, por eso nunca usamos add_node.
    # Y no repite conexiones ya puestas: por eso quedan 176 aristas y no 1502
    grafo_pases.add_edge(jugador_que_pasa, jugador_que_recibe)

# PASO 4: REVISAR QUE EL GRAFO QUEDO BIEN

# "number_of_nodes()" es la funcion que cuenta los nodos, "node" es nodo.
# Un nodo = un jugador. Salen 16
cantidad_jugadores = grafo_pases.number_of_nodes()

# "number_of_edges()" cuenta las aristas: parejas que conectaron al menos una
# vez en un sentido. Salen 176
cantidad_conexiones = grafo_pases.number_of_edges()

# "print" escribe en la terminal. Entre comillas el texto y despues de la coma
# el numero que guardamos en la variable
print("Jugadores en el grafo (nodos):", cantidad_jugadores)
print("Conexiones distintas entre jugadores (aristas):", cantidad_conexiones)
# "print()" con parentesis vacios deja un renglon en blanco
print()

print("Lista de jugadores:")
# "grafo_pases.nodes()" da todos los nodos y "sorted" los ordena alfabeticamente.
# "for jugador in" repite una vez por cada uno, guardandolo en "jugador"
for jugador in sorted(grafo_pases.nodes()):
    print(" -", jugador)

# PASO 5: PREPARAR EL TAMANO DE CADA CIRCULO

# "degree()" da el GRADO de cada nodo: con cuantos companeros distintos conecta
# un jugador (flechas que salen mas las que entran). "dict" lo guarda como
# diccionario, o sea parejas de "nombre: numero"
grados_por_jugador = dict(grafo_pases.degree())

# Los corchetes arman una lista. "for jugador in grafo_pases.nodes()" recorre
# jugador por jugador, "grados_por_jugador[jugador]" busca su grado y "* 70" lo
# agranda (si no, los circulos saldrian diminutos). Mas grado = mas grande
tamanos_de_nodos = [grados_por_jugador[jugador] * 70 for jugador in grafo_pases.nodes()]

# PASO 6: CALCULAR DONDE VA CADA JUGADOR

# "nx.spring_layout" inventa las posiciones con un modelo de resortes: trata
# cada arista como un resorte que jala, entonces los que se pasan mucho quedan
# cerca y los que casi no conectan quedan en la orilla.
#   "grafo_pases" es el grafo que acomoda
#   "seed=7" es la semilla del azar: hace que salga igual cada vez que corre
#   "k=1.5" es la separacion entre nodos, para que los nombres no se encimen
posiciones_de_nodos = nx.spring_layout(grafo_pases, seed=7, k=1.5)

# "plt.figure" crea el lienzo donde se dibuja. "figsize" es el tamano en
# pulgadas: 14 de ancho por 10 de alto
plt.figure(figsize=(14, 10))

# PASO 7: DIBUJAR LAS FLECHAS

# "draw" es dibujar y "edges" aristas: dibuja las flechas. Va primero para que
# queden por debajo de los circulos
nx.draw_networkx_edges(
    grafo_pases,              # que grafo dibujar
    posiciones_de_nodos,      # donde va cada jugador (lo del paso 6)
    edge_color="gray",        # "edge_color" = color de la flecha, "gray" gris
    alpha=0.4,                # "alpha" = transparencia (0 invisible, 1 solido)
    width=0.8,                # "width" = grosor de la linea
    arrowsize=14,             # "arrow" es flecha, "arrowsize" el tamano de la punta
    arrowstyle="-|>",         # "arrowstyle" = forma de la punta, aca triangulo.
                              # La punta muestra la direccion del pase
    connectionstyle="arc3,rad=0.12",
                              # "arc3" curva la flecha y "rad" es cuanto la curva.
                              # Si fueran rectas, el pase de ida y el de vuelta
                              # entre dos jugadores quedarian encimados
    node_size=tamanos_de_nodos,
                              # "node_size" le avisa el tamano del circulo para que
                              # la punta pare en la orilla y no se esconda debajo
)

# PASO 8: DIBUJAR LOS CIRCULOS

# "nodes" es nodos: dibuja un circulo por jugador
nx.draw_networkx_nodes(
    grafo_pases,                  # que grafo
    posiciones_de_nodos,          # donde va cada uno
    node_size=tamanos_de_nodos,   # "node_size" = tamano, el que armamos en el paso 5
    node_color="#f58282",         # "node_color" = color. El # y las letras son
                                  # codigo hexadecimal, aca un rojo claro
    alpha=0.9,                    # transparencia casi solida
)

# PASO 9: ESCRIBIR LOS NOMBRES

# "labels" es etiquetas: escribe el texto encima del nodo. Como el nodo YA es
# el nombre del jugador, lo agarra tal cual sin pasarle nada extra
nx.draw_networkx_labels(
    grafo_pases,
    posiciones_de_nodos,
    font_size=9,              # "font" es la letra, "font_size" su tamano
    font_weight="bold",       # "font_weight" = grosor de la letra, "bold" negrita
)

# PASO 10: GUARDAR LA IMAGEN

# "plt.title" pone el titulo arriba del dibujo: entre comillas el texto y
# "fontsize=14" el tamano de esa letra
plt.title("Croacia - Grafo de pases completados en fase de grupos (Qatar 2022)", fontsize=14)
# "axis" son los ejes X y Y y "off" los apaga. Los apagamos porque las
# posiciones las invento spring_layout, no son coordenadas reales de la cancha
plt.axis("off")
# "tight_layout" aprieta los margenes para que no se corte nada en la orilla
plt.tight_layout()
# "save" guardar y "fig" figura: guarda la imagen. Entre comillas el nombre del
# archivo que crea y "dpi=150" la calidad, que se ve bien proyectada
plt.savefig("grafo_croacia.png", dpi=150)
# "plt.show" abre la ventana para verlo. Va DESPUES de savefig: al reves
# matplotlib limpia el lienzo y guardaria una imagen en blanco
plt.show()
