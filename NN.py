import math

##
# Brute force Nearest Neighbor approximation
##

def dist(pt1, pt2):
  return math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1]-pt2[1])**2)

# Given a point and a list, returns p \in lst s.t. dist(p, pt) is minimal
def nearest(pt, lst):
  best = float('inf')
  bestInd = -1
  for i in range(len(lst)):
    if dist(lst[i], pt) < best:
      best = dist(lst[i], pt)
      bestInd = i
    
  (lst[0], lst[bestInd]) = (lst[bestInd], lst[0])
  
  return (lst[0], lst[1:])


def tsp(lst):
  order = [lst[0]]
  lst = lst[1:]

  while (len(lst) > 0):
    last = order[len(order)-1]
    (near, lst) = nearest(last, lst)
    order.append(near)
  
  return order
