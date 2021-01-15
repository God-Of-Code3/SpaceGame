from V2.Code.Constants import *
from V2.Code.Methods import *
from V2.Code.Skills import *

import pygame


class Controller:
    def __init__(self, world, skills=[]):
        self.managed = None
        self.world = world
        self.skills = SkillList(0, 0, self, self.world, skills)
        self.skills_args = dict()
        self.skills_args["use"] = False
        self.skills_args["using"] = False
        self.skills_args["using_cords"] = (0, 0)

    def set_managed(self, managed):
        self.managed = managed

    def control(self):
        pass

    def control_object(self, obj):
        pass

    def update(self):
        self.skills.control()
        self.skills.update(self.skills_args)

    def update_skills_args(self):
        self.skills_args["use"] = False
        
    def move_to_direction(self, direction):
        x, y = math.cos(direction * math.pi / 180), math.sin(direction * math.pi / 180)
        sp = min(self.managed.max_speed[0], self.managed.max_speed[1])
        nes = [0, 0]
        nes[0], nes[1] = x * sp, y * sp
        self.managed.acceleration = [0, 0]
        if nes[0] - self.managed.speed[0] < 1:
            self.managed.set_acceleration(x=-2)
        elif nes[0] - self.managed.speed[0] > 1:
            self.managed.set_acceleration(x=2)

        if nes[1] < self.managed.speed[1]:
            self.managed.set_acceleration(y=-2)
        elif nes[1] > self.managed.speed[1]:
            self.managed.set_acceleration(y=2)


class Player(Controller):
    def control(self):
        self.update_skills_args()
        for event in self.world.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.managed.set_acceleration(x=1)
                if event.key == pygame.K_w:
                    self.managed.set_acceleration(y=-1)
                if event.key == pygame.K_a:
                    self.managed.set_acceleration(x=-1)
                if event.key == pygame.K_s:
                    self.managed.set_acceleration(y=1)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.managed.set_acceleration(x=-1)
                if event.key == pygame.K_w:
                    self.managed.set_acceleration(y=1)
                if event.key == pygame.K_a:
                    self.managed.set_acceleration(x=1)
                if event.key == pygame.K_s:
                    self.managed.set_acceleration(y=-1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.skills.check_pos(event.pos):
                    self.skills_args["use"] = True
                    self.skills_args["using"] = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.skills_args["using"] = False
        self.skills_args["using_coords"] = click_coords_to_real(self.world.cam, pygame.mouse.get_pos())


class Enemy(Controller):
    def __init__(self, target, world, skills=[], beh="attack"):
        super().__init__(world, skills=skills)
        self.sum_acceleration = [0, 0]
        self.target = target
        self.target_ship = target.managed
        self.beh = beh
        self.args = {"attacking": 0, "dist_to_target": 0}

    def control_object(self, obj):

        if obj.material and obj != self:
            d = math.hypot(self.managed.coords[0] - obj.coords[0], self.managed.coords[1] - obj.coords[1])
            if d < MIN_DIST_TO_OBJECTS and self.beh != "escape":
                if isinstance(obj, Bullet) and obj.master != self.managed:
                    self.move_to_direction(180 + to_point(*self.managed.coords, *obj.coords))
            if obj == self.target_ship:
                self.skills_args["use"] = False
                direction_to_target = to_point(*self.managed.coords, *obj.coords)
                if self.beh == "attack":
                    attacking = self.args["attacking"]
                    self.args["attacking"] = 0
                    self.args["dist_to_target"] = d
                    if attacking < 7:
                        if d > MAX_DIST_TO_ENEMY:
                            self.managed.stop(True, True)
                            self.move_to_direction(direction_to_target)
                        else:
                            isset = False
                            ready = False
                            for i, skill in enumerate(self.skills.skills):
                                if skill is not None:
                                    if isinstance(skill, CopperShellShot) or isinstance(skill, PlasmaShot):
                                        isset = True
                                        if skill.number != 0:
                                            if isinstance(skill, CopperShellShot) or isinstance(skill, PlasmaShot):
                                                self.skills.select(i)
                                                ready = True
                                                break
                            if isset and ready:
                                self.skills_args["use"] = True
                                self.skills_args["using_coords"] = obj.coords

                            if isset and not ready:
                                self.beh = "escape"
                    if self.managed.health < self.managed.max_health // 2:
                        self.beh = "escape"
                elif self.beh == "escape":
                    self.managed.stop(True, True)
                    if d < MAX_DIST_TO_ENEMY * 2:
                        self.move_to_direction(180 + direction_to_target)
                elif self.beh == "air_attack":
                    self.skills.select(0)
                    if self.skills.skills[self.skills.selected].number == 0:
                        self.skills.select(1)
                    if self.skills.skills[self.skills.selected].number != 0:
                        self.skills_args["use"] = True
                        self.skills_args["using"] = True
                        self.skills_args["using_coords"] = obj.coords
                    if abs(self.managed.coords[1]) < MIN_AIR_ATTACK_HEIGHT:
                        self.move_to_direction(270)
            else:
                if math.hypot(obj.coords[0] - self.target.managed.coords[0],
                              obj.coords[1] - self.target.managed.coords[1]) < self.args["dist_to_target"]:
                    self.args["attacking"] += 1
            if isinstance(obj, Bullet) and obj.master != self.managed:
                direction = to_point(0, 0, *obj.speed) % 360
                direction2 = to_point(*obj.coords, *self.managed.coords) % 360
                angle = get_angle(direction, direction2)
                if abs(angle) < MIN_BULLET_ANGLE:
                    delta = 90 if angle > 0 else -90
                    self.move_to_direction(direction2 + delta)

        if abs(self.managed.coords[1]) < 600:
            self.managed.set_acceleration(y=-2)

    def control(self):
        """if self.sum_acceleration[0] != 0 or self.sum_acceleration[1] != 0:
            dx = self.sum_acceleration[0]
            dy = self.sum_acceleration[1]
            angle = to_point(0, 0, dx, dy)
            self.move_to_direction(angle)
            self.sum_acceleration = [0, 0]
        else:"""
        self.managed.stop(True, True)
