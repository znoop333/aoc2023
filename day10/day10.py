import numpy as np
from collections import defaultdict, deque
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
               '.': [],
               }

    # 'S' is very special! it can connect to two pipes in any direction, but only if the target direction is a valid
    # connector. e.g., if 'S' is acting like 'F', it can connect on the right to '7', '-', 'J', but not 'L', '|', or '.'
    # I'll check this requirement for all nodes, even though only 'S' really requires it if the graph is valid.
    # an invalid graph might have something like 'LLL' which should be illegal because adjacent 'L' cannot connect.

    valid_targets = {
        (0, 1): ['7', '-', 'J'],
        (0, -1): ['L', '-', 'F'],
        (1, 0): ['L', '|', 'J'],
        (-1, 0): ['7', '|', 'F'],
    }

    for dr, dc in offsets[node]:
        ii = row + dr
        jj = col + dc
        if 0 <= ii < height and 0 <= jj < width and graph[ii, jj] in valid_targets[(dr, dc)]:
            yield graph[ii, jj], ii, jj


def floodfill(graph: np.array) -> int:
    height, width = graph.shape
    # we'll keep track of both which nodes have been visited and their distances using a new matrix, rather than
    # modifying the existing one in-place. This sacrifices memory in favor of speed.
    unvisited_dist = -1
    dist = unvisited_dist * np.ones((height, width), dtype=int)
    seed_r, seed_c = np.argwhere(graph == 'S')[0]
    dist[seed_r, seed_c] = 0

    q = deque()
    for ng, nr, nc in neighbors4(seed_r, seed_c, graph):
        q.append((nr, nc, 1))

    while len(q):
        node_r, node_c, node_d = q.popleft()
        if dist[node_r, node_c] == unvisited_dist:
            dist[node_r, node_c] = node_d
        else:
            dist[node_r, node_c] = min(dist[node_r, node_c], node_d)

        for ng, nr, nc in neighbors4(node_r, node_c, graph):
            prev_unvisited = dist[nr, nc] == unvisited_dist
            if prev_unvisited:
                q.append((nr, nc, node_d + 1))

    return np.max(dist), dist


def clean_graph(graph: np.array, dist: np.array) -> np.array:
    # get rid of all junk tiles. if any pipe tile was not reachable from 'S', it's junk.
    unvisited_dist = -1
    unvisited_r, unvisited_c = np.nonzero(dist == unvisited_dist)
    print_graph(graph)
    # print_graph(dist)
    for ii in range(len(unvisited_r)):
        graph[unvisited_r[ii], unvisited_c[ii]] = '.'

    print('After cleaning: ')
    print_graph(graph)

    return graph


def print_graph(graph: np.array):
    height, width = graph.shape
    s = ''
    for ii in range(height):
        s += ''.join(graph[ii, :]) + '\n'
    print(s)


def pad_graph(graph: np.array) -> np.array:
    # to make this easier to reason about, I'll pad in-between tiles so that all "exterior" regions are connected.

    # padding in-between tiles:
    # left-right: '-x' tiles become '--x' (extend the pipe left-right) for any other 'x' character (not '-')
    # 'Fx' becomes 'F-x', 'Lx' -> 'L-x', 'x7' -> 'x-7', 'xJ' -> 'x-J'
    # any other left-right characters 'xy' pad to 'x*y'. '*' will be used in the flood fill, but doesn't count as '.'

    height, width = graph.shape
    lr_padded = np.empty((height, 2 * width), dtype='<U1')
    for c in range(0, width, 2):
        lr_padded[:, 2 * c] = graph[:, c]
        for r in range(height):
            if graph[r, c] in ('F', 'L', '-') or graph[r, c + 1] in ('7', 'J'):
                lr_padded[r, 2 * c + 1] = '-'
            else:
                lr_padded[r, 2 * c + 1] = ' '

    # vertical padding is similar: additional '|' characters are used to extend the pipes, and other areas
    # are filled in with '*'.
    padded = np.empty((2 * height, 2 * width), dtype='<U1')
    for r in range(0, height, 2):
        lr_padded[2 * r, :] = graph[r, :]
        for c in range(width):
            if graph[r, c] in ('F', '7', '|') or graph[r, c + 1] in ('L', 'J'):
                lr_padded[2 * r + 1, c] = '|'
            else:
                lr_padded[2 * r + 1, c] = ' '

    # I'll also pad 1 tile around all edges, which will connect any islands created by the pipe cutting all
    # the way across the graph.
    graph = np.pad(padded, (1, 1), mode='constant', constant_values=(' ', ' '))

    return graph


def main():
    # with open("input.txt", "r") as f:
    # with open("test_input.txt", "r") as f:
    with open("test_input3.txt", "r") as f:
        input = f.read()

    graph = parse_input(input)
    answer, dist = floodfill(graph)
    graph = clean_graph(graph, dist)
    graph = pad_graph(graph)
    print_graph(graph)

    print(f'The answer is {answer}.')


if __name__ == '__main__':
    main()
