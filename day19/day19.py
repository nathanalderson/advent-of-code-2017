#! /usr/bin/env python3
import string
import time

# (dr, dc)
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

def main():
    test_maze = """\
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ """.splitlines()
    print(follow(test_maze))

    maze = [line.strip("\n") for line in open("input", "r").readlines()]
    letters, steps = follow(maze)
    print("part1 (letters) =", letters)
    print("part2 (steps) =", steps)

def follow(maze):
    r, c = find_start(maze)
    print("start", r, c)
    dr, dc = DOWN
    found = ""
    steps = 0
    while True:
        # time.sleep(0.1)
        steps += 1
        val = maze[r][c]
        # print(val)
        if val == '|' or val == '-':
            r += dr
            c += dc
        elif val in string.ascii_uppercase:
            found += val
            r += dr
            c += dc
        if val == '+':
            try_dr, try_dc = turn_left(dr, dc)
            try_r, try_c = r+try_dr, c+try_dc
            if maze[try_r][try_c] != '+' and maze[try_r][try_c] != ' ':
                # print("turning left")
                dr, dc = try_dr, try_dc
                r += dr
                c += dc
            else:
                # print("turning right")
                dr, dc = turn_right(dr, dc)
                r, c = r+dr, c+dc
        elif val == ' ':
            break
    return found, steps-1

def turn_left(dr,dc):
    if (dr,dc) == UP:
        return LEFT
    if (dr,dc) == DOWN:
        return RIGHT
    if (dr,dc) == LEFT:
        return DOWN
    if (dr,dc) == RIGHT:
        return UP

def turn_right(dr,dc):
    if (dr,dc) == UP:
        return RIGHT
    if (dr,dc) == DOWN:
        return LEFT
    if (dr,dc) == LEFT:
        return UP
    if (dr,dc) == RIGHT:
        return DOWN

def find_start(maze):
    c = next(c for c,v in enumerate(maze[0]) if v == "|")
    r = 0
    return r,c

if __name__ == "__main__":
    main()
