#! /usr/bin/env python3

def main():
    lines = open("input", "r").readlines()
    pipes = {
        int(k) : [int(p) for p in ps.strip().split(", ")]
        for (k,ps) in (line.split(" <-> ") for line in lines)
    }
    group0 = set([0])
    explore = [0]
    while explore:
        p = explore.pop()
        more = pipes[p]
        for m in more:
            if m not in group0:
                group0.add(m)
                explore.append(m)
    print(group0)
    print(len(group0))


if __name__ == "__main__":
    main()
