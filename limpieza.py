import pandas as pd

# Cargamos el csv con todos los pases de Croacia en todo el Mundial
# (incluye fase de grupos, octavos, cuartos, semis y final)
df = pd.read_csv("datos_croacia/pases_croacia.csv")

# El proyecto pide usar únicamente los 3 partidos de fase de grupos,
# el resto de rondas (Round of 16, Quarter-finals, etc.) se descarta
df = df[df["fase"] == "Group Stage"]

# De todas las columnas del csv, para el grafo solo necesitamos
# quién dio el pase, quién lo recibió y si se completó o no
df = df[["jugador_nombre", "receptor_nombre", "resultado"]]

# Nos quedamos solo con los pases completados: son los que representan
# la circulación real del balón entre jugadores (un pase incompleto
# no conecta a los dos jugadores en la cancha)
df = df[df["resultado"] == "Complete"]

# Guardamos el resultado ya limpio para que el script del grafo
# lo use directamente sin repetir este proceso
df.to_csv("pases_limpios.csv", index=False)
print(f"Pases completados en fase de grupos: {len(df)}")
