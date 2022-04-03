import heapq
import itertools
from random import random

from numpy import math
from game_logic import BLACK, WHITE, Game, EMPTY

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

def a_star_hex(game: Game, next_neighbours, initial_positions, heuristic, goal):
    heap = Heap()
    distance_from_initial = {} # G Function
    father_node = {}

    def make_path(current_game, action):
        path = []
        while action is not None:
            path.insert(0, (current_game, action))
            current_game, action = father_node[action]
        return path

    player_turn = game.turn
    
    for initial_position in initial_positions:
        current_game = game.clone_play(*initial_position)
        current_game.turn = player_turn
        distance_from_initial[initial_position] = 0
        father_node[initial_position] = game, None
        heap.push((heuristic(game, initial_position), initial_position, random(), current_game)) # Saving (Score, Game, Action to get there, (X,Y))

    while heap:
        cost, action, _, current_game = heap.pop()
        
        if goal(current_game):
            return make_path(current_game, action)
        
        # All states in the search space are different
        for x,y in next_neighbours(game, action):
            if (x,y) in distance_from_initial:
                continue
            if current_game[x,y] == EMPTY:
                next_game = current_game.clone_play(x,y)
            else:
                next_game = current_game.__clone__()
            next_game.turn = player_turn
            eval_distance = distance_from_initial[action] + 1
            distance_from_initial[(x,y)] = eval_distance + 1
            father_node[(x,y)] = current_game, action 
            eval_heuristic = heuristic(game, (x,y))
            heap.push((eval_distance + eval_heuristic, (x,y), random(), next_game)) # Max Heap
        
    return

def euclidean_heuristic(game: Game, play_made):
    x,y = play_made
    position1, position2 = game.size - 1 if game.turn == 1 else x, game.size - 1 if game.turn == 0 else y 
    return math.sqrt((x - position1) ** 2 + (y - position2) ** 2)

def rank(game: Game, player):

    def goal(game: Game):
        """
        A winner exists
        """
        return game.winner() != EMPTY

    def heuristic(game:Game, position):
        if game[position] == game.current():
            return 0
        else:
            return euclidean_heuristic(game, position)

    def get_next_actions(current_game: Game, action):
        next = set()
        # for i,j in [(i,j) for i,j in itertools.permutations(range(game.size), 2) if current_game[i,j] in [current_game.current(), EMPTY]]:
            # next.update(pos for pos in game.neighbour(i,j) if current_game[pos] == EMPTY)
        for i,j in [(i,j) for i,j in current_game.neighbour(*action) if current_game[i,j] in [current_game.current(), EMPTY]]:
            next.add((i,j))
        return next

    def get_pos(i):
        return (i if player == WHITE else 0, i if player == BLACK else 0)

    path = a_star_hex(game, get_next_actions, [get_pos(i) for i in range(game.size) if game[get_pos(i)] == EMPTY], heuristic, goal)

    def action_weight(action):
        x,y = action
        after_game_current = game.clone_play(x,y)
        # new_game = game.__clone__()
        # new_game.turn = (new_game.turn + 1) % 2
        # after_game_enemy = game.clone_play(x,y)
        if after_game_current.winner() == player:
            return 1000
        elif after_game_current.winner() != EMPTY:
            return -1000
        # TODO Add Node heuristic here
        return node_heuristic(after_game_current, player)
    
    actions_to_take = []

    for _, action in path:
        if game[action] == EMPTY:
            weight = action_weight(action)
            actions_to_take.append((-weight, action))
    
    actions_to_take.sort()

    return [y for _,y in actions_to_take]

def node_heuristic(current_game: Game, player):
    current_player_roots = [0,1] if player == WHITE else [2,3]
    value = 0
    row_columns = set()
    for x in range(current_game.size):
        for y in range(current_game.size):
            if current_game[x,y] != EMPTY:
                # How many nodes are connected to the edges
                if current_game.root(current_game.position(x,y)) in [current_game.root(z) for z in current_player_roots]:
                    value += 1
                # How many columns or row are used
                if current_game[x,y] == player:
                    row_columns.add(y if player == WHITE else x)
    return value + len(row_columns)
