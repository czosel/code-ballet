#!/usr/bin/env python


# TODO(KNR): enforce Python 3

import itertools


class Queue(object):
    def __init__(self):
        self._items = []

    def __bool__(self):
        return bool(self._items)

    def enqueue(self, item):
        self._items.insert(0, item)

    def dequeue(self):
        return self._items.pop()


# class Stack(object):
#     def __init__(self):
#         self._items = []

#     def __bool__(self):
#         return bool(self._items)

#     def push(self, item):
#         self._items.push(item)

#     def pop(self):
#         return self._items.pop()


class Board(object):
    def __init__(self, parent):
        self._parent = parent
        self._home = range(0, self._parent.height())
        self._interim = []
        self._target = []

    def moves(self):
        pass

    def is_solved(self):
        # TODO(KNR): creating range over and over again is wasteful
        return (self._home == [] and self._interim == [] and self._target == range(0, self._parent.height()))

    def _pad_stack(self, stack):
        pad = [-1] * self._parent.height()
        pad.extend(stack)
        return pad[-self._parent.height():]

    @staticmethod
    def _get_column_width(disk):
        return 1 + (disk) * 2

    def _get_row(self, a, b, c):
        column_width = Board._get_column_width(self._parent.height()) + 2  # add padding
        return (('-' * Board._get_column_width(a)).center(column_width) + '|' +
                ('-' * Board._get_column_width(b)).center(column_width) + '|' +
                ('-' * Board._get_column_width(c)).center(column_width))

    def __str__(self):
        return '\n'.join(self._get_row(a, b, c) for a, b, c in
                         itertools.zip_longest(self._pad_stack(self._home),
                                               self._pad_stack(self._interim),
                                               self._pad_stack(self._target),
                                               fillvalue=-1))


class Moves(object):
    def __init__(self, height):
        self._height = height

    def height(self):
        return self._height

    def solve(self):
        initial = Board.start(self, self._height)
        queue = Queue()
        queue.enqueue(initial)
        while queue:
            board = queue.dequeue()
            if board.is_solved():
                print(board)
                break
            for move in board.moves():
                queue.enqueue(move)
