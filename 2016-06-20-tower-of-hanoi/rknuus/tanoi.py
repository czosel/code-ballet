#!/usr/bin/env python


# TODO(KNR): enforce Python 3

import argparse
import copy
import itertools
import sys


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


class Tower(object):
    def __init__(self, height):
        self._height = height
        # TODO(KNR): replace lists by numbers and set bits for the disks, measure memory and runtime performance
        self._home = list(reversed(range(0, self._height)))
        self._interim = []
        self._target = []

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and other._home == self._home and
                other._interim == self._interim and other._target == self._target)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        # Lists are not hashable, so convert them to strings.
        # Avoid that Towers with swapped lists generate the same hash by salting each list.
        return hash('a'+str(self._home)) ^ hash('b'+str(self._interim)) ^ hash('c'+str(self._target))

    def moves(self):
        # TODO(KNR): factor out duplicate code
        if self._home:
            if not self._interim or self._home[-1] < self._interim[-1]:
                Tower = copy.deepcopy(self)
                Tower._interim.append(Tower._home.pop())
                yield Tower
            if not self._target or self._home[-1] < self._target[-1]:
                Tower = copy.deepcopy(self)
                Tower._target.append(Tower._home.pop())
                yield Tower
        if self._interim:
            if not self._home or self._interim[-1] < self._home[-1]:
                Tower = copy.deepcopy(self)
                Tower._home.append(Tower._interim.pop())
                yield Tower
            if not self._target or self._interim[-1] < self._target[-1]:
                Tower = copy.deepcopy(self)
                Tower._target.append(Tower._interim.pop())
                yield Tower
        if self._target:
            if not self._home or self._target[-1] < self._home[-1]:
                Tower = copy.deepcopy(self)
                Tower._home.append(Tower._target.pop())
                yield Tower
            if not self._interim or self._target[-1] < self._interim[-1]:
                Tower = copy.deepcopy(self)
                Tower._interim.append(Tower._target.pop())
                yield Tower

    def is_solved(self):
        # TODO(KNR): creating range over and over again is wasteful
        # TODO(KNR): it's an invariant, that the total number of disks remains constant, so
        # can check home and interim only (or target only), check performance
        return (self._home == [] and self._interim == [] and self._target == list(reversed(range(0, self._height))))

    # TODO(KNR): is there a simpler and more elegant way?
    def _pad_stack(self, stack):
        pad = [-1] * self._height
        pad.extend(reversed(stack))
        return pad[-self._height:]

    @staticmethod
    def _get_column_width(disk):
        return 1 + (disk) * 2

    def _get_row(self, a, b, c):
        column_width = Tower._get_column_width(self._height) + 2  # add padding
        return (('-' * Tower._get_column_width(a)).center(column_width) + '|' +
                ('-' * Tower._get_column_width(b)).center(column_width) + '|' +
                ('-' * Tower._get_column_width(c)).center(column_width))

    def __str__(self):
        return '\n'.join(self._get_row(a, b, c) for a, b, c in
                         itertools.zip_longest(self._pad_stack(self._home),
                                               self._pad_stack(self._interim),
                                               self._pad_stack(self._target),
                                               fillvalue=-1))


class Priests(object):
    def __init__(self, height):
        self._height = height

    def transfer(self):
        queue = Queue()
        tower = Tower(height=self._height)
        # TODO(KNR): only works for really small heights
        # TODO(KNR): is it faster to use a set to keep track of all seen towers?
        # To keep track of all intermediate towers and the tracks to get there.
        seen = {}
        queue.enqueue(tower)
        seen[tower] = [tower]
        while queue:
            tower = queue.dequeue()
            if tower.is_solved():
                track = seen[tower]
                print('solution has {0} moves:\n'.format(len(track)-1))
                print('\n{0}\n\n\n'.format('=' * 3 * (3 + tower._get_column_width(self._height))).join(str(b) for b in track))  # TODO(KNR): return or yield
                # Exercise for the reader: prove that there is one and only one shortest solution
                break
            for move in tower.moves():
                # Probably because we use breadth first search we don't have to cover the case
                # that we have seen an intermediate tower but got a shorter track later on.
                if move not in seen:
                    queue.enqueue(move)
                    track = copy.deepcopy(seen[tower])
                    track.append(move)
                    seen[move] = track
        print('done')


def main(args):
    arguments = argparse.ArgumentParser()
    arguments.add_argument('height', type=int, help='height of the tower')
    args = arguments.parse_args()
    priests = Priests(height=args.height)
    priests.transfer()


if __name__ == "__main__":
    main(args=sys.argv)
