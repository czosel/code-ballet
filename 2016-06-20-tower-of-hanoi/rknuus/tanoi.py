#!/usr/bin/env python


# TODO(KNR): enforce Python 3

import copy
import itertools


# TODO(KNR): replace by built-in queue and test performance
class Queue(object):
    def __init__(self):
        self._items = []

    def __bool__(self):
        return bool(self._items)

    def enqueue(self, item):
        self._items.insert(0, item)

    def dequeue(self):
        return self._items.pop()


class Board(object):
    def __init__(self, parent):
        # TODO(KNR): it shouldn't matter whether we store a pointer to parent or the height
        self._parent = parent
        # TODO(KNR): replace lists by numbers and set bits for the disks, measure memory and runtime performance
        self._home = list(reversed(range(0, self._parent.height())))
        self._interim = []
        self._target = []

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and other._home == self._home and
                other._interim == self._interim and other._target == self._target)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash('a'+str(self._home)) ^ hash('b'+str(self._interim)) ^ hash('c'+str(self._target))

    def moves(self):
        if self._home:
            if not self._interim or self._home[-1] < self._interim[-1]:
                board = copy.deepcopy(self)
                board._interim.append(board._home.pop())
                yield board
            if not self._target or self._home[-1] < self._target[-1]:
                board = copy.deepcopy(self)
                board._target.append(board._home.pop())
                yield board
        if self._interim:
            if not self._home or self._interim[-1] < self._home[-1]:
                board = copy.deepcopy(self)
                board._home.append(board._interim.pop())
                yield board
            if not self._target or self._interim[-1] < self._target[-1]:
                board = copy.deepcopy(self)
                board._target.append(board._interim.pop())
                yield board
        if self._target:
            if not self._home or self._target[-1] < self._home[-1]:
                board = copy.deepcopy(self)
                board._home.append(board._target.pop())
                yield board
            if not self._interim or self._target[-1] < self._interim[-1]:
                board = copy.deepcopy(self)
                board._interim.append(board._target.pop())
                yield board

    def is_solved(self):
        # TODO(KNR): creating range over and over again is wasteful
        # TODO(KNR): it's an invariant, that the total number of disks remains constant, so
        # can check home and interim only (or target only), check performance
        return (self._home == [] and self._interim == [] and self._target == list(reversed(range(0, self._parent.height()))))

    # TODO(KNR): is there a simpler and more elegant way?
    def _pad_stack(self, stack):
        pad = [-1] * self._parent.height()
        pad.extend(reversed(stack))
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
        queue = Queue()
        board = Board(parent=self)
        # TODO(KNR): only works for really small heights
        seen = {}
        queue.enqueue(board)
        seen[board] = [board]
        assert board in seen
        solution = 1
        while queue:
            board = queue.dequeue()
            if board.is_solved():
                track = seen[board]
                print('solution {0} with {1} moves:\n'.format(solution, len(track)-1))
                print('\n{0}\n\n\n'.format('=' * 3 * (3 + Board._get_column_width(self._height))).join(str(b) for b in track))  # TODO(KNR): return or yield
                solution += 1
            for move in board.moves():
                if move not in seen:
                    queue.enqueue(move)  # TODO(KNR): if current track is shorter, remove move from queue before adding it again
                    track = copy.deepcopy(seen[board])
                    track.append(move)
                    seen[move] = track
                    assert move in seen
        print('done')


def main():
    # TODO(KNR): replace height by command line argument
    moves = Moves(2)
    moves.solve()


if __name__ == "__main__":
    main()
