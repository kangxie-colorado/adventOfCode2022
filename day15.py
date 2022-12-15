import re
import sys
from multiprocessing import Pool

doneDone = False


def print_matrix(mat, row_start, row_end, col_start, col_end):
    print(f"Columns: {col_start} to {col_end}")
    m, n = len(mat), len(mat[0])
    for j in range(n):
        row = f'{j:< 3}    '
        for i in range(m):
            if col_start <= i <= col_end:
                row = f"{row}{mat[i][j]}"
        if row_start <= j <= row_end:
            print(row)

    print()


def get_blocked_on_line(target_y, filename):
    blocked = set()
    beacon_on_line = set()
    with open(filename) as f:
        for line in f:
            line = line.strip()
            # don't miss the '-' sign
            sensor_x, sensor_y, beacon_x, beacon_y = [int(i) for i in re.findall(r'-*\d+', line)]
            # print(sensor_x, sensor_y, beacon_x, beacon_y)
            if beacon_y == target_y:
                beacon_on_line.add((beacon_x, beacon_y))
            manhattan_dist = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

            delta_y = abs(sensor_y - target_y)
            delta_x = 0
            while delta_y + delta_x <= manhattan_dist:
                blocked.add((sensor_x + delta_x, target_y))
                blocked.add((sensor_x - delta_x, target_y))
                delta_x += 1

    return len(blocked) - len(beacon_on_line)


def find_undetected_coord_naive(filename, max_coord):
    max_coord += 1
    detected = [['.'] * max_coord for _ in range(max_coord)]
    with open(filename) as f:
        for line in f:
            line = line.strip()
            # don't miss the minus sign
            sensor_x, sensor_y, beacon_x, beacon_y = [int(i) for i in re.findall(r'-*\d+', line)]
            if 0 <= sensor_x < max_coord and 0 <= sensor_y < max_coord:
                detected[sensor_x][sensor_y] = 'S'
            if 0 <= beacon_x < max_coord and 0 <= beacon_y < max_coord:
                detected[beacon_x][beacon_y] = 'B'
            manhattan_dist = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

            for dx in range(manhattan_dist + 1):
                for dy in range(manhattan_dist + 1 - dx):
                    for d1, d2 in {(-1, 1), (1, 1), (-1, -1), (1, -1)}:
                        nx, ny = sensor_x + d1 * dx, sensor_y + d2 * dy
                        if 0 <= nx < max_coord and 0 <= ny < max_coord:
                            if detected[nx][ny] == '.':
                                detected[nx][ny] = '#'

    # print_matrix(detected, 0, max_coord, 0, max_coord)
    for x in range(max_coord):
        for y in range(max_coord):
            if detected[x][y] == '.':
                return x * 4000000 + y


