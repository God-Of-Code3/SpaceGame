import pygame
import os
import sys
import time


class SpriteAnimation(pygame.sprite.Sprite):
    frames = pygame.sprite.Group()
    
    def __init__(self, *group, x, y, original, actions):
        super().__init__(*group)
        self.original = original.image
        self.rect = self.original.get_rect() # Прямоугольник
        self.rect.x = x
        self.rect.y = y
        # Действия
        self.actions = actions
        self.action_now = self.actions.keys()[0]
        self.time = self.actions[self.actions.keys()[0]]['frames'][1]
        # Таймер
        pygame.time.set_timer(MYEVENTTYPE, self.time)
        
    def draw(self, screen, action): # Анимация
        image = pygame.image.load(self.actions[self.action_now]['frames'][0]) # Загрузка изображения
        self.time = self.actions[self.action_now]['frames'][1]
        pygame.time.set_timer(MYEVENTTYPE, self.time)
        
    def update(self, camera, rotation, *events): # Изменение параметров
        # Изменение размера картинки
        w = int(self.rect.width * camera.get_zoom())
        h = int(self.rect.height * camera.get_zoom())
        self.original = pygame.transform.scale(self.original, (w, h))
        self.rect.width *= camera.get_zoom()
        self.rect.height *= camera.get_zoom()
        
        # Вращение изображения с прямоугольником
        rot_image = pygame.transform.rotate(self.original, rotation)
        rot_rect = self.rect.copy()
        rot_rect.center = rot_image.get_rect().center
        self.original = rot_image.subsurface(rot_rect).copy()      
        
        # Перемещение изображения относительно камеры
        x = SIZE[0] / 2 + (self.rect.x - self.rect.width / 2 - camera.get_position()[0]) * camera.get_zoom()
        y = SIZE[1] / 2 + (self.rect.y - self.rect.height / 2 - camera.get_position()[1]) * camera.get_zoom()
        self.rect.center = (x, y)
        
        # Таймер кадров
        MYEVENTTYPE = pygame.USEREVENT + 1
        for e in events:
            if e.type == MYEVENTTYPE:
                self.action_now = self.actions[self.action_now]['next']
