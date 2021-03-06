# -*- coding: utf8 -*-

__author__ = 'Suilan Estévez Velarde'

from tools import oo
from game_logic import *

def minimax(game, player, depth, h, moves):
    """Retorna el mejor tablero para el jugador
    correspondiente
    """
    best, value = maxplay(game, None, player, depth, h, moves)
    return best

def maxplay(game, play, player, depth, h, moves):
    """Retorna la mejor jugada tablero para el jugador"""
    best = None
    best_value = -oo

    if game.winner() != EMPTY:
        return play, 1 if game.winner() == player else -1

    if not depth:
        return play, h(game, player)

    for x,y in moves(game, player):
        b, value = minplay(game.clone_play(x,y), (x,y), player, depth - 1, h, moves)

        if value > best_value:
            best = (x,y)
            best_value = value

    return best, best_value

def minplay(game, play, player, depth, h, moves):
    """Retorna la mejor jugada para el jugador contrario"""
    best = None
    best_value = oo

    if game.winner() != EMPTY:
        return play, 1 if game.winner() != player else 0

    if not depth:
        return play, h(game, player)

    for x,y in moves(game, player):
        _, value = maxplay(game.clone_play(x,y), (x,y), player, depth - 1, h, moves)

        if value < best_value:
            best = (x,y)
            best_value = value

    return best, best_value


# ALPHA-BETA

def alpha_beta(game, player, depth, h, moves):
    """Retorna el mejor tablero para el jugador
    correspondiente
    """
    best, value = maxplay_alpha_beta(game, None, player, depth, h, moves, -oo, oo)
    return best

def maxplay_alpha_beta(game, play, player, depth, h, moves, alpha, beta):
    """Retorna la mejor jugada tablero para el jugador"""
    best = None
    best_value = -oo

    if game.winner() != EMPTY:
        return play, 1 if game.winner() == player else -1

    if not depth:
        return play, h(game, player)

    for x,y in moves(game, player):
        _, value = minplay_alpha_beta(game.clone_play(x,y), (x,y), player, depth - 1, h, moves, alpha, beta)

        if value > best_value:
            best = (x,y)
            best_value = value
            alpha = max(alpha, best_value)
        if best_value >= beta:
            return best, best_value

    return best, best_value

def minplay_alpha_beta(game, play, player, depth, h, moves, alpha, beta):
    """Retorna la mejor jugada para el jugador contrario"""
    best = None
    best_value = oo

    if game.winner() != EMPTY:
        return play, 1 if game.winner() != player else 0

    if not depth:
        return play, h(game, player)

    for x,y in moves(game, player):
        _, value = maxplay_alpha_beta(game.clone_play(x,y), (x,y), player, depth - 1, h, moves, alpha, beta)

        if value < best_value:
            best = (x,y)
            best_value = value
            beta = min(beta, best_value)
        if best_value <= alpha:
            return best, best_value


    return best, best_value