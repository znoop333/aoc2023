import numpy as np
from collections import defaultdict
from math import prod, sqrt, floor, ceil


def parse_input(input: str):
    first_line = input.split()[0]
    width = len(first_line)
    height = len(input.split())
    graph = np.array([ch for ln in input.split() for ch in ln])
    graph = graph.reshape([height, width])
    return graph


def neighbors4(row: int, col: int, graph: np.array):
    # yield the in-bounds 4-connectivity neighbors for any position [row,col] in a 2d grid
    height, width = graph.shape
    node = graph[row][col]

    offsets = {'F': [(0, 1), (1, 0)],
               '7': [(0, -1), (1, 0)],
               'J': [(0, -1), (-1, 0)],
               'L': [(0, 1), (-1, 0)],
               '-': [(0, 1), (0, -1)],
               '|': [(-1, 0), (1, 0)],
               'S': [(-1, 0), (1, 0), (0, 1), (0, -1)],
               }

    # 'S' is very special!

    for dr, dc in offsets[node]:
        ii, jj = row + dr, col + dc
        if 0 <= ii < width and 0 <= jj < height:
            yield graph[ii, jj], ii, jj


def main():
    # with open("input.txt", "r") as f:
    with open("test_input.txt", "r") as f:
        input = f.read()

    graph = parse_input(input)
    answer = 0

    print(f'The answer is {answer}.')


if __name__ == '__main__':
    main()
