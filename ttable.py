import collections
import chess
import numpy

# store 2^32 transpositions in the hash table


class TTable(object):

    def __init__(self, size=0xFFFFFFFF):
        self.hash_size = size
        # buckets of 4 for each index
        self.table = {}
        self.tracker = 0

    # add an entry into the table
    def add_entry(self, zobrist_key: int, depth: int, evaluation: int,
                  flag: int, bestmove: str, age: int):

        # always replace
        if(len(self.table) < self.hash_size):
            key = zobrist_key % self.hash_size
            self.table[key] = Entry(
                zobrist_key, depth, evaluation, flag, bestmove, age)

    # probe the table for a position

    def probe(self):
        self.tracker += 1

    def clear(self):
        self.table = {}


class Entry(object):
    def __init__(self, zobrist_key, depth, evaluation, flag, bestmove, age):
        self.zobrist_key = zobrist_key
        self.depth = depth
        self.eval = evaluation
        self.flag = flag
        self.bestmove = bestmove
        self.age = age
