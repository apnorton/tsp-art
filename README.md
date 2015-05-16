tsp-art
=======

This is (essentially) my final project for CS Theory (CS 3102) at UVa.  The goal was to write an approximation for an NP-complete problem; I chose the Travelling Salesman with a particular application to creating ["TSP Art"](http://www.oberlin.edu/math/faculty/bosch/tspart-page.html).  My reasoning was that this project, moreso than others, lent itself to the creation of easily understood diagrams that even my non-technical friends could appreciate.

As a general overview, my program works in three steps:

  1. Stipple the image
  2. Use the "nearest neighbor" heuristic to create a TSP estimate
  3. Fix all intersecting edges

More detailed information on how these processes work is documented below.

To run the program, you must have the Python Imaging Library ([Pillow](https://pypi.python.org/pypi/Pillow/)) installed and be using Python 3.  The usage is:
```
$ python3 TSPArt.py [image name]
```

The program will display some status information; when it indicates that the run is complete, the final image will be stored in the same directory as the program. 

Stippling
---------

I use the method of [Weighted Voronoi Stippling](http://mrl.nyu.edu/~ajsecord/npar2002/npar2002_ajsecord_preprint.pdf) to convert a given image into its stippled equivalent.  The linked paper is a very good description of what is happening, so I recommend anyone interested read that.  However, I did take a few liberties when creating my version that I will document below:
  1. Weighted Voronoi Stippling does a great job of turning a poor stippling estimate into a great stippling estimate, but we need a starting point.  To create this starting point, I randomly place a single stipple point in the center of a `n`-by-`n` cell (where `n` is determined from the size of the image) based on the the average intensity of the grayscale image in that cell.
  2. The paper uses a 3D graphics card to compute the Voronoi diagram at each step; this is highly efficient, but somewhat difficult to do in Python.  I created each Voronoi diagram using a breadth-first search from the stipple points, which is slower but easier to implement.
  3. Finally, the paper mentions a way to reduce the computation required to find the centers of mass for each Vornoi cell.  Although this should be somewhat straighforward to implement with Python, I didn't do so to save programming time.

Approximation
-------------

The next step in the process is to approximate a solution to the Travelling Salesman Problem.  Obviously, the better your approximation, the better your end result will be.  I originally was going to use Simulated Annealing, but that resulted in some pretty awful results with even just a few stipple points.  At this point, I was running out of time to work on this project, and so settled on the Nearest Neighbor heuristic.

To use this heuristic, you choose a starting point at random and build a path by repeatedly selecting the nearest stipple point to the current path endpoint.  The simplest approach (which I used) takes Ɵ(n^2) time (from each endpoint, examine all other unchosen points).

A better (and faster) heuristic is to use a preorder traversal of a minimum spanning tree.  This would only take Ɵ(n lg n) time and is relatively simple to write; I am not entirely sure why I didn't use this approach instead.  It can be shown that this MST approach will return a path that is, in the worst-case, twice as long the optimal TSP solution.

Intersection Correction
-----------------------

The above approximation step should produce a good result, but we'd really like to eliminate any self-intersections in the proposed solution curve.  It is rather trivial to see that an exact TSP solution will never intersect, and removing intersections by reconnecting the four points associated with two intersecting segments will always shorten the proposed path.

To really describe my approach for intersection removal, I'll need to create some graphics and trace out my algorithm.  However, the general idea is to perform a Ɵ(n^2) scan for intersecting segments, then replace each pair with two segments that do not intersect yet maintain path connectivity.  This is made simpler by treating each segment as a directed segment and "following" the segments around the curve.
