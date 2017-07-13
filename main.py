import numpy as np
import matplotlib.pyplot as plt
from random import random
from utils import *
import math
import time

def generate_points(n, size):
    points = list()
    for i in range(n):
        x = (2*random() - 1)*size
        y = (2*random() - 1)*size
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


def shake(r, rf, half_thickness):
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
            # lines.append([p1, p2])
            line_left, line_right = get_double_line([p1, p2], half_thickness)
            lines.append(line_left)
            lines.append(line_right)

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


def get_double_line(center_line, half_thickness):
    x1 = center_line[0][0]
    y1 = center_line[0][1]

    x2 = center_line[1][0]
    y2 = center_line[1][1]

    dx = x2 - x1
    dy = y2 - y1

    length = math.sqrt(dx * dx + dy * dy)

    n1 = np.array([-dy, dx]) / length
    n2 = np.array([dy, -dx]) / length

    xleft1 = x1 + n1[0] * half_thickness
    xright1 = x1 + n2[0] * half_thickness

    yleft1 = y1 + n1[1] * half_thickness
    yright1 = y1 + n2[1] * half_thickness
    xleft2 = x2 + n1[0] * half_thickness
    xright2 = x2 + n2[0] * half_thickness

    yleft2 = y2 + n1[1] * half_thickness
    yright2 = y2 + n2[1] * half_thickness

    l1 = [np.array([xleft1, yleft1]), np.array([xleft2, yleft2])]
    l2 = [np.array([xright1, yright1]), np.array([xright2, yright2])]

    return l1, l2


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
        w += np.linalg.norm(p1 - p2)
    return w


rf = formation_square6(2)
r = generate_points(6, 5)



for p in r:
    plt.plot(p[0],p[1], 'k+')
for p in rf:
    plt.plot(p[0],p[1], 'ro')

t_start = time.time()
k, w, perm = shake(r, rf, 0.1)
print "time: " + str(time.time() - t_start)

for i in range(len(r)):
    x1 = rf[i][0]
    y1 = rf[i][1]
    x2 = r[perm[i]][0]
    y2 = r[perm[i]][1]
    plt.plot([x1, x2], [y1, y2], 'm--')

plt.xlim([-6, 6])
plt.ylim([-6, 6])
plt.show()