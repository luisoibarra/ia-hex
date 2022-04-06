# DAL Team
- Luis Ernesto Ibarra C511
- Luis Enrique Dalmau C511
- Abel Cruz C511

## Problema

Se tiene un tablero hexagonal de NxN en el cual juegan dos jugadores poniendo una ficha blanca o negra en dependencia del jugador al que le toque, gana el jugador que primero logre hacer un camino que conecte los laterales (Blanco) o la parte superior con la inferior (Negro)


## Modelación

Para modelar el problema se representa un juego como un grafo en el que los estados en los que puede estar el juego son los nodos y las aristas las posibles jugadas a realizar en dicho estado. Un estado es las posiciones de las fichas en el tablero y el turno en el cual se encuentra el juego. Las aristas entre estos nodos se representan mediante tuplas de dos elementos que representan dónde el jugador va a poner la ficha. 

Dada las definiciones anteriores un camino en el grafo representa un posible juego realizado por jugadores, si este camino parte desde el estado inicial y llega hasta un nodo terminal es considerado un posible juego completo.

Para este problema un jugador se considera una función que dado un estado del juego devuelve la acción a realizar por este.

## Implementación

En la implementación del jugador se realizó una implementación de la poda alpha-beta, la cual reduce significativamente el tiempo de decisión de la jugada en comparación con el minimax clásico.

Se realizó una búsqueda A* con heurística de distancia en coordenadas cúbicas la cual es usada para calcular eficientemente el camino hacia la meta.

### Heurística

**Variante Luiso (Inicial)**

La heurística implementada consiste en una combinación lineal de tres ideas escenciales, estas tratan de cubrir los defectos entre ellas para poder tener una que estime mejor el estado del tablero.

Para la explicación se asumirá que el jugador a maximizar es el blanco, lo que significa que su objetivo es conectar los laterales.

- Cantidad de nodos en las componentes conexas laterales (h1): Esta heurística cuenta los nodos conectados a los laterales, mientras más nodos estén conectados a estos mejor la puntuación. Esta heurística tiene como inconveniente que las jugadas en vertical sobre una columna ya tomada puntúa igual que una jugada que disminuya la distancia entre los laterales
- Cantidad de columnas ocupadas (h2): Esta heurística cuenta la cantidad de columnas ocupadas, es un poderoso criterio si se combina con h1 ya que el defecto de esta es que no garantiza la conexidad, lo cual es garantizado por h1.
- Nodos faltantes para ganar (h3): Esta heurística calcula el camino por donde se tienen que poner menos nodos para ganar y devuelve esta cantidad, se usa principalemnte para desambiguar en algunos casos sobre donde poner nodos en tomando en cuenta solamente h1 y h2. La implementación de esta usa A*.
- Distancia entre nodos blancos y negros (h4): Esta heurística calcula la distancia entre todos los elementos blancos con todos los elementos negros. Se usa para elegir jugadas que acerquen o alejen de los nodos adversarios para entorpecer sus movimientos o dar más libertad de movimiento al jugador que la hizo.

## Resultados

### Heurística rush_player:

La heurística formada por h1 + h2 vence sin problemas al rush_player y al random player tiene una probabilidad de 3.5/8 de ganarle.

### Heurística random_player:

La heurística formada por h1 + h2 + 1/h4 es vencida por el rush_player cuando el jugador implementado comienza jugando, pero es la más efectiva encontrada contra el random_player ganando 7/8 aproximadamente. 

### Heurística mejor camino

Esta heurística está formada por 1/h3, para potenciar la cantidad menor de nodos. Esta heurística aunque se demora un poco más que las anteriores logra vences al rush_player siempre y al random_player le gana con una probabilidad de 7/8, igualando la heurística de mejor rendimiento contra este.