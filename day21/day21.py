#! /usr/bin/env python3
import itertools
import numpy
import math

def main():
    image = numpy.array([list(".#."), list("..#"), list("###")])
    patterns = [line.strip().split(" => ") for line in open("input", "r").readlines()]
    test_patterns = [ ["../.#", "##./#../..."]
                    , [".#./..#/###", "#..#/..../..../#..#"] ]
    image = enhance(image, patterns)
    print(image)
    image = enhance(image, patterns)
    print(image)
    image = enhance(image, patterns)
    print(image)

def enhance(image, patterns):
    # print("enhance", image)
    size = len(image)
    if size == 2 or size == 3:
        for pattern in patterns:
            new_image = try_pattern(image, *pattern)
            if new_image is not None:
                return new_image
        else:
            raise Exception("No patterns matched")
    else:
        if size % 2 == 0:
            chunks = chunk(image, 2)
        else:
            chunks = chunk(image, 3)
        enhanced_chunks = [enhance(c, patterns) for c in chunks]
        # print("enhanced_chunks", enhanced_chunks)
        return combine(enhanced_chunks)

def try_pattern(image, pattern, out):
    # print("try_pattern", pattern)
    if pattern_matches(image, pattern):
        return image_string_to_array(out)
    else:
        return None

def image_string_to_array(s):
    return numpy.array([numpy.array(list(r)) for r in s.split("/")])

def image_array_to_string(a):
    return "/".join("".join(r.tolist()) for r in a)

def pattern_matches(image, pattern):
    images = [ image, flip_horizontal(image), flip_vertical(image), rotate(image),
               rotate(rotate(image)), rotate(rotate(rotate(image))) ]
    for i in images:
        s = image_array_to_string(i)
        print(s, pattern)
        if s == pattern:
            return True
    return False

def combine(chunks):
    # print("combine", chunks)
    size = int(math.sqrt(len(chunks)))
    rows = [chunks[i:i+size] for i in range(0, len(chunks), size)]
    combined_rows = [numpy.hstack(row) for row in rows]
    return numpy.vstack(combined_rows)

def chunk(image, size):
    return [ image[i:i+size, j:j+size]
             for i,j in itertools.product(range(0, len(image), size), repeat=2) ]

def flip_horizontal(image):
    return numpy.array([list(reversed(line)) for line in image])

def flip_vertical(image):
    return numpy.array(list(reversed(image)))

def rotate(image):
    return numpy.array(list(zip(*image[::-1])))

if __name__ == "__main__":
    main()
