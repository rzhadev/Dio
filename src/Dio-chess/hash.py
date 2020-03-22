from chess.polyglot import zobrist_hash, POLYGLOT_RANDOM_ARRAY
import chess
import typing


Z_ARR = POLYGLOT_RANDOM_ARRAY

# apply an xor to the current hashkey based on a move
# needs to be applied before the board.push and after the board.pop (queries the board positions)
def applyHash(key, board, move : chess.Move):
    pivot = 1 if board.piece_at(move.from_square).color else 0
    
    from_square = move.from_square  
    from_piece_type = board.piece_type_at(move.from_square)
    fpiece_index = (typing.cast(chess.PieceType, from_piece_type) - 1) * 2 + pivot
    to_square = move.to_square

    # move the piece at the source square
    key ^= Z_ARR[64 * fpiece_index + from_square]
    key ^= Z_ARR[64 * fpiece_index + to_square]
            
    # update castling rights
    if (from_piece_type == chess.KING):
        # castling move
        if(chess.square_distance(from_square, to_square) > 1):
            rook_index = (typing.cast(chess.PieceType, chess.ROOK) - 1) * 2 + pivot

            # queenside
            if(to_square == chess.C1 or to_square == chess.C8):
                if(board.turn):
                    key ^= Z_ARR[64 * rook_index + chess.A1]
                    key ^= Z_ARR[64 * rook_index + chess.D1]
                    key ^= Z_ARR[769]
                else:
                    key ^= Z_ARR[64 * rook_index + chess.A8]
                    key ^= Z_ARR[64 * rook_index + chess.D8]
                    key ^= Z_ARR[771]

            # kingside
            elif(to_square == chess.G1 or to_square == chess.G8):
                if(board.turn):
                    key ^= Z_ARR[64 * rook_index + chess.H1]
                    key ^= Z_ARR[64 * rook_index + chess.F1]
                    key ^= Z_ARR[768]
                else:
                    key ^= Z_ARR[64 * rook_index + chess.H8]
                    key ^= Z_ARR[64 * rook_index + chess.F8]
                    key ^= Z_ARR[770]
        # non castling move with king moving
        else:
            if board.has_castling_rights(board.turn):
                if board.turn:
                    key ^= Z_ARR[768]
                    key ^= Z_ARR[769]
                else:
                    key ^= Z_ARR[770]
                    key ^= Z_ARR[771]

    elif from_piece_type == chess.ROOK:
        if board.has_queenside_castling_rights(board.turn):
            if board.turn:
                key ^= Z_ARR[769]
            else:
                key ^= Z_ARR[771]
        if board.has_kingside_castling_rights(board.turn):
            if board.turn:
                key ^= Z_ARR[768]
            else:
                key ^= Z_ARR[770]
    
    # capture moves
    if board.is_capture(move) and not board.is_en_passant(move):
        # remove the piece at the moving to square
        to_piece_type = board.piece_type_at(to_square)
        tpiece_index = (typing.cast(chess.PieceType, to_piece_type) - 1) * 2 + (1 if board.piece_at(move.to_square).color else 0)
        key ^= Z_ARR[64 * tpiece_index + to_square]
    
    # promotion
    if(from_piece_type == chess.PAWN and (chess.square_rank(to_square) == 0 or chess.square_rank(to_square) == 7)):
        if move.promotion:
            new_p_index = (typing.cast(chess.PieceType, move.promotion) - 1) * 2 + pivot
            # replace current piece type with new piece type
            key ^= Z_ARR[64 * fpiece_index + to_square]
            key ^= Z_ARR[64 * new_p_index + to_square]
    
    # update ep rights (chess.polyglot)
    if board.ep_square:
        if board.turn == chess.WHITE:
            ep_mask = chess.shift_down(chess.BB_SQUARES[board.ep_square])
        else:
            ep_mask = chess.shift_up(chess.BB_SQUARES[board.ep_square])
        ep_mask = chess.shift_left(ep_mask) | chess.shift_right(ep_mask)

        if ep_mask & board.pawns & board.occupied_co[board.turn]:
            key ^= Z_ARR[772 + chess.square_file(board.ep_square)]

    if(board.is_en_passant(move)):
        to_square_file = chess.square_file(to_square)
        if board.turn:
            capture_rank = chess.square_rank(to_square) - 1
            cap_square = chess.square(to_square_file, capture_rank)
            tpiece_index = (typing.cast(chess.PieceType, chess.PAWN) - 1) * 2
            key ^= Z_ARR[64 * tpiece_index + cap_square]
        else:
            capture_rank = chess.square_rank(to_square) + 1
            cap_square = chess.square(to_square_file, capture_rank)
            tpiece_index = (typing.cast(chess.PieceType, chess.PAWN) - 1) * 2 + 1
            key ^= Z_ARR[64 * tpiece_index + cap_square]

    return key



if __name__ == '__main__':    
    # castling test
    #b = chess.Board('rnb1kbnr/pp1q1ppp/8/2ppp3/2PPP3/2N1B3/PPQ2PPP/R3KBNR w KQkq - 0 1')
    # cap test
    b = chess.Board('rnbqkbnr/1pp1P1p1/3p1p2/p6p/8/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1')
    # ep test
    #b = chess.Board('rnbqkb1r/ppp2ppp/8/3pP3/3Qn3/5N2/PPP2PPP/RNB1KB1R w KQkq d6 0 6')

    #b = chess.Board()

    move = chess.Move.from_uci('e7d8')
    key = zobrist_hash(b) 
    print(b)
    print(key)
    
    key = applyHash(key, b, move)
    b.push(move)

    print(b)
    print(key)

    b.pop()
    key = applyHash(key, b, move)

    print(b)
    print(key)

