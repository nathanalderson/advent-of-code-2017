#! /usr/bin/env python3
import itertools

def main():
    # genA = generator(618, 16807)
    # genB = generator(814, 48271)
    # count = count_matches(genA, genB, 40000000)
    # print("part1: count =", count)
    genA2 = generator(618, 16807, 4)
    genB2 = generator(814, 48271, 8)
    count2 = count_matches(genA2, genB2, 5000000)
    print("part2: count =", count2)

def count_matches(genA, genB, rounds):
    count = 0
    for i in range(rounds):
        a, b = next(genA), next(genB)
        if i % 1000000 == 0:
            print("round", i/1000000, "Million")
        if a & 0xffff == b & 0xffff:
            count += 1
    return count

def generator(seed, factor, multiples_of=1):
    val = seed
    while True:
        val = (val * factor) % 2147483647
        if val % multiples_of == 0:
            yield val


if __name__ == "__main__":
    main()
