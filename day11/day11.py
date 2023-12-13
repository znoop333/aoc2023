import numpy as np
from collections import defaultdict, deque
from math import prod, sqrt, floor, ceil


def parse_input(input: str):
    first_line = input.split()[0]
    width = len(first_line)
    height = len(input.split())
    universe = np.array([ch for ln in input.split() for ch in ln])
    universe = universe.reshape([height, width])
    return universe


def find_galaxies(universe):
    return np.argwhere(universe == '#')


def expand_galaxies(galaxies, universe):
    height, width = universe.shape
    expand_r = []
    for r in range(height):
        if np.all(universe[r, :] == '.'):
            expand_r.append(r)

    expand_c = []
    for c in range(width):
        if np.all(universe[:, c] == '.'):
            expand_c.append(c)

    num_galaxies, _ = galaxies.shape
    offsets = np.zeros(galaxies.shape, dtype=int)
    for ix in range(num_galaxies):
        for r in expand_r:
            if galaxies[ix, 0] > r:
                offsets[ix, 0] += 1
        for c in expand_c:
            if galaxies[ix, 1] > c:
                offsets[ix, 1] += 1

    galaxies += offsets

    return galaxies


def pairwise_dist(galaxies):
    # using the taxicab distance metric, find the distance between all pairs of galaxies
    total = 0
    num_galaxies, _ = galaxies.shape
    for i in range(num_galaxies):
        for j in range(i + 1, num_galaxies):
            d = abs(galaxies[j, 0] - galaxies[i, 0]) + abs(galaxies[j, 1] - galaxies[i, 1])
            total += d
            # print(f'Between galaxy {i} and galaxy {j}: {d}')

    return total


def main():
    with open("input.txt", "r") as f:
    # with open("test_input.txt", "r") as f:
        input = f.read()
    # input = """ """

    universe = parse_input(input)
    galaxies = find_galaxies(universe)
    galaxies = expand_galaxies(galaxies, universe)

    answer = pairwise_dist(galaxies)

    print(f'The answer is {answer}.')


if __name__ == '__main__':
    main()
