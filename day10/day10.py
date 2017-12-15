#! /usr/bin/env python3

class Circular(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        new_key = self._adjust_key(key)
        if isinstance(new_key, int):
            return super().__getitem__(new_key)
        elif self._is_normal_key(new_key):
            print("__getitem__(): normal key", new_key)
            return super().__getitem__(new_key)
        else:
            upper = super().__getitem__(slice(new_key.start, None, new_key.step))
            lower = super().__getitem__(slice(None, new_key.stop, new_key.step))
            print("__getitem__(): ", upper, lower)
            upper.extend(lower)
            print("__getitem__(): ", upper)
            return upper

    def __setitem__(self, key, value):
        new_key = self._adjust_key(key)
        if isinstance(new_key, int):
            return super().__setitem__(new_key, value)
        elif self._is_normal_key(new_key):
            return super().__setitem__(new_key, value)
        else:
            upperslice = slice(new_key.start, None, new_key.step)
            uppervalue = value[0:len(self)-new_key.start]
            super().__setitem__(upperslice, uppervalue)
            lowerslice = slice(None, new_key.stop, new_key.step)
            lowervalue = value[len(self)-new_key.start:len(self)]
            super().__setitem__(lowerslice, lowervalue)

    def _adjust_key(self, key):
        if isinstance(key, int):
            new_key = key % len(self)
        elif isinstance(key, slice):
            try:
                new_start = key.start % len(self)
            except TypeError:
                new_start = None
            try:
                new_stop = key.stop % len(self)
            except TypeError:
                new_stop = None
            new_key = slice(new_start, new_stop, key.step)
        else:
            raise TypeError
        return new_key

    def _is_normal_key(self, key):
        return (key.start is None or
                key.stop is None or
                key.start <= key.stop)

def main():
    testLengths = [3,4,1,5]
    testBoard = Circular(range(5))
    testResult = play(testBoard, testLengths)
    print("testResult = ", testResult)

    # lengths = [147,37,249,1,31,2,226,0,161,71,254,243,183,255,30,70]
    # board = Circular(range(256))
    # result = play(board, lengths)
    # print("result = ", result[0:10])

def play(board, lengths):
    pos = 0
    skip = 0
    for l in lengths:
        print(board, l, pos, skip)
        span = board[pos:pos+l]
        span.reverse()
        board[pos:pos+l] = span
        pos = (pos+l+skip) % len(board)
        skip = skip+1
    return board

if __name__ == "__main__":
    main()
