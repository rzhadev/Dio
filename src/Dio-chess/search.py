import chess
import time
import sys
import os
from datetime import datetime
from datetime import timedelta
from evaluate import position_score


# negamax with alphabeta
# max(a,b) == -min(-a, -b)

'''
    iterative deepening loop
'''
def root(board, seconds=30):
    DEPTH = 1
    BESTSCORE = -float("inf")
    BESTMOVE = chess.Move.null()
    COLOR = board.turn  
    START = datetime.utcnow()
    TIME = timedelta(seconds=seconds)
    while datetime.utcnow() - START < TIME:
        for move in board.legal_moves:
            # autoset promotion to queen if its legal
            move.promotion = 5
            if not board.is_legal(move):
                move.promotion = None
            board.push(move)
            print(board)
            pos_score = negamax(board, -float("inf"), float("inf"), DEPTH, COLOR, START, TIME)
            board.pop()
            if pos_score > BESTSCORE:
                BESTSCORE = pos_score
                BESTMOVE = move
        print(f"CURR TIME   {datetime.utcnow() - START}")
        print(f"best move: {BESTMOVE}:{BESTSCORE}")
        print(f"depth {DEPTH}")
        DEPTH += 1
    return BESTMOVE

'''
    fail soft negamax search function
'''
def negamax(board, alpha, beta, depth, color, time_start, time_given):
    if depth == 0 or (datetime.utcnow() - time_start) >= time_given:
        return position_score(board, color)
    bestscore = -float("inf")
    for move in board.legal_moves:
        board.push(move)
        score = -negamax(board, -beta, -alpha, depth - 1, color, time_start, time_given)
        board.pop()
        if score >= beta:
            return score
        if score > bestscore:
            bestscore = score
            if score > alpha:
                alpha = score

    return bestscore

b = chess.Board()
print(root(b))