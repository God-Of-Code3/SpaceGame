import pygame
from Classes.Starship import *
from Classes.Bullet import *
from Classes.Skill import *


class Player:
    def __init__(self, world, cam, sprites_group, cls):
        self.ship, self.skills_list = create_ship(world, cam, sprites_group, 100, -700, cls)
        #self.skills_list.add(PlasmaShot)

    def control(self, events, level):
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
                        x, y = click_coords_to_real(level.get("cam"), event.pos)
                        self.skills_list.use({"real_click_x": x, "real_click_y": y,
                                              "level": level})

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if "laser" in self.ship.effects:
                        self.ship.effects.pop('laser', None)
        if "laser" in self.ship.effects:
            x, y = click_coords_to_real(level.get("cam"), pygame.mouse.get_pos())
            direction = to_point(self.ship.x, self.ship.y, x, y)
            self.ship.effects["laser"].set_direction(direction % 360)

    def update(self):
        self.skills_list.update()

    def draw(self, screen, camera):

        for effect in self.ship.effects:
            self.ship.effects[effect].draw(screen, camera)

    def draw_interface(self, screen):
        self.skills_list.draw(screen)

    def get_info_for_drawing(self):
        return self.ship.info_for_drawing()
