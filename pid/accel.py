# coding=utf8


import math

# Finding PID coefficients
# Period of stable oscillations when Kp != 0, others = 0
Tz = 7.0
Tx = 2.0

Kp = [0.6, 0.6 * 1]
Ki = None
Kv = None

vel_d = 0


# default pid params from pixHawk
# vel_p_xy = 0.09
# vel_p_z  = 0.6
# vel_d_xy = 0.01
# vel_d_z  = 0.008
# vel_i_xy = 0.02
# vel_i_z  = 0.15

# vel_p_xy = 0.09
vel_p_xy = 2
vel_p_z  = 0.6
vel_d_xy = 0.02
vel_d_z  = 0.15
vel_i_xy = 0.02
vel_i_z  = 0.15



class AccelPIDRegulator:
    def __init__(self):

        """
        В основном вычисление ускорений схоже с кодом в mc_pos_control_main  - в pixHawk
        """
        global Ki
        global Kv

        self.integ = [0, 0, 0]

        t = 0.001
        # works only while dt = 0.001
        Kv = [0.2, Kp[1] * Tz / 8. / 2000 / t]
        Ki = [0, 0, 2. * Kp[1] / Tz * 700 * t]
        # Kv = [0.13, Kp[1] * Tz / 8. / 2000 / t]

        self.vel_x_derivative = LowPassDerivative()
        self.vel_y_derivative = LowPassDerivative()
        self.vel_z_derivative = LowPassDerivative()

    # x - np.array([., ., .,]) - current coordinates
    # v - np.array([., ., .,]) - current vel
    def get_accel_trj(self, tr, x, v, dt):
        self.integ[0] += (tr.x[0] - x[0]) * dt
        self.integ[1] += (tr.x[1] - x[1]) * dt
        self.integ[2] += (tr.x[2] - x[2]) * dt

        ax = Kp[0] * (tr.x[0] - x[0]) + Kv[0] * (tr.v[0] - v[0]) + tr.a[0] + Ki[0] * self.integ[0]
        ay = Kp[0] * (tr.x[1] - x[1]) + Kv[0] * (tr.v[1] - v[1]) + tr.a[1] + Ki[1] * self.integ[1]
        az = Kp[1] * (tr.x[2] - x[2]) + Kv[1] * (tr.v[2] - v[2]) + tr.a[2] + Ki[2] * self.integ[2]

        return ax, ay, az

    def get_accel_to_wp(self, x_error, vel_error, dt):

        """
        Calculate acceleration using pid.
        """
        if x_error is None or vel_error is None:
            raise Exception("delta_x or delta_v is None in PID")

        self.integ[0] += x_error[0] * dt
        self.integ[1] += x_error[1] * dt
        self.integ[2] += x_error[2] * dt

        ax = Kp[0] * x_error[0] + Kv[0] * vel_error[0] + Ki[0] * self.integ[0]
        ay = Kp[0] * x_error[1] + Kv[0] * vel_error[1] + Ki[1] * self.integ[1]
        az = Kp[1] * x_error[2] + Kv[1] * vel_error[2] + Ki[2] * self.integ[2]

        return ax, ay, az

    def get_accel_to_wp2(self, x_error, vel_error, dt):

        """
        Вычисляем ускорение на основе PID:
        есть невязка по координате
        есть невязка по скорости
        есть интегральная составляющая вычисленная интегрированием невязки по скорости.
        """
        if x_error is None or vel_error is None:
            raise Exception("delta_x or delta_v is None in PID")

        self.integ[0] += vel_error[0] * dt
        self.integ[1] += vel_error[1] * dt
        self.integ[2] += vel_error[2] * dt

        ax = Kp[0] * x_error[0] + Kv[0] * vel_error[0] + Ki[0] * self.integ[0]
        ay = Kp[0] * x_error[1] + Kv[0] * vel_error[1] + Ki[1] * self.integ[1]
        az = Kp[1] * x_error[2] + Kv[1] * vel_error[2] + Ki[2] * self.integ[2]

        return ax, ay, az

    def get_accel_to_wp_px4(self, vel_error, dt):

        """
        Полная копия вычисления , как в pixHawk:
        есть невязка по скорости
        есть невязка по ускорениям (усоркение вычисляется с испльзование low pass filter)
        есть интгеральная составляющая, вычисленная инт - ем невязки по скорости

        """
        if vel_error is None:
            raise Exception("delta_v is None in PID")

        a_x = self.vel_x_derivative.update(vel_error[0], dt)
        a_y = self.vel_y_derivative.update(vel_error[1], dt)
        a_z = self.vel_z_derivative.update(vel_error[2], dt)

        self.integ[0] += vel_error[0] * dt
        self.integ[1] += vel_error[1] * dt
        self.integ[2] += vel_error[2] * dt

        ax = vel_p_xy * vel_error[0] + vel_d_xy * a_x + vel_i_xy * self.integ[0]
        ay = vel_p_xy * vel_error[1] + vel_d_xy * a_y + vel_i_xy * self.integ[1]
        az = vel_p_z  * vel_error[2] + vel_d_z  * a_z + vel_i_z  * self.integ[2]

        return ax, ay, az


class LowPassDerivative:

    # low pass frequency
    lp_f = 5

    def __init__(self):
        self.prev_in = None
        self.filter_prev = None

    def update(self, _input, _dt):

        if self.prev_in is not None:
            filter_in = (_input - self.prev_in) / _dt

            if self.filter_prev is None:
                self.filter_prev = filter_in

            b = 2 * math.pi * self.lp_f * _dt
            a = b / (1 + b)

            self.filter_prev = (a * filter_in + (1 - a) * self.filter_prev)
            output = self.filter_prev
        else:

            self.filter_prev = 0
            output = 0

        self.prev_in = _input
        return output









