from collections import deque
from typing import Deque


def get_matrix(filename):
    return open(filename).read().split('\n')


def shortest_path(mat, multi_starting=False):
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    m, n = len(mat), len(mat[0])
    res = 100000000
    for r in range(m):
        for c in range(n):
            if (not multi_starting and mat[r][c]) == 'S' or (multi_starting and mat[r][c] in 'aS'):
                q = [(r, c, 0)]
                visited = set()
                while q:
                    x, y, steps = q[0]
                    q = q[1:]

                    if mat[x][y] == 'E':
                        res = min(res, steps)

                    if (x, y) in visited:
                        continue
                    visited.add((x, y))

                    curr = mat[x][y]
                    if curr == 'S':
                        curr = 'a'

                    for dx, dy in dirs:
                        nx, ny = dx + x, dy + y
                        if 0 <= nx < m and 0 <= ny < n:
                            newC = mat[nx][ny]
                            if mat[nx][ny] == 'E':
                                newC = 'z'
                            if ord(newC) <= ord(curr) + 1:
                                q.append((nx, ny, steps + 1))

    return res if res < 100000000 else -1


# some algorithm make it faster
def shortest_path(mat, multi_starting=False):
    def search(q: Deque):
        visited = set()
        while q:
            count = len(q)
            while count:
                x, y, step = q.popleft()
                if mat[x][y] == 'E':
                    return step

                if (x, y) in visited:
                    continue
                visited.add((x, y))

                curr = mat[x][y]
                if curr == 'S':
                    curr = 'a'
                for dx, dy in dirs:
                    nx, ny = dx + x, dy + y
                    if 0 <= nx < m and 0 <= ny < n:
                        newC = mat[nx][ny]
                        if mat[nx][ny] == 'E':
                            newC = 'z'
                        if ord(newC) <= ord(curr) + 1:
                            q.append((nx, ny, step + 1))
                count -= 1
        return -1

    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    m, n = len(mat), len(mat[0])
    q = deque()
    for r in range(m):
        for c in range(n):
            if not multi_starting and mat[r][c] == 'S':
                q.append((r, c, 0))
                return search(q)
            if multi_starting and mat[r][c] in 'aS':
                q.append((r, c, 0))
    return search(q)


# turn it into some DAG search using indegrees
# okay.. cannot do that -- it can travel to equal or lower spots
# not a DAG
# def shortest_path(mat, multi_starting=False):
#     ...


if __name__ == '__main__':
    input_file = 'day12_sample.txt'
    mat = get_matrix(input_file)
    print(shortest_path(mat))
    print(shortest_path(mat, multi_starting=True))

    input_file = 'day12_input.txt'
    mat = get_matrix(input_file)
    print(shortest_path(mat))
    print(shortest_path(mat, multi_starting=True))
