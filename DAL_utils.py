import heapq

from numpy import math
from game_logic import Game, EMPTY

class Heap:

    def __init__(self) -> None:
        self.__heap = []

    def push(self, item):
        heapq.heappush(self.__heap, item)

    def pop(self):
        return heapq.heappop(self.__heap)

    def __len__(self):
        return len(self.__heap)

    def __iter__(self):
        return iter(self.__heap)

    def __bool__(self):
        return bool(self.__heap)

def a_star_hex(game: Game, inital_position, heuristic, goal):
    heap = Heap()
    distance_from_initial = {} # G Function
    father_node = {}

    def make_path(current_game, action):
        path = []
        while current_game is not None:
            path.insert(0, (current_game, action))
            current_game, action = father_node[str(current_game)]
        return path

    distance_from_initial[str(game)] = 0 # Game string representation is the key
    father_node[str(game)] = None, None
    player_turn = game.turn
    
    heap.push((heuristic(game), game, inital_position)) # Saving (Score, Game, Action to get there, (X,Y))

    while heap:
        cost, current_game, action = heap.pop()
        
        if goal(current_game):
            make_path(current_game, action)
        
        # All states in the search space are different
        for x,y in [pos for pos in current_game.neighbour(*action) if current_game[pos] == EMPTY]:
            next_game = current_game.clone_play(x,y)
            next_game.turn = player_turn # Initial player keeps playing
            eval_distance = distance_from_initial[str(current_game)] + 1
            eval_heuristic = heuristic(next_game, (x,y))
            heap.push((eval_distance + eval_heuristic, next_game, (x,y)))
        
def euclidean_heuristic(game: Game, jugada):
    x,y = jugada
    # TODO ver bien si la posicion esta bien
    position1, position2 = game.size - 1 if game.turn == 0 else x, game.size - 1 if game.turn == 1 else y 
    return math.sqrt((x - position1) ** 2 + (y - position2) ** 2)


