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


def rotate_vector(vector, direction):
    length = math.hypot(*vector)
    current_vector_direction = to_point(0, 0, *vector)
    new_vector_direction = current_vector_direction + direction
    new_vector = math.cos(new_vector_direction * math.pi / 180) * length, \
        math.sin(new_vector_direction * math.pi / 180) * length
    return new_vector


def round_vector(vector, d=3):
    return list(map(lambda x: round(x * 10 ** d) / (10 ** d), vector))


def get_vector_by_other_vector(vector1, vector2):
    return rotate_vector(vector1, to_point(0, 0, *vector2) % 360 - 90)


def get_vector_by_other_vector_minus(vector1, vector2):
    return rotate_vector(vector1, -to_point(0, 0, *vector2) % 360 + 90)


def speed_calcs2(coords1, coords2, speed1, speed2, m1, m2):
    vector2 = coords2[0] - coords1[0], coords2[1] - coords1[1]
    vector1_1 = speed1
    vector1_2 = speed2
    vector3 = get_vector_by_other_vector_minus(vector1_1, vector2)
    vector4 = get_vector_by_other_vector_minus(vector1_2, vector2)
    y1, y2 = speed_calcs(vector3[1], vector4[1], m1, m2)
    vector3, vector4 = [vector3[0], y1], [vector4[0], y2]
    vector1_1 = round_vector(get_vector_by_other_vector(vector3, vector2))
    vector1_2 = round_vector(get_vector_by_other_vector(vector4, vector2))
    return vector1_1, vector1_2
