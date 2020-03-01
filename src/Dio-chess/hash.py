import numpy as np
import chess

PIECES = 12
SQUARES = 64
PIECE_INDEX = {'P':0, 'N':1, 'B':2,'R':3, 'Q':4, 'K':5, 'p':6, 'n':7, 'b':8, 'r':9, 'q':10, 'k':11}

# zobrist hashing for transposition table look up
# could maybe add in turn/castling/ep 

def initZobrist():
    zobrist = np.zeros((PIECES, SQUARES), dtype=np.uint64) 
    for i in range(SQUARES):
        for j in range(PIECES):
            zobrist[j][i] = np.random.randint(1, 2**64-1, dtype=np.uint64)

    return zobrist

def calculateHash(board : chess.Board, zobrist):
    hashval = np.uint64(0)   
    for i in range(SQUARES):
        if board.piece_at(i) is not None:
            piece = PIECE_INDEX[board.piece_at(i).symbol()]
            hashval = np.bitwise_xor(hashval, zobrist[piece][i])
    return hashval

# apply a move to the current hash key of the board, undo a move from applying again
def applyHash(hash_value, zobrist, from_piece : chess.Piece, from_square, to_piece : chess.Piece, to_square):
    # capture move
    if to_piece is not None:
        piece1 = PIECE_INDEX[from_piece.symbol()]
        piece2 = PIECE_INDEX[to_piece.symbol()]
        hash_value = np.bitwise_xor(hash_value, zobrist[piece1][to_square])
        hash_value = np.bitwise_xor(hash_value, zobrist[piece2][to_square])
        hash_value = np.bitwise_xor(hash_value, zobrist[piece1][from_square])
    else:
        piece = PIECE_INDEX[from_piece.symbol()]
        hash_value = np.bitwise_xor(hash_value, zobrist[piece][from_square])
        hash_value = np.bitwise_xor(hash_value, zobrist[piece][to_square])

    return hash_value
        
