#! /usr/bin/env python3
import math
import collections

def main():
    particles = get_particles()
    # part 1
    # for i in range(2000):
    #     tick1(particles)
    # print("part 1:", find_nearest(particles))
    # part 2
    for i in range(500):
        tick2(particles)
    print("part 2:", len(particles))

def find_nearest(particles):
    dists = [dist(p) for p in particles]
    return dists.index(min(dists))

def dist(particle):
    x,y,z = particle['p']
    return abs(x) + abs(y) + abs(z)

def tick1(particles):
    for i,p in enumerate(particles):
        new_v = vector_add(p['v'], p['a'])
        new_p = vector_add(p['p'], new_v)
        p['v'] = new_v
        p['p'] = new_p

def tick2(particles):
    positions = collections.defaultdict(list)
    for i,p in enumerate(particles):
        new_v = vector_add(p['v'], p['a'])
        new_p = vector_add(p['p'], new_v)
        p['v'] = new_v
        p['p'] = new_p
        positions[tuple(new_p)].append(i)
    remove = []
    for pos, particle_nums in positions.items():
        if len(particle_nums) > 1:
            remove.extend(particle_nums)
    remove.sort()
    remove.reverse()
    for i in remove:
        particles.pop(i)

def vector_add(v1, v2):
    return [i+j for i,j in zip(v1, v2)]

def get_particles():
    return [parse_line(l) for l in open("input", "r").readlines()]

def parse_line(l):
    pvas = [f.split("=") for f in l.split(", ")]
    return {
        k : [int(x.strip("<> \n")) for x in v.split(",")] for k,v in pvas
    }


if __name__ == "__main__":
    main()
