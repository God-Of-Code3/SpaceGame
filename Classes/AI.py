import pygame
from Classes.Starship import *
from Classes.Bullet import *
from Classes.Skill import *


MAX_DIST_TO_ENEMY = 600  # Максимальное расстояние до противника
MAX_DIST_FOR_ACCELERATION = 1000  # Максимальное расстояние до противника для разгона


class AI:
    def __init__(self, ship, enemy):
        self.ship = ship
        self.skills_list = SkillList(0, 0, 5, self.ship, random.randint(3, 120))
        self.skills_list.add(PlasmaShot)
        self.skills_list.add(LaserShot)

        self.enemy = enemy
        self.timer = 0

    def control(self, events, bullets, camera, objects):
        dist_to_enemy = math.hypot(self.ship.x - self.enemy.ship.x, self.ship.y - self.enemy.ship.y)
        direction_to_enemy = to_point(self.ship.x, self.ship.y, self.enemy.ship.x, self.enemy.ship.y)
        if dist_to_enemy < MAX_DIST_TO_ENEMY:
            self.move_to_direction(180 + direction_to_enemy)
        elif MAX_DIST_FOR_ACCELERATION > dist_to_enemy > MAX_DIST_TO_ENEMY:
            self.skills_list.selected = 0
            if random.randint(0, 1) == 0:
                dist_x = self.enemy.ship.x - self.ship.x
                dist_y = self.enemy.ship.y - self.ship.y
                x_sp = math.cos(direction_to_enemy * math.pi / 180) * 10
                y_sp = math.sin(direction_to_enemy * math.pi / 180) * 10
                x = self.enemy.ship.x + (dist_x / x_sp) * self.enemy.ship.speed_x + (dist_x / x_sp) ** 2 * \
                    self.enemy.ship.acceleration_x / 2
                y = self.enemy.ship.y + (dist_y / y_sp) * self.enemy.ship.speed_y + (dist_y / y_sp) ** 2 * \
                    self.enemy.ship.acceleration_y / 2
                if math.hypot(self.enemy.ship.x - x, self.enemy.ship.y - y) > 300:
                    x, y = self.enemy.ship.x, self.enemy.ship.y
                self.skills_list.use({"real_click_x": x, "real_click_y": y,
                                      "bullets": bullets})
            self.timer += 1
            self.timer %= 100
            if self.timer == 0:
                self.ship.set_acceleration(x=random.randint(-1, 1) / 4, y=random.randint(-1, 1) / 4)
        else:
            self.move_to_direction(direction_to_enemy)

        if "laser" in self.ship.effects:
            self.ship.effects["laser"].set_direction(direction_to_enemy % 360)

    def move_to_direction(self, direction):
        x, y = math.cos(direction * math.pi / 180), math.sin(direction * math.pi / 180)
        sp = min(self.ship.max_speed_x, self.ship.max_speed_y)
        nes_x, nes_y = x * sp, y * sp

        if nes_x < self.ship.speed_x:
            self.ship.set_acceleration(x=-1)
        elif nes_x > self.ship.speed_x:
            self.ship.set_acceleration(x=1)
        if nes_y < self.ship.speed_y:
            self.ship.set_acceleration(y=-1)
        elif nes_y > self.ship.speed_y:
            self.ship.set_acceleration(y=1)

    def update(self):
        self.skills_list.update()

    def draw(self, screen, camera):
        for effect in self.ship.effects:
            self.ship.effects[effect].draw(screen, camera)
        self.skills_list.draw(screen)

    def get_info_for_drawing(self):
        return self.ship.info_for_drawing()
