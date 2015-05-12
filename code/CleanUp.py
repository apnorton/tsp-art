import math 
from PIL import Image
from PIL import ImageDraw
from Seg import Seg
from itertools import product

##
# Cleans up intersections
##

def dist(pt1, pt2):
  return math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1]-pt2[1])**2)

## Intersection algo taken from http://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
def ccw(A, B, C):
  return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

def intersects(seg1, seg2):
  A = seg1[0]
  B = seg1[1]
  C = seg2[0]
  D = seg2[1]
  return ccw(C,D,A) != ccw(C,D,B) and ccw(A,B,C) != ccw(A,B,D)

def isAdj(seg1, seg2):
  return seg1[0] == seg2[0] or seg1[0] == seg2[1] or seg1[1] == seg2[0] or seg1[1] == seg2[1]

def getCrossings(set1, set2):
  retVal = set() 
  for (seg1, seg2) in product(set1, set2):
    if (seg1.isAdj(seg2)): continue
    if (intersects(seg1.toList(), seg2.toList())):
      retVal.add((seg1, seg2))

  return retVal

# Fix the intersection issues
def correct(segSet, im): 
  ct = 0
  crossingSet = getCrossings(segSet, segSet)
  while crossingSet:
    (seg1, seg2) = crossingSet.pop()
    segSet.remove(seg1)
    segSet.remove(seg2)

    # Delink these segments entirely
    seg1.nextSeg.prevSeg = None
    seg1.prevSeg.nextSeg = None
    seg2.nextSeg.prevSeg = None
    seg2.prevSeg.nextSeg = None

    # Follow seg1 to the end:
    endSeg = seg1.nextSeg
    while (endSeg.nextSeg != None):
      endSeg = endSeg.nextSeg

    seg1.nextSeg.reverse()

    newSeg1 = Seg(seg1.sharedPt(seg1.prevSeg), seg2.sharedPt(seg2.prevSeg))
    newSeg2 = Seg(seg2.sharedPt(seg2.nextSeg), seg1.sharedPt(seg1.nextSeg))
      
    newSeg1.prevSeg = seg1.prevSeg
    newSeg1.nextSeg = seg2.prevSeg
    newSeg2.prevSeg = seg1.nextSeg
    newSeg2.nextSeg = seg2.nextSeg
    newSeg1.prevSeg.nextSeg = newSeg1
    newSeg1.nextSeg.prevSeg = newSeg1
    newSeg2.prevSeg.nextSeg = newSeg2
    newSeg2.nextSeg.prevSeg = newSeg2

    segSet.add(newSeg1)
    segSet.add(newSeg2)

    # delete old edges from crossing set
    crossingSet = {c for c in crossingSet if c[0]!=seg1 and c[0]!=seg2 and c[1]!=seg1 and c[1]!=seg2}
    crossingSet = crossingSet | getCrossings({newSeg1, newSeg2}, segSet)

  return segSet
  

def computeDist(lst):
  retVal = dist(lst[0], lst[len(lst)-1])
  for i in range(len(lst)-1):
    retVal += dist(lst[i], lst[i+1])

  return retVal
