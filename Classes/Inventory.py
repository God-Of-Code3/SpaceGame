import pygame
from Shop import Shop
from Button import Button
from Information import Information
from Constants import *
from GetInfo import get_info


global_pressed = False # Производится ли перемещение
TICK = 10


def start_game():
    pass


class Inventory():
    def __init__(self, screen,
                 inv_slots, wi, hi,
                 player_slots, wp, hp,
                 money_score):
        self.items_away = None
        self.tick = 0

        self.shop = None

        self.blocked = None
        self.show_info = False
        self.double_click = None
        self.first_click = None
        self.info = None
        
        self.selected = False
        self.pressed = False
        self.shop_icon_color = SHOP_ICON_COLOR
        self.shop_icon = pygame.image.load(FILES_WAY + TO_SHOP_NAME)
        self.shop_icon = pygame.transform.scale(self.shop_icon,
                                            (int(SHOP_HEIGHT / 2),
                                             int(SHOP_HEIGHT / 2)))

        self.trsh_slctd = False
        self.trsh_prssd = False
        self.trash_icon_color = SHOP_ICON_COLOR
        self.trash_icon = pygame.image.load(FILES_WAY + TRASH_NAME)
        self.trash_icon = pygame.transform.scale(self.trash_icon,
                                                 (int(SHOP_HEIGHT / 2),
                                                  int(SHOP_HEIGHT / 2)))
        
        self.money_score = money_score
        
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
            
        self.to_battle = Button('Начать', TEXT_COLOR, TEXT_SIZE, FONT, 
                                (SIZE[0] - TO_BATTLE_BTN_SIZE[0]) / 2,
                                SIZE[1] - self.size * self.h2 - PAD1 - PAD2 - TO_BATTLE_BTN_SIZE[1] - BTN_PAD,
                                *TO_BATTLE_BTN_SIZE,
                                (BTN_CLR1, BTN_CLR2, BTN_CLR3), True)

        # Добавление слотов
        self.items = [None] * self.w1
        for i in range(self.w1):
            self.items[i] = [None] * self.h1
        
        for i in self.inv_slots:
            x, y, n = i[1], i[2], i[3]
            xpos = (SIZE[0] - self.size * self.w1) / 2 + x * self.size + PAD3
            ypos = y * self.size + PAD3 + SHOP_HEIGHT + PAD5
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
        if self.shop:
            self.shop.drawing(screen)
        else:
            if self.tick < TICK:
                self.tick += 1
            else:
                self.tick = 0

            # Рисование панели магазина
            pygame.draw.rect(screen, SHOP_COLOR, (0, 0, SIZE[0], SHOP_HEIGHT))
            
            self.shop_color()
            pygame.draw.rect(screen, SHOP_SQUARE_COLOR,
                             (0, 0, SHOP_HEIGHT, SHOP_HEIGHT))
            pygame.draw.circle(screen, self.shop_icon_color,
                               (SHOP_HEIGHT / 2, SHOP_HEIGHT / 2),
                               SHOP_HEIGHT / 2 - PAD7 * 2)
            screen.blit(self.shop_icon, (SHOP_HEIGHT / 4, SHOP_HEIGHT / 4))
            
            text = pygame.font.Font(FONT, MONEY_SIZE).render(str(self.money_score) + '$',
                                                             True, MONEY_COLOR)
            screen.blit(text, (SHOP_HEIGHT + PAD6, (SHOP_HEIGHT - MONEY_SIZE / 2) / 2))

            self.trash_color()
            pygame.draw.rect(screen, SHOP_SQUARE_COLOR,
                             (SIZE[0] - SHOP_HEIGHT, 0, SHOP_HEIGHT, SHOP_HEIGHT))
            pygame.draw.circle(screen, self.trash_icon_color,
                               (SIZE[0] - SHOP_HEIGHT / 2, SHOP_HEIGHT / 2),
                               SHOP_HEIGHT / 2 - PAD7 * 2)
            screen.blit(self.trash_icon, (SIZE[0] - SHOP_HEIGHT * 3 / 4, SHOP_HEIGHT / 4))
            
            # Рисование инвентаря
            pygame.draw.rect(screen, INVENTORY_COLOR,
                             ((SIZE[0] - self.size * self.w1) / 2 - PAD2,
                              SHOP_HEIGHT + PAD5 - PAD2,
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
                                     j * self.size + SHOP_HEIGHT + PAD5,
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
                self.square_pulling(screen, x, y, self.items,
                                    i[0], self.inv_slots, n)
                
            # Рисование слотов игрока
            for i in self.player_slots:
                x, y, n = i[1], i[2], i[3]
                self.player_items[x][y].drawing(screen)
                self.square_pulling(screen, x, y, self.player_items,
                                    i[0], self.player_slots, n)
                
            # Рисование слота движущегося предмета
            if self.square_clone:
                self.square_clone.drawing(screen)
                
            # Рисование кнопки "В бой"
            self.to_battle.drawing(screen)
            
            # Рисование движущегося квадрата поверх остальных
            for q in self.inv_slots:
                x, y = q[1], q[2]
                if self.items[x][y].moving:
                    self.items[x][y].drawing(screen)
                
            for q in self.player_slots:
                x, y = q[1], q[2]
                if self.player_items[x][y].moving:
                    self.player_items[x][y].drawing(screen)
                
            if self.info:
                self.info.drawing(screen)

            # Отделение более одного предмета от кучи
            if self.items_away and global_pressed and self.tick == 0:
                if self.items_away[3][self.items_away[1]][self.items_away[2]].count > 1:
                    self.minus_1(*self.items_away)
                elif self.items_away[3][self.items_away[1]][self.items_away[2]].count == 1:
                    self.items_away[3][self.items_away[1]][self.items_away[2]].down = False
                    self.items_away = None
                self.double_click = None
    
    # Притягивание квадрата    
    def square_pulling(self, screen, x, y, arr, q, icons, n):
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
                    sqy = (j + 0.5) * self.size + SHOP_HEIGHT + PAD5
                    
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
                sqy = (self.clone_info[2] + 0.5) * self.size + SHOP_HEIGHT + PAD5
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
        
    def get_free_slots(self, arr):
        n = 0
        for i in arr:
            for j in i:
                if not j:
                    n += 1
        return n
    
    def get_inventory_slots(self):
        return self.inv_slots
    
    def get_player_slots(self):
        return self.player_slots
    
    def in_arrays(self, name):
        if name in [i[0] for i in self.inv_slots]:
            return True
        elif name in [i[0] for i in self.player_slots]:
            return True
        else:
            return False
    
    def go_to_skills_shop(self):
        self.shop = Shop(self)
    
    def shop_color(self):
        if self.selected:
            if self.pressed:
                self.shop_icon_color = PRESSED_ICON_COLOR
            else:
                self.shop_icon_color = SELECTED_ICON_COLOR
        else:
            self.shop_icon_color = SHOP_ICON_COLOR

    def trash_color(self):
        if self.trsh_slctd:
            if self.trsh_prssd:
                self.trash_icon_color = PRESSED_ICON_COLOR
            else:
                self.trash_icon_color = SELECTED_ICON_COLOR
        else:
            self.trash_icon_color = SHOP_ICON_COLOR
    
    def controller(self, event, screen):
        if self.shop:
            if not self.shop.controller(event, screen):
                self.money_score = self.shop.money_score
                self.shop = None
        else:
            if not self.show_info:
                global global_pressed

                # Для панели магазина
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SHOP_HEIGHT > event.pos[0] > 0 and SHOP_HEIGHT > event.pos[1] > 0:
                        self.pressed = True
                        self.go_to_skills_shop()
                    elif SIZE[0] > event.pos[0] > SIZE[0] - SHOP_HEIGHT and SHOP_HEIGHT > event.pos[1] > 0:
                        self.trsh_prssd = True
                        if global_pressed:
                            self.delete_square()
                elif event.type == pygame.MOUSEMOTION:
                    if SHOP_HEIGHT > event.pos[0] > 0 and SHOP_HEIGHT > event.pos[1] > 0:
                        self.selected = True
                    else:
                        self.selected = False
                        self.pressed = False

                    if SIZE[0] > event.pos[0] > SIZE[0] - SHOP_HEIGHT and SHOP_HEIGHT > event.pos[1] > 0:
                        self.trsh_slctd = True
                    else:
                        self.trsh_slctd = False
                        self.trsh_prssd = False
                
                # Кнопка в бой
                if event.type == pygame.MOUSEMOTION:
                    if self.to_battle.on_button(event.pos):
                        self.to_battle.selected(True)
                    else:
                        self.to_battle.selected(False)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.to_battle.on_button(event.pos):
                        self.to_battle.pressed(True)
                        start_game()
                    else:
                        self.to_battle.pressed(False)
                
                # Для инвентаря
                pressing = False
                
                if not global_pressed and self.square_clone:
                    self.destroy_clone()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        self.items_away = None
                elif event.type == pygame.MOUSEMOTION:
                    if self.items_away:
                        self.items_away = (*self.items_away[:6], event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        for i in self.inv_slots:
                            x, y = i[1], i[2]
                            if self.items[x][y].down and global_pressed:
                                if self.items[x][y].count > 1:
                                    self.items_away = (screen, x, y, self.items, self.inv_slots, i, event.pos)
                                    break
                                elif self.items[x][y].count == 1:
                                    self.items[x][y].down = False
                                    pressing = False
                                    break
                            elif not global_pressed:
                                if self.items[x][y].count > 1:
                                    if self.items[x][y].on:
                                        self.minus_half(screen, x, y, self.items, self.inv_slots, i)
                                        pressing = True
                                        self.double_click = None
                                        break
                                    
                        for i in self.player_slots:
                            x, y = i[1], i[2]
                            if self.player_items[x][y].down and global_pressed:
                                if self.player_items[x][y].count > 1:
                                    self.items_away = (screen, x, y, self.player_items, self.player_slots, i, event.pos)
                                    break
                                elif self.player_items[x][y].count == 1:
                                    self.player_items[x][y].down = False
                                    pressing = False
                                    break
                            elif not global_pressed:
                                if self.player_items[x][y].count > 1:
                                    if self.player_items[x][y].on and not global_pressed:
                                        self.minus_half(screen, x, y, self.player_items, self.player_slots, i)
                                        pressing = True
                                        self.double_click = None
                                        break
                
                if self.double_click:
                    self.first_click = self.double_click
                self.double_click = None
                
                for i in self.inv_slots:
                    x, y = i[1], i[2]
                    if self.items[x][y].controller(event, screen):
                        pressing = True
                    
                    cell = self.get_cell((self.items[x][y].xm, self.items[x][y].ym),
                                         None, self.items, False)[1:4]
                    if cell != (x, y, self.items):
                        self.blocked = (x, y, self.items)
                    if not global_pressed:
                        self.first_click = None
                        self.blocked = None
                   
                    if (x, y, self.items) != self.blocked and\
                       self.items[x][y].down and\
                       event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.double_click = (x, y, self.items)               
                         
                for i in self.player_slots:
                    x, y = i[1], i[2]
                    if self.player_items[x][y].controller(event, screen):
                        pressing = True
                    
                    cell = self.get_cell((self.player_items[x][y].xm, self.player_items[x][y].ym),
                                         None, self.player_items, False)[1:4]
                    if cell != (x, y, self.player_items):
                        self.blocked = (x, y, self.player_items)
                    if not global_pressed:
                        self.first_click = None
                        self.blocked = None
                   
                    if (x, y, self.player_items) != self.blocked and\
                       self.player_items[x][y].down and\
                       event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.double_click = (x, y, self.player_items)
                
                if self.square_clone:
                    if self.square_clone.controller(event, screen):
                        pressing = True
                    '''x, y = self.clone_info[1], self.clone_info[2]
                    if self.clone_info[4][x][y] and self.clone_info[4][x][y].down and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.double_click = (x, y, self.player_items)'''
                    
                global_pressed = pressing
                
                # Для информации
                if self.double_click and self.first_click == self.double_click:
                    self.show_info = True
            elif not self.info:
                if self.first_click:
                    x, y = self.first_click[0], self.first_click[1]
                    if self.first_click[2][x][y]:
                        name = self.first_click[2][x][y].image_name
                        if self.first_click[2][x][y].count == -1:
                            self.info = Information(name, self.money_score,
                                                    get_info(name),
                                                    self.get_free_slots(self.first_click[2]))
                        else:
                            self.info = Information(name, self.money_score, get_info(name))                        
                        self.first_click[2][x][y].down = False
                    else:
                        self.show_info = False                
                else:
                    self.show_info = False
                self.double_click = None
            else:
                if not self.info.controller(event, screen):
                    if self.info.buy:
                        x, y = self.first_click[0], self.first_click[1]
                        if self.first_click[2][x][y].count == -1:
                            for _ in range(self.info.count):
                                cell = self.get_cell((self.first_click[2][x][y].xm + self.first_click[2][x][y].w / 2,
                                             self.first_click[2][x][y].ym + self.first_click[2][x][y].h / 2),
                                            self.first_click[2][x][y].image_name,
                                            self.first_click[2])
                                self.add_square(screen, *cell, True)
                        else:
                            self.first_click[2][x][y].count += self.info.count
                        self.money_score -= self.info.count * self.info.info['cost']
                    
                    self.first_click = None
                    self.show_info = False
                    self.info = None

    def delete_square(self):
        for i in self.inv_slots:
            x, y = i[1], i[2]
            if self.items[x][y].down:
                if self.items[x][y].count == -1:
                    self.money_score += int(get_info(self.items[x][y].image_name)['cost'] / 2)
                else:
                    self.money_score += int(self.items[x][y].count * get_info(self.items[x][y].image_name)['cost'] / 2)

                del self.inv_slots[self.inv_slots.index((self.items[x][y].image_name,
                                                         x, y, self.items[x][y].count))]
                self.items[x][y] = None
                break

        for i in self.player_slots:
            x, y = i[1], i[2]
            if self.player_items[x][y].down:
                if self.player_items[x][y].count == -1:
                    self.money_score += int(get_info(self.player_items[x][y].image_name)['cost'] / 2)
                else:
                    self.money_score += int(self.player_items[x][y].count * get_info(self.player_items[x][y].image_name)['cost'] / 2)

                del self.player_slots[self.player_slots.index((self.player_items[x][y].image_name,
                                                               x, y, self.player_items[x][y].count))]
                self.player_items[x][y] = None
                break
     
    def add_square(self, screen, image, x, y, arr, slots, change_pos):
        if not change_pos:
            a = [(i[0], i[1], i[2]) for i in slots].index((image, x, y))
            
            if slots == self.inv_slots:
                xp = (SIZE[0] - self.size * self.w1) / 2 + (self.inv_slots[a][1] + 0.5) * self.size
                yp = (self.inv_slots[a][2] + 0.5) * self.size + SHOP_HEIGHT + PAD5
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
                               n, arr, slots)
        else:
            if slots == self.inv_slots:
                xp = (SIZE[0] - self.size * self.w1) / 2 + x * self.size + PAD3
                yp = y * self.size + PAD3 + SHOP_HEIGHT + PAD5
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
                if get_info(image)['indivisible']:
                    n = -1
                else:
                    n = 1
                    
                slots.append((image, x, y, n))
                arr[x][y] = Square(screen, image, xp, yp,
                                    self.size - PAD3 * 2,
                                    self.size - PAD3 * 2, n)                
            
    def get_cell(self, mouse_pos, q=None, inf_arr=None, near=True):
        # Присвоение ближайшей клетке
        m = 1000000
        pos = (0, 0)
        
        px = mouse_pos[0]
        py = mouse_pos[1]
        if inf_arr == self.items or not inf_arr:
            for i in range(self.w1):
                for j in range(self.h1):
                    if not near or (self.items[i][j] == None or\
                                    (self.items[i][j] != None and\
                       q == self.items[i][j].image_name and\
                       self.items[i][j].count != -1)):
                        sqx = (SIZE[0] - self.size * self.w1) / 2 + (i + 0.5) * self.size
                        sqy = (j + 0.5) * self.size + SHOP_HEIGHT + PAD5
                        
                        if ((px - sqx) ** 2 + (py - sqy) ** 2) ** 0.5 <= m:
                            pos = (i, j)
                            m = ((px - sqx) ** 2 + (py - sqy) ** 2) ** 0.5
                            arr = self.items
                            slots = self.inv_slots
                        
        if inf_arr == self.player_items or not inf_arr:
            for i in range(self.w2):
                for j in range(self.h2):
                    if not near or (self.player_items[i][j] == None or\
                       (self.player_items[i][j] != None and\
                       q == self.player_items[i][j].image_name and\
                       self.player_items[i][j].count != -1)):
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
        
    def minus_1(self, screen, x, y, arr, slots, elem, pos):
        a = [i[:3] for i in slots].index(elem[:3])
        slots[a] = (slots[a][0], slots[a][1], slots[a][2], arr[x][y].count - 1)
        arr[x][y].count -= 1

        data = self.get_cell(pos, slots[a][0])
        if (data[1], data[2]) == (x, y) and data[3] == arr:
            self.add_square(screen, *data, False)
        else:
            self.add_square(screen, *data, True)
            
    def minus_half(self, screen, x, y, arr, slots, elem):
        a = slots.index(elem)
        slots[a] = (slots[a][0], slots[a][1], slots[a][2],
                    arr[x][y].count // 2 + arr[x][y].count % 2)
        
        if slots == self.inv_slots:
            xp = (SIZE[0] - self.size * self.w1) / 2 + (slots[a][1] + 0.5) * self.size
            yp = (slots[a][2] + 0.5) * self.size + SHOP_HEIGHT + PAD5
        else:
            xp = (SIZE[0] - self.size * self.w2) / 2 + (slots[a][1] + 0.5) * self.size
            yp = SIZE[1] - (slots[a][2] + 0.5) * self.size - PAD1        
        
        self.square_clone = Square(screen, slots[a][0],
                                   xp - self.size / 2 + PAD3 + 1,
                                   yp - self.size / 2 + PAD3 + 1,
                                   self.size - PAD3 * 2,
                                   self.size - PAD3 * 2,
                                   arr[x][y].count // 2)
        self.clone_info = (slots[a][0], slots[a][1], slots[a][2],
                           arr[x][y].count // 2, arr, slots)
        
        arr[x][y].count = arr[x][y].count // 2 + arr[x][y].count % 2


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
        self.image = pygame.image.load(FILES_WAY + image)
        self.image = pygame.transform.scale(self.image,
                                            (int(self.w - PAD4 * 2),
                                             int(self.h - PAD4 * 2)))
        
        self.down = False
        self.on = False
        
        self.moving = False
        self.xm = self.x
        self.ym = self.y
    
    
    def controller(self, event, screen): # Обработка событий мыши
        pressing = False
        global global_pressed

        if event.type == pygame.MOUSEMOTION:
            if self.on_button(event.pos):
                self.selected(True)
            else:
                self.selected(False)
        elif event.type == pygame.MOUSEBUTTONDOWN and\
             (event.button == 1 or event.button == 3) and not global_pressed:
            if self.on_button(event.pos):
                self.pressed(True, screen)
                global_pressed = True
                pressing = True
        
        if self.down:
            pressing = True
            if event.type == pygame.MOUSEBUTTONDOWN and\
             (event.button == 1 or (event.button == 3 and not self.moving)):
                if not self.moving:
                    if self.on_button(event.pos):
                        self.moving = True
                        self.x, self.y = event.pos[0] - self.xm, event.pos[1] - self.ym
                else:
                    self.move_screen.blit(screen, (0, 0))
                    pressing = False
                    self.moving = False
            elif event.type == pygame.MOUSEMOTION:
                if self.moving:
                    self.xm, self.ym = event.pos[0] - self.x, event.pos[1] - self.y
                    pressing = True
                else:
                    pressing = False
        else:
            pressing = False
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
    
'''# Пример
if __name__ == '__main__':
    pygame.init()
    size = width, height = SIZE[0], SIZE[1]
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('black'))

    inv = Inventory(screen,
                    [('1.jpg', 4, 0, 5), ('2.jpg', 3, 1, -1)], 9, 3,
                    [('3.jpg', 4, 0, 100)], 8, 1,
                    1000)

    running = True
    while running:
        screen.fill(pygame.Color('black'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                inv.controller(event, screen)
        inv.drawing(screen)
        pygame.display.flip()
    pygame.quit()'''
