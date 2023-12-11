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
    diff_first = a[0]
    while np.any(a):
        d += 1
        a = np.diff(a)
        sum_last += a[-1]
        if d % 2 == 1:
            diff_first -= a[0]
        else:
            diff_first += a[0]

    return d, sum_last, diff_first


def main():
    with open("input.txt", "r") as f:
    # with open("test_input.txt", "r") as f:
        input = f.read()

    oasis = parse_input(input)
    answer = 0
    answer_part2 = 0
    for o in oasis:
        d, sum_last, diff_first = diff_count(o)
        print(f'diff_count({o}) = {d}, sum_last {sum_last}')
        answer += sum_last
        answer_part2 += diff_first

    print(f'The answer is {answer}.\nPart 2 answer {answer_part2}')


if __name__ == '__main__':
    main()
