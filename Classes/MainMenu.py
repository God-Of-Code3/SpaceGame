import pygame
from Classes.Button import Button
from Classes.Inventory import Inventory


SIZE = (1200, 900) # Размер окна
SPEED = 0.1 # скорость прокрутки фона в (пикселей в кадр)
#FPS = 60
BACKGROUND = '1.jpg' # файл фона
FILES_WAY = 'data\\' # путь к файлам

# Кнопка
BTN_SIZE = (200, 100)

TEXT_COLOR = pygame.Color(255, 255, 255)
TEXT_SIZE = 32
FONT = None # Шрифт

BTN_CLR1 = pygame.Color(150, 150, 150)
BTN_CLR2 = pygame.Color(100, 100, 100)
BTN_CLR3 = pygame.Color(50, 50, 50)


def get_inventory():
    return ([('1.jpg', 4, 0, 5), ('2.jpg', 3, 1, -1)], 9, 3,
            [('3.jpg', 4, 0, 100)], 8, 1,
            1000)


class MainMenu():
    def __init__(self, background, speed):
        self.inventory = None
        
        self.to_battle = Button('В бой', TEXT_COLOR, TEXT_SIZE, FONT, 
                                (SIZE[0] - BTN_SIZE[0]) / 2,
                                (SIZE[1] - BTN_SIZE[1]) / 2,
                                *BTN_SIZE,
                                (BTN_CLR1, BTN_CLR2, BTN_CLR3), True)
        
        #self.speed = speed / FPS
        self.speed = speed
        
        self.background = pygame.image.load(FILES_WAY + background)
        self.height = int(self.background.get_height() * (SIZE[0] / self.background.get_width()))
        self.background = pygame.transform.scale(self.background, (SIZE[0], self.height))
        self.pos_y = 0
    
    def drawing(self, screen):
        if self.inventory:
            self.inventory.drawing(screen)
        else:
            screen.blit(self.background, (0, self.pos_y))
            screen.blit(self.background, (0, self.pos_y - self.height))
            
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
                    self.inventory = Inventory(screen, *get_inventory())                
                else:
                    self.to_battle.pressed(False)
        
        
# Пример
if __name__ == '__main__':
    pygame.init()
    size = width, height = SIZE[0], SIZE[1]
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('black'))

    menu = MainMenu(BACKGROUND, SPEED)

    #fps = FPS
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
        #clock.tick(fps)
    pygame.quit()
