k_p = 2
k_v = 2


def get_prop_diff_control(x, x_d, v):
    return k_p * (x_d - x) - k_v * (v)