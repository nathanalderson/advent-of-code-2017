#! /usr/bin/env python3
import collections
import math

UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)

CLOCKWISE = [UP, RIGHT, DOWN, LEFT]
CCLOCKWISE = list(reversed(CLOCKWISE))

def main():
    test_board = set([(1,1), (-1,0)])
    assert play(test_board, 10000, burst1) == 5587
    board = get_board(open('input', 'r'))
    print("part 1:", play(board, 10000, burst1))

def get_board(f):
    lines = [l.strip() for l in f.readlines()]
    height = len(lines)
    width = len(lines[0])
    board = set()
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '#':
                x, y = col-(width//2), -(row-(height//2))
                board.add((x,y))
    return board

def play(board, rounds, burst_function):
    pos = (0,0)
    direction = UP
    infections = 0
    for r in range(rounds):
        if r % 1000 == 0:
            print("round", r)
        pos, direction, infected = burst_function(board, pos, direction)
        infections += infected
    return infections

def burst1(board, pos, direction):
    if pos in board:
        turn = turn_right
        board.remove(pos)
        infect = False
    else:
        turn = turn_left
        board.add(pos)
        infect = True
    new_dir = turn(direction)
    new_pos = vadd(pos, new_dir)
    return new_pos, new_dir, int(infect)

def turn_right(direction):
    return CLOCKWISE[(CLOCKWISE.index(direction)+1) % len(CLOCKWISE)]

def turn_left(direction):
    return CCLOCKWISE[(CCLOCKWISE.index(direction)+1) % len(CCLOCKWISE)]

def vadd(v1, v2):
    return tuple(i+j for i,j in zip(v1, v2))

if __name__ == "__main__":
    main()

