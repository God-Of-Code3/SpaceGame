from V2.Code.Constants import *
from V2.Code.Methods import *

import pygame


class Controller:
    def __init__(self, world):
        self.managed = None
        self.world = world

    def set_managed(self, managed):
        self.managed = managed

    def control(self):
        self.managed.acceleration = [0, 0]

    def control_object(self, obj):
        pass


class Player(Controller):
    def control(self):
        acceleration = 0.1
        for event in self.world.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.managed.acceleration[1] -= acceleration
                if event.key == pygame.K_s:
                    self.managed.acceleration[1] += acceleration
                if event.key == pygame.K_a:
                    self.managed.acceleration[0] -= acceleration
                if event.key == pygame.K_d:
                    self.managed.acceleration[0] += acceleration

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.managed.acceleration[1] -= -acceleration
                if event.key == pygame.K_s:
                    self.managed.acceleration[1] += -acceleration
                if event.key == pygame.K_a:
                    self.managed.acceleration[0] -= -acceleration
                if event.key == pygame.K_d:
                    self.managed.acceleration[0] += -acceleration


class Enemy(Controller):
    def __init__(self, *args):
        super().__init__(*args)
        self.sum_acceleration = [0, 0]

    def control_object(self, obj):
        if obj.material:
            d = math.hypot(self.managed.coords[0] - obj.coords[0], self.managed.coords[1] - obj.coords[1])
            if d < MIN_DIST_TO_OBJECTS:
                dx = (self.managed.coords[0] - obj.coords[0]) / MIN_DIST_TO_OBJECTS
                dy = (self.managed.coords[1] - obj.coords[1]) / MIN_DIST_TO_OBJECTS
                self.sum_acceleration[0] += dx
                self.sum_acceleration[1] += dy

    def control(self):
        acceleration = 0.1
        if self.sum_acceleration[0] != 0 and self.sum_acceleration[1] != 0:
            hyp = math.hypot(*self.sum_acceleration)
            dx = self.sum_acceleration[0] / hyp
            dy = self.sum_acceleration[1] / hyp

            self.managed.acceleration = [dx * acceleration, dy * acceleration]
            self.sum_acceleration = [0, 0]
        else:
            if self.managed.speed != [0, 0]:
                hyp = math.hypot(*self.managed.speed)
                dx = self.managed.speed[0] / hyp
                dy = self.managed.speed[1] / hyp

                self.managed.acceleration = [-dx * acceleration, -dy * acceleration]
