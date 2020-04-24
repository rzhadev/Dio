import chess

# count the number of nodes explored for a certain depth from a given position


def perft(board, depth):
    nodes = 0
    if depth == 0:
        return 1
    else:
        for move in board.legal_moves:
            board.push(move)
            if(not board.is_game_over()):
                nodes += perft(board, depth - 1)
            board.pop()
    return nodes

