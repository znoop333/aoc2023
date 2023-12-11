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
    sum_last = a[-1]
    while np.any(a):
        d += 1
        a = np.diff(a)
        sum_last += a[-1]

    return d, sum_last


def main():
    with open("input.txt", "r") as f:
    # with open("test_input.txt", "r") as f:
        input = f.read()

    oasis = parse_input(input)
    answer = 0
    for o in oasis:
        d, sum_last = diff_count(o)
        print(f'diff_count({o}) = {d}, sum_last {sum_last}')
        answer += sum_last

    print(f'The answer is {answer}')


if __name__ == '__main__':
    main()
