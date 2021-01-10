import pygame


SIZE = (1000, 1000)
SQUARE_COLOR = pygame.Color(255, 0, 0)
SELECTED_COLOR = pygame.Color(150, 0, 0)
PRESSED_COLOR = pygame.Color(100, 0, 0)

INVENTORY_COLOR = pygame.Color(100, 100, 100)
CELLS_COLOR = pygame.Color(255, 255, 255)
CELLS_WIDTH = 2

PAD1 = 50 # внешний отступ
PAD2 = 10 # отступ ячеек от стен
PAD3 = 10 # отступ внутри ячеек
PAD4 = 5 # отступ картинки от квадрата

FONT = None
TEXT_SIZE = 32
TEXT_COLOR = pygame.Color(255, 255, 255)

global_pressed = False


class Inventory():
    def __init__(self, inv_slots, wi, hi, player_slots, wp, hp):
        self.square_clone = None
        self.clone_info = ('image', 'x', 'y', 'count', 'arr', 'slots')
        
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
        
        for i in self.inv_slots:
            x, y, n = i[1], i[2], i[3]
            xpos = (SIZE[0] - self.size * self.w1) / 2 + x * self.size + PAD3
            ypos = PAD1 + y * self.size + PAD3         
            self.items[x][y] = Square(screen, i[0], xpos, ypos,
                                      self.size - PAD3 * 2,
                                      self.size - PAD3 * 2, n)
            
        # Добавление слотов игрока
        self.player_items = [None] * self.w2
        for i in range(self.w2):
            self.player_items[i] = [None] * self.h2
        
        for i in self.player_slots:
            x, y, n = i[1], i[2], i[3]
            xpos = (SIZE[0] - self.size * self.w2) / 2 + x * self.size + PAD3
            ypos = SIZE[1] - self.size * self.h2 + y * self.size - PAD1 + PAD3
            self.player_items[x][y] = Square(screen, i[0], xpos, ypos,
                                          self.size - PAD3 * 2,
                                          self.size - PAD3 * 2, n)
                                          
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
        for i in self.inv_slots:
            x, y, n = i[1], i[2], i[3]
            self.items[x][y].drawing(screen)
            self.square_pulling(x, y, self.items,
                                i[0], self.inv_slots, n)
            
        # Рисование слотов игрока
        for i in self.player_slots:
            x, y, n = i[1], i[2], i[3]
            self.player_items[x][y].drawing(screen)
            self.square_pulling(x, y, self.player_items,
                                i[0], self.player_slots, n)
            
        # Рисование слота движущегося предмета
        if self.square_clone:
            self.square_clone.drawing(screen)          
                    
        # Рисование движущегося квадрата поверх остальных
        for q in self.inv_slots:
            x, y = q[1], q[2]
            if self.items[x][y].moving:
                self.items[x][y].drawing(screen)
            
        for q in self.player_slots:
            x, y = q[1], q[2]
            if self.player_items[x][y].moving:
                self.player_items[x][y].drawing(screen)
    
    # Притягивание квадрата    
    def square_pulling(self, x, y, arr, q, icons, n):
        # Присвоение ближайшей клетке
        m = 1000000
        nearest_square = (0, 0)
        to_inventory = False
        union = False
        clone = False
        pos = (0, 0)
        
        px = arr[x][y].xm + arr[x][y].w / 2
        py = arr[x][y].ym + arr[x][y].h / 2
        for i in range(self.w1):
            for j in range(self.h1):
                if (arr[x][y].count == -1 and self.items[i][j] == None or\
                   self.items[i][j] == arr[x][y]) or\
                   (arr[x][y].count != -1 and self.items[i][j] == None) or\
                   (arr[x][y].count != -1 and self.items[i][j] != None and\
                   q == self.items[i][j].image_name and self.items[i][j].count != -1):
                    sqx = (SIZE[0] - self.size * self.w1) / 2 + (i + 0.5) * self.size
                    sqy = PAD1 + (j + 0.5) * self.size
                    
                    if ((px - sqx) ** 2 + (py - sqy) ** 2) ** 0.5 <= m:
                        pos = (i, j)
                        m = ((px - sqx) ** 2 + (py - sqy) ** 2) ** 0.5
                        nearest_square = (sqx - self.size / 2 + PAD3 + 1,
                                          sqy - self.size / 2 + PAD3 + 1)
                        to_inventory = True
                        
                        if self.items[i][j] != None and q == self.items[i][j].image_name:
                            union = True
                        else:
                            union = False
                    
                    
        for i in range(self.w2):
            for j in range(self.h2):
                if (arr[x][y].count == -1 and self.player_items[i][j] == None or\
                   self.player_items[i][j] == arr[x][y]) or\
                   (arr[x][y].count != -1 and self.player_items[i][j] == None) or\
                   (arr[x][y].count != -1 and self.player_items[i][j] != None and\
                   q == self.player_items[i][j].image_name and\
                   self.player_items[i][j].count != -1):
                    sqx = (SIZE[0] - self.size * self.w2) / 2 + (i + 0.5) * self.size
                    sqy = SIZE[1] - (j + 0.5) * self.size - PAD1
                        
                    if ((px - sqx) ** 2 + (py - sqy) ** 2) ** 0.5 <= m:
                        pos = (i, j)
                        m = ((px - sqx) ** 2 + (py - sqy) ** 2) ** 0.5
                        nearest_square = (sqx - self.size / 2 + PAD3 + 1,
                                          sqy - self.size / 2 + PAD3 + 1)
                        to_inventory = False
                        
                        if self.player_items[i][j] != None and q == self.player_items[i][j].image_name:
                            union = True
                        else:
                            union = False
                            
        if self.square_clone:
            if self.clone_info[5] == self.inv_slots:
                sqx = (SIZE[0] - self.size * self.w1) / 2 + (self.clone_info[1] + 0.5) * self.size
                sqy = PAD1 + (self.clone_info[2] + 0.5) * self.size
            else:
                sqx = (SIZE[0] - self.size * self.w2) / 2 + (self.clone_info[1] + 0.5) * self.size
                sqy = SIZE[1] - (self.clone_info[2] + 0.5) * self.size - PAD1
            
            if ((px - sqx) ** 2 + (py - sqy) ** 2) ** 0.5 <= m:
                pos = (self.clone_info[1], self.clone_info[2])
                m = ((px - sqx) ** 2 + (py - sqy) ** 2) ** 0.5
                nearest_square = (sqx - self.size / 2 + PAD3 + 1,
                                  sqy - self.size / 2 + PAD3 + 1)
                clone = True
                    
        # Изменение координат
        if clone:
            if not arr[x][y].moving:
                arr[x][y].xm = nearest_square[0]
                arr[x][y].ym = nearest_square[1]
                del icons[[i[1:3] for i in icons].index((pos[0], pos[1]))]
                n += self.square_clone.count
                    
                self.square_clone = Square(screen, q,
                                         arr[x][y].xm,
                                         arr[x][y].ym,
                                         arr[x][y].w,
                                         arr[x][y].h, n)
                self.clone_info = (q, pos[0], pos[1], n, arr, icons)
                self.destroy_clone()
        else:
            if not arr[x][y].moving:
                arr[x][y].xm = nearest_square[0]
                arr[x][y].ym = nearest_square[1]
                
                q_index = [i[1:4] for i in icons].index((x, y, n))
                if ((arr == self.items and to_inventory) or\
                   (arr == self.player_items and not to_inventory)):
                    if (icons[q_index][1], icons[q_index][2]) != pos:
                        if union:
                            del icons[[i[1:3] for i in icons].index((pos[0], pos[1]))]
                            q_index = [i[1:4] for i in icons].index((x, y, n))
                            n += arr[pos[0]][pos[1]].count
                            
                        arr[pos[0]][pos[1]] = Square(screen, q,
                                                 arr[x][y].xm,
                                                 arr[x][y].ym,
                                                 arr[x][y].w,
                                                 arr[x][y].h, n)
                        arr[x][y] = None
                        icons[q_index] = (q, pos[0], pos[1], n)
                else:
                    if arr == self.items:
                        other_arr = self.player_items
                        other_icons = self.player_slots
                    else:
                        other_arr = self.items
                        other_icons = self.inv_slots
                        
                    if union:
                        del other_icons[[i[1:3] for i in other_icons].index((pos[0], pos[1]))]
                        q_index = [i[1:4] for i in icons].index((x, y, n))
                        n += other_arr[pos[0]][pos[1]].count
                            
                    other_arr[pos[0]][pos[1]] = Square(screen, q,
                                                        arr[x][y].xm,
                                                        arr[x][y].ym,
                                                        arr[x][y].w,
                                                        arr[x][y].h, n)
                    arr[x][y] = None
                    other_icons.append((q, pos[0], pos[1], n))
                    del icons[q_index]            
        
    def get_inventory_slots(self):
        return self.inv_slots
    
    def get_player_slots(self):
        return self.player_slots
     
    def add_square(self, screen, image, x, y, arr, slots, change_pos):
        if not change_pos:
            a = [(i[0], i[1], i[2]) for i in slots].index((image, x, y))
            
            if slots == self.inv_slots:
                xp = (SIZE[0] - self.size * self.w1) / 2 + (self.inv_slots[a][1] + 0.5) * self.size
                yp = PAD1 + (self.inv_slots[a][2] + 0.5) * self.size
            else:
                xp = (SIZE[0] - self.size * self.w2) / 2 + (self.player_slots[a][1] + 0.5) * self.size
                yp = SIZE[1] - (self.player_slots[a][2] + 0.5) * self.size - PAD1            
            
            if self.square_clone:
                n = self.square_clone.count + 1
            else:
                n = 1
            self.square_clone = Square(screen, slots[a][0],
                                       xp - self.size / 2 + PAD3 + 1,
                                       yp - self.size / 2 + PAD3 + 1,
                                       self.size - PAD3 * 2,
                                       self.size - PAD3 * 2, n)
            self.clone_info = (slots[a][0], slots[a][1], slots[a][2],
                               arr[x][y].count // 2, arr, slots)
        else:
            if slots == self.inv_slots:
                xp = (SIZE[0] - self.size * self.w1) / 2 + x * self.size + PAD3
                yp = PAD1 + y * self.size + PAD3
            else:
                xp = (SIZE[0] - self.size * self.w2) / 2 + x * self.size + PAD3
                yp = SIZE[1] - self.size * self.h2 + y * self.size - PAD1 + PAD3
                
            if (image, x, y) in [(i[0], i[1], i[2]) for i in slots]:
                a = [(i[0], i[1], i[2]) for i in slots].index((image, x, y))
                slots[a] = (image, x, y, slots[a][3] + 1)
                arr[x][y] = Square(screen, image, xp, yp,
                                    self.size - PAD3 * 2,
                                    self.size - PAD3 * 2,
                                    slots[a][3])
            else:
                slots.append((image, x, y, 1))
                arr[x][y] = Square(screen, image, xp, yp,
                                    self.size - PAD3 * 2,
                                    self.size - PAD3 * 2, 1)                
            
    def get_cell(self, mouse_pos, q):
        # Присвоение ближайшей клетке
        m = 1000000
        pos = (0, 0)
        
        px = mouse_pos[0]
        py = mouse_pos[1]
        for i in range(self.w1):
            for j in range(self.h1):
                if self.items[i][j] == None or (self.items[i][j] != None and\
                   q == self.items[i][j].image_name and self.items[i][j].count != -1):
                    sqx = (SIZE[0] - self.size * self.w1) / 2 + (i + 0.5) * self.size
                    sqy = PAD1 + (j + 0.5) * self.size
                    
                    if ((px - sqx) ** 2 + (py - sqy) ** 2) ** 0.5 <= m:
                        pos = (i, j)
                        m = ((px - sqx) ** 2 + (py - sqy) ** 2) ** 0.5
                        arr = self.items
                        slots = self.inv_slots
                    
        for i in range(self.w2):
            for j in range(self.h2):
                if self.player_items[i][j] == None or (self.player_items[i][j] != None and\
                   q == self.player_items[i][j].image_name and self.player_items[i][j].count != -1):
                    sqx = (SIZE[0] - self.size * self.w2) / 2 + (i + 0.5) * self.size
                    sqy = SIZE[1] - (j + 0.5) * self.size - PAD1
                        
                    if ((px - sqx) ** 2 + (py - sqy) ** 2) ** 0.5 <= m:
                        pos = (i, j)
                        m = ((px - sqx) ** 2 + (py - sqy) ** 2) ** 0.5
                        arr = self.player_items
                        slots = self.player_slots
        return (q, *pos, arr, slots)
    
    def destroy_clone(self):
        self.clone_info[4][self.clone_info[1]][self.clone_info[2]] = self.square_clone
        self.clone_info[5].append((self.clone_info[0],
                                   self.clone_info[1],
                                   self.clone_info[2],
                                   self.clone_info[3]))
        self.clone_info[4][self.clone_info[1]][self.clone_info[2]].down = False
        self.square_clone = None
        self.clone_info = None
    
    def controller(self, event, screen):
        global global_pressed
        pressing = False
        
        if not global_pressed and self.square_clone:
            self.destroy_clone()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                for i in self.inv_slots:
                    x, y = i[1], i[2]
                    if self.items[x][y].down and self.items[x][y].count > 1:
                        a = self.inv_slots.index(i)
                        self.inv_slots[a] = (self.inv_slots[a][0],
                                             self.inv_slots[a][1],
                                             self.inv_slots[a][2],
                                             self.items[x][y].count - 1)
                        self.items[x][y].count -= 1

                        data = self.get_cell(event.pos, self.inv_slots[a][0])
                        if (data[1], data[2]) == (x, y) and data[3] == self.items:
                            self.add_square(screen, *data, False)
                        else:
                            self.add_square(screen, *data, True)                        
                        break
                    elif self.items[x][y].down and self.items[x][y].count == 1:
                        self.items[x][y].down = False
                        break
                    elif self.items[x][y].on and\
                         not self.items[x][y].down and\
                         self.items[x][y].count > 1:
                        a = self.inv_slots.index(i)
                        self.inv_slots[a] = (self.inv_slots[a][0],
                                             self.inv_slots[a][1],
                                             self.inv_slots[a][2],
                                             self.items[x][y].count // 2 + self.items[x][y].count % 2)
                                             
                        xp = (SIZE[0] - self.size * self.w1) / 2 + (self.inv_slots[a][1] + 0.5) * self.size
                        yp = PAD1 + (self.inv_slots[a][2] + 0.5) * self.size                 
                        self.square_clone = Square(screen,
                                                   self.inv_slots[a][0],
                                                   xp - self.size / 2 + PAD3 + 1,
                                                   yp - self.size / 2 + PAD3 + 1,
                                                   self.size - PAD3 * 2,
                                                   self.size - PAD3 * 2,
                                                   self.items[x][y].count // 2)
                        self.clone_info = (self.inv_slots[a][0],
                                           self.inv_slots[a][1],
                                           self.inv_slots[a][2],
                                           self.items[x][y].count // 2,
                                           self.items,
                                           self.inv_slots)
                        
                        self.items[x][y].count = self.items[x][y].count // 2 + self.items[x][y].count % 2
                        break
                            
                for i in self.player_slots:
                    x, y = i[1], i[2]
                    if self.player_items[x][y].down and self.player_items[x][y].count > 1:
                        a = self.player_slots.index(i)
                        self.player_slots[a] = (self.player_slots[a][0],
                                                self.player_slots[a][1],
                                                self.player_slots[a][2],
                                                self.player_items[x][y].count - 1)
                        self.player_items[x][y].count -= 1

                        data = self.get_cell(event.pos, self.player_slots[a][0])
                        if (data[1], data[2]) == (x, y) and data[3] == self.player_items:
                            self.add_square(screen, *data, False)
                        else:
                            self.add_square(screen, *data, True)
                        break
                    elif self.player_items[x][y].down and self.player_items[x][y].count == 1:
                        self.player_items[x][y].down = False
                        break
                    elif self.player_items[x][y].on and\
                         not self.player_items[x][y].down and\
                         self.player_items[x][y].count > 1:
                        a = self.player_slots.index(i)
                        self.player_slots[a] = (self.player_slots[a][0],
                                             self.player_slots[a][1],
                                             self.player_slots[a][2],
                                             self.player_items[x][y].count // 2 + self.player_items[x][y].count % 2)
                        
                        xp = (SIZE[0] - self.size * self.w2) / 2 + (self.player_slots[a][1] + 0.5) * self.size
                        yp = SIZE[1] - (self.player_slots[a][2] + 0.5) * self.size - PAD1
                        self.square_clone = Square(screen,
                                                   self.player_slots[a][0],
                                                   xp - self.size / 2 + PAD3 + 1,
                                                   yp - self.size / 2 + PAD3 + 1,
                                                   self.size - PAD3 * 2,
                                                   self.size - PAD3 * 2,
                                                   self.player_items[x][y].count // 2)
                        self.clone_info = (self.player_slots[a][0],
                                           self.player_slots[a][1],
                                           self.player_slots[a][2],
                                           self.player_items[x][y].count // 2,
                                           self.player_items,
                                           self.player_slots)
                        
                        self.player_items[x][y].count = self.player_items[x][y].count // 2 + self.player_items[x][y].count % 2
                        break
        
        for i in self.inv_slots:
            x, y = i[1], i[2]
            if self.items[x][y].controller(event):
                pressing = True
            global_pressed = pressing
                    
        for i in self.player_slots:
            x, y = i[1], i[2]
            if self.player_items[x][y].controller(event):
                pressing = True
            global_pressed = pressing
        
        if self.square_clone:
            if self.square_clone.controller(event):
                pressing = True
        global_pressed = pressing


class Square:
    def __init__(self, screen, image, x, y, w, h, count):
        self.count = count
        
        self.move_screen = pygame.Surface(screen.get_size())
        self.color = SQUARE_COLOR
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        
        self.image_name = image
        self.image = pygame.image.load('data\\' + image)
        self.image = pygame.transform.scale(self.image,
                                            (int(self.w - PAD4 * 2),
                                             int(self.h - PAD4 * 2)))
        
        self.down = False
        self.on = False
        
        self.moving = False
        self.xm = self.x
        self.ym = self.y
        
    def controller(self, event): # Обработка событий мыши
        pressing = False
        global global_pressed

        if event.type == pygame.MOUSEMOTION:
            if self.on_button(event.pos):
                self.selected(True)
            else:
                self.selected(False)
        elif event.type == pygame.MOUSEBUTTONDOWN and\
             (event.button == 1 or (event.button == 3 and not global_pressed)):
            if self.on_button(event.pos):
                self.pressed(True, screen)
                pressing = True
        
        if self.down:
            pressing = True
            if event.type == pygame.MOUSEBUTTONDOWN and\
             (event.button == 1 or event.button == 3 and not self.moving):
                if not self.moving:
                    if self.on_button(event.pos):
                        self.moving = True
                        self.x, self.y = event.pos[0] - self.xm, event.pos[1] - self.ym
                else:
                    self.move_screen.blit(screen, (0, 0))
                    self.moving = False
            if event.type == pygame.MOUSEMOTION:
                if self.moving:
                    self.xm, self.ym = event.pos[0] - self.x, event.pos[1] - self.y
                    pressing = True
        else:
            self.moving = False
            
        return pressing

    def animation(self): # Смена цвета квадрата
        if self.moving:
            self.color = PRESSED_COLOR
        elif self.on:
            self.color = SELECTED_COLOR
        else:
            self.color = SQUARE_COLOR

    def drawing(self, screen): # Отрисовка
        # Квадрат
        self.animation()
        self.rect = pygame.Rect((self.xm, self.ym, self.w, self.h))
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Картинка
        screen.blit(self.image, (self.xm + PAD4, self.ym + PAD4))
        
        # Количество
        if self.count != -1:
            text = pygame.font.Font(FONT, TEXT_SIZE).render(str(self.count),
                                                            True, TEXT_COLOR)
            screen.blit(text, (self.xm + self.w - TEXT_SIZE * len(str(self.count)) / 5,
                               self.ym - TEXT_SIZE / 5))
        
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
    
# Пример
if __name__ == '__main__':
    pygame.init()
    size = width, height = SIZE[0], SIZE[1]
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('black'))

    inv = Inventory([('1.jpg', 4, 0, 5), ('1.jpg', 3, 1, -1)], 10, 8,
                    [('1.jpg', 4, 0, 100)], 8, 1)

    running = True
    while running:
        screen.fill(pygame.Color('black'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            else:
                inv.controller(event, screen)
        inv.drawing(screen)
        pygame.display.flip()
    pygame.quit()
