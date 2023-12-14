import numpy as np
from collections import defaultdict, deque
from math import prod, sqrt, floor, ceil


def parse_input(input: str):
    nrows = len(input.split('\n'))
    patterns = [''] * nrows
    conditions = [''] * nrows
    for row, line in enumerate(input.split('\n')):
        patterns[row], conditions[row] = line.split(' ')

    return patterns, conditions


def number2pattern(i: int):
    return bin(i)[2:]


def consistency_check(ps, hs, pattern: str, up_to_pi: int = -1, strict_length_check=True):
    if strict_length_check and np.sum(ps) + np.sum(hs) != len(pattern):
        return False, -1
    if not np.all(ps[1:-1]):
        return False, -2

    num_h = len(hs) if (up_to_pi == -1) else up_to_pi

    pattern_index = 0
    for i in range(num_h):
        for pi in range(ps[i]):
            if pattern[pattern_index] not in '.?':
                return False, pattern_index
            pattern_index += 1

        for hi in range(hs[i]):
            if pattern[pattern_index] not in '#?':
                return False, pattern_index
            pattern_index += 1

    if (up_to_pi == -1):
        for pi in range(ps[-1]):
            if pattern[pattern_index] not in '.?':
                return False, pattern_index
            pattern_index += 1

    return True, pattern_index


def consistency_check_tests():
    # should be true, this is a solution
    print(consistency_check([0, 1, 1, 0], [1, 1, 3], '???.###'))

    # should be false: having two blocks of periods touching
    print(consistency_check([0, 0, 2, 0], [1, 1, 3], '???.###'))

    # should be false: too many periods
    print(consistency_check([1, 1, 1, 0], [1, 1, 3], '???.###'))

    # testing up_to_pi (partial comparisons)

    # should be true, this is a partial solution
    print(consistency_check([0, 1, 17, 0], [1, 1, 3], '???.###', up_to_pi=2, strict_length_check=False))

    # should be false, this is not a valid solution at p[i=1]
    print(consistency_check([0, 17, 1, 0], [1, 1, 3], '???.###', up_to_pi=2, strict_length_check=False))

    1


def solve(pattern, condition) -> int:
    N = len(pattern)
    c = 0
    h = np.array([int(s) for s in condition.split(',')])
    num_h = len(h)
    sum_h = np.sum(h)
    p = np.ones((num_h + 1,), dtype=int)
    # the first and last values can be 0, but the min value of every other p is 1.
    p[0] = 0
    p[-1] = 0

    def rec(i: int):
        1

    return c


def main():
    with open("d12_input.txt", "r") as f:
        input = f.read()

    patterns, conditions = parse_input(input)
    print(number2pattern(31))

    answer = 0
    for k in range(len(patterns)):
        answer += solve(patterns[k], conditions[k])
    print(answer)

    # general approach: the conditions string '1,1,3'
    # can be described as p0 h0 p1 h1 p2 h2 p3
    # where p0 is a run of periods, e.g., p0 = 3 means '...'
    # and h0 is a run of hashes, e.g., h0 = 1 means '#'
    # so if p = [0, 1, 1, 0] and h=[1,1,3] then the output string is '#.#.###'
    # another example: p = [2, 0, 0, 0] and h=[1,1,3] then the output string is '..#####'.
    # the former is a valid solution to '???.###' but the latter is not.

    # the values of h are exactly given by the conditions string, and
    # the values of p are unknown but constrained by the pattern string.
    # the problem statement is to determine how many values of p are possible.
    # the first and last p (p0 and p3) can be zero-length, but all other p must be at least 1
    # or else the hash runs would be overlapping.

    # the sum of all p and h must be exactly N, the length of the pattern string,
    # so one degree of freedom in p can be eliminated, e.g., p3 = N - sum(h) - (p0 + p1 + p2).

    # we can explore the space of p lengths using a backtracking algorithm
    # which can be outlined as:
    # we'll brute force each pi in p, where pi in [0, N],
    # and quickly abandon any trees that cannot satisfy the constraints above.
    # the function recurses on pj for j>i, except for j=N-1, because p[N-1]=N-sum(h)-sum(p[:-2]).
    # a global counter will increase every time a complete, valid p vector is completed.
    # the worst-case runtime is N!, which is probably better than 2**N for brute-forcing all the integers with a length of N bits.

    # the current state of the recursion is based on:
    # which value of p is being considered: when p[i] is being tested, p[j] for j<i is assumed to be valid and fixed.
    # p[k] for k>i are unknown, but each p[k] > 0 except for p[N-1], so the maximum value for p[i] is given by:
    # M[i] = N - sum(p[j]) - count(p[k]) + 1. With this upper bound on p[i], we'll recurse and brute force all possible values of p[i] in [0, M[i]].

    # Upon entering p[i+1], p[i] is now fixed at some positive integer, so M[i+1] < M[i], which guarantees progress towards some solution(s).
    # With backtracking, we hope that infeasible choices of p[i] can be pruned as quickly as possible.
    # If M[i+1] = 0 and i<N-1, there is no feasible solution.

    1


if __name__ == '__main__':
    consistency_check_tests()
    main()
