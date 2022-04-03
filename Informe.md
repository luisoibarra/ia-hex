# DAL Team
- Luis Ernesto Ibarra C511
- Luis Enrique Dalmau C511
- Abel Cruz C511

## Problema

Se tiene un tablero hexagonal de NxN en el cual juegan dos jugadores poniendo una ficha blanca o negra en dependencia del jugador al que le toque, gana el jugador que primero logre hacer un camino que conecte los laterales (Blanco) o la parte superior con la inferior (Negro)


## Modelación

Para modelar el problema se representan los diferentes estados en los que puede estar el juego como nodos. Un estado es las posiciones de las fichas en el tablero y el turno en el cual se encuentra el juego. Para manejar las jugadas en el juego las aristas entre estos nodos representan las posibles jugadas a realizar por el jugador correspondiente. Estas jugadas se presentan como una tupla en la que se especifica el lugar en donde se va a poner la ficha del jugador correspondiente. 

Dada las definiciones anteriores un camino en el árbol representa un posible juego realizado por jugadores, si este camino parte desde el estado inicial y llega hasta un nodo final es considerado un posible juego completo.

Para este problema un jugador se considera una función que dado un estado del juego devuelve la acción a realizar por este. 

## Implementación

En la implementación del jugador se realizó una implementación de la poda alpha-beta, la cual reduce significativamente el tiempo de decisión de la jugada en comparación con el minimax clásico.

### Heurística

**Variante Luiso (Inicial)**

La heuristica tiene en cuenta maximizar la cantidad de nodos en las componentes conexas que unen la parte izquierda/arriba con la parte derecha/abajo. Esta condición por si sola no contribuye a un jugador bueno ya que solo con este criterio el jugador ve con igual peso una jugada en la cual no se avance hacia el objetivo sino que se juegue hacia arriba-abajo/laterales. Para mitigar lo anterior se agregó otro factor a la heurística el cual es cantidad de columnas/filas ocupadas por el jugador. Con este cambio las jugadas que no avanzan hacia acercarse ahora se ven opacadas por las que lo hacen.

Se tiene como función final (Asumiendo que juegan las blancas):

CantDeNodosEnComponenteConexaIzquierda + CantDeNodosEnComponenteConexaDerecha + CantDeColumnasTomadas
