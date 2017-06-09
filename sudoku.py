#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import time
import sys
from PIL import Image
import pytesseract

START_TIME = time.time()
THRESHOLD = 100


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = 0
        self.available = []


def init_sudoku(sudoku_image):
    x_delta, y_delta = sudoku_image.size[0] // 9, sudoku_image.size[1] // 9
    sudoku_table = []
    for i in range(81):
        x = i % 9
        y = i // 9
        number_region = (x_delta * x + 20, y_delta * y + 20, x_delta * (x + 1) - 20, y_delta * (y + 1) - 20)
        n = pytesseract.image_to_string(sudoku_image.crop(number_region), config="-psm 10 -l sdlangpro")
        sudoku_table.append(int(n) if n else 0)
    return sudoku_table


def get_row(point, sudoku):
    row = set(sudoku[point.y * 9:(point.y + 1) * 9])
    row.remove(0)
    return row  # set type


def get_col(point, sudoku):
    col = set(sudoku[point.x % 9::9])
    col.remove(0)
    return col  # set type


def get_block(point, sudoku):
    block_x = point.x // 3
    block_y = point.y // 3
    start = block_y * 3 * 9 + block_x * 3
    block = []
    block.extend(sudoku[start: start + 3])
    block.extend(sudoku[start + 9:start + 9 + 3])
    block.extend(sudoku[start + 9 + 9:start + 9 + 9 + 3])
    block_set = set(block)
    block_set.remove(0)
    return block_set  # set type


def is_valid(p, test_value, sudoku):
    return (test_value not in get_row(p, sudoku) and
            test_value not in get_col(p, sudoku) and
            test_value not in get_block(p, sudoku))


def init_point(sudoku):
    point_list = []
    for i, value in enumerate(sudoku):
        if value == 0:
            p = Point(i % 9, i // 9)
            p.available.extend(filter(lambda v: is_valid(p, v, sudoku), range(1, 10)))
            point_list.append(p)
    return point_list


def add_sudoku_point(point):
    sudoku[point.y * 9 + point.x] = point.value


def remove_sudoku_point(point):
    sudoku[point.y * 9 + point.x] = 0


def try_insert(point, sudoku):
    avail_nums = point.available
    for v in avail_nums:
        point.value = v
        if check(point, sudoku):
            add_sudoku_point(point)
            if not point_list:
                return True
            next_point = point_list.pop()
            result = try_insert(next_point, sudoku)
            if result:
                return True
            # Reset the soduku and try the next possible value
            remove_sudoku_point(point)
            point_list.append(next_point)
    else:
        if not point_list:
            # try insert failed after we tried all the points
            return False


def check(p, sudoku):
    if p.value == 0:
        print('not assign value to point p!!')
        return False
    return is_valid(p, p.value, sudoku)


def show_sudoku(sudoku):
    row = ['| '] * 9
    for i in range(9):
        for j in range(9):
            row[i] += str(sudoku[i * 9 + j]) + ' '
            if j % 3 == 2:
                row[i] += '| '
    for i in range(len(row)):
        if i % 3 == 0:
            print('-------------------------')
        print(row[i])
    print('-------------------------\n')


if __name__ == '__main__':
    # sudoku = [
    #    0, 0, 0, 0, 7, 4, 0, 0, 0,
    #    0, 4, 7, 6, 9, 0, 3, 1, 0,
    #    0, 0, 6, 0, 1, 0, 0, 5, 0,
    #    0, 6, 0, 0, 2, 0, 7, 4, 0,
    #    5, 0, 0, 0, 0, 0, 0, 3, 0,
    #    0, 9, 2, 0, 0, 0, 0, 0, 0,
    #    0, 0, 0, 0, 3, 0, 0, 0, 0,
    #    0, 0, 0, 7, 0, 0, 1, 6, 0,
    #    1, 0, 5, 0, 0, 0, 0, 0, 0,
    # ]
    #sudoku_image_name = 'testmap/test1.png'
    if len(sys.argv) == 2:
        sudoku_image_name = sys.argv[1]
    else:
        print('Args ERROR!')
        exit()
    sudoku_box = (50, 430, 1190, 1570)
    original_pic = Image.open(sudoku_image_name).convert('L')
    image_transfer_table = [0 if v < THRESHOLD else 1 for v in range(256)]
    sudoku_image = original_pic.crop(sudoku_box).point(image_transfer_table, '1')
    sudoku = init_sudoku(sudoku_image)
    show_sudoku(sudoku)
    point_list = init_point(sudoku)
    p = point_list.pop()
    try_insert(p, sudoku)
    used_time = time.time() - START_TIME
    show_sudoku(sudoku)
    print('\nuse time: %f s' % (used_time))
