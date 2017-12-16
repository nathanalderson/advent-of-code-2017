#! /usr/bin/env python3

class Circular(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        if isinstance(key, int):
            rval = super().__getitem__(key % len(self))
            return rval
        else:
            rval = [self.__getitem__(k) for k in range(key.start, key.stop)]
            return rval

    def __setitem__(self, key, value):
        if isinstance(key, int):
            super().__setitem__(key % len(self), value)
        else:
            for i, k in enumerate(range(key.start, key.stop)):
                self.__setitem__(k, value[i])

def main():
    testLengths = [3,4,1,5]
    testBoard = Circular(range(5))
    testResultBoard, _, _ = knot_round(testBoard, testLengths, 0, 0)
    print("testResult = ", testResultBoard)

    lengths = [147,37,249,1,31,2,226,0,161,71,254,243,183,255,30,70]
    board = Circular(range(256))
    resultBoard, _, _ = knot_round(board, lengths, 0, 0)
    print("result =", resultBoard[0:10])
    print("product =", resultBoard[0] * resultBoard[1])

    # part2
    raw = "147,37,249,1,31,2,226,0,161,71,254,243,183,255,30,70"
    p2lengths = [ord(c) for c in raw] + [17, 31, 73, 47, 23]
    h = knot_hash(p2lengths)
    print("hash =", show_hash(h))

def knot_hash(lengths):
    board = Circular(range(256))
    pos = 0
    skip = 0
    for i in range(64):
        board, pos, skip = knot_round(board, lengths, pos, skip)
    return densify(board)

def densify(sparse_hash):
    chunks = (sparse_hash[i:i+16] for i in range(0, len(sparse_hash), 16))
    rval = (xor(l) for l in chunks)
    return rval

def xor(l):
    rval = 0
    for x in l:
        rval = rval ^ x
    return rval

def show_hash(h):
    return "".join("{:02x}".format(x) for x in h)

def knot_round(board, lengths, pos, skip):
    for l in lengths:
        span = board[pos:pos+l]
        span.reverse()
        board[pos:pos+l] = span
        pos = (pos+l+skip) % len(board)
        skip = skip+1
    return board, pos, skip

if __name__ == "__main__":
    main()
