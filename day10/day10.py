#! /usr/bin/env python3

class Circular(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        if isinstance(key, int):
            rval = super().__getitem__(key % len(self))
            # print("getitem (int)", key, rval)
            return rval
        else:
            rval = [self.__getitem__(k) for k in range(key.start, key.stop)]
            # print("getitem (slice)", key, rval)
            return rval

    def __setitem__(self, key, value):
        if isinstance(key, int):
            super().__setitem__(key % len(self), value)
            # print("setitem (int)", key, value)
        else:
            # print("setitem (slice)", key, value)
            for i, k in enumerate(range(key.start, key.stop)):
                self.__setitem__(k, value[i])

def main():
    testLengths = [3,4,1,5]
    testBoard = Circular(range(5))
    testResultBoard, testPos, testSkip = knot_round(testBoard, testLengths, 0, 0)
    print("testResult = ", testResultBoard)

    lengths = [147,37,249,1,31,2,226,0,161,71,254,243,183,255,30,70]
    board = Circular(range(256))
    resultBoard, pos, skip = knot_round(board, lengths, 0, 0)
    print("result = ", resultBoard[0:10])
    print("product = ", resultBoard[0] * resultBoard[1])

def knot_round(board, lengths, pos, skip):
    for l in lengths:
        # print(board, l, pos, skip)
        span = board[pos:pos+l]
        span.reverse()
        board[pos:pos+l] = span
        pos = (pos+l+skip) % len(board)
        skip = skip+1
    return board, pos, skip

if __name__ == "__main__":
    main()
