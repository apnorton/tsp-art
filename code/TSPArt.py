from PIL import Image
from PIL import ImageStat
from PIL import ImageDraw
import copy
import random
import sys
import itertools
import VoronoiDiagram
from cleanup import correct
import NN
from Seg import Seg

##
#   readImage(filename) retrieves the specified image and returns
# a black-and-white version of that image.
##
def readImage(filename):
  #todo: filepath verification
  im = Image.open(filename).convert('L')
  return im

##
#   stipple(image) converts the provided image into a list of tuples
# describing point locations.  This is not too easy... but I'm doing
# it a dumb way.
##

def stipple(im, bxSz, itr):
  xSz = im.size[0]
  ySz = im.size[1]

  cutoff = ImageStat.Stat(im).mean[0]

  # Create initial, evenly distributed VD
  genPts = []
  for x in itertools.product(range(0, xSz-int(bxSz/2), bxSz), range(0, ySz-int(bxSz/2), bxSz)):
    box = (x[0], x[1], x[0]+bxSz, x[1]+bxSz)
    region = im.crop(box)
    if (ImageStat.Stat(region).mean[0]/255 < random.random()):
      genPts.append((x[0]+int(bxSz/2), x[1]+int(bxSz/2)))

  # Iterate for convergence
  for i in range(itr):
    im2 = copy.deepcopy(im)
    m = VoronoiDiagram.getVoronoi(genPts, (xSz, ySz))

    draw = ImageDraw.Draw(im2)

    for pt in genPts:
      drawCirc(draw, (pt[0], pt[1]), 1, (0))
    
    centroids = VoronoiDiagram.findCentroids(m, (xSz, ySz), len(genPts), lambda x, y : 1-im.getpixel((x, y))/255)

    genPts = [(round(pt[0]), round(pt[1])) for pt in centroids]
    
    print('Completed iteration {} of stippling.'.format(i))
    im2.save('./Img' + str(i) + '.jpg')

  return genPts

def drawCirc(draw, pt, r, color):
  pt0 = (pt[0]-r, pt[1]-r)
  pt1 = (pt[0]+r, pt[1]+r)
  draw.ellipse([pt0, pt1], fill=color)

def createSegSet(lst):
  segList = [Seg(lst[i], lst[i+1]) for i in range(len(lst)-1)] + [Seg(lst[0], lst[len(lst)-1])]
  for i in range(len(segList)):
    segList[i].prevSeg = segList[i-1]
    segList[i].nextSeg = segList[(i+1)%len(segList)]

  return set(segList)
  
def drawSegSet(segSet, sz, fname, red=set(), green=set(), blue=set()):
  im = Image.new('RGB', sz, (255, 255, 255))
  draw = ImageDraw.Draw(im)
  
  for seg in segSet:
    draw.line(seg.toList(), fill=(127, 127, 127), width=1)

  for seg in red:
    draw.line(seg.toList(), fill=(255, 0, 0), width=2)

  for seg in green:
    draw.line(seg.toList(), fill=(0, 255, 0), width=2)

  for seg in blue:
    draw.line(seg.toList(), fill=(0, 0, 255), width=2)

  del draw

  im.save(fname)

if __name__ == '__main__':
  sys.setrecursionlimit(6000)
  # bounds check
  if (len(sys.argv) < 2):
    print('Usage: python3 {} filename', sys.argv[0])

  filename = sys.argv[1]
  print('Attempting to open {}.'.format(filename))
  im = readImage(filename)
  if (max(im.size) > 600):
    im = im.resize((int(600*(float(im.size[0])/max(im.size))), int(600*(float(im.size[1])/max(im.size)))))
  print('Opened.')

  print('Attempting to stipple...')
  cellSize = 2

  # Create a stippled version of the image; limit 6000 px.
  lst = stipple(im, cellSize, 0)
  while (len(lst) > 6000):
    cellSize += 1
    lst = stipple(im, cellSize, 0)
  lst = stipple(im, cellSize, 8)
  print('There are {} points.'.format(len(lst)))
  print('Stippled!')

  print('Attempting TSP with naive NN...')
  lst = NN.tsp(lst)

  print('Now converting to list of segments...')
  segSet = createSegSet(lst)

  ## Let's make sure all of our segments share a point...
  print('Correcting any overlaps...')
  drawSegSet(segSet, im.size, 'start.jpg')
  segSet = correct(segSet, im)
  drawSegSet(segSet, im.size, 'end.jpg')
  print('Done.')
