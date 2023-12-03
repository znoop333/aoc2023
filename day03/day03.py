import numpy as np
from collections import defaultdict
from math import prod

def parse_schematic(input: str) -> np.array:
    # create an array representation of a text schematic input.
    # the newlines are significant!
    first_line = input.split()[0]
    width = len(first_line)
    height = len(input.split())
    schematic = np.array([ch for ln in input.split() for ch in ln])
    schematic = schematic.reshape([height, width])

    return schematic


def neighbors8(row: int, col: int, schematic: np.array):
    # yield the in-bounds 8-connectivity neighbors for any position [row,col] in a 2d grid
    height, width = schematic.shape
    for ii in range(row - 1, row + 2):
        for jj in range(col - 1, col + 2):
            if 0 <= ii < width and 0 <= jj < height:
                yield schematic[ii, jj], ii, jj


def walk(schematic: np.array) -> int:
    # traverse a 2D graph doing a modified flood fill:
    # when encountering any integer, combine it into the current integer
    # also check its 8 neighbors for any non-integer, non-period symbol.
    # if a qualifying symbol is found, add the integer to the total
    total = 0

    height, width = schematic.shape
    current_int = None
    found_symbol = False
    for ii in range(0, height):
        for jj in range(0, width):
            if schematic[ii, jj].isdigit():
                if current_int is None:
                    current_int = int(schematic[ii, jj])
                else:
                    current_int = 10 * current_int + int(schematic[ii, jj])

                for ch, _, _ in neighbors8(ii, jj, schematic):
                    if not ch.isdigit() and ch != '.':
                        found_symbol = True
            else:
                if current_int is not None and found_symbol:
                    total += current_int
                current_int = None
                found_symbol = False

    return total


def walk_part2(schematic: np.array) -> int:
    # traverse a 2D graph doing a modified flood fill:
    # when encountering any integer, combine it into the current integer
    # also check its 8 neighbors for any '*'.
    # keep track of which integers had a '*' neighbor, and for the '*' with exactly 2 ints, sum them up
    total = 0

    height, width = schematic.shape
    current_int = None
    found_symbol = None
    gear_locations = defaultdict(list)  # keys: (ii,jj) for the gear, values: list of ints at this gear.
    for ii in range(0, height):
        for jj in range(0, width):
            if schematic[ii, jj].isdigit():
                if current_int is None:
                    current_int = int(schematic[ii, jj])
                else:
                    current_int = 10 * current_int + int(schematic[ii, jj])

                for ch, gi, gj in neighbors8(ii, jj, schematic):
                    if ch == '*':
                        found_symbol = (gi, gj)
            else:
                if current_int is not None and found_symbol is not None:
                    gear_locations[found_symbol].append(current_int)
                current_int = None
                found_symbol = None

    for loc, gears in gear_locations.items():
        if len(gears) == 2:
            total += prod(gears)

    return total


def main():
    #with open("test_input.txt", "r") as f:
    with open("input.txt", "r") as f:
        input = f.read()

    schematic = parse_schematic(input)
    # avoid edge effect using padding
    schematic = np.pad(schematic, (1, 1), 'constant', constant_values=('.', '.'))
    # part 1
    print(walk(schematic))

    # part 2
    print(walk_part2(schematic))


if __name__ == '__main__':
    main()
