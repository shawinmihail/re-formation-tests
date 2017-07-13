from sympy.utilities.iterables import multiset_permutations
import numpy as np
eps = 0.05

def perp( a ) :
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b


def seg_intersect(a1,a2, b1,b2):
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = np.dot( dap, db)
    num = np.dot( dap, dp )
    d = denom.astype(float)
    if abs(d) < eps:
        d = eps
    return (num / d)*db + b1

def isIntersection(p1, p2, q1, q2):
    p1, p2 = inf_check(p1, p2)
    q1, q2 = inf_check(q1, q2)
    p = seg_intersect(p1, p2, q1, q2)
    u1 = p[0] > p1[0] and p[0] < p2[0]
    u2 = p[0] < p1[0] and p[0] > p2[0]
    u3 = p[0] > q1[0] and p[0] < q2[0]
    u4 = p[0] < q1[0] and p[0] > q2[0]
    return (u1 or u2) and (u3 or u4)


def line(p1, p2):
    dx = p1[0]-p2[0]
    if dx == 0:
        dx = eps
    dy = p1[1]-p2[1]
    k = dx/dy
    b = p1[1] - k*p1[0]
    return k,b


def permutations(points):
    return multiset_permutations(points)

def inf_check(p1, p2):
    dx = p1[0]-p2[0]
    if abs(dx) < eps:
        p1[0] -= eps/2
        p2[0] += eps/2
    return p1, p2



# p1 = np.array( [-1.,0.])
# p2 = np.array( [1., 0.])
# q1 = np.array( [0.,-1.])
# q2 = np.array( [0., 1.])
#
# print(isIntersection(p1, p2, q1, q2))