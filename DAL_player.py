# Player Template
# IMPORTANT: 	This module must have a function called play
# 				that receives a game and return a tuple of
#				two integers who represent a valid move on
#				the game.

from DAL_utils import closest_path_heuristic, node_heuristic, rank
from game_logic import *
from DAL_minimax import minimax, alpha_beta

# game_logic
#
# 	EMPTY		
#	PLAYER[0]	
#	PLAYER[1]

# game
# 	-> current (W or B)
#		It refers to the player who must play in
#		this turn.
#	-> indexing
#		game[i,j] return the player who have played
#		on position <i;j> (compare with PLAYER[0] 
#		and PLAYER[1]). EMPTY if none player have
#		played there.
#	-> neighbour
#		creates an iterator that yields all 
#		coordinates <x;y> who are neighbour of 
#		current coordinates.
#
#		for nx, ny in game.neighbour(x, y):
#			print(nx, ny)


def play(game, player):
	# Code Here
	return alpha_beta(game, player, 3, heuristic, moves)
	# return alpha_beta(game, player, 3, heuristic, ranked_moves)


def moves(game, player):
	for x in range(game.size):
		for y in range(game.size):
			if game[x, y] == EMPTY:
				yield (x, y)

def ranked_moves(game, player):
	moves = rank(game, player)
	return moves[:8]

def heuristic(game, player):
	# Code Here
	# return node_heuristic(game, player)
	return closest_path_heuristic(game, player)


