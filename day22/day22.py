#! /usr/bin/env python3
import collections
import math

UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)

CLOCKWISE = [UP, RIGHT, DOWN, LEFT]
CCLOCKWISE = list(reversed(CLOCKWISE))

CLEAN = 0
INFECTED = 1
WEAKENED = 2
FLAGGED = 3

def main():
    test_board = {(1,1): INFECTED, (-1,0): INFECTED}
    assert play(test_board, 10000, burst1) == 5587
    board = get_board(open('input', 'r'))
    print("part 1:", play(board, 10000, burst1))
    board2 = get_board(open('input', 'r'))
    print("part 2:", play(board2, 10000000, burst2))

def get_board(f):
    lines = [l.strip() for l in f.readlines()]
    height = len(lines)
    width = len(lines[0])
    board = {}
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '#':
                x, y = col-(width//2), -(row-(height//2))
                board[(x,y)] = INFECTED
    return board

def play(board, rounds, burst_function):
    pos = (0,0)
    direction = UP
    infections = 0
    for r in range(rounds):
        if r % 1000000 == 0:
            print("round", r)
        pos, direction, infected = burst_function(board, pos, direction)
        infections += infected
    return infections

def burst1(board, pos, direction):
    if board.get(pos, CLEAN) == INFECTED:
        turn = turn_right
        del board[pos]
        infect = False
    else:
        turn = turn_left
        board[pos] = INFECTED
        infect = True
    new_dir = turn(direction)
    new_pos = vadd(pos, new_dir)
    return new_pos, new_dir, int(infect)

def burst2(board, pos, direction):
    status = board.get(pos, CLEAN)
    infect = False
    if status == CLEAN:
        new_dir = turn_left(direction)
        board[pos] = WEAKENED
    elif status == WEAKENED:
        new_dir = direction
        infect = True
        board[pos] = INFECTED
    elif status == INFECTED:
        new_dir = turn_right(direction)
        board[pos] = FLAGGED
    elif status == FLAGGED:
        new_dir = turn_right(turn_right(direction))
        board[pos] = CLEAN
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

