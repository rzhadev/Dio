import chess
import time
import sys
import os
import math
from evaluate import static_eval


def root(board, depth, maxplayer):
    bestscore = -float("inf")
    bestmove = None
    for move in board.legal_moves:
        board.push(move)
        score = alphabeta(board, depth - 1, -float("inf"), float("inf"), False)
        board.pop()
        if score > bestscore:
            bestscore = score
            bestmove = move
    return bestmove


def alphabeta(board, depth, alpha, beta, maxplayer):
    if depth == 0:
        return static_eval(board)
    bmove = None
    if maxplayer:
        score = -float("inf")
        for move in board.legal_moves:
            board.push(move)
            score = max(score, alphabeta(board, depth-1, alpha, beta, False))
            board.pop()
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return score
    else:
        score = float("inf")
        for move in board.legal_moves:
            board.push(move)
            score = min(score, alphabeta(board, depth-1, alpha, beta, True))
            board.pop()
            beta = min(beta, score)
            if alpha >= beta:
                break
        return score


start = time.time()
board = chess.Board()
print(root(board, 5, True))
end = time.time()
print(f'{end-start} seconds')
