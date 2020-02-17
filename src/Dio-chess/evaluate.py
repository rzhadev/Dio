import chess
# centipawn scale
POINT_VAL = {
    1: 100,  # pawn
    2: 350,  # knight
    3: 350,  # bishop
    4: 525,  # rook
    5: 1000,  # queen
    6: 20000  # king
}

# reverse() gives white perspective
PIECE_TABLES = {
    # PAWN TABLE
    1: [[0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5,  5, 10, 25, 25, 10,  5,  5],
        [0,  0,  0, 20, 20,  0,  0,  0],
        [5, -5, -10,  0,  0, -10, -5,  5],
        [5, 10, 10, -20, -20, 10, 10,  5],
        [0,  0,  0,  0,  0,  0,  0,  0]],
    # KNIGHT TABLE
    2: [[-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20,  0,  0,  0,  0, -20, -40],
        [-30,  0, 10, 15, 15, 10,  0, -30],
        [-30,  5, 15, 20, 20, 15,  5, -30],
        [-30,  0, 15, 20, 20, 15,  0, -30],
        [-30,  5, 10, 15, 15, 10,  5, -30],
        [-40, -20,  0,  5,  5,  0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]],
    # BISHOP TABLE
    3: [[-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,  0,  0,  0,  0,  0,  0, -10],
        [-10,  0,  5, 10, 10,  5,  0, -10],
        [-10,  5,  5, 10, 10,  5,  5, -10],
        [-10,  0, 10, 10, 10, 10,  0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10,  5,  0,  0,  0,  0,  5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]],
    # ROOK TABLE
    4: [[0,  0,  0,  0,  0,  0,  0,  0],
        [5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [0,  0,  0,  5,  5,  0,  0,  0]],
    # QUEEN TABLE
    5: [[-20, -10, -10, -5, -5, -10, -10, -20],
        [-10,  0,  0,  0,  0,  0,  0, -10],
        [-10,  0,  5,  5,  5,  5,  0, -10],
        [-5,  0,  5,  5,  5,  5,  0, -5],
        [0,  0,  5,  5,  5,  5,  0, -5],
        [-10,  5,  5,  5,  5,  5,  0, -10],
        [-10,  0,  5,  0,  0,  0,  0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]],
    # KING TABLE
    6: [[-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, 20,  0,  0,  0,  0, 20, 20],
        [20, 30, 10,  0,  0, 10, 30, 20]],
    # KINGLATE TABLE
    7: [[-50, -40, -30, -20, -20, -30, -40, -50],
        [-30, -20, -10,  0,  0, -10, -20, -30],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-30, -10, 30, 40, 40, 30, -10, -30],
        [-30, -10, 30, 40, 40, 30, -10, -30],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-30, -30,  0,  0,  0,  0, -30, -30],
        [-50, -30, -30, -30, -30, -30, -30, -50]]
}


def static_eval(board: chess.Board):
    value_sum = 0
    for pos, piece in board.piece_map().items():
        pos_file = chess.square_file(pos)
        pos_rank = chess.square_rank(pos)
        perspective = 1 if piece.color else -1
        value_sum += POINT_VAL[piece.piece_type] * perspective
        value_sum += list(reversed(PIECE_TABLES[piece.piece_type]))[pos_rank][pos_file] if piece.color else PIECE_TABLES[piece.piece_type][pos_rank][pos_file] * perspective  # noqa
    return value_sum * (1 if board.turn else -1)

def static_eval1(board: chess.Board):
    value_sum = 0
    for pos, piece in board.piece_map().items():
        pos_file = chess.square_file(pos)
        pos_rank = chess.square_rank(pos)
        perspective = 1 if piece.color else -1
        value_sum += POINT_VAL[piece.piece_type] * perspective
        value_sum += list(reversed(PIECE_TABLES[piece.piece_type]))[pos_rank][pos_file] if piece.color else PIECE_TABLES[piece.piece_type][pos_rank][pos_file] * perspective  # noqa
    return value_sum