# Proyecto de Grafos - Estilo de Juego (Croacia, Qatar 2022)

Proyecto para la clase de Análisis y Diseño de Algoritmos, a cargo del
catedrático Luis Angel Tórtola y el auxiliar Christian Barrios.

El objetivo es construir un grafo que represente cómo circuló el balón
entre los jugadores de Croacia durante la fase de grupos del Mundial
Qatar 2022, y a partir de ese grafo interpretar el estilo de juego del
equipo. Lo más importante del proyecto no es el código en sí, sino la
lectura futbolística que se pueda armar a partir de los resultados.

## Los datos

El archivo `datos_croacia/pases_croacia.csv` trae el detalle de todos los
pases de Croacia en el Mundial completo: 7 partidos en total (fase de
grupos, octavos de final, cuartos de final, semifinal y el partido por el
tercer lugar, que Croacia terminó ganando).

Columnas más relevantes del csv:

- `fase`: ronda del partido. Solo se usan los registros donde vale
  `"Group Stage"`.
- `oponente`: rival de ese partido (Bélgica, Canadá o Marruecos en fase
  de grupos).
- `jugador_nombre` / `receptor_nombre`: quién da el pase y quién lo
  recibe.
- `resultado`: si el pase fue `Complete` o `Incomplete` (también existen
  otros valores raros como `Out`, `Pass Offside`, `Unknown`, que no se
  usan).
- Hay otras columnas (`longitud_pase`, `minuto`, coordenadas `inicio_x`,
  `inicio_y`, `fin_x`, `fin_y`, etc.) que el csv trae pero que este
  proyecto no utiliza, porque no hacen falta para el grafo que se decidió
  construir.

Para este proyecto solo se usan los 3 partidos de fase de grupos (contra
Bélgica, Canadá y Marruecos), que en total suman 1802 pases, de los
cuales 1502 fueron completados.

## Estructura del proyecto

- `datos_croacia/pases_croacia.csv` - dataset original, tal cual se
  recibió, sin modificar.
- `limpieza.py` - primer script del flujo. Se encarga de:
  1. Cargar el csv completo.
  2. Quedarse solo con los partidos de fase de grupos.
  3. Descartar las columnas que no se necesitan, dejando solo
     `jugador_nombre`, `receptor_nombre` y `resultado`.
  4. Quedarse solo con los pases marcados como `Complete`.
  5. Guardar ese resultado en `pases_limpios.csv`.
- `pases_limpios.csv` - salida de `limpieza.py`. Es el archivo que usa
  `grafo.py` para no tener que repetir la limpieza cada vez.
- `grafo.py` - segundo script del flujo. Lee `pases_limpios.csv`,
  construye el grafo con NetworkX, imprime en consola un resumen (número
  de jugadores, número de conexiones y la lista de jugadores) y genera la
  visualización con Matplotlib, guardándola como `grafo_croacia.png`.
- `grafo_croacia.png` - imagen ya generada del grafo, lista para usar en
  la presentación en clase.

## Decisiones sobre el grafo

El enunciado pide justificar varias decisiones de diseño del grafo; estas
son las que se tomaron y por qué:

- **Dirigido**: un pase tiene dirección, sale de un jugador y llega a
  otro. Nos interesa poder distinguir quién reparte juego (muchas
  salidas) de quién principalmente recibe (muchas entradas), algo que se
  perdería con un grafo no dirigido.
- **Sin peso**: una flecha de A hacia B simplemente significa que A le
  completó al menos un pase a B en la fase de grupos. No se usa la
  cantidad de pases ni la longitud como peso; lo que interesa para leer
  el estilo de juego es la estructura de la red (con cuántos compañeros
  distintos conecta cada jugador), no el volumen exacto de pases entre
  cada par.
- **Un solo grafo consolidado**: en vez de armar un grafo por partido, se
  juntan los 3 partidos de fase de grupos en un único grafo. Esto da una
  visión general del estilo de juego del equipo en todo el grupo, en
  lugar de tres lecturas separadas por rival.
- **Solo pases completados**: un pase incompleto no llega a conectar
  realmente a los dos jugadores en la cancha (el balón no llegó), así que
  no se considera como una arista del grafo. Solo se toman los pases con
  `resultado == "Complete"`.
- **Nodos con nombre, no con id**: aunque el csv trae un `jugador_id`
  numérico, se usa `jugador_nombre` como nodo para que el grafo se pueda
  leer directamente al mostrarlo, sin tener que cruzar contra una tabla
  de nombres.
- **Tamaño de nodo según su grado**: en la visualización, el tamaño del
  círculo de cada jugador es proporcional a su grado (con cuántos
  compañeros distintos tiene conexión, sumando las flechas que salen y
  las que entran). Mientras más conectado está un jugador en la red, más
  grande se ve.

## Cómo correrlo

Requiere Python 3 con las librerías `pandas`, `networkx` y `matplotlib`
instaladas (`pip install pandas networkx matplotlib`).

```
python3 limpieza.py
python3 grafo.py
```

El primer script lee `datos_croacia/pases_croacia.csv` y genera
`pases_limpios.csv`. El segundo lee ese archivo, construye el grafo,
imprime el resumen en la terminal y guarda la imagen final en
`grafo_croacia.png`.

## Próximos pasos

Falta la parte más importante del proyecto: la interpretación futbolística
del grafo (quiénes son los jugadores más conectados, qué dice eso del
estilo de juego de Croacia en la fase de grupos, etc.), que se preparará
de cara a la presentación en clase.
