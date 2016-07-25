Goals
=====
- implement a naive and straight forward solution without consulting literature first
- play with ideas and find possible optimizations
- learn how to time code execution in Python
- standard queue of Python seems to be thread-safe, check if own non thread-safe implementation is faster
- check out py.test

Achieved
========
- rather OO-like implementation with a couple of functional implementation details
- timing of expressions with little dependencies is straight forward, timing of entire scripts not so much
- asyncio provides a faster queue than the thread-safe one
- wrote a couple of py.tests

Pending
=======
- could only test minor optimizations, not algorithmic ones
  - for the initial position the first move depends on whether the stack height is even or odd, may be this observation can be generalized to reduce the search space

