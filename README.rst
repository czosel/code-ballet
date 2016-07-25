===========
Code Ballet
===========

`PAST CODE BALLET SOLUTIONS`_

.. _`PAST CODE BALLET SOLUTIONS`: https://github.com/adfinis-sygroup/code-ballet/pulls?q=is%3Apr+is%3Aclosed+label%3Aballet

Having a background in maths and functional-programming helps a lot writing good
code. I know this when I see what `David McIver`_ does. Most of us do not have that
background and learning only by reading and toying with what you read isn't
effective. Going all mental and doing everything in Haskell isn't a solution
either.

.. _`David McIver`: http://hypothesis.works

So I decided to do a mothly-ish puzzle to flex our maths-muscles. It is like
code-golf_, but with different goals:

* Write a nice, easy to understand solution

* While being as pythonic-functional as possible

* **Define** your own goal (if it makes sense). Examples:

  - Learn what the "import itertools" and "import functools" can do for you

  - Use generators

  - Solve it with a custom higher-order function

  - ...

* After entry deadline it is important to discuss all the entries

  - And maybe come up with a improved, combined solution

.. _code-golf: https://en.wikipedia.org/wiki/Code_golf

What is pythonic-functional
===========================

First of all please contribute to this section, I don't intend to define this
all by myself.

Articles:

* `This is probably`_ most important definition

* Pyrsistent_ is a helpful tool

* `From set-theory to monads`_ (I still don't get them)

.. _`This is probably`: https://docs.python.org/dev/howto/functional.html
.. _Pyrsistent: http://pyrsistent.readthedocs.io/en/latest/
.. _`From set-theory to monads`: https://bartoszmilewski.com/2011/01/09/monads-for-the-curious-programmer-part-1/

Rules:

* You are allowed to emulate functional-concepts in python if it helps to prove
  a point

* There are things that are strictly unpythonic: ie. DO NOT emulate tail recursion
  optimization

  - There are other ways to keep stack-depth in check: `compare drop2() / drop3()`_

* Try to avoid side-effects or use them only for optimization like memoize

* Python 3.5+ man, really dude!

Tips:

* Click_ helps a lot

.. _Click: http://click.pocoo.org/6/

.. _`compare drop2() / drop3()`: https://gist.github.com/ganwell/a2c9136398fbbd70796ad15b0778ae68

How to conduct a code-ballet
============================

* The platform is Github

* Code-ballets are issues

* Solutions are pull-requests (@AdSy: Leeave the pull-requests open![1])

* Directory structure

.. code-block:: text
   
    * _resources/
    * 2016-05-03-[name of problem]/
    | * [github-user]/
    | | README.rst
    | | requirements.txt
    | | [name of problem].py

* Describe your goals in README.rst

* Solve the code-ballet as early as possible

* Submit the solution as late as possible

[1] In order to discuss on the pull-request and maybe add few commits to the PR after discussion. I will creae a branch     where all the entries are merge, so you can easily test them.

Contribute code-ballets
=======================

If you have a code-ballet you'd like to submit, please open a issue with the
label "queue", without telling what the ballet is about, yet. I will assign a
date to release the ballet.
