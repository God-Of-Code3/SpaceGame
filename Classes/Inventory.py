import pygame


SIZE = (1000, 800)
SQUARE_COLOR = pygame.Color(255, 0, 0)
SELECTED_COLOR = pygame.Color(150, 0, 0)
PRESSED_COLOR = pygame.Color(100, 0, 0)

INVENTORY_COLOR = pygame.Color(100, 100, 100)
CELLS_COLOR = pygame.Color(255, 255, 255)
CELLS_WIDTH = 2

PAD1 = 20 # внешний отступ
PAD2 = 10 # отступ ячеек от стен
PAD3 = 10 # отступ внутри ячеек
PAD4 = 5 # отступ картинки от квадрата


class Inventory:
    def __init__(self, inv_slots, wi, hi, player_slots, wp, hp):
        self.inv_slots = inv_slots
        self.player_slots = player_slots
        
        self.w1, self.h1 = wi, hi
        self.w2, self.h2 = wp, hp
        
        if self.w1 >= self.w2:
            self.size = (SIZE[0] - PAD1 * 2) / self.w1
        else:
            self.size = (SIZE[0] - PAD1 * 2) / self.w2

        # Добавление слотов
        self.items = [None] * self.w1
        for i in range(self.w1):
            self.items[i] = [None] * self.h1
        
        for i in list(self.inv_slots.keys()):
            x, y = self.inv_slots[i][0], self.inv_slots[i][1]
            self.items[x][y] = Square(screen, i,
                                      (SIZE[0] - self.size * self.w1) / 2 + x * self.size + PAD3,
                                      PAD1 + y * self.size + PAD3,
                                      self.size - PAD3 * 2,
                                      self.size - PAD3 * 2)
            
        # Добавление слотов игрока
        self.player_items = [None] * self.w2
        for i in range(self.w2):
            self.player_items[i] = [None] * self.h2
        
        for i in list(self.player_slots.keys()):
            x, y = self.player_slots[i][0], self.player_slots[i][1]
            self.player_items[x][y] = Square(screen, i,
                                          (SIZE[0] - self.size * self.w2) / 2 + x * self.size + PAD3,
                                          SIZE[1] - self.size * self.h2 + y * self.size - PAD1 + PAD3,
                                          self.size - PAD3 * 2,
                                          self.size - PAD3 * 2)
                                          
    def drawing(self, screen):
        # Рисование инвентаря
        pygame.draw.rect(screen, INVENTORY_COLOR,
                         ((SIZE[0] - self.size * self.w1) / 2 - PAD2,
                          PAD1 - PAD2,
                          self.size * self.w1 + PAD2 * 2,
                          self.size * self.h1 + PAD2 * 2))
        
        pygame.draw.rect(screen, INVENTORY_COLOR,
                         ((SIZE[0] - self.size * self.w2) / 2 - PAD2,
                         SIZE[1] - self.size * self.h2 - PAD1 - PAD2,
                         self.size * self.w2 + PAD2 * 2,
                         self.size * self.h2 + PAD2 * 2))
        
        # Рисование сетки
        for i in range(self.w1):
            for j in range(self.h1):
                pygame.draw.rect(screen, CELLS_COLOR,
                                 ((SIZE[0] - self.size * self.w1) / 2 + i * self.size,
                                 PAD1 + j * self.size,
                                 self.size + 1,
                                 self.size + j % 2 + 1),
                                 CELLS_WIDTH)
        for i in range(self.w2):
            for j in range(self.h2):
                pygame.draw.rect(screen, CELLS_COLOR,
                                 ((SIZE[0] - self.size * self.w2) / 2 + i * self.size,
                                 SIZE[1] - (j + 1) * self.size - PAD1,
                                 self.size + 1,
                                 self.size + j % 2 + 1),
                                 CELLS_WIDTH)
    
        # Рисование слотов инвентаря
        for q in list(self.inv_slots.keys()):
            x, y = self.inv_slots[q][0], self.inv_slots[q][1]
            self.items[x][y].drawing(screen)
            self.square_pulling(x, y, self.items, q, self.inv_slots)
            
        # Рисование слотов игрока
        for q in list(self.player_slots.keys()):
            x, y = self.player_slots[q][0], self.player_slots[q][1]
            self.player_items[x][y].drawing(screen)
            self.square_pulling(x, y, self.player_items, q, self.player_slots)
                    
        # Рисование движущегося квадрата поверх остальных
        for q in list(self.inv_slots.keys()):
            x, y = self.inv_slots[q][0], self.inv_slots[q][1]
            if self.items[x][y].moving:
                self.items[x][y].drawing(screen)
            
        for q in list(self.player_slots.keys()):
            x, y = self.player_slots[q][0], self.player_slots[q][1]
            if self.player_items[x][y].moving:
                self.player_items[x][y].drawing(screen)
    
    # Притягивание квадрата    
    def square_pulling(self, x, y, arr, q, dictionary):
        # Присвоение ближайшей клетке
        m = 1000000
        nearest_square = (0, 0)
        to_inventory = False
        pos = (0, 0)
        
        px = arr[x][y].xm + arr[x][y].w / 2
        py = arr[x][y].ym + arr[x][y].h / 2
        for i in range(self.w1):
            for j in range(self.h1):
                if self.items[i][j] == None or self.items[i][j] == arr[x][y]:
                    sqx = (SIZE[0] - self.size * self.w1) / 2 + (i + 0.5) * self.size
                    sqy = PAD1 + (j + 0.5) * self.size
                    
                    if ((px - sqx) ** 2 + (py - sqy) ** 2) ** 0.5 <= m:
                        pos = (i, j)
                        m = ((px - sqx) ** 2 + (py - sqy) ** 2) ** 0.5
                        nearest_square = (sqx - self.size / 2 + PAD3 + 1,
                                          sqy - self.size / 2 + PAD3 + 1)
                        to_inventory = True                    
                    
        for i in range(self.w2):
            for j in range(self.h2):
                if self.player_items[i][j] == None or self.player_items[i][j] == arr[x][y]:
                    sqx = (SIZE[0] - self.size * self.w2) / 2 + (i + 0.5) * self.size
                    sqy = SIZE[1] - (j + 0.5) * self.size - PAD1
                        
                    if ((px - sqx) ** 2 + (py - sqy) ** 2) ** 0.5 <= m:
                        pos = (i, j)
                        m = ((px - sqx) ** 2 + (py - sqy) ** 2) ** 0.5
                        nearest_square = (sqx - self.size / 2 + PAD3 + 1,
                                          sqy - self.size / 2 + PAD3 + 1)
                        to_inventory = False                    
                    
        # Изменение координат
        if not arr[x][y].moving:
            arr[x][y].xm = nearest_square[0]
            arr[x][y].ym = nearest_square[1]
            if dictionary[q] != pos:
                if (arr == self.items and to_inventory) or (arr == self.player_items and not to_inventory):
                    arr[pos[0]][pos[1]] = Square(screen, q,
                                             arr[x][y].xm,
                                             arr[x][y].ym,
                                             arr[x][y].w,
                                             arr[x][y].h)
                    arr[x][y] = None
                    dictionary[q] = pos
                else:
                    if arr == self.items:
                        other_arr = self.player_items
                        other_dict = self.player_slots
                    else:
                        other_arr = self.items
                        other_dict = self.inv_slots
                        
                    other_arr[pos[0]][pos[1]] = Square(screen, q,
                                             arr[x][y].xm,
                                             arr[x][y].ym,
                                             arr[x][y].w,
                                             arr[x][y].h)
                    arr[x][y] = None
                    del dictionary[q]
                    other_dict[q] = pos
        
    def get_inventory_slots(self):
        return self.inv_slots
    
    def get_player_slots(self):
        return self.player_slots
     
    def controller(self, event):
        for i in list(self.inv_slots.keys()):
            x, y = self.inv_slots[i][0], self.inv_slots[i][1]
            self.items[x][y].controller(event)
            
        for i in list(self.player_slots.keys()):
            x, y = self.player_slots[i][0], self.player_slots[i][1]
            self.player_items[x][y].controller(event)


