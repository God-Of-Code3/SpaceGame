from Classes.Starship import *
import pygame
import time


class VisualHandler:
    def __init__(self, level):
        self.level = level
        self.shaking = 0
        self.last_health = 0

    def draw(self):
        start_time = time.time()
        self.level.get("screen").fill((55, 29, 171))  # Заливка экрана

        if self.level.get("player").ship.health > 0:  # Позиционирование камеры относительно корабля игрока
            self.level.get("cam").cam_pos = (self.level.get("player").ship.x, self.level.get("player").ship.y)
        if self.last_health > self.level.get("player").ship.health:  # Активация тряски
            self.shaking = 0
            if self.level.get("player").ship.health <= 0 and self.last_health > 0:
                self.level.get("all_sprites").remove_internal(self.level.get("player").ship.sprite)
                self.level.get("expls").append(Explosion(self.level.get("player").ship.x,
                                                         self.level.get("player").ship.y, 300,
                                                         self.level.get("cam")))
            self.last_health = self.level.get("player").ship.health

        if self.shaking != 0 and False:  # Тряска
            sh_lvl = 5
            self.level.get("cam").cam_pos = (self.level.get("cam").cam_pos[0] + random.randint(-sh_lvl, sh_lvl),
                                             self.level.get("cam").cam_pos[1] + random.randint(-sh_lvl, sh_lvl))
        drawing = []  # Список отрисовок
        for bullet in self.level.get("bullets"):  # Добавление снарядов в список для отрисовки
            drawing.append(bullet.info_for_drawing())

        # Отрисовка объектов из списка отрисовки
        self.level.get("cam").drawing(drawing, self.level.get("cam").cam_pos, self.level.get("cam").zoom_value)
        self.level.get("all_sprites").update()
        # Отрисовка уровня прочности кораблей
        for spr in self.level.get("all_sprites").sprites():
            if isinstance(spr.master, Starship):
                w, h = max(100 * self.level.get("cam").zoom_value, 40), max(20 * self.level.get("cam").zoom_value, 8)
                x = spr.rect.center[0] - w / 2
                y = spr.rect.y - h - 10

                percent = max(int(spr.master.health / spr.master.max_health * w), 0)
                pygame.draw.rect(self.level.get("screen"), (41, 255, 62), (x, y, percent, h))
                pygame.draw.rect(self.level.get("screen"), (255, 255, 255), (x, y, w, h), 1)

        # Отрисовка спрайтов

        for ai in self.level.get("enemys_ai"):
            ai.draw(self.level.get("screen"), self.level.get("cam"))
        self.level.get("player").draw(self.level.get("screen"), self.level.get("cam"))
        start_time = time.time()
        self.level.get("all_sprites").draw(self.level.get("screen"))


        # Отрисовка планеты
        self.level.get("planet").draw(self.level.get("screen"))

        # Отрисовка взрывов
        for expl in self.level.get("expls"):
            expl.draw(self.level.get("screen"))
        print(time.time() - start_time)
        start_time = time.time()
        # Отрисовка интерфейса игрока
        self.level.get("player").draw_interface(self.level.get("screen"))

        self.shaking = max(0, self.shaking - 1)
        pygame.display.flip()
        print(time.time() - start_time)
        start_time = time.time()
