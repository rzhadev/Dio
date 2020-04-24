# Dio
# homebrewing a chess engine and hoping it doesnt suck (it does)
## Current Features
## -negamax alphabeta search function
## -iterative deepening framework, around 10 seconds per move
## -static evaluation function, only considers piece square tables and raw piece value 
## -utility perft function to count explored nodes
## -zobrist hash function from chess.polyglot, with an incremental key update function to speed up index calculation
## -transposition table of size 2^16
## TODO
## -improve the evaluation function, pawn structure and king safety
## -opening books
## -move ordering** (null move, killer heuristic, hash move)
## -track PV and pv moves
## -improve ttable replacement scheme, maybe add buckets
## -