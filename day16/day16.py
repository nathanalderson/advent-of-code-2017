#! /usr/bin/env python3
import functools
import itertools

def main():
    test_raw_moves = "s1,x3/4,pe/b".strip().split(",")
    testmoves = [toMove(m) for m in test_raw_moves]
    testprogs = list("abcde")
    dance(testprogs, testmoves)
    print("test:", "".join(testprogs))
    raw_moves = open("input", "r").read().strip().split(",")
    moves = [toMove(m) for m in raw_moves]
    progs = list("abcdefghijklmnop")
    dance(progs, moves)
    print("part 1:", "".join(progs))
    progs = list("abcdefghijklmnop")
    for i in range(999999960, 1000000000):
        dance(progs, moves)
    print("part 2:", "".join(progs))

def toMove(s):
    if s.startswith("s"):
        return functools.partial(spin, int(s[1:]))
    elif s.startswith("x"):
        slash = s.index("/")
        a = int(s[1:slash])
        b = int(s[slash+1:])
        return functools.partial(exchange, a, b)
    elif s.startswith("p"):
        return functools.partial(partner, s[1], s[3])

def dance(progs, moves):
    for move in moves:
        move(progs)

def spin(x, progs):
    progs[:] = progs[-x:] + progs[:-x]

def exchange(a, b, progs):
    progs[a], progs[b] = progs[b], progs[a]

def partner(a, b, progs):
    exchange(progs.index(a), progs.index(b), progs)

if __name__ == "__main__":
    main()
