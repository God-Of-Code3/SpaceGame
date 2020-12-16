import pygame
from Functions.Math import *


class Starship:
    def __init__(self, x, y, image, width, height, health, image_width=0, image_height=0, mass=100):
        # Определение свойств объекта корабля
        self.x = x
        self.y = y
        self.image = image
        self.img = pygame.image.load(self.image).convert()  # Загрузка и конвертирование иображения
        self.img.set_colorkey((255, 255, 255))
        self.width = width
        self.height = height
        self.health = health
        self.mass = mass
        self.image_width = width if image_width == 0 else image_width
        self.image_height = height if image_height == 0 else image_height
        self.effects = []
        # Текущая скорость
        self.direction = 0  # направление вектора скорости
        self.speed_x = 0  # проекция вектора скорости на x
        self.speed_y = 0  # на y
        # Текущее ускорение
        self.acceleration_x = 0
        self.acceleration_y = 0
        # Максимальная скорость корабля
        self.max_speed_x = 10
        self.max_speed_y = 10
        # Ускорение корабля по осям
        self.ship_acceleration_x = 0.1
        self.ship_acceleration_y = 0.1
        # Трение
        self.friction_x = 0.01
        self.friction_y = 1
        # Упругость

    def update(self):  # Обновление
        # Изменение координат в зависимости от скорости
        self.x += self.speed_x
        self.y += self.speed_y
        # Ускорение корабля
        self.speed_x += self.acceleration_x
        self.speed_y += self.acceleration_y

        if abs(self.speed_x) > self.max_speed_x:
            self.speed_x = self.max_speed_x * (abs(self.speed_x) / self.speed_x)

        if abs(self.speed_y) > self.max_speed_y:
            self.speed_y = self.max_speed_y * (abs(self.speed_y) / self.speed_y)

        if self.acceleration_x == 0 and self.speed_x != 0:
            self.speed_x -= self.friction_x * abs(self.speed_x) / self.speed_x

        if self.acceleration_y == 0 and self.speed_y != 0:
            self.speed_y -= self.friction_y * abs(self.speed_y) / self.speed_y * (abs(self.speed_y) / self.max_speed_y)

    def kick(self, other, give=False):
        self.cancel_movement()
        other.cancel_movement()
        self.speed_x, other.speed_x = speed_calcs(self.speed_x, other.speed_x, self.mass, other.mass)
        self.speed_y, other.speed_y = speed_calcs(self.speed_y, other.speed_y, self.mass, other.mass)
        self.x += self.speed_x
        self.y += self.speed_y
        other.x += other.speed_x
        other.y += other.speed_y

    def cancel_movement(self):
        self.x -= self.speed_x
        self.y -= self.speed_y

    def check_intersection_with_ship(self, other):
        if self.x - self.width / 2 <= other.x - other.width / 2 <= self.x + self.width / 2 or \
                self.x - self.width / 2 <= other.x + other.width / 2 <= self.x + self.width / 2:
            if self.y - self.height / 2 <= other.y - other.height / 2 <= self.y + self.height / 2 or \
                    self.y - self.height / 2 <= other.y + other.height / 2 <= self.y + self.height / 2:
                self.kick(other, True)
                return True
        return False

    def set_acceleration(self, x=0, y=0):  # Изменение ускорения корабля
        self.acceleration_x += self.ship_acceleration_x * x
        self.acceleration_y += self.ship_acceleration_y * y

    def info_for_drawing(self):  # Выдача информации для отрисовки
        data = dict()
        data["x"] = self.x
        data["y"] = self.y
        data["img"] = self.img
        data["width"] = self.image_width
        data["height"] = self.image_height
        data["rot"] = 0
        return data
