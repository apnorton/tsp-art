tsp-art
=======

This is (essentially) my final project for CS Theory (CS 3102) at UVa.  The goal was to write an approximation for an NP-complete problem; I chose the Travelling Salesman with a particular application to creating ["TSP Art"](http://www.oberlin.edu/math/faculty/bosch/tspart-page.html).  My reasoning was that this project, moreso than others, lent itself to the creation of easily understood diagrams that even my non-technical friends could appreciate.

As a general overview, my program works in three steps:

  1. Stipple the image
  2. Use the "nearest neighbor" heuristic to create a TSP estimate
  3. Fix all intersecting edges

More detailed information on how these processes work is documented below.

