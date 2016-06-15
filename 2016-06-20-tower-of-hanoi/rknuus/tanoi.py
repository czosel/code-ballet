#!/usr/bin/env python


# TODO(KNR): enforce Python 3

import argparse
import asyncio
import copy
import itertools
import sys
import timeit


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

    @staticmethod
    def _can_move(source, target):
        return (not target or source[-1] < target[-1])

    def moves(self):
        # TODO(KNR): factor out duplicate code, need to put all list members into a list of lists or a tuple
        if self._home:
            if Tower._can_move(source=self._home, target=self._interim):
                tower = copy.deepcopy(self)
                tower._interim.append(tower._home.pop())
                yield tower
            if Tower._can_move(source=self._home, target=self._target):
                tower = copy.deepcopy(self)
                tower._target.append(tower._home.pop())
                yield tower
        if self._interim:
            if Tower._can_move(source=self._interim, target=self._home):
                tower = copy.deepcopy(self)
                tower._home.append(tower._interim.pop())
                yield tower
            if Tower._can_move(source=self._interim, target=self._target):
                tower = copy.deepcopy(self)
                tower._target.append(tower._interim.pop())
                yield tower
        if self._target:
            if Tower._can_move(source=self._target, target=self._home):
                tower = copy.deepcopy(self)
                tower._home.append(tower._target.pop())
                yield tower
            if Tower._can_move(source=self._target, target=self._interim):
                tower = copy.deepcopy(self)
                tower._interim.append(tower._target.pop())
                yield tower

    def is_solved(self):
        # Because the total number of disks remains constant, it's enough to
        # check whether home and interim are empty
        return (self._home == [] and self._interim == [])

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
        queue = asyncio.Queue()
        tower = Tower(height=self._height)
        # TODO(KNR): only works for really small heights
        # TODO(KNR): is it faster to use a set to keep track of all seen towers?
        seen = {}
        queue.put_nowait(tower)
        seen[tower] = [tower]
        positions = 0
        while not queue.empty():
            tower = queue.get_nowait()
            positions += 1
            if tower.is_solved():
                track = seen[tower]
                solution = 'solution has {0} moves (searched {1} positions):\n'.format(len(track)-1, positions)
                solution += '\n{0}\n\n\n'.format('=' * 3 * (3 + tower._get_column_width(self._height))).join(str(b) for b in track)
                return solution
            for move in tower.moves():
                # Because we use breadth first search we don't have to cover the case
                # that we have seen an intermediate tower but got a shorter track later on.
                if move not in seen:
                    queue.put_nowait(move)
                    track = copy.deepcopy(seen[tower])
                    track.append(move)
                    seen[move] = track
        print('Done, let\'s pray.')


def main(args):
    arguments = argparse.ArgumentParser()
    arguments.add_argument('height', type=int, help='height of the tower')
    arguments.add_argument('--timeit', action='store_true', help='print timing information')
    args = arguments.parse_args()
    if args.timeit:
        print(timeit.timeit('priests.transfer()', number=5, setup='from __main__ import Priests; priests = Priests({0})'.format(args.height), globals=globals()),
              ' (for 5 runs)')
    else:
        priests = Priests(height=args.height)
        solution = priests.transfer()
        print(solution)


if __name__ == "__main__":
    main(args=sys.argv)
