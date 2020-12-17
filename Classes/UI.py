import pygame
from math import pi

# Константы схемы оформления
SIZE = (1000, 1000)

BUTTON_COLOR = pygame.Color('black')
MOUSE_ON_BUTTON_COLOR = pygame.Color('grey')
PRESSED_BUTTON_COLOR = pygame.Color('white')

TEXT_COLOR = pygame.Color('red')
TEXT_SIZE = 50

OUTLINE_COLOR = pygame.Color('green')
OUTLINE_FATNESS = 2


class Button:
    def __init__(self, text, x, y, w, h, rounding=True):
        self.color = BUTTON_COLOR
        self.rounding = rounding
        self.text = text

        # Сохранение области нажатия
        if rounding: # Круглая ли кнопка
            self.rect = pygame.Rect(x - h, y, w + h * 2, h)
        else:
            self.rect = pygame.Rect(x - h / 2, y, w + h, h)

        # Переменные размеров
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # Значения нажатия
        self.on = False
        self.down = False

    def animation(self): # Анимация при нажатии
        if self.on and self.down:
            self.color = PRESSED_BUTTON_COLOR
        elif self.on:
            self.color = MOUSE_ON_BUTTON_COLOR
        else:
            self.color = BUTTON_COLOR

    def drawing(self, screen):  # Нарисовать кнопку
        self.animation() # Запуск анимации

        # Рисование кнопки
        pygame.draw.rect(screen, self.color, (self.x - self.h / 2, self.y, self.w + self.h, self.h), 0)
        if self.rounding:
            pygame.draw.circle(screen, self.color, (self.x - self.h / 2, self.y + self.h / 2), self.h / 2)
            pygame.draw.circle(screen, self.color, (self.x + self.w + self.h / 2, self.y + self.h / 2), self.h / 2)

            pygame.draw.arc(screen, OUTLINE_COLOR, (self.x + self.w, self.y, self.h, self.h),
                            pi * 3 / 2, pi / 2, OUTLINE_FATNESS)
            pygame.draw.arc(screen, OUTLINE_COLOR, (self.x - self.h, self.y, self.h, self.h + 2),
                            pi / 2, pi * 3 / 2, OUTLINE_FATNESS)

            pygame.draw.line(screen, OUTLINE_COLOR, (self.x - self.h / 2, self.y),
                             (self.x + self.w + self.h / 2 + 4, self.y), OUTLINE_FATNESS)
            pygame.draw.line(screen, OUTLINE_COLOR, (self.x - self.h / 2 - 4, self.y + self.h),
                             (self.x + self.w + self.h / 2, self.y + self.h), OUTLINE_FATNESS)
        else:
            pygame.draw.rect(screen, OUTLINE_COLOR, (self.x - self.h / 2, self.y, self.w + self.h, self.h),
                             OUTLINE_FATNESS)

        # Отрисовка текста
        to_write = pygame.font.SysFont("Calibri", int(TEXT_SIZE)).render(self.text, 1, TEXT_COLOR)
        screen.blit(to_write, ((self.x + self.w / 2) - to_write.get_width() / 2, (self.y + self.h / 2) - to_write.get_height() / 2))


class Menu(Button): # Кнопка меню
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
        self.down = value
        self.action()

    def action(self):
        pass # Пока пустая


class StatusBar(Button): # Значение чего-либо
    def change_value(self, value): # Изменение значения
        self.text = self.text + ': ' + str(value)


# Пример
if __name__ == '__main__':
    pygame.init()
    size = width, height = SIZE[0], SIZE[1]
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('black'))

    menu = Menu('Menu', 120, 10, 200, 100)

    energy = StatusBar('energy', SIZE[0] - 320, 10, 200, 100)
    strength = StatusBar('strength', SIZE[0] - 320, SIZE[1] - 110, 200, 100)
    energy.change_value(100)
    strength.change_value(100)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                if menu.on_button(event.pos):
                    menu.selected(True)
                else:
                    menu.selected(False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu.on_button(event.pos):
                    menu.pressed(True)
                else:
                    menu.pressed(False)
        screen.fill(pygame.Color('black'))
        menu.drawing(screen)
        energy.drawing(screen)
        strength.drawing(screen)
        pygame.display.flip()
    pygame.quit()
