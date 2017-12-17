#! /usr/bin/env python3

def main():
    lines = open("input", "r").readlines()
    pipes = {
        int(k) : [int(p) for p in ps.strip().split(", ")]
        for (k,ps) in (line.split(" <-> ") for line in lines)
    }
    group0 = getGroup(0, pipes)
    print("part1 =", len(group0))
    numGroups = 0
    while pipes:
        numGroups += 1
        nextNode = list(pipes.keys())[0]
        group = getGroup(nextNode, pipes)
        for g in group:
            pipes.pop(g)
    print("part2 =", numGroups)

def getGroup(rootNode, pipes):
    group = set([rootNode])
    explore = [rootNode]
    while explore:
        p = explore.pop()
        more = pipes[p]
        for m in more:
            if m not in group:
                group.add(m)
                explore.append(m)
    return group


if __name__ == "__main__":
    main()
