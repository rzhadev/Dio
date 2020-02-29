import chess
import time
import sys
import os
import math
from evaluate import static_eval

# negamax with alphabeta
# max(a,b) == -min(-a, -b)

# fail hard negamax


def root(board, depth):
    bestscore = -float("inf")
    bestmove = None
    for move in board.legal_moves:
        board.push(move)
        score = negamax(board, -float("inf"), float("inf"), depth)
        board.pop()
        print(f"{move}:{score}")
        if score > bestscore:
            bestscore = score
            bestmove = move
    return bestmove


def negamax(board, alpha, beta, depth):
    if depth == 0:
        return static_eval(board)
    bestscore = -float("inf")
    for move in board.legal_moves:
        board.push(move)
        score = -negamax(board, -beta, -alpha, depth - 1)
        board.pop()
        if score >= beta:
            return score
        if score > bestscore:
            bestscore = score
            if score > alpha:
                alpha = score

    return bestscore


start = time.time()
b = chess.Board()
s = root(b, 4)
print(s)
end = time.time()
print(f"{end-start} sec")


