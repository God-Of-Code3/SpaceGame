import pygame
import math


class Bullet:
    def __init__(self, x, y, direction, speed, image, image_width, image_height):
        self.x = x
        self.y = y

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

    def info_for_drawing(self):  # Выдача информации для отрисовки
        data = dict()
        data["x"] = self.x
        data["y"] = self.y
        data["img"] = self.img
        data["width"] = self.image_width
        data["height"] = self.image_height
        data["rot"] = -(self.direction + 180) % 360
        return data

    def check_intersection(self, other):
        if other.x - other.width / 2 < self.x < other.x + other.width / 2:
            if other.y - other.height / 2 < self.y < other.y + other.height / 2:
                return True