# 4M*4M which is 16 Trillion
# look like I'd better get it done with multiple processing
# also the memory will not be enough
# okay... so probably I could deal with sub-matrix
# dealing with 1000*1000 sub matrix
class Solution:
    def __init__(self):
        self.sensors = set()
        self.beacons = set()
        self.sensorMap = {}

    def worker2(self, config):
        # okay.. it is not that good just to lie at the mh+1 for all the sensors
        # this is not logically complete
        print(config)
        # print(self.sensors)
        x_start, y_start, l = config
        undetected = []

        for sx, sy, mh in self.sensors:
            sensor_undetectable = set()
            for dx in range(mh + 2):
                dy = mh + 1 - dx
                for d1, d2 in {(-1, 1), (1, 1), (-1, -1), (1, -1)}:
                    nx, ny = sx + d1 * dx, sy + d2 * dy
                    if x_start <= nx < x_start + l and y_start <= ny < y_start + l:
                        sensor_undetectable.add((nx, ny))
            undetected.append(sensor_undetectable)

        set1 = undetected[0]
        for i in range(1, len(undetected)):
            set1 = set1.intersection(undetected[i])

        print(set1)

    def worker(self, config):
        print(config)
        # print(self.sensors)
        x_start, y_start, l = config
        matrix = [[0] * l for _ in range(l)]
        counted = 0

        for x in range(l):
            for y in range(l):
                x_coord = x + x_start
                y_coord = y + y_start

                if matrix[x][y] == 0:
                    for sx, sy, mh in self.sensors:
                        if abs(x_coord - sx) + abs(y_coord - sy) <= mh:
                            matrix[x][y] = 1
                            counted += 1
                            break

        if counted == l * l:
            return

        for x in range(l):
            for y in range(l):
                if matrix[x][y] == 0:
                    with open('day15.txt', 'a+') as f:
                        print(x + x_start, y + y_start, file=f)
                        global doneDone
                        doneDone = True
                        print("FOUND!!!!")

                    # return (x + x_start) * 4000000 + y + y_start
        # print_matrix(matrix, 0, 999, 0, 999)
        # return None

    def get_sensors_beacons(self, filename):
        with open(filename) as f:
            for line in f:
                line = line.strip()
                # don't miss the minus sign
                sensor_x, sensor_y, beacon_x, beacon_y = [int(i) for i in re.findall(r'-*\d+', line)]
                manhattan_dist = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
                self.sensors.add((sensor_x, sensor_y, manhattan_dist))
                self.sensorMap[(sensor_x, sensor_y)] = manhattan_dist
                self.beacons.add((beacon_x, beacon_y))

    def find_undetected_coord(self, filename, max_coord):
        # using multiple processing
        l = 2000
        # we can deal with first row and first column separately if needed
        # x_start = y_start = 1
        workload_configs = []
        for x_scale in range(0, max(1, max_coord // l)):
            for y_scale in range(0, max(1, max_coord // l)):
                x_start = x_scale * l + 1
                y_start = y_scale * l + 1
                # res = worker(x_start, y_start, min(l, max_coord))
                workload_configs.append((x_start, y_start, min(l, max_coord)))

        import random
        random.shuffle(workload_configs)
        with Pool(processes=4) as pool:
            if not doneDone:
                pool.map(self.worker, workload_configs)

    def find_that_coord(self, max_coord):
        range_by_row = {row: [(0, max_coord + 1)] for row in range(max_coord + 1)}  # uncovered range: [start,end)
        for sx, sy, mh in self.sensors:
            # if sx == 16 and sy == 7:
            #     # for debug
            #     a = 0
            for row, ranges in range_by_row.items():
                new_ranges = ranges
                if sy - mh <= row <= sy + mh:
                    # inside my cover range horizontally/vertically
                    new_ranges = []
                    for start, end in ranges:
                        # x is col remember; y is row
                        # abs(sx - col) is now <= mh; abs(sy - row) is now <= mh
                        # the d_row will be below
                        # the range will sy-d_row:sy+d_row (sx-d_col, sx+d_col), do I want to use equal value for point?
                        # maybe still left close and right open
                        d_col = mh - abs(sy - row)
                        # so between [sy-d_row, col] and [sy+d_row, col], this interval is blocked
                        # they could overlap/contain/miss-each-other, this should handle all scenarios
                        if start < min(sx - d_col, end):
                            # sx - d_col should be blocked, so it can act as end
                            new_ranges.append([start, min(sx - d_col, end)])
                        if max(sx + d_col, start) < end:
                            # sx + d_col should be blocked, so it can not act as start, must + 1
                            new_ranges.append([max(sx + d_col + 1, start), end])
                range_by_row[row] = new_ranges

        for row, ranges in range_by_row.items():
            # row_string = f'{row:<3}'
            # row_arr = ['#'] * (max_coord + 1)
            # for start, end in ranges:
            #     for i in range(start, end):
            #
            # row_string = f"{row_string} {''.join(row_arr)}"
            # print(row_string)
            if ranges:
                print(row, ranges)
        print()


if __name__ == '__main__':
    input_file = 'day15_sample.txt'
    print(get_blocked_on_line(10, input_file))
    S = Solution()
    S.get_sensors_beacons(input_file)
    # S.find_undetected_coord(input_file, 20)
    S.find_that_coord(20)

    input_file = 'day15_input.txt'
    print(get_blocked_on_line(2000000, input_file))
    S = Solution()
    S.get_sensors_beacons(input_file)
    # S.find_undetected_coord(input_file, 20)
    S.find_that_coord(4000000)
