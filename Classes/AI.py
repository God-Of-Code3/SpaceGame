import pygame
from Classes.Starship import *
from Classes.Bullet import *
from Classes.Skill import *


MAX_DIST_TO_ENEMY = 2500  # Максимальное расстояние до противника
MAX_DIST_FOR_ACCELERATION = 1000  # Максимальное расстояние до противника для разгона
MIN_DIST_TO_SHIP = 400
MIN_DIST_TO_ENEMY = 600
PLASMA_SHOT_DIST = 800
COPPER_SHELL_SHOT_DIST = 1200

AIR_ATTACK_MIN_HEIGHT = 2500


class AI:
    def __init__(self, ship, enemy, skills):
        self.ship = ship
        self.skills_list = skills

        self.enemy = enemy
        self.timer = 0
        self.behaviour = self.ship.behaviour

    def control(self, events, level):
        self.ship.stop(True, True)
        dist_to_enemy = math.hypot(self.ship.x - self.enemy.ship.x, self.ship.y - self.enemy.ship.y)
        direction_to_enemy = to_point(self.ship.x, self.ship.y, self.enemy.ship.x, self.enemy.ship.y)
        if self.enemy.ship.health > 0:
            if self.behaviour == "attack":
                n = 0
                for obj in [*level.get("enemys_ships"), level.get("player").ship]:
                    if obj != self.ship:
                        dist = math.hypot(obj.x - self.enemy.ship.x, obj.y - self.enemy.ship.y)
                        if dist < dist_to_enemy:
                            n += 1
                if n < 10:
                    if dist_to_enemy < 1000:
                        if self.ship.y > self.enemy.ship.y - MIN_DIST_TO_ENEMY:
                            self.ship.set_acceleration(y=-1)

                        if self.enemy.ship.y - MAX_DIST_TO_ENEMY < self.ship.y < self.enemy.ship.y - MIN_DIST_TO_ENEMY:
                            if self.ship.speed_y < 0:
                                self.ship.set_acceleration(y=1)
                            if self.ship.speed_y > 0:
                                self.ship.set_acceleration(y=-1)

                        if self.ship.y < self.enemy.ship.y - MAX_DIST_TO_ENEMY:
                            self.ship.set_acceleration(y=1)

                        if self.ship.x < self.enemy.ship.x - MIN_DIST_TO_ENEMY:
                            self.ship.set_acceleration(x=-1)
                        elif self.ship.x > self.enemy.ship.x + MIN_DIST_TO_ENEMY:
                            self.ship.set_acceleration(x=1)
                    else:
                        self.move_to_direction(direction_to_enemy)
                    if dist_to_enemy <= COPPER_SHELL_SHOT_DIST:
                        self.skills_list.use({"real_click_x": self.enemy.ship.x, "real_click_y": self.enemy.ship.y,
                                              "level": level})
                    if self.ship.health < self.ship.max_health / 2:
                        self.behaviour = "escape"
            if self.behaviour == "escape":
                if dist_to_enemy < MAX_DIST_TO_ENEMY:
                    self.move_to_direction(direction_to_enemy + 180)
                if dist_to_enemy > MAX_DIST_TO_ENEMY:
                    self.move_to_direction(direction_to_enemy)
                self.skills_list.use({"real_click_x": self.enemy.ship.x, "real_click_y": self.enemy.ship.y,
                                      "level": level})

            if self.behaviour == "air_attack":
                if -self.ship.y < AIR_ATTACK_MIN_HEIGHT:
                    self.ship.set_acceleration(y=-1)
                else:
                    for i, skill in enumerate(self.skills_list.skills):
                        if isinstance(skill, LaserShot) and "laser" not in self.ship.effects:
                            self.skills_list.selected = i
                            self.skills_list.use({"real_click_x": self.enemy.ship.x, "real_click_y": self.enemy.ship.y,
                                          "level": level})
                        if isinstance(skill, LaserShot):
                            break
                if "laser" in self.ship.effects:
                    x, y = self.enemy.ship.x, self.enemy.ship.y
                    direction = to_point(self.ship.x, self.ship.y, x, y) % 360
                    current_direction = self.ship.effects["laser"].direction % 360
                    angle = get_angle(current_direction, direction)
                    delta = 0
                    if abs(angle) > 1:
                        delta = 0.1 if angle > 0 else -0.1
                    self.ship.effects["laser"].set_direction(current_direction + delta)

        for obj in [*level.get("enemys_ships"), level.get("player").ship]:
            dist = math.hypot(obj.x - self.ship.x, obj.y - self.ship.y)
            if obj != self.ship and dist < MIN_DIST_TO_SHIP:
                direction = to_point(obj.x, obj.y, self.ship.x, self.ship.y)
                self.ship.stop(True, True)
                self.move_to_direction(direction)

        for obj in level.get("bullets"):
            dist = math.hypot(obj.x - self.ship.x, obj.y - self.ship.y)
            direction_from_bullet = to_point(obj.x, obj.y, self.ship.x, self.ship.y) % 360
            angle = obj.direction % 360 - direction_from_bullet
            if angle > 180:
                angle = 360 - angle
            if angle < -180:
                angle = - (360 + angle)
            if dist < MIN_DIST_TO_SHIP * 10 and (abs(angle) < 10 or (abs(angle) < 30 and self.behaviour ==
                                                                     "air_attack")):
                direction = to_point(obj.x, obj.y, self.ship.x, self.ship.y)
                self.ship.stop(True, True)
                dop = 90
                if angle < 0:
                    dop = -90
                self.move_to_direction(direction - dop)

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

    def get_info_for_drawing(self):
        return self.ship.info_for_drawing()
