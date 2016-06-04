import collections
import pyrsistent
from hypothesis import given
from hypothesis import strategies as st

Move = collections.namedtuple('Move', ('src', 'dst'))


class Frame(object):
    __slots__ = (
        'frames',
        'ret',
        'args',
        'kwargs',
    )

    def __init__(self, *args, **kwargs):
        self.frames = ()
        self.ret    = None
        self.args   = args
        self.kwargs = kwargs

# #### Helpers #####


def memoize_info(func):
    print(
        "%s cache hit-ratio count=%d, miss=%d, ratio=%f" % (
            func.func.__name__,
            func.count,
            func.miss,
            float(func.count - func.miss) / func.count
        )
    )


def move_print(move):
    print(" * %s " % repr(move))


def memoize(function):
    """Caching results of a function"""

    def memoizer(*args, **kwargs):
        """Memoize helper"""
        cache = memoizer.cache
        memoizer.count += 1
        key = (args, frozenset(kwargs))
        res = cache.get(key)
        if res is None:
            memoizer.miss += 1
            res = function(*args, **kwargs)
            cache[key] = res
        return res

    def clear():
        memoizer.cache = {}
        memoizer.count = 0
        memoizer.miss = 0
    memoizer.func = function
    memoizer.clear = clear
    clear()
    return memoizer


def traverse(structure, leave=Move, flat=pyrsistent.pvector()):
    for item in structure:
        if isinstance(item, leave):
            flat = flat.append(item)
        else:
            flat = traverse(item, leave, flat)
    return flat


def stack_machine(f_func, f_result, *args, **kwargs):
    stack = []
    visit = []
    stack.append(Frame(*args, **kwargs))

    try:
        while True:
            frame = stack.pop()
            visit.append(frame)
            cont, new_frames = f_func(frame, *frame.args, **frame.kwargs)
            frame.frames = new_frames
            if cont:
                stack.extend(new_frames)
    except IndexError:
        pass

    try:
        while True:
            frame = visit.pop()
            f_result(frame, *frame.args, **frame.kwargs)
    except IndexError:
        pass

    return frame.ret

# #### Hanoi evolution #####


def print_hanoi(n, src=0, dst=2, tmp=1):
    if n < 1:
        return
    print_hanoi(n - 1, src, tmp, dst)
    move_print(Move(src, dst))
    print_hanoi(n - 1, tmp, dst, src)


def recursive_hanoi(n, src=0, dst=2, tmp=1):
    if n < 1:
        return ()
    return (
        recursive_hanoi(n - 1, src, tmp, dst),
        Move(src, dst),
        recursive_hanoi(n - 1, tmp, dst, src),
    )


@memoize
def memoize_hanoi(n, src=0, dst=2, tmp=1):
    if n < 1:
        return ()
    return (
        memoize_hanoi(n - 1, src, tmp, dst),
        Move(src, dst),
        memoize_hanoi(n - 1, tmp, dst, src),
    )


def machine_hanoi(n, src=0, dst=2, tmp=1):

    end = Frame()
    end.ret = ()

    def hanoi(frame, n, src, dst, tmp):
        if n < 1:
            return False, (end, end)
        return True, (
            Frame(n - 1, src, tmp, dst),
            Frame(n - 1, tmp, dst, src),
        )

    def result(frame, n, src, dst, tmp):
        frame.ret = (
            frame.frames[0].ret,
            Move(src, dst),
            frame.frames[1].ret,
        )

    return stack_machine(
        hanoi,
        result,
        n,
        src=src,
        dst=dst,
        tmp=tmp,
    )


print("""
===================
The hanoi evolution
===================

print_hanoi(4)
==============

The standard stuff with side-effects.
""".strip())
print("\n")

print_hanoi(4)

print("\n")
print("""
recursive_hanoi(4)
==================

Basic pure-functional hanoi as seen on haskell-TV.
""".strip())
print("\n")

list(map(
    move_print,
    traverse(
        recursive_hanoi(4)
    )
))


print("\n")
print("""
memoize_hanoi(100)
==================

Pure-functional hanoi with memoize.
""".strip())
print("\n")
memoize_hanoi(100)
memoize_info(memoize_hanoi)

print("\n")
print("""
memoize_hanoi(1000)
===================

Deep pure-functional hanoi with memoize.

-> RecursionError: maximum recursion depth exceeded in comparison

Now we have to modify the stack that we reach base caches early. But this time
it is actually impossible because our base-case is defined by stack-depth. So
lets try to build a generic stack machine as a higher-order function.
""".strip())

# memoize_hanoi(1000)

print("\n")
print("""
machine_hanoi(4)
================

stack machine based hanoi.
""".strip())
print("\n")

list(map(
    move_print,
    traverse(
        machine_hanoi(3)
    )
))


# #### Tests #####


@given(st.integers(0, 14))
def test_basic_solotions(disks):
    rec = recursive_hanoi(disks)
    mem = memoize_hanoi(disks)
    assert rec == mem

test_basic_solotions()
