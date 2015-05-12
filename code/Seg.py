##
# A segment class.  Essentially a doubly-linked list with some point data.
##
class Seg:
  pt1 = None
  pt2 = None
  def __init__(self, pt1, pt2):
    self.pt1 = pt1
    self.pt2 = pt2
    self.nextSeg = None
    self.prevSeg = None

  def reverse(self):
    if (self.nextSeg != None):
      self.nextSeg.reverse()

    (self.nextSeg, self.prevSeg) = (self.prevSeg, self.nextSeg)
    
  def toList(self):
    return [self.pt1, self.pt2]

  def __str__(self):
    return '[{},{}; next={}, prev={}]'.format(self.pt1, self.pt2, self.nextSeg.toList(), self.prevSeg.toList())

  def __repr__(self):
    return self.__str__()

  def isAdj(self, other):
    return self.pt1 == other.pt1 or self.pt2 == other.pt1 or self.pt1 == other.pt2 or self.pt2 == other.pt2

  def sharedPt(self, seg):
    otherPts = {seg.pt1, seg.pt2}
    myPts = {self.pt1, self.pt2}
    (shared,) = myPts & otherPts
    return shared

