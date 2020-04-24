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


def root(board, key, seconds=30):
    DEPTH = 1
    BESTSCORE = -float("inf")
    BESTMOVE = chess.Move.null()
    COLOR = board.turn
    START = datetime.utcnow()
    TIME = timedelta(seconds=seconds)
    global ttable
    while datetime.utcnow() - START < TIME:
        print(f"depth {DEPTH}")
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
        DEPTH += 1
    return BESTMOVE


'''
    fail soft negamax search function
'''


def negamax(board, alpha, beta, depth, color, time_start, time_given, key):
    global ttable
    alphaorig = alpha
    keyorig = key
    entry = ttable.probe(key)
    if (entry is not None) and entry.depth >= depth:
        if entry.flag == 'exact':
            return entry.evaluation
        elif entry.flag == 'lower':
            alpha = max(entry.evaluation, alpha)
        elif entry.flag == 'upper':
            beta = min(entry.evaluation, beta)

        if alpha >= beta:
            return entry.evaluation

    if depth == 0 or (datetime.utcnow() - time_start) >= time_given or board.is_game_over():  # noqa
        return position_score(board, color)
    bestscore = -float("inf")
    moves = board.legal_moves
    # order moves
    for move in moves:
        key = apply_hash(key, board, move)
        board.push(move)

        score = -negamax(board, -beta, -alpha, depth - 1,
                         color, time_start, time_given, key)

        board.pop()
        key = apply_hash(key, board, move)
        # max(score, beta)

        if score >= beta:
            return score
        if score > bestscore:
            bestscore = score
            if score > alpha:
                alpha = score

    flag = ''
    if bestscore <= alphaorig:
        flag = 'upper'
    elif bestscore >= beta:
        flag = 'lower'
    else:
        flag = 'exact'

    ttable.insert(keyorig, depth, bestscore, flag)

    return bestscore


ttable = TTable()
b = chess.Board()
while True:
    key = zobrist_hash(b)
    print(b)
    qmove = input('move input:')
    move = chess.Move.from_uci(qmove)
    b.push(move)
    cmove = root(b, key=key)
    b.push(cmove)



'''
for k, v in ttable.table.items():
    print(f'{k},{v.evaluation}')
'''