import pygame
from Functions.Math import *
from Classes.Animation import *
from Classes.Skill import *
import json


class Starship:
    def __init__(self, world, x, y, width, height, health, cam, sprites_group, sprite_frames, image_width=0,
                 image_height=0, mass=100, cls="Bug", behaviour="attack"):
        # Определение свойств объекта корабля
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.max_health = health
        self.energy = 1000
        self.mass = mass
        self.image_width = width if image_width == 0 else image_width
        self.image_height = height if image_height == 0 else image_height
        self.effects = dict()
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
        self.friction_x = 0.03
        self.friction_y = 0.05
        # Спрайт
        self.sprite = Anim(sprites_group, cam, sprite_frames, self, self.image_width, self.image_height)
        # Класс
        self.cls = cls
        self.behaviour = behaviour
        self.anim_controller = AnimController(self)
        self.cam = cam
        # Мир
        self.world = world

    def update(self, objects, i):  # Обновление
        # Изменение координат в зависимости от скорости
        self.x += self.speed_x * ACCELERATION
        self.y += self.speed_y * ACCELERATION
        # Ускорение корабля
        self.speed_x += self.acceleration_x * ACCELERATION
        self.speed_y += self.acceleration_y * ACCELERATION

        if abs(self.speed_x) > self.max_speed_x:
            self.speed_x = self.max_speed_x * (abs(self.speed_x) / self.speed_x)

        if abs(self.speed_y) > self.max_speed_y:
            self.speed_y = self.max_speed_y * (abs(self.speed_y) / self.speed_y)

        # Трение
        if self.acceleration_x == 0 and self.speed_x != 0:
            if abs(self.speed_x) < 0.01:
                self.speed_x = 0
            elif abs(self.speed_x) < self.friction_x:
                self.speed_x = 0
            else:
                self.speed_x -= self.friction_x * abs(self.speed_x) / self.speed_x

        if self.acceleration_y == 0 and self.speed_y != 0:
            if abs(self.speed_y) < 0.01:
                self.speed_y = 0
            elif abs(self.speed_y) < self.friction_y:
                self.speed_y = 0
            else:
                self.speed_y -= self.friction_y * abs(self.speed_y) / self.speed_y

        for effect in self.effects:
            self.effects[effect].update(objects[0:i] + objects[i+1:len(objects)])

        for obj in objects[i + 1:len(objects)]:
            if obj != self:
                self.check_intersection_with_ship(obj)

        if self.y + self.height / 2 > 0:
            self.y = -self.height / 2 - 1
            self.speed_y = -self.speed_y * 0.5

        self.anim_controller.update()
        return self.health > 0

    # Удар об противника
    def kick(self, other):
        self.cancel_movement()
        other.cancel_movement()
        self_speed, other_speed = speed_calcs2((self.x, self.y), (other.x, other.y), (self.speed_x, self.speed_y),
                                                   (other.speed_x, other.speed_y), self.mass, other.mass)
        self.speed_x, self.speed_y = self_speed
        other.speed_x, other.speed_y = other_speed
        if abs(self.x - other.x) / (self.width / 2 + other.width / 2) > abs(self.y - other.y) / (self.height / 2 +
                                                                                             other.height / 2):
            if self.x < other.x:
                other.x = self.x + self.width / 2 + other.width / 2 + 10
            else:
                other.x = self.x - self.width / 2 - other.width / 2 - 10
        else:
            if self.y < other.y:
                other.y = self.y + self.height / 2 + other.height / 2 + 10
            else:
                other.y = self.y - self.height / 2 - other.height / 2 - 10

    # Отмена действия
    def cancel_movement(self):
        self.x -= self.speed_x
        self.y -= self.speed_y

    # Проверка пересечения
    def check_intersection_with_ship(self, other):
        if self.x - self.width / 2 <= other.x - other.width / 2 <= self.x + self.width / 2 or \
                self.x - self.width / 2 <= other.x + other.width / 2 <= self.x + self.width / 2 or \
                other.x - other.width / 2 <= self.x - self.width / 2 <= other.x + other.width / 2 or \
                other.x - other.width / 2 <= self.x + self.width / 2 <= other.x + other.width / 2:
            if self.y - self.height / 2 <= other.y - other.height / 2 <= self.y + self.height / 2 or \
                    self.y - self.height / 2 <= other.y + other.height / 2 <= self.y + self.height / 2 or \
                    other.y - other.height / 2 <= self.y - self.height / 2 <= other.y + other.height / 2 or \
                    other.y - other.height / 2 <= self.y + self.height / 2 <= other.y + other.height / 2:
                self.kick(other)
                return True
        return False

    def check_intersection_with_point(self, point):
        if self.x - self.width / 2 < point[0] < self.x + self.width / 2 and self.y - self.height / 2 < point[1] < \
                self.y + self.height / 2:
            return True
        return False

    def set_acceleration(self, x=0, y=0):  # Изменение ускорения корабля
        self.acceleration_x += self.ship_acceleration_x * x
        self.acceleration_y += self.ship_acceleration_y * y

    def stop(self, x=False, y=False):
        if x:
            self.acceleration_x = 0

        if y:
            self.acceleration_y = 0


class AnimController:
    def __init__(self, master):
        self.master = master
        self.last_accleration_x = 0

    def update(self):
        if self.master.cls == "Hindenburg":
            if abs(self.master.acceleration_x) > abs(self.last_accleration_x):
                self.master.sprite.set_state("start")
            if self.master.acceleration_x == 0:
                if self.master.sprite.state in ["moving", "start"]:
                    self.master.sprite.set_state("stop")
        self.last_accleration_x = self.master.acceleration_x


def create_ship(world, cam, sprites_group, x, y, cls):
    file = open("Data/classes.json", "r", encoding="utf-8")
    data0 = json.load(file)
    data = data0[cls]
    file.close()

    ship = Starship(world, x, y, data["cwidth"], data["cheight"], data["hp"], cam, sprites_group, data["anim"],
                    data["width"], data["height"], data["mass"], cls=cls, behaviour=data["behaviour"])
    ship.ship_acceleration_x = data["ax"]
    ship.ship_acceleration_y = data["ay"]
    ship.max_speed_x = data["msx"]
    ship.max_speed_y = data["msy"]
    ship.friction_x = data["fx"]
    ship.friction_y = data["fy"]

    skills = SkillList(0, 0, 5, ship)
    for skill in data["equipment"]:
        skills.add(eval(skill))
        skills.skills[-1].number = data["equipment"][skill]

    return ship, skills
