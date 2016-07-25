===================================
Stable Marriage Problem Code-Ballet
===================================

This_ is the problem to solve: https://www.youtube.com/watch?v=Qcv1IqHWAzg

How to conduct a code-ballet_

.. _this: https://www.youtube.com/watch?v=Qcv1IqHWAzg

.. _code-ballet: https://github.com/adfinis-sygroup/code-ballet/blob/master/README.rst

Constraints
===========

* Python, python and python-only, which makes it much easier to compare and
  comment on solutions

* Implement a generic solution that accepts configurations as input or generates
  configurations automatically

* Jupyter_ notebooks are most welcome, but please write a requirements.txt, so
  the notebook runs without errors

.. _Jupyter: http://jupyter.org/

Problems
========

We have a whole bunch of problems for you to solve, you can solve any one or all
as you wish:

Declaration
-----------

Define the problem with some formalism. Either the general goal of stable
marriages or the result of the described algorithm: Every woman has the best
possible match and every man the worst possible.

Solver
------

* Use a solver or optimizer to solve the problem
  
  * If you defined the general goal, you probably need some generic optimizer like
    genetic algorithms

  * If you defined the result of the algorithm classic solvers or optimizers_
    might work

* Or write a solver

.. _optimizers: http://docs.scipy.org/doc/scipy/reference/optimize.html

Algorithm
---------

* Implement the algorithm functional

* Implement the algorithm iterative

Elaboration / Proof
-------------------

* Elaborate on the marriage problem, find extensions, new properties and try to
  prove them

  * i.e. there are (no) other solutions than the above algorithm found
    
    * If you used an optimizer you've probably already proven that

  * i.e. there are fair solutions (define fair)

    * There is a algorithm to find fair solutions

    * There is a single fairest solution (maybe only interesting if fairness is
      an integer)

    * There is good optimizer to find fair solutions (by doing it)

  * Other properties?

  * Proof by contradiction by finding a contradicting example: using
    hypothesis_, genetic algorithms, optimizers, solvers or what you like

  * Prove it by using SymPy_ or any other maths tool

* Solve halting problem on this

About this section: We actually have no clue what we are taking about :-) Since
we are no mathematicians we need to try this ideas ourself to get a notion
whether the idea makes sense: Maybe there is nothing beyond what was said in the
video.

.. _hypothesis: http://hypothesis.works
.. _SymPy: http://www.sympy.org/
