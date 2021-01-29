import pygame
from Constants import FILES_WAY
from math import pi


class Button:
    def __init__(self, text, text_color, text_size, font,
                 x, y, w, h, colors, rounding=False,
                 images=None):
        self.images = None
        if images:
            self.text_color = pygame.Color(255, 255, 255)
            self.sequence = 0
            self.images = []
            for frame in images:
                self.images.append(pygame.transform.scale(pygame.image.load(FILES_WAY + frame), (w, h)))
        else:
            self.text_color = text_color

        self.blocked = False
        
        self.text = text
        self.text_size = text_size
        self.font = font
        
        self.colors = colors
        self.color = self.colors[0]
        
        self.rounding = rounding

        # Область нажатия
        self.rect = pygame.Rect(x, y, w, h)

        # Переменные размеров
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # Значения нажатия
        self.on = False
        self.down = False

    def frames_animation(self):
        if self.images:
            if len(self.images) == self.sequence + 1:
                self.sequence = 0
            else:
                self.sequence += 1

    def animation(self): # Анимация при нажатии
        if len(self.colors) == 4 and self.blocked:
            self.color = self.colors[3]
            if self.images:
                self.text_color = pygame.Color(100, 100, 100)
        elif self.on and self.down:
            self.color = self.colors[2]
            if self.images:
                self.text_color = pygame.Color(150, 150, 150)
        elif self.on:
            self.color = self.colors[1]
            if self.images:
                self.text_color = pygame.Color(200, 200, 200)
        else:
            self.color = self.colors[0]
            if self.images:
                self.text_color = pygame.Color(255, 255, 255)

    def drawing(self, screen):  # Нарисовать кнопку
        self.animation()  # Запуск анимации

        if self.images:
            screen.blit(self.images[self.sequence], (self.x, self.y))
        else:
            # Рисование кнопки
            if self.rounding:
                round = int(self.h / 2)
            else:
                round = 0
            pygame.draw.rect(screen, self.color, (self.x, self.y,
                                                  self.w, self.h), 0, round)

        # Отрисовка текста
        to_write = pygame.font.SysFont(self.font, self.text_size).render(self.text, 1, self.text_color)
        screen.blit(to_write, (
        (self.x + self.w / 2) - to_write.get_width() / 2, (self.y + self.h / 2) - to_write.get_height() / 2))
        
    def block(self, value):
        self.blocked = value

    def selected(self, value): # Ниже функции для нажатия
        if not value:
            self.down = False
        # self.down = False
        self.on = value

    def on_button(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    def pressed(self, value):
        if not self.blocked:
            self.down = value
