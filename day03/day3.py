#! /usr/bin/env python3

from itertools import *
from collections import defaultdict

# part 2

def spiral():
    x,y = 0,0
    dx,dy = 1,0
    while True:
        if (abs(x) == abs(y) and [dx,dy] != [1,0]) or (x>0 and y == 1-x):
            dx, dy = -dy, dx # corner, change direction
        yield x, y
        x, y = x+dx, y+dy

def neighbor_coords(x,y):
    return ((x-1, y+1), (x, y+1), (x+1, y+1),
            (x-1, y  ),           (x+1, y  ),
            (x-1, y-1), (x, y-1), (x+1, y-1))

input = 277678
grid = {(0,0): 1}
spiral = spiral()
next(spiral)
for (x,y) in spiral:
    print(x,y)
    v = 0
    for coord in neighbor_coords(x,y):
        v += grid.get(coord, 0)
    grid[(x,y)] = v
    if v > input:
        print(v)
        break
