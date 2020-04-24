import chess
import numpy

# need to handle collisions and replacement scheme


class TTable(object):
    # store 2^16 positions by default
    def __init__(self, size=0xFFFF):
        self.size = size
        self.table = {}
        self.tracker = 0

    # insert a key into the table
    def insert(self, zkey, depth, evaluation, flag):
        key = zkey % self.size
        entry = Entry(zkey, depth, evaluation, flag)
        if len(self.table) >= self.size:
            self.clear()
        self.table[key] = entry

    # probe the table for a position
    # key = full key % self.size

    def probe(self, zkey):
        key = zkey % self.size
        if key in self.table.keys():
            self.tracker += 1
            # return the entry object
            return self.table[key]
        return None

    # reset table when it fills up
    def clear(self):
        self.table = {}


class Entry(object):
    def __init__(self, zobrist_key, depth, evaluation, flag):
        self.zobrist_key = zobrist_key
        self.depth = depth
        self.evaluation = evaluation
        self.flag = flag
