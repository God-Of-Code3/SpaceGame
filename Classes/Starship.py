import pygame


class Starship:
    def __init__(self, x, y, image, width, height, health, image_width=0, image_height=0):
        # Определение свойств объекта корабля
        self.x = x
        self.y = y
        self.image = image
        self.img = pygame.image.load(self.image).convert()  # Загрузка и конвертирование иображения
        self.width = width
        self.height = height
        self.health = health
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
        self.max_speed_x = 2
        self.max_speed_y = 2
        # Ускорение корабля по осям
        self.ship_acceleration_x = 0.01
        self.ship_acceleration_y = 0.01

    def update(self):  # Обновление
        # Изменение координат в зависимости от скорости
        self.x += self.speed_x
        self.y += self.speed_y
        # Ускорение корабля
        self.speed_x += self.acceleration_x
        self.speed_y += self.acceleration_y

        if abs(self.speed_x) > self.max_speed_x:
            self.speed_x -= self.acceleration_x

        if abs(self.speed_y) > self.max_speed_y:
            self.speed_y -= self.acceleration_y

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
