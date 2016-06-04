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


class Stack(object):
    def __init__(self):
        self._items = []

    def __bool__(self):
        return bool(self._items)

    def push(self, item):
        self._items.push(item)

    def pop(self):
        return self._items.pop()


class Board(object):
    @classmethod
    def start(cls, height):
        # TODO(KNR): bad idea to use "global" variable, on the other hand
        # each Board represents just a single state during the game, so
        # we probably lack a parent type
        cls._height = height  # actually equals to len(home) + len(interim) + len(target)
        return Board(range(0, height), [], [])

    def __init__(self, home, interim, target):
        self._home = home
        self._interim = interim
        self._target = target

    def moves(self):
        pass

    def is_solved(self):
        # TODO(KNR): creating range over and over again is wasteful
        return (self._home == [] and self._interim == [] and self._target == range(0, Board._height))

    @staticmethod
    def _pad_stack(stack):
        pad = [-1] * Board._height
        pad.extend(stack)
        return pad[-Board._height:]

    @staticmethod
    def _get_column_width(disk):
        return 1 + (disk) * 2

    @staticmethod
    def _get_row(a, b, c):
        column_width = Board._get_column_width(Board._height) + 2  # add padding
        return (('-' * Board._get_column_width(a)).center(column_width) + '|' +
                ('-' * Board._get_column_width(b)).center(column_width) + '|' +
                ('-' * Board._get_column_width(c)).center(column_width))

    def __str__(self):
        return '\n'.join(Board._get_row(a, b, c) for a, b, c in
                         itertools.zip_longest(Board._pad_stack(self._home),
                                               Board._pad_stack(self._interim),
                                               Board._pad_stack(self._target),
                                               fillvalue=-1))


def solve(n):
    initial = Board.start(n)
    queue = Queue()
    queue.enqueue(initial)
    while queue:
        board = queue.dequeue()
        if board.is_solved():
            print(board)
            break
        for move in board.moves():
            queue.enqueue(move)
