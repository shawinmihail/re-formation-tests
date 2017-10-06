import copy
import numpy as np
import math


class Loop:

    def __init__(self, copter, _radius, omega):
        self.speed = copter.v
        self.v0 = copy.deepcopy(copter.v)

        self.x = copter.x
        self.x0 = copy.deepcopy(copter.x)

        self.omega = np.cross([-1, 0, 0], self.v0) * omega / np.linalg.norm(self.v0)

        self.finished = False
        self.radius = _radius

        self.cos_alpha = self.v0[1] / math.sqrt(math.pow(self.v0[0], 2) + math.pow(self.v0[1], 2))
        self.sin_alpha = self.v0[0] / math.sqrt(math.pow(self.v0[0], 2) + math.pow(self.v0[1], 2))


    def get_speed(self):
        v_norm = np.cross(self.omega, self.get_r())
        return v_norm

    def get_r(self):
        return np.asarray([0, -self.radius, 0]) + self.x - self.x0

        # a.append([r * math.cos(i * d_phi - math.pi / 2) * sin_alpha,
        #           r * math.cos(i * d_phi - math.pi / 2) * cos_alpha,
        #           r * math.sin(i * d_phi - math.pi / 2)])
