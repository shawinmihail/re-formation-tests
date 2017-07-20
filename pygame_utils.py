def transform_to_screen_system(_x, _y, display_config):
    ratio = display_config[0]
    width = display_config[1]
    height = display_config[2]

    x_px = _x * ratio
    y_px = _y * ratio


    return int(width / 2. + x_px), int(height/ 2. - y_px)