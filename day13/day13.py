#! /usr/bin/env python3

def main():
    # depth -> (range, pos, direction)
    initial_scanners = {
        int(l[0]) : (int(l[1]), 0, "down") for l in (
            line.split(": ") for line in open("input", "r").readlines())
    }
    severity = run_it(initial_scanners.copy())
    print("part1: severity =", severity)

def run_it(scanners):
    finish_line = 97
    severity = 0
    for d in range(finish_line):
        scanner_range, scanner_pos, _ = scanners.get(d, (0, -1, "down"))
        if scanner_pos == 0:
            severity += d * scanner_range
        advance_scanners(scanners)
    return severity

def advance_scanners(scanners):
    for d, (r, p, dir) in scanners.items():
        next_dir = dir
        if dir == "down":
            next_pos = p + 1
            if next_pos == r:
                next_pos = p - 1
                next_dir = "up"
        else:
            next_pos = p - 1
            if next_pos == -1:
                next_pos = p + 1
                next_dir = "down"
        scanners[d] = (r, next_pos, next_dir)

if __name__ == "__main__":
    main()
