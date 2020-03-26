import chess
import sys
from datetime import datetime
from datetime import timedelta
from evaluate import position_score
from hash import apply_hash
from chess.polyglot import zobrist_hash
from ttable import TTable, Entry
from util import perft

# negamax with alphabeta
# max(a,b) == -min(-a, -b)

'''
    iterative deepening loop
'''


def root(board, key, seconds=5):
    DEPTH = 1
    BESTSCORE = -float("inf")
    BESTMOVE = chess.Move.null()
    COLOR = board.turn
    START = datetime.utcnow()
    TIME = timedelta(seconds=seconds)
    global ttable
    while datetime.utcnow() - START < TIME:
        for move in board.legal_moves:
            # autoset promotion to queen if its legal
            move.promotion = 5
            if not board.is_legal(move):
                move.promotion = None
            key = apply_hash(key, board, move)
            board.push(move)
            # print(board)

            pos_score = negamax(board, -float("inf"),
                                float("inf"), DEPTH, COLOR, START, TIME, key)

            board.pop()
            key = apply_hash(key, board, move)
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


def negamax(board, alpha, beta, depth, color, time_start, time_given, key):
    global ttable

    if depth == 0 or (datetime.utcnow() - time_start) >= time_given:
        return position_score(board, color)
    bestscore = -float("inf")
    for move in board.legal_moves:
        key = apply_hash(key, board, move)
        board.push(move)

        score = -negamax(board, -beta, -alpha, depth - 1,
                         color, time_start, time_given, key)

        board.pop()
        key = apply_hash(key, board, move)
        if score >= beta:
            return score
        if score > bestscore:
            bestscore = score
            if score > alpha:
                alpha = score

    return bestscore


POSITIONS = 0
ttable = TTable()
b = chess.Board()
key = zobrist_hash(b)
print(key)
print(root(b, key=key))
