from V2.Code.Constants import *
from V2.Code.Methods import *

import pygame


class Planet:
    def __init__(self, y, image, width, height, world):
        self.image = pygame.image.load(image).convert_alpha()
        self.width, self.height = width, height
        self.world = world
        self.y = y
        self.bottom_color = self.image.get_at((0, self.image.get_rect().height - 1))

    def draw(self, screen):
        """bottom_y = cam.pos[1] + cam.size[1] / 2 / zoom
        if self.y >= bottom_y:"""
        cam = self.world.cam
        zoom = cam.zoom
        w, h = int(self.width * zoom) + 1, int(self.height * zoom) + 1
        img = pygame.transform.scale(self.image, (w, h))
        cam_left = cam.pos[0] - cam.size[0] / 2 / zoom
        cam_right = cam.pos[0] + cam.size[0] / 2 / zoom
        nearest_x = (cam_left // self.width) * self.width
        y = int(cam.size[1] / 2 + (self.y - cam.pos[1]) * zoom)
        i = 0
        while nearest_x < cam_right:
            nearest_x = (cam_left // self.width + i) * self.width
            i += 1
            x = int(cam.size[0] / 2 + (nearest_x - cam.pos[0]) * zoom)

            screen.blit(img, (x, y))
        bottom_y = y + h
        if bottom_y < cam.size[1]:
            pygame.draw.rect(screen, self.bottom_color[0:3], (0, y + h, cam.size[0], cam.size[1] - bottom_y))