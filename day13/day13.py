#! /usr/bin/env python3
import itertools

def main():
    lines = open("input", "r").readlines()
    # [(depth, range)]
    scanners = [
        (int(d), int(r))
        for d,r in (line.split(": ") for line in lines)
    ]
    severity = sum(d * r
                   for d, r in scanners
                   if scanner_pos(r, d) == 0)
    print("part1: severity =", severity)
    delay = next(delay for delay in itertools.count()
                 if not any(scanner_pos(r, delay+d) == 0
                            for d, r in scanners)
                )
    print("part2: delay =", delay)

def scanner_pos(r, time):
    positions = tuple(range(r)) + tuple(range((r-2), 0, -1))
    return positions[time % len(positions)]

if __name__ == "__main__":
    main()
