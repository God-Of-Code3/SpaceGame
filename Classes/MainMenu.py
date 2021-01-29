import pygame
import json
from Button import Button
from Inventory import Inventory
from Settings import Settings
from Constants import *


# МЕНЮ
with open('ScreenSize.json') as size:
    s = json.load(size)
SIZE = tuple([key[1] for key in s.items()])

FPS = 60
SPEED = 1 # скорость прокрутки фона в (пикселей в кадр)
BACKGROUND = 'background.jpg' # файл фона
TO_SETTINGS_NAME = 'settings_icon.png' # имя файла иконки настроек
FRAMES = ['1.jpg', '2.jpg', '3.jpg', '4.png', '5.png'] # Кадры анимации кнопки
FRAMES_SPEED = 10 # Интервал между кадрами


def get_inventory():
    return ([('1.jpg', 4, 0, 5), ('2.jpg', 3, 1, -1)], 9, 3,
            [('3.jpg', 4, 0, 100)], 8, 1,
            1000)


class MainMenu():
    def __init__(self, background, speed, clock):
        self.inventory = None

        self.btl_n = 0
        self.btl_max = FRAMES_SPEED
        self.to_battle = Button('В бой', TEXT_COLOR, TEXT_SIZE, FONT, 
                                (SIZE[0] - BTN_SIZE[0] / 2) / 2,
                                (SIZE[1] - BTN_SIZE[1] / 2) / 2,
                                *START_BTN_SIZE,
                                (BTN_CLR1, BTN_CLR2, BTN_CLR3), True,
                                FRAMES)
        
        self.speed = speed
        self.clock = clock
        
        self.background = pygame.image.load(FILES_WAY + background)
        self.height = int(self.background.get_height() * (SIZE[0] / self.background.get_width()))
        self.background = pygame.transform.scale(self.background, (SIZE[0], self.height))
        self.pos_y = 0

        self.settings = None
        self.selected = False
        self.pressed = False
        self.settings_icon_color = SHOP_ICON_COLOR
        self.settings_icon = pygame.image.load(FILES_WAY + TO_SETTINGS_NAME)
        self.settings_icon = pygame.transform.scale(self.settings_icon,
                                                   (int(SHOP_HEIGHT / 2),
                                                    int(SHOP_HEIGHT / 2)))

    def settings_color(self):
        if self.selected:
            if self.pressed:
                self.settings_icon_color = PRESSED_ICON_COLOR
            else:
                self.settings_icon_color = SELECTED_ICON_COLOR
        else:
            self.settings_icon_color = SHOP_ICON_COLOR
    
    def drawing(self, screen):
        self.clock.tick(FPS)
        if self.inventory:
            self.inventory.drawing(screen)
        else:
            screen.blit(self.background, (0, self.pos_y))
            screen.blit(self.background, (0, self.pos_y - self.height))
            
            self.pos_y += self.speed
            if self.pos_y > self.height:
                self.pos_y = 0

            # Рисование панели магазина
            pygame.draw.rect(screen, SHOP_COLOR, (0, 0, SIZE[0], SHOP_HEIGHT))

            text = pygame.font.Font(FONT, MONEY_SIZE).render(str(get_inventory()[6]) + '$',
                                                             True, MONEY_COLOR)
            screen.blit(text, (SHOP_HEIGHT + PAD6, (SHOP_HEIGHT - MONEY_SIZE / 2) / 2))

            self.settings_color()
            pygame.draw.rect(screen, SHOP_SQUARE_COLOR,
                             (0, 0, SHOP_HEIGHT, SHOP_HEIGHT))
            pygame.draw.circle(screen, self.settings_icon_color,
                               (SHOP_HEIGHT / 2, SHOP_HEIGHT / 2),
                               SHOP_HEIGHT / 2 - PAD7 * 2)
            screen.blit(self.settings_icon, (SHOP_HEIGHT / 4, SHOP_HEIGHT / 4))

            # Рисование кнопки "В бой"
            self.btl_n += self.speed
            if self.btl_n > self.btl_max:
                self.to_battle.frames_animation()
                self.btl_n = 0

            self.to_battle.drawing(screen)

            if self.settings:
                self.settings.drawing(screen)

    def go_to_settings(self):
        self.settings = Settings(SIZE)
    
    def controller(self, event, screen):
        global SIZE
        if self.inventory:
            self.inventory.controller(event, screen)
        elif self.settings:
            if not self.settings.controller(event, screen):
                self.settings = None
                self.selected = False

                # МЕНЮ
                with open('ScreenSize.json') as size:
                    s = json.load(size)

                SIZE = tuple([key[1] for key in s.items()])
                self.to_battle = Button('В бой', TEXT_COLOR, TEXT_SIZE, FONT,
                                        (SIZE[0] - BTN_SIZE[0] / 2) / 2,
                                        (SIZE[1] - BTN_SIZE[1] / 2) / 2,
                                        *START_BTN_SIZE,
                                        (BTN_CLR1, BTN_CLR2, BTN_CLR3), True,
                                        FRAMES)
                self.background = pygame.transform.scale(self.background, (SIZE[0], self.height))
                return pygame.display.set_mode(SIZE)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SHOP_HEIGHT > event.pos[0] > 0 and SHOP_HEIGHT > event.pos[1] > 0:
                    self.pressed = True
                    self.go_to_settings()
            elif event.type == pygame.MOUSEMOTION:
                if SHOP_HEIGHT > event.pos[0] > 0 and SHOP_HEIGHT > event.pos[1] > 0:
                    self.selected = True
                else:
                    self.selected = False
                    self.pressed = False

            if event.type == pygame.MOUSEMOTION:
                if self.to_battle.on_button(event.pos):
                    self.to_battle.selected(True)
                else:
                    self.to_battle.selected(False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.to_battle.on_button(event.pos):
                    self.to_battle.pressed(True)
                    self.inventory = Inventory(screen, *get_inventory(), SIZE)
                else:
                    self.to_battle.pressed(False)
        return screen
        
        
# Пример
if __name__ == '__main__':
    pygame.init()
    size = SIZE[0], SIZE[1]
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('black'))

    clock = pygame.time.Clock()
    menu = MainMenu(BACKGROUND, SPEED, clock)

    running = True
    while running:
        screen.fill(pygame.Color('black'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                screen = menu.controller(event, screen)
        menu.drawing(screen)
        pygame.display.flip()
    pygame.quit()
