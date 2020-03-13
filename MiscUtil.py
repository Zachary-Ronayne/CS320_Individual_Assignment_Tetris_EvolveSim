import math


# find the distance between 2 points
# p1 and p2 are tuples in the form (x, y)
def distance(p1, p2):
    return math.sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))
