import pygame
from Classes.Starship import *
from Classes.Bullet import *
from Classes.Skill import *


class Player:
    def __init__(self):
        self.ship = Starship(100, 250, "Assets/Images/Ships/Starship1.png", 38, 20, 1000, 38, 20)
        self.ship = Starship(1900, 600, "Assets/Images/Ships/Starship1.png", 38, 20, 1000, 38, 20)
        #self.laser = Laser(self.ship.x, self.ship.y, to_point(self.ship.x, self.ship.y, *pygame.mouse.get_pos()))
        self.camera = None

        self.skills_list = SkillList(0, 0, 5, self.ship)
        self.skills_list.add(PlasmaShot)
        self.skills_list.add(LaserShot)

    def control(self, events, bullets, screen):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.ship.set_acceleration(x=1)
                if event.key == pygame.K_w:
                    self.ship.set_acceleration(y=-1)
                if event.key == pygame.K_a:
                    self.ship.set_acceleration(x=-1)
                if event.key == pygame.K_s:
                    self.ship.set_acceleration(y=1)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.ship.set_acceleration(x=-1)
                if event.key == pygame.K_w:
                    self.ship.set_acceleration(y=1)
                if event.key == pygame.K_a:
                    self.ship.set_acceleration(x=1)
                if event.key == pygame.K_s:
                    self.ship.set_acceleration(y=-1)
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    if not self.skills_list.check_click():
                        self.skills_list.use({"real_click_x": event.pos[0], "real_click_y": event.pos[1],
                                              "bullets": bullets})

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if "laser" in self.ship.effects:
                        self.ship.effects.pop('laser', None)
        if "laser" in self.ship.effects:
            self.ship.effects["laser"].set_direction(to_point(self.ship.x, self.ship.y, *pygame.mouse.get_pos()) % 360)

    def draw(self, screen):
        for effect in self.ship.effects:
            self.ship.effects[effect].draw(screen)

    def get_info_for_drawing(self):
        return self.ship.info_for_drawing()
