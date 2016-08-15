Goals:

- focus on functional style & readability over performance
- without looking at existing solutions
- vanilla python

Result:

- first attempt at functional solution failed (round-based approach was not a good idea)
- implemented procedural solution for reference
- second shot at functional solution yielded a working solution, that can be easily extended to give not just one solution to a given stable marriage problem, but all of them. 

This solution is outlined here:

1) convert both preference sets to a matrix, where the entries are the preferences expressed as numbers: 0 = favorite, 1 = 2nd best, ... 
2) add the two matrices (after transposing one of them, such that rows represent women and columns men) - lets call this "mututal preference matrix"

3) find the lowest number in the matrix -> this is a match!
4) cross out the row and the column of the last match, as these two people are now not available for matching anymore.
5) repeat at (3) with the updated matrix, until only one entry remains (which represents the last match)

The situations, where multiple choices for the lowest number in the matrix exist, correspond to multiple possible solutions.

Possible next steps:
- actually return all results
- rate the results by fairness
- check performance compared to procedural approach
- .. and so much more? ;)
