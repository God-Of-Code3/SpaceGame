import pygame
import os
import sys
import math
from numba import njit, prange, jit
import time
import random
import numpy as np

pygame.init()


def load_image(name, colorkey=None):
    fullname = name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def to_point(ax, ay, bx, by):
    if ay == by:
        return 0 if bx > ax else 180
    elif ax == bx:
        return 90 if by > ay else 270
    else:
        angle = math.atan2(by - ay, bx - ax)
        angle = angle + math.pi * 2 if angle < 0 else angle
        return angle / math.pi * 180


def line_intersection(line1, line2, coords=False):
    xdiff = [line1[0][0] - line1[1][0], line2[0][0] - line2[1][0]]
    ydiff = [line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]]

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if not coords:
        return div != 0
    if div == 0:
        return False

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def rotate_vector(v, a):
    angle = to_point(0, 0, *v)
    angle -= a
    d = math.hypot(*v)
    v2 = [math.cos(math.pi / 180 * angle) * d, math.sin(math.pi / 180 * angle) * d]
    v2 = [round(v2[i], 4) for i in range(2)]
    return v2


def projection_on_vector(v1, v2):
    angle = to_point(0, 0, *v2)
    v3 = rotate_vector(v1, angle)
    return v3


def speed_calcs(v1, v2, m1, m2):
    v3 = (2 * m2 * v2 + (m1 - m2) * v1) / (m1 + m2)
    v4 = (2 * m1 * v1 + (m2 - m1) * v2) / (m1 + m2)
    return v3, v4


def collision(coords1, coords2, speed1, speed2, mass1, mass2):
    angle = to_point(*coords1, *coords2)

    speed1_r = rotate_vector(speed1, angle + 90)
    speed2_r = rotate_vector(speed2, angle + 90)

    speeds = speed_calcs(speed1_r[1], speed2_r[1], mass1, mass2)

    speed1_r, speed2_r = [speed1_r[0], speeds[0]], [speed2_r[0], speeds[1]]

    speed1 = rotate_vector(speed1_r, -(angle + 90))
    speed2 = rotate_vector(speed2_r, -(angle + 90))

    force = abs(speeds[0] - speeds[1])

    return speed1, speed2, force
