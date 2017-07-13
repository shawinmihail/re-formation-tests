import numpy as np
import matplotlib.pyplot as plt
from random import random
from utils import *

def generate_points(n):
    x = 20.
    points = list()
    for i in range(n):
        x = (random()-0.5)*x*2
        y = (random()-0.5)*x*2
        points.append(np.array([x,y]))
    return points

def formation_square6(a):
    p1 = a*np.array([1.,1.])
    p2 = a*np.array([1.,0.])
    p3 = a*np.array([1.,-1.])
    p4 = a*np.array([-1.,1.])
    p5 = a*np.array([-1.,-1.])
    p6 = a*np.array([-1.,0.])
    return [p1,p2,p3,p4,p5,p6]

def formation_wedge6():
    a = 2
    p1 = a*np.array([3.,0.])
    p2 = a*np.array([2.,-1.])
    p3 = a*np.array([2.,1.])
    p4 = a*np.array([1.,2.])
    p5 = a*np.array([1.,0.])
    p6 = a*np.array([1.,-2.])
    return [p1,p2,p3,p4,p5,p6]


def shake(r, rf):
    assert len(r)==len(rf)
    s = len(r)
    perms = list(permutations(range(s)))
    min_k = float('+inf')
    min_w = float('+inf')
    best_perm = None
    for perm in perms:
        lines = list()
        for k in range(s):
            p1 = r[perm[k]]
            p2 = rf[k]
            lines.append([p1, p2])
        k = count_intersections(lines)
        w = calc_weigt_func(lines)
        # if k == 0:
        #     min_k = k
        #     min_perm = perm
        #     return min_k, min_perm
        if k < min_k:
            min_k = k
            best_perm = perm
            min_w = w
        elif k == min_k and w < min_w:
            min_k = k
            best_perm = perm
            min_w = w
    return min_k, min_w, best_perm


def count_intersections(lines):
    k = 0
    for line1 in lines:
        for line2 in lines:
            if np.array_equal(line1,line2):
                continue
            if isIntersection(line1[0], line1[1], line2[0], line2[1]):
                k+=1
    return k


def calc_weigt_func(lines):
    w = 0
    for line1 in lines:
        p1 = line1[0]
        p2 = line1[1]
        w = np.linalg.norm(p1 - p2)
    return w


rf = formation_wedge6()
r = formation_square6(5)
# rf = generate_points(6)
for p in r:
    plt.plot(p[0],p[1], 'k+')
for p in rf:
    plt.plot(p[0],p[1], 'ro')

k, w, perm = shake(r, rf)
# print(k)
for i in range(len(r)):
    x1 = rf[i][0]
    y1 = rf[i][1]
    x2 = r[perm[i]][0]
    y2 = r[perm[i]][1]
    plt.plot([x1, x2], [y1, y2], 'm--')

plt.xlim([-10, 10])
plt.ylim([-10, 10])
plt.show()