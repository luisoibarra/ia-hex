import heapq
import itertools
from math import log2
from random import random

from numpy import math
from tools import oo
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
        current_game = game.clone_play(*initial_position) if game[initial_position] == EMPTY else game.__clone__()
        current_game.turn = player_turn
        distance_from_initial[initial_position] = distance = 0 if game[initial_position] != EMPTY else 1
        father_node[initial_position] = game, None
        heap.push((distance + heuristic(game, initial_position), initial_position, random(), current_game)) # Saving (Score, Game, Action to get there, (X,Y))

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

def cubic_distance(x1,y1, x2,y2):
    s1 = -x1-y1 # Axial to Cubic coordinates
    s2 = -x2-y2
    distance = (abs(x1 - x2) + abs(y1 - y2) + abs(s1 - s2))/2
    return distance

def cubic_distance_heuristic(game: Game, play_made):
    x,y = play_made
    minim = oo
    for i in range(game.size):
        if game.turn == 1:
            position1 = game.size - 1
        else:
            position1 = i
        if game.turn == 0:
            position2 = game.size - 1
        else:
            position2 = i
        # return math.sqrt((x - position1) ** 2 + (y - position2) ** 2)
        distance = cubic_distance(x, y, position1, position2)
        minim = min(minim, distance)
    return minim

def rank(game: Game, player):

    path = a_star_hex(game, get_next_actions, initial_position(game, player), a_star_heuristic, a_start_goal)

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


def a_start_goal(game: Game):
    """
    A winner exists
    """
    return game.winner() != EMPTY


def a_star_heuristic(game:Game, position):
    distance = cubic_distance_heuristic(game, position)
    if game[position] == game.current():
        return distance - 1
    else:
        return distance


def initial_position(game:Game, player):
    
    def get_pos(i):
        return (i if player == WHITE else 0, i if player == BLACK else 0)

    return [get_pos(i) for i in range(game.size) if game[get_pos(i)] in [EMPTY, player]]

def get_next_actions(current_game: Game, action):
    next = set()
    # for i,j in [(i,j) for i,j in itertools.permutations(range(game.size), 2) if current_game[i,j] in [current_game.current(), EMPTY]]:
        # next.update(pos for pos in game.neighbour(i,j) if current_game[pos] == EMPTY)
    for i,j in [(i,j) for i,j in current_game.neighbour(*action) if current_game[i,j] in [current_game.current(), EMPTY]]:
        next.add((i,j))
    return next


def node_heuristic(current_game: Game, player):
    current_player_roots = [0,1] if player == WHITE else [2,3]
    connected_nodes = 0
    white = set()
    black = set()
    row_columns = set()
    for x in range(current_game.size):
        for y in range(current_game.size):
            item = current_game[x,y]
            if item != EMPTY:
                # How many nodes are connected to the edges
                if current_game.root(current_game.position(x,y)) in [current_game.root(z) for z in current_player_roots]:
                    connected_nodes += 1
                # How many columns or row are used
                if current_game[x,y] == player:
                    row_columns.add(y if player == WHITE else x)
                if item == WHITE:
                    white.add((x,y))
                else:
                    black.add((x,y))

    # Distance between nodes
    distance = 0
    for wx,wy in white:
        for bx,by in black:
            distance += cubic_distance(wx,wy,bx,by)

    # How much is left to win
    # nodes_left = 0
    # current_game = current_game.__clone__()
    # current_game.turn = (current_game.turn+1)%2
    # path = a_star_hex(current_game, get_next_actions, initial_position(current_game, player), cubic_distance_heuristic, a_start_goal)
    # for _,action in path:
    #     if current_game[action] == EMPTY:
    #         nodes_left += 1


    return connected_nodes + len(row_columns) + 1/distance# + log2(1/nodes_left)
