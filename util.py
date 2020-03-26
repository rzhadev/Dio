import chess


def perft(board, depth):
    nodes = 0
    if depth == 0:
        return 1
    else:
        for move in board.legal_moves:
            board.push(move)
            if(not board.is_game_over):
                nodes += perft(board, depth - 1)
            board.pop()
    return nodes


b = chess.Board()
print(perft(b, 10))
