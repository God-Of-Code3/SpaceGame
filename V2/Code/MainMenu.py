import pygame
from V2.Code.Button import Button
from V2.Code.Inventory import Inventory
from V2.Code.InventoryConstants import *


# FPS = 60


def get_inventory():
    return ([('1.jpg', 4, 0, 5), ('2.jpg', 3, 1, -1)], 9, 3,
            [('3.jpg', 4, 0, 100)], 8, 1,
            1000)


BACKGROUND = './Assets/Images/Other/SpaceBg.jpg'
SPEED = 0


class MainMenu():
    def __init__(self, background, speed):
        self.inventory = None

        self.to_battle = Button('В бой', TEXT_COLOR, TEXT_SIZE, FONT,
                                (SIZE[0] - BTN_SIZE[0] / 2) / 2,
                                (SIZE[1] - BTN_SIZE[1] / 2) / 2,
                                *START_BTN_SIZE,
                                (BTN_CLR1, BTN_CLR2, BTN_CLR3), False)

        # self.speed = speed / FPS
        self.speed = speed

        self.background = pygame.image.load(background)
        self.height = self.background.get_height()
        """self.background = pygame.transform.scale(self.background, (SIZE[0], self.height))"""
        self.pos_y = 0
        self.pos_x = (SIZE[0] - self.background.get_width()) // 2

    def drawing(self, screen):
        if self.inventory:
            self.inventory.drawing(screen)
        else:
            x, y = pygame.mouse.get_pos()
            x -= SIZE[0] // 2
            y -= SIZE[1] // 2
            k = -0.02
            screen.blit(self.background, (self.pos_x + x * k, self.pos_y + y * k))
            screen.blit(self.background, (self.pos_x + x * k, self.pos_y - self.height + y * k))

            self.pos_y += self.speed
            if self.pos_y > self.height:
                self.pos_y = 0

            self.to_battle.drawing(screen)

    def controller(self, event, screen):
        if self.inventory:
            self.inventory.controller(event, screen)
        else:
            if event.type == pygame.MOUSEMOTION:
                if self.to_battle.on_button(event.pos):
                    self.to_battle.selected(True)
                else:
                    self.to_battle.selected(False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.to_battle.on_button(event.pos):
                    self.to_battle.pressed(True)
                    return True


# Пример
if __name__ == '__main__':
    pygame.init()
    size = width, height = SIZE[0], SIZE[1]
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('black'))

    menu = MainMenu(BACKGROUND, SPEED)

    # fps = FPS
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(pygame.Color('black'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                menu.controller(event, screen)
        menu.drawing(screen)
        pygame.display.flip()
        # clock.tick(fps)
    pygame.quit()