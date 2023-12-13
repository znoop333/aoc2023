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

    offsets = np.zeros(galaxies.shape)
    if expand_r:
        for ix in range(galaxies.shape[0]):
            for r in expand_r:
                if galaxies[ix, 0] >= r:
                    offsets[ix, 0] += 1

    if expand_c:
        for ix in range(galaxies.shape[0]):
            for c in expand_c:
                if galaxies[ix, 1] >= c:
                    offsets[ix, 1] += 1

    galaxies += offsets

    return 1


def main():
    # with open("input.txt", "r") as f:
    with open("test_input.txt", "r") as f:
        input = f.read()
    # input = """ """

    universe = parse_input(input)
    galaxies = find_galaxies(universe)

    answer = 0
    # answer = count_dots(universe)
    # print_universe(universe)

    print(f'The answer is {answer}.')


if __name__ == '__main__':
    main()
