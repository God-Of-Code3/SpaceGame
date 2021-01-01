import pygame


class Planet:
    def __init__(self, y, image, width, height, cam):
        self.image = pygame.image.load(image).convert_alpha()
        self.width, self.height = width, height
        self.cam = cam
        self.y = y
        self.bottom_color = self.image.get_at((0, self.image.get_rect().height - 1))

    def draw(self, screen):
        """bottom_y = self.cam.cam_pos[1] + self.cam.size[1] / 2 / self.cam.zoom_value
        if self.y >= bottom_y:"""
        w, h = int(self.width * self.cam.zoom_value) + 1, int(self.height * self.cam.zoom_value) + 1
        img = pygame.transform.scale(self.image, (w, h))
        cam_left = self.cam.cam_pos[0] - self.cam.size[0] / 2 / self.cam.zoom_value
        cam_right = self.cam.cam_pos[0] + self.cam.size[0] / 2 / self.cam.zoom_value
        nearest_x = (cam_left // self.width) * self.width
        y = int(self.cam.size[1] / 2 + (self.y - self.cam.cam_pos[1]) * self.cam.zoom_value)
        i = 0
        while nearest_x < cam_right:
            nearest_x = (cam_left // self.width + i) * self.width
            i += 1
            x = int(self.cam.size[0] / 2 + (nearest_x - self.cam.cam_pos[0]) * self.cam.zoom_value)

            screen.blit(img, (x, y))
        bottom_y = y + h
        if bottom_y < self.cam.size[1]:
            pygame.draw.rect(screen, self.bottom_color[0:3], (0, y + h, self.cam.size[0], self.cam.size[1] - bottom_y))


class World:
    def __init__(self, width):
        self.range = (0, width)
