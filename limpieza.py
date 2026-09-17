# "import" trae una libreria ya hecha, "pandas" maneja csv como tabla,
# "as pd" le pone apodo para escribir pd en vez de pandas
import pandas as pd

# "df" viene de dataframe (marco de datos), asi le dice pandas a su tabla.
# "pd.read_csv" abre el csv, entre parentesis la ruta del archivo
df = pd.read_csv("datos_croacia/pases_croacia.csv")

# "df["fase"] == "Group Stage"" pregunta fila por fila si es fase de grupos.
# El "df[...]" de afuera se queda solo con las que dieron Verdadero
df = df[df["fase"] == "Group Stage"]

# Los corchetes dobles [[ ]] son una lista de COLUMNAS a conservar.
# El csv trae muchas mas (minuto, coordenadas), pero solo usamos estas 3
df = df[["jugador_nombre", "receptor_nombre", "resultado"]]

# Mismo filtro pero con la columna resultado: solo los "Complete".
# Un pase fallado no conecta a nadie porque el balon nunca llego
df = df[df["resultado"] == "Complete"]

# "to_csv" guarda la tabla en un archivo nuevo ("to" es hacia).
# "index=False" evita escribir la numeracion de filas que pandas pone sola
df.to_csv("pases_limpios.csv", index=False)

# La "f" antes de las comillas deja meter valores entre llaves { }.
# "len(df)" cuenta las filas que quedaron: 1502 pases completados
print(f"Pases completados en fase de grupos: {len(df)}")
