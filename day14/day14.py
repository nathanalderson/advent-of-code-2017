#! /usr/bin/env python3
from day10 import *
import pickle
import itertools

USE_PICKLE = True
PICKLE_FILE = "row_binary.pickle"

def main():
    row_binary = get_row_binary()
    row_counts = [b.count("1") for b in row_binary]
    # for row in row_binary:
        # print(row)
    print("part1 =", sum(row_counts))
    groups = 0
    while find_and_kill_group(row_binary):
        groups += 1
    print("part2 =", groups)

def find_and_kill_group(row_binary):
    try:
        next_one = next((x,y)
                        for (x,y)
                        in itertools.product(range(len(row_binary)), range(len(row_binary[0])))
                        if row_binary[x][y] == 1)
        kill_group_at(*next_one, row_binary)
        return True
    except StopIteration:
        return False

def kill_group_at(x, y, row_binary):
    # print("killing group at", x, y)
    explore = [(x,y)]
    while explore:
        x,y = explore.pop()
        if row_binary[x][y] == 1:
            row_binary[x][y] = 0
            explore.extend(neighbors(x,y))

def neighbors(x,y):
    return [(x,y) for (x,y)
            in [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]
            if 0 <= x < 128 and 0 <= y < 128]

def get_row_binary():
    if USE_PICKLE:
        with open(PICKLE_FILE, "rb") as f:
            return pickle.load(f)
    else:
        base = "hxtvlmkl"
        row_strings = [base+"-"+str(i) for i in range(128)]
        row_hashes = [knot_hash(s) for s in row_strings]
        row_binary = [to_binary(h) for h in row_hashes]
        with open(PICKLE_FILE, "wb") as f:
            pickle.dump(row_binary, f)
        return row_binary

def to_binary(h):
    return [int(c) for c in "".join("{:08b}".format(x) for x in h)]

if __name__ == "__main__":
    main()
