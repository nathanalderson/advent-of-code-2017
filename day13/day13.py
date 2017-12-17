#! /usr/bin/env python3
import itertools

def main():
    # depth -> (range, pos, direction)
    scanners = {
        int(l[0]) : int(l[1]) for l in (
            line.split(": ") for line in open("input", "r").readlines())
    }
    severity = sum(pos * scanners[pos]
                for pos in scanners
                if scanner_pos(scanners[pos], pos) == 0)
    print("part1: severity =", severity)
    delay = next(delay for delay in itertools.count()
                 if not any(scanner_pos(scanners[pos], delay+pos) == 0
                            for pos in scanners)
                )
    print("part2: delay =", delay)

def scanner_pos(height, time):
    positions = tuple(range(height)) + tuple(range((height-2), 0, -1))
    return positions[time % len(positions)]

if __name__ == "__main__":
    main()
