#! /usr/bin/env python3

def main():
    testmoves = "s1,x3/4,pe/b".strip().split(",")
    testprogs = list("abcde")
    dance(testprogs, testmoves)
    print("test:", "".join(testprogs))
    moves = open("input", "r").read().strip().split(",")
    progs = list("abcdefghijklmnop")
    dance(progs, moves)
    print("part1:", "".join(progs))
    # for i in range(1000000000 - 1):
    #     if i % 100 == 0:
    #         print(i)
    #     dance(progs, moves)
    # print("part2:", "".join(progs))

def dance(progs, moves):
    for move in moves:
        if move.startswith("s"):
            a = int(move[1:])
            spin(a, progs)
        elif move.startswith("x"):
            slash = move.index("/")
            a = int(move[1:slash])
            b = int(move[slash+1:])
            exchange(a, b, progs)
        elif move.startswith("p"):
            a = move[1]
            b = move[3]
            partner(a, b, progs)

def spin(x, progs):
    progs[:] = progs[-x:] + progs[:-x]

def exchange(a, b, progs):
    progs[a], progs[b] = progs[b], progs[a]

def partner(a, b, progs):
    exchange(progs.index(a), progs.index(b), progs)

if __name__ == "__main__":
    main()
