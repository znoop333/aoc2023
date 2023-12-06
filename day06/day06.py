import numpy as np
from collections import defaultdict
from math import prod


def parse_input(input: str):
    for ln in input.split('\n'):
        if 'Time' in ln:
            ln = ln.replace('Time:', '')
            times = [int(x) for x in ln.split()]
        elif 'Distance' in ln:
            ln = ln.replace('Distance:', '')
            distances = [int(x) for x in ln.split()]

    return times, distances


def main():
    with open("test_input.txt", "r") as f:
    # with open("input.txt", "r") as f:
        input = f.read()

    times, distances = parse_input(input)
    print(times, distances)


if __name__ == '__main__':
    main()
