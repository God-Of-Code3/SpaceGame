import math


def to_point(x1, y1, x2, y2):
    if y1 == y2:
        direction = 0 if x2 > x1 else 180
    elif x1 == x2:
        direction = 90 if y2 > y1 else 270
    else:
        direction = -math.atan((x2 - x1) / (y2 - y1)) / math.pi * 180 + 90
        if y2 < y1:
            direction += 180
    if direction < 0:
        direction = 360 + direction
    return direction


def speed_calcs(v1, v2, m1, m2):
    v3 = (2 * m2 * v2 + (m1 - m2) * v1) / (m1 + m2)
    v4 = (2 * m1 * v1 + (m2 - m1) * v2) / (m1 + m2)
    return v3, v4