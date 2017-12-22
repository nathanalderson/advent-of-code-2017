#! /usr/bin/env python3
import collections

UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)

CLOCKWISE = [UP, RIGHT, DOWN, LEFT]
CCLOCKWISE = list(reversed(CLOCKWISE))

def main():
    test_board = set([(1,1), (-1,1)])
    print("part 1", play(test_board, 1))

def play(board, rounds):
    pos = (0,0)
    direction = UP
    infections = 0
    for r in range(rounds):
        if r % 1000 == 0:
            print("round", r)
        pos, direction, infected = burst(board, pos, direction)
        infections += infected
    print(board)
    return infections

def burst(board, pos, direction):
    if pos in board:
        turn = turn_right
        board.remove(pos)
        infect = False
    else:
        turn = turn_left
        board.add(pos)
        infect = True
    new_dir = turn(direction)
    return vadd(pos, new_dir), turn(new_dir), int(infect)

def turn_right(direction):
    return CLOCKWISE[(CLOCKWISE.index(direction)+1) % len(CLOCKWISE)]

def turn_left(direction):
    return CCLOCKWISE[(CCLOCKWISE.index(direction)+1) % len(CCLOCKWISE)]

def vadd(v1, v2):
    return tuple(i+j for i,j in zip(v1, v2))

if __name__ == "__main__":
    main()