class Square:
    def __init__(self, screen, image, x, y, w, h):
        self.move_screen = pygame.Surface(screen.get_size())
        self.color = SQUARE_COLOR
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        
        self.image = pygame.image.load('..\\Assets\\Images\\Skills\\' + image)
        self.image = pygame.transform.scale(self.image,
                                            (int(self.w - PAD4 * 2),
                                             int(self.h - PAD4 * 2)))
        
        self.down = False
        self.on = False
        
        self.moving = False
        self.xm = self.x
        self.ym = self.y
        
    def controller(self, event):  # Обработка событий мыши
        if event.type == pygame.MOUSEMOTION:
            if self.on_button(event.pos):
                self.selected(True)
            else:
                self.selected(False)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.on_button(event.pos):
                self.pressed(True, screen)
            else:
                self.pressed(False, screen)
        
        if self.down:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.on_button(event.pos):
                    self.moving = True
                    self.x, self.y = event.pos[0] - self.xm, event.pos[1] - self.ym
            if event.type == pygame.MOUSEBUTTONUP:
                self.move_screen.blit(screen, (0, 0))
                self.moving = False
            if event.type == pygame.MOUSEMOTION:
                if self.moving:
                    self.xm, self.ym = event.pos[0] - self.x, event.pos[1] - self.y
        else:
            self.moving = False

    def animation(self): # Смена цвета квадрата
        if self.moving:
            self.color = PRESSED_COLOR
        elif self.on:
            self.color = SELECTED_COLOR
        else:
            self.color = SQUARE_COLOR

    def drawing(self, screen): # Отрисовка
        self.animation()
        self.rect = pygame.Rect((self.xm, self.ym, self.w, self.h))
        pygame.draw.rect(screen, self.color, self.rect)
        
        screen.blit(self.image, (self.xm + PAD4, self.ym + PAD4))        
        
    # Ниже функции для определения нажатия
    def selected(self, value):
        self.on = value

    def on_button(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    def pressed(self, value, screen):
        self.down = value
        self.action(screen)

    def action(self, screen):
        pass
    
# Пример
if __name__ == '__main__':
    pygame.init()
    size = width, height = SIZE[0], SIZE[1]
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('black'))

    inv = Inventory({'CopperShell.png': (4, 0), 'LaserRay.png': (3, 1), 'PlasmaShot.png': (5, 2)}, 9, 3,
                    {'SmallRocket.png': (3, 0)}, 8, 1)

    running = True
    while running:
        screen.fill(pygame.Color('black'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            else:
                inv.controller(event)
        inv.drawing(screen)
        pygame.display.flip()
    print()
    pygame.quit()
