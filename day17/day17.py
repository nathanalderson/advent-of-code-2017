#! /usr/bin/env python3

def main():
    assert play(3, 2017)[0] == 638
    result1, _ = play(316, 2017)
    print("part 1 =", result1)
    _, result2 = play(316, 50000000)
    print("part 2 =", result)

def play(stepsize, rounds):
    buff = [0]
    pos = 0
    for i in range(rounds):
        if i % 100000 == 0:
            print("round", i)
        pos = ((pos + stepsize) % len(buff)) + 1
        buff.insert(pos, i+1)
    return buff[pos+1], buff[buff.index(0)+1]

if __name__ == "__main__":
    main()
