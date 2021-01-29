import pygame
import json
from Button import Button
from Constants import *

RESOLUTIONS = [(1280, 1024), (1440, 900), (1600, 900), (1920, 1080)]


class Settings:
    def __init__(self, size):
        self.size = size

        self.count = RESOLUTIONS.index(self.size)

        self.x = (self.size[0] - SETTINGS_SIZE[0]) / 2
        self.y = (self.size[1] - SETTINGS_SIZE[1]) / 2
        self.buttons = [Button('X', TEXT_COLOR, CLOSE_BUTTON, FONT,
                               self.x + SETTINGS_SIZE[0] - PAD15,
                               self.y - PAD15, PAD15, PAD15,
                               (CLOSE_COLOR1, CLOSE_COLOR2, CLOSE_COLOR3), True),
                        Button('<', TEXT_COLOR, CLOSE_BUTTON, FONT,
                               self.x + PAD16, self.y + PAD16, PAD17, PAD17,
                               (BUY_COLOR1, BUY_COLOR2, BUY_COLOR3, BUY_COLOR4)),
                        Button('>', TEXT_COLOR, CLOSE_BUTTON, FONT,
                               self.x + SETTINGS_SIZE[0] - PAD17 - PAD16, self.y + PAD16, PAD17, PAD17,
                               (BUY_COLOR1, BUY_COLOR2, BUY_COLOR3, BUY_COLOR4))]

    def drawing(self, screen):
        # Окно
        pygame.draw.rect(screen, INFO_COLOR, (self.x, self.y,
                                              SETTINGS_SIZE[0], SETTINGS_SIZE[1]))

        # Верхняя панель
        pygame.draw.rect(screen, CLOSE_PANEL_COLOR, (self.x, self.y - PAD15,
                                                     SETTINGS_SIZE[0], PAD15))
        window = pygame.font.SysFont(FONT, int(CLOSE_BUTTON - PAD10)).render('Настройки', True,
                                                                             TEXT_COLOR)
        screen.blit(window, (self.x + PAD15,
                             self.y - PAD15 + window.get_height() / 2))

        # Выбранное разрешение
        resol = pygame.font.SysFont(FONT, int(CLOSE_BUTTON - PAD10)).render('*'.join([str(i) for i in RESOLUTIONS[self.count]]),
                                                                            True, TEXT_COLOR)
        screen.blit(resol, (self.x + (SETTINGS_SIZE[0] - resol.get_width()) / 2,
                            self.y + PAD17 - resol.get_height() / 2))

        # Кнопки
        for button in self.buttons:
            button.drawing(screen)

    def controller(self, event, screen):
        if self.buttons[0].down:
            resolution = {'x': RESOLUTIONS[self.count][0], 'y': RESOLUTIONS[self.count][1]}
            with open('ScreenSize.json', 'w') as size:
                json.dump(resolution, size)
                print(resolution)
            return False
        elif self.buttons[1].down and self.count > 0:
            self.buttons[1].down = False
            self.count -= 1
        elif self.buttons[2].down and self.count + 1 < len(RESOLUTIONS):
            self.buttons[2].down = False
            self.count += 1

        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                if button.on_button(event.pos):
                    button.selected(True)
                else:
                    button.selected(False)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.on_button(event.pos):
                    button.pressed(True)
                else:
                    button.pressed(False)
        return True
