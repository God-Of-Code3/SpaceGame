from V2.Code.Methods import *
from V2.Code.Constants import *


class Camera:
    def __init__(self):
        self.pos = [0, 0]
        self.zoom = 0.2
        self.zoom_step = 0.1
        self.min_zoom = 0.2
        self.max_zoom = 1
        self.size = SIZE

    def apply(self, entity):
        entity.rect = entity.image.get_rect()
        entity.rect.center = (int((entity.coords[0] - self.pos[0]) * self.zoom + self.size[0] / 2),
                              int((entity.coords[1] - self.pos[1]) * self.zoom + self.size[1] / 2))

    def posite(self, entity):
        self.pos = entity.coords

    def control(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.zoom *= 1 + self.zoom_step
                if event.button == 5:
                    self.zoom *= 1 - self.zoom_step
                if self.zoom < self.min_zoom:
                    self.zoom = self.min_zoom
                if self.zoom > self.max_zoom:
                    self.zoom = self.max_zoom
