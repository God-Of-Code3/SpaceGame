import pygame
import math
from Functions.Math import *
LASER_MAX_LENGTH = 12000


class Bullet:
    def __init__(self, x, y, direction, speed, image, image_width, image_height):
        self.x = x
        self.y = y
        self.damage = 100
        self.direction = direction
        self.speed = speed
        self.image = image
        self.img = pygame.image.load(self.image).convert()  # Загрузка и конвертирование иображения
        self.img.set_colorkey((255, 255, 255))
        self.image_width = image_width
        self.image_height = image_height

    def update(self):  # Обновление
        self.x += math.cos(self.direction * math.pi / 180) * self.speed
        self.y += math.sin(self.direction * math.pi / 180) * self.speed
        return True

    def info_for_drawing(self):  # Выдача информации для отрисовки
        data = dict()
        data["x"] = self.x
        data["y"] = self.y
        data["img"] = self.img
        data["width"] = self.image_width
        data["height"] = self.image_height
        data["rot"] = (self.direction - 180) % 360
        return data

    def check_intersection(self, other):
        if other.x - other.width / 2 < self.x < other.x + other.width / 2:
            if other.y - other.height / 2 < self.y < other.y + other.height / 2:
                return True


class Plasma(Bullet):
    def __init__(self, x, y, direction, speed, image, image_width, image_height, age):
        super().__init__(x, y, direction, speed, image, image_width, image_height)
        self.age = age
        self.damage = 300

    def update(self):
        super().update()
        self.age -= 1

        self.speed *= 0.97
        self.damage *= 0.97
        if abs(self.speed) < 5:
            self.age = 0
        return self.age > 0


class CopperShell(Bullet):
    def __init__(self, x, y, direction, speed, image, image_width, image_height, age):
        super().__init__(x, y, direction, speed, image, image_width, image_height)
        self.age = age
        self.damage = 20

    def update(self):
        super().update()
        self.age -= 1
        return self.age > 0


class Laser:
    def __init__(self, x, y, direction, master):
        self.x = x
        self.y = y
        self.direction = direction
        self.end_x = self.x + math.cos(math.pi / 180 * self.direction) * LASER_MAX_LENGTH
        self.end_y = self.y + math.sin(math.pi / 180 * self.direction) * LASER_MAX_LENGTH
        self.master = master

    def check_intersection_with_rectangle(self, x, y, width, height):  # проверка пересечения с прямоугольником
        self_line = (self.x, self.y), (self.end_x, self.end_y)
        line1 = (x - width / 2, y - height / 2), (x + width / 2, y - height / 2)
        line2 = (x - width / 2, y - height / 2), (x - width / 2, y + height / 2)
        line3 = (x + width / 2, y + height / 2), (x + width / 2, y - height / 2)
        line4 = (x + width / 2, y + height / 2), (x - width / 2, y + height / 2)

        res1 = get_coords(*line1[0], *line1[1], *self_line[0], *self_line[1])
        res2 = get_coords(*line2[0], *line2[1], *self_line[0], *self_line[1])
        res3 = get_coords(*line3[0], *line3[1], *self_line[0], *self_line[1])
        res4 = get_coords(*line4[0], *line4[1], *self_line[0], *self_line[1])
        results = [res1, res2, res3, res4]
        return results

    def set_direction(self, direction):  # установить направление
        self.direction = direction

    def check_intersection(self, objects):  # проверить пересечени
        results = [[self.check_intersection_with_rectangle(o.x, o.y, o.width, o.height), o] for o in objects]
        if len(list(filter(lambda res: any(res[0]), results))) > 0:
            results = list(filter(lambda res: any(res[0]), results))
            min_obj = min(results, key=lambda res: math.hypot(res[1].x - self.x, res[1].y - self.y))
            dist = math.hypot(min_obj[1].x - self.x, min_obj[1].y - self.y)
            self.end_x, self.end_y = self.x + math.cos(self.direction * math.pi / 180) * dist, \
                self.y + math.sin(self.direction * math.pi / 180) * dist
            min_obj[1].health -= 10
        else:
            self.end_x = self.x + math.cos(math.pi / 180 * self.direction) * LASER_MAX_LENGTH
            self.end_y = self.y + math.sin(math.pi / 180 * self.direction) * LASER_MAX_LENGTH

    def draw(self, screen, camera):
        x1 = camera.size[0] / 2 + (self.x - camera.cam_pos[0]) * camera.zoom_value
        y1 = camera.size[1] / 2 + (self.y - camera.cam_pos[1]) * camera.zoom_value

        x2 = camera.size[0] / 2 + (self.end_x - camera.cam_pos[0]) * camera.zoom_value
        y2 = camera.size[1] / 2 + (self.end_y - camera.cam_pos[1]) * camera.zoom_value

        pygame.draw.line(screen, (255, 100, 0), (x1, y1), (x2, y2), 5)
        pygame.draw.line(screen, (255, 0, 0), (x1, y1), (x2, y2), 3)
        pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2), 1)

    def update(self, objects, **kwargs):
        self.x = self.master.x
        self.y = self.master.y
        self.check_intersection(objects)
