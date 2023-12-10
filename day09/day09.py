import numpy as np
from collections import defaultdict
from math import prod, sqrt, floor, ceil


def parse_input(input: str):
    oasises = []
    for ln in input.split('\n'):
        oasis = np.array([int(x) for x in ln.split()])
        oasises.append(oasis)

    return oasises


def diff_count(a: np.array) -> int:
    # how many times must the array "a" be diff'ed until it's all zeros?
    d = 0
    while np.any(a):
        d += 1
        a = np.diff(a)

    return d


def main():
    # with open("input.txt", "r") as f:
    with open("test_input.txt", "r") as f:
        input = f.read()

    extrapolated_sum = 0
    oasis = parse_input(input)
    for o in oasis:
        d = diff_count(o)
        extrapolated = 0
        extrapolated_sum += extrapolated
        print(f'diff_count({o}) = {d}')

    1


if __name__ == '__main__':
    main()
