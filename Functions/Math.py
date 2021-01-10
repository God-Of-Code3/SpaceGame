import math

timer_counter = 0

ACCELERATION = 1.6


def get_counter():
    global timer_counter
    timer_counter += 1
    return timer_counter


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


def get_angle(direction1, direction2):
    angle = direction2 - direction1
    if angle > 180:
        angle = 180 - angle
    if angle < -180:
        angle = - (180 + angle)
    return angle


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


def get_coords(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
    v1 = (bx2-bx1)*(ay1-by1)-(by2-by1)*(ax1-bx1)
    v2 = (bx2-bx1)*(ay2-by1)-(by2-by1)*(ax2-bx1)
    v3 = (ax2-ax1)*(by1-ay1)-(ay2-ay1)*(bx1-ax1)
    v4 = (ax2-ax1)*(by2-ay1)-(ay2-ay1)*(bx2-ax1)
    values = (v1*v2 < 0) and (v3*v4 < 0)
    return values


def click_coords_to_real(camera, pos):

    real_x = camera.cam_pos[0] + (pos[0] - camera.size[0] / 2) / camera.zoom_value
    real_y = camera.cam_pos[1] + (pos[1] - camera.size[1] / 2) / camera.zoom_value
    return real_x, real_y