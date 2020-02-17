import chess
import time
import sys
import os
import math
from evaluate import static_eval
from evaluate import static_eval1

#negamax with alphabeta
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

def alphabeta(board, depth, alpha, beta, maxplayer):
    if depth == 0:
        return static_eval1(board)
    if maxplayer:
        score = -float("inf")
        for move in board.legal_moves:
            board.push(move)
            score = max(score, alphabeta(board, depth - 1, alpha, beta, False))
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
print(negamax(board, -float("inf"), float("inf"), 5))
end = time.time()
print(f'{end-start} seconds')
print(alphabeta(board, 5, -float("inf"), float("inf"), True))
end1 = time.time()
print(f'{end1-end} seconds')
