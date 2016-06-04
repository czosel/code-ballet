==============
Tower of hanoi
==============

First I evolve the tower of hanoi from a simple print() based solution to a
pure-functional-memoized solution, showing the power of dynamic programming.
Then I try to solve hanoi(1000) which fails because of maximum recursion depth.
So I evolve a stack_machine()-based solution (with a infinite stack) and finally
we can solve hanoi(2000) in under 0.04s.

To study the code, have the output of tower-of-hanoi.py and the source side by
side.

I wonder - is there a way to solve hanoi(2000) with python using dynamic
programming without a stack-machine? All my attempts to change iterative
solutions to make them memoizable ended in solutions that had a stack, so in the
end I preferred the somewhat awkward but generic solution using the
stack_machine().

Stack overflows really seem to be a fundamental problem in dynamic-programming.
