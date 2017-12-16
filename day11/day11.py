#! /usr/bin/env python3

# direction -> (dx,dy,dz)
cube_directions = {
    "n": (0,1,-1),
    "ne": (1,0,-1),
    "se": (1,-1,0),
    "s": (0,-1,1),
    "sw": (-1,0,1),
    "nw": (-1,1,0)
}

def move(pos, direction):
    d = cube_directions[direction]
    return tuple(pos[i] + d[i] for i in range(3))

def distance(pos1, pos2):
    return abs(sum(abs(pos1[i]) - abs(pos2[i]) for i in range(3)) / 2)

def main():
    f = open("input", "r")
    path = f.read().strip().split(",")
    start = (0,0,0)
    pos = start
    positions = [start]
    for d in path:
        pos = move(pos, d)
        positions.append(pos)
    distances = [distance(start, pos) for pos in positions]
    print("final dist =", distances[-1])
    print("max dist =", max(distances))

if __name__ == "__main__":
    main()
