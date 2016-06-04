import collections
import pyrsistent
from hypothesis import given
from hypothesis import strategies as st

Move = collections.namedtuple('Move', ('src', 'dst'))

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

# #### Tests #####


@given(st.integers(0, 14))
def test_basic_solotions(disks):
    rec = recursive_hanoi(disks)
    mem = memoize_hanoi(disks)
    assert rec == mem

test_basic_solotions()
