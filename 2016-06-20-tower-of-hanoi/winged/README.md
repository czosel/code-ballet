
Solution in Erlang for Towers of Hanoi, dynamic programming
===========================================================

Uses dynamic programming as proposed. However we do not use a full supervisor structure.
Instead, I start a separate process that I use as a "solution server", which is basically
a side effect for caching / memoizing solutions.

Running
-------

    % # compile first:
    % erlc hanoi.erl

    % # execute and show output for solution of a 5-stack
    % erl -noshell -exit -run hanoi hanoi_cmdline 5

    % # execute and show output for solution of a 50-stack
    % erl -noshell -exit -run hanoi hanoi_cmdline 50

    % # execute, calculate, but don't show output
    % erl -noshell -exit -run hanoi hanoi_cmdline 5000 disable-output


Tweaks / Variants
-----------------

There are some code-level options to tweak (or un-tweak, rather).  Look at the
first few lines of code:

    config(use_only_exact)         -> false;
    config(server_store_solutions) -> true.

If you want to disable storing solutions in the solution server (and basically
run without memoizing), you can set `server_store_solutions` to `false`, and it
will run reaaaally slow.

If you only want to use exact solution matches, you can set `use_only_exact` to
`true`.


Notes
-----

On finding similar solutions: This is done in the solution server by trying all
permutations of the task at hand, and telling the client whether it was an
exact match or "only" a similar match.

Funny side note: I never found any exact matches when allowing similar matches
-- it always finds the similar matches first and reuses them.  Therefore I
think that implementing that feature was a very good idea :)

Note that we don't store the actual steps anymore, since we're not going to
output them anyway. Let stdout be the memory and let the user look it up...
much faster (for us, certainly not for the user)! I quickly ran into memory
problems when trying to store the whole solution tree (despite not using it in
the output)
