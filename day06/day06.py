import numpy as np
from collections import defaultdict
from math import prod, sqrt, floor, ceil


def parse_input(input: str):
    for ln in input.split('\n'):
        if 'Time' in ln:
            ln = ln.replace('Time:', '')
            times = [int(x) for x in ln.split()]
        elif 'Distance' in ln:
            ln = ln.replace('Distance:', '')
            distances = [int(x) for x in ln.split()]

    return times, distances


def intervalWidth(M: int, D: int) -> int:
    # let F(x) be the distance travelled after waiting x seconds to "charge" the boat.
    # F(x) = x*(M-x)   for x in [0, M] (integers) where M is the maximum amount of time available
    # we want to determine how many values of x satisfy:
    # F(x) > D , for D being the given distance to beat.
    # let f(x) be the continuous version of F(x), with the same constraints.
    # if D is the distance to beat, we can define:
    # then g(x) = f(x) - D = x(M-x) - D = -x^2 + M*x - D == 0
    # use the quadratic formula to find the values of x:
    x1 = (M + sqrt(M ** 2 - 4 * D)) / 2
    x2 = (M - sqrt(M ** 2 - 4 * D)) / 2
    # to relate these real values back to discrete values in F(x), we have to check the edge conditions
    i1 = ceil(x1)
    i2 = floor(x2)
    F = lambda x: x * (M - x)
    width = i1 - i2 - 1 + int(F(i1) > D) + int(F(i2) > D)
    return width


def main():
    with open("input.txt", "r") as f:
    # with open("test_input.txt", "r") as f:
        input = f.read()

    times, distances = parse_input(input)
    for i in range(len(times)):
        print(times[i], distances[i], intervalWidth(times[i], distances[i]))


if __name__ == '__main__':
    main()
