import pygame


SIZE = (1200, 900) # Размер окна
FONT = None # Шрифт
global_pressed = False # Производится ли перемещение
FILES_WAY = 'data\\' # Путь для файлов
HIGH_FILES_WAY = 'data\\high-quality-textures\\' # Путь для файлов в высоком разрешении
HIGH_QUALITY = (400, 400) # Разрешение картинок в описании


# Константы инвентаря

INVENTORY_COLOR = pygame.Color(100, 100, 100) # цвета ячеек
CELLS_COLOR = pygame.Color(255, 255, 255)
SQUARE_COLOR = pygame.Color(255, 0, 0) # цвета предметов
SELECTED_COLOR = pygame.Color(150, 0, 0)
PRESSED_COLOR = pygame.Color(100, 0, 0)
#INFO_COLOR = pygame.Color(0, 100, 100)

CELLS_WIDTH = 2 # ширина границы ячеек
# Отступы инвентаря
PAD1 = 75 # внешний
PAD2 = 10 # ячейки от стен
PAD3 = 10 # внутри ячеек
PAD4 = 5 # картинки от квадрата
# Текст кол-ва предметов
TEXT_SIZE = 32
TEXT_COLOR = pygame.Color(255, 255, 255)


# Константы магазина

SHOP_COLOR = pygame.Color(150, 150, 150) # цвета
SHOP_SQUARE_COLOR = pygame.Color(255, 255, 255)
SHOP_ICON_COLOR = pygame.Color(0, 0, 0)
SELECTED_ICON_COLOR = pygame.Color(50, 50, 50)
PRESSED_ICON_COLOR = pygame.Color(100, 100, 100)

SHOP_NAME = 'shop_icon.png' # имя файла иконки магазина
SHOP_HEIGHT = 80 # размер панели магазина
# Отступы магазина
PAD5 = 30 # панель магазина от инвентаря (-PAD2)
PAD6 = 10 # кол-во денег
PAD7 = 2 # кнопка магазина
# Текст кол-ва денег
MONEY_SIZE = 32
MONEY_COLOR = pygame.Color(0, 0, 0)


# Константы окна информации

INFO_COLOR = pygame.Color(125, 125, 125) # цвета
PANEL_COLOR = pygame.Color(150, 0, 0)
CLOSE_PANEL_COLOR = pygame.Color(100, 0, 0)
DESCR_COLOR = pygame.Color(150, 150, 150)
BUY_COLOR1 = pygame.Color(150, 150, 150)
BUY_COLOR2 = pygame.Color(125, 125, 125)
BUY_COLOR3 = pygame.Color(100, 100, 100)
BUY_COLOR4 = pygame.Color(75, 75, 75)
CLOSE_COLOR1 = pygame.Color(150, 0, 0)
CLOSE_COLOR2 = pygame.Color(125, 0, 0)
CLOSE_COLOR3 = pygame.Color(100, 0, 0)

CLOSE_BUTTON = 40 # размер кнопки выхода
BETWEEN = 5 # расстояние между строками значений
INDENT = 5 # Отступ перед абзацем (в пробелах)
# Отступы информации
PAD8 = 30 # внешний
PAD9 = 20 # между панелями
PAD10 = 10 # внутри панели покупки
PAD11 = 125 # от рамок окна


def get_info(image_name):
    return {'image': HIGH_FILES_WAY + image_name,
            'name': "Супер мега пушка Сокрушитель миров 3000 ультра экстрим круть",
            'description': ["Слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова",
                            "Слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова"],
            'cost': 10,
            'specifications': {'spec1': "Значение свойства spec1",
                               'spec2': "Значение свойства spec2",
                               'spec3': "Значение свойства spec3"}}


class Information():
    def __init__(self, item_name, money_score, free_slots=None):
        self.free_slots = free_slots
        self.got_space = True
        
        self.count = 1
        self.buy = False
        self.got_money = True
        
        self.item_name = item_name
        self.money_score = money_score
        self.info = get_info(self.item_name)
        
        self.item_icon = pygame.image.load(self.info['image'])
        self.item_icon = pygame.transform.scale(self.item_icon, HIGH_QUALITY)
        
        # Для покупки
        x = PAD11 + PAD8 + HIGH_QUALITY[0] + PAD10 * 2 + PAD9
        y = PAD11 + PAD8 + HIGH_QUALITY[1] + PAD10 * 2 + PAD9
        w = SIZE[0] - (PAD8 + PAD11 + PAD10) * 2 - HIGH_QUALITY[0] - PAD9
        h = SIZE[1] - (PAD8 + PAD11 + PAD10) * 2 - HIGH_QUALITY[1] - PAD9
        
        self.buttons = [Button('X', CLOSE_BUTTON, SIZE[0] - PAD11 - CLOSE_BUTTON,
                               PAD11 - CLOSE_BUTTON,
                               CLOSE_BUTTON, CLOSE_BUTTON, (CLOSE_COLOR1,
                                                            CLOSE_COLOR2,
                                                            CLOSE_COLOR3)),
                        Button('Купить', TEXT_SIZE,
                               x + w / 2 + PAD10, y + h / 3 + PAD10,
                               w / 2 - PAD10 * 2, h * 2 / 3 - PAD10 * 2,
                               (BUY_COLOR1, BUY_COLOR2, BUY_COLOR3, BUY_COLOR4)),
                        Button('<', TEXT_SIZE,
                               x + PAD10, y + h / 3 + PAD10,
                               w / 2 / 5 - PAD10, h / 3 - PAD10,
                               (BUY_COLOR1, BUY_COLOR2, BUY_COLOR3, BUY_COLOR4)),
                        Button('>', TEXT_SIZE,
                               x + w / 2 / 5 * 4 + PAD10, y + h / 3 + PAD10,
                               w / 2 / 5 - PAD10, h / 3 - PAD10,
                               (BUY_COLOR1, BUY_COLOR2, BUY_COLOR3, BUY_COLOR4))]
    
    def drawing(self, screen):
        for button in self.buttons:
            button.block(False)
            
        if self.count == 1:
            self.buttons[2].block(True)
        if self.count == self.money_score // self.info['cost']:
            self.buttons[3].block(True)
            
        if self.money_score < self.info['cost']:
            self.got_money = False
            self.buttons[1].block(True)
            self.buttons[2].block(True)
            self.buttons[3].block(True)
        elif (self.free_slots or self.free_slots == 0) and self.count > self.free_slots:
            self.got_space = False
            self.buttons[1].block(True)
            self.buttons[3].block(True)
        elif self.money_score // self.info['cost'] > self.count > 1:
            self.got_space = True
        else:
            self.got_space = True
        
        # Верхняя панель
        pygame.draw.rect(screen, CLOSE_PANEL_COLOR, (PAD11, PAD11 - CLOSE_BUTTON,
                                                     SIZE[0] - PAD11 * 2,
                                                     CLOSE_BUTTON))
        window = pygame.font.SysFont(FONT, int(CLOSE_BUTTON - PAD10)).render('Оборудование и снаряжение', True, TEXT_COLOR)
        screen.blit(window, (PAD11 + PAD10,
                             PAD11 - CLOSE_BUTTON + window.get_height() / 2))
        # Окно
        pygame.draw.rect(screen, INFO_COLOR, (PAD11, PAD11,
                                              SIZE[0] - PAD11 * 2,
                                              SIZE[1] - PAD11 * 2))
        # Картинка
        pygame.draw.rect(screen, PANEL_COLOR, (PAD11 + PAD8, PAD11 + PAD8,
                                              HIGH_QUALITY[0] + PAD10 * 2,
                                              HIGH_QUALITY[1] + PAD10 * 2))
        screen.blit(self.item_icon, (PAD11 + PAD8 + PAD10, PAD11 + PAD8 + PAD10))
        # Значения
        pygame.draw.rect(screen, PANEL_COLOR, (PAD11 + PAD8,
                                               PAD11 + PAD8 + HIGH_QUALITY[1] + PAD10 * 2 + PAD9,
                                               HIGH_QUALITY[0] + PAD10 * 2,
                                               SIZE[1] - (PAD8 + PAD11 + PAD10) * 2 - HIGH_QUALITY[1] - PAD9))
        line = 0
        for value in list(self.info['specifications'].keys()):
            line += 1
            values = pygame.font.SysFont(FONT, int((HIGH_QUALITY[0]) / 15)).render(value + ': ' + self.info['specifications'][value], True, TEXT_COLOR)
            screen.blit(values, (PAD11 + PAD8 + PAD10 * 2,
                                 PAD11 + PAD8 + HIGH_QUALITY[1] + PAD9 + PAD10 + line * (values.get_height() + BETWEEN)))
        # Описание
        x = PAD11 + PAD8 + HIGH_QUALITY[0] + PAD10 * 2 + PAD9
        y = PAD11 + PAD8
        w = SIZE[0] - (PAD8 + PAD11 + PAD10) * 2 - HIGH_QUALITY[0] - PAD9
        h = HIGH_QUALITY[1] + PAD10 * 2
        pygame.draw.rect(screen, DESCR_COLOR, (x, y, w, h))
        
        line1 = 0
        text = ' ' * INDENT
        test = ''
        for i in self.info['name'].split():
            test = text
            test += (i + ' ')
            name = pygame.font.SysFont(FONT, int(TEXT_SIZE)).render(test, True, TEXT_COLOR)
            if name.get_width() > w - PAD10 * 3:
                name = pygame.font.SysFont(FONT, int(TEXT_SIZE)).render(text, True, TEXT_COLOR)
                screen.blit(name, (x + PAD10 * 2, y + PAD10 * 2 + TEXT_SIZE * line1))
                text = i + ' '
                line1 += 1
            else:
                text = test
        name = pygame.font.SysFont(FONT, int(TEXT_SIZE)).render(test, True, TEXT_COLOR)
        screen.blit(name, (x + PAD10 * 2, y + PAD10 * 2 + TEXT_SIZE * line1))
        
        line2 = 0
        text = ''
        test = ''
        par_num_orig = 0
        for paragraph in self.info['description']:
            par_num = 0
            text = ' ' * INDENT
            for i in paragraph.split():
                test = text
                test += (i + ' ')
                name = pygame.font.SysFont(FONT, int(TEXT_SIZE / 1.5)).render(test, True, TEXT_COLOR)
                if name.get_width() > w - PAD10 * 3:
                    name = pygame.font.SysFont(FONT, int(TEXT_SIZE / 1.5)).render(text, True, TEXT_COLOR)
                    screen.blit(name, (x + PAD10 * 2,
                                       y + PAD10 * 7 + TEXT_SIZE * (line1 + line2) + par_num_orig))
                    par_num += name.get_height()
                    text = i + ' '
                    line2 += 1
                else:
                    text = test
            name = pygame.font.SysFont(FONT, int(TEXT_SIZE / 1.5)).render(test, True, TEXT_COLOR)
            screen.blit(name, (x + PAD10 * 2, 
                               y + PAD10 * 7 + TEXT_SIZE * (line1 + line2) + par_num_orig))
            line2 += 1
            par_num_orig = par_num
        # Покупка
        x = PAD11 + PAD8 + HIGH_QUALITY[0] + PAD10 * 2 + PAD9
        y = PAD11 + PAD8 + HIGH_QUALITY[1] + PAD10 * 2 + PAD9
        w = SIZE[0] - (PAD8 + PAD11 + PAD10) * 2 - HIGH_QUALITY[0] - PAD9
        h = SIZE[1] - (PAD8 + PAD11 + PAD10) * 2 - HIGH_QUALITY[1] - PAD9
        pygame.draw.rect(screen, PANEL_COLOR, (x, y, w, h))
        pygame.draw.rect(screen, BUY_COLOR1, (x + PAD10, y + PAD10,
                                             w - PAD10 * 2,
                                             h / 3 - PAD10))
        cost1 = pygame.font.SysFont(FONT, int(h / 4 - PAD10)).render('Цена', True, TEXT_COLOR)
        screen.blit(cost1, (x + PAD10 * 2,
                            (y + h / 5) - cost1.get_height() / 2))
        cost2 = pygame.font.SysFont(FONT, int(h / 4 - PAD10)).render(str(self.info['cost'] * self.count) + '$', True, TEXT_COLOR)
        screen.blit(cost2, (x + w - cost2.get_width() - PAD10 * 2,
                            (y + h / 5) - cost2.get_height() / 2))
        if self.got_money:
            pygame.draw.rect(screen, BUY_COLOR1, (x + w / 10 + PAD10,
                                                 y + h / 3 + PAD10,
                                                 w / 10 * 3 - PAD10,
                                                 h / 3 - PAD10))
            buy = pygame.font.SysFont(FONT, int(h / 4 - PAD10)).render(str(self.count), True, TEXT_COLOR)
            screen.blit(buy, ((x + w / 4 + PAD10 / 2) - buy.get_width() / 2,
                              (y + h / 2 + PAD10 / 2) - buy.get_height() / 2))        
            
            pygame.draw.rect(screen, BUY_COLOR1, (x + PAD10, y + h * 2 / 3 + PAD10,
                                                 w / 2 - PAD10,
                                                 h / 3 - PAD10 * 2))        
            money = pygame.font.SysFont(FONT, int(h / 4 - PAD10)).render(str(self.money_score) + '$', True, TEXT_COLOR) # + ' (-' + str(self.info['cost'] * self.count) + '$)'
            screen.blit(money, ((x + w / 4) - money.get_width() / 2,
                                (y + h / 6 * 5) - money.get_height() / 2))
            
            if self.got_space or not (self.free_slots or self.free_slots == 0):               
                for button in self.buttons:
                    button.drawing(screen)
            else:
                pygame.draw.rect(screen, BUY_COLOR4, (x + w / 2 + PAD10,
                                                      y + h / 3 + PAD10,
                                                      w / 2 - PAD10 * 2,
                                                      h * 2 / 3 - PAD10 * 2))
                no_space = pygame.font.SysFont(FONT, int(TEXT_SIZE / 1.5)).render('Недостаточно места', True, TEXT_COLOR)
                screen.blit(no_space, ((x + w / 4 * 3) - no_space.get_width() / 2,
                                       (y + h / 3 * 2) - no_space.get_height() / 2))
                self.buttons[0].drawing(screen)
                self.buttons[2].drawing(screen)
                self.buttons[3].drawing(screen)
        else:
            no_money = pygame.font.SysFont(FONT, int(h / 3 - PAD10)).render('Недостаточно средств', True, TEXT_COLOR)
            screen.blit(no_money, ((x + w / 2) - no_money.get_width() / 2,
                                   (y + h / 3 * 2) - no_money.get_height() / 2))
            self.buttons[0].drawing(screen)
    
    def controller(self, event, screen):
        if self.buttons[0].down:
            return False
        elif self.buttons[1].down:
            self.buy = True
            return False
        elif self.buttons[2].down and self.count > 1:
            self.buttons[2].down = False
            self.count -= 1
        elif self.buttons[3].down and self.count < self.money_score // self.info['cost']:
            self.buttons[3].down = False
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
    
class Button():
    def __init__(self, text, text_size, x, y, w, h, colors):
        self.blocked = False
        
        self.text = text
        self.text_size = text_size
        
        self.colors = colors
        self.color = self.colors[0]

        # Сохранение области нажатия
        self.rect = pygame.Rect(x, y, w, h)

        # Переменные размеров
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # Значения нажатия
        self.on = False
        self.down = False

    def animation(self): # Анимация при нажатии
        if len(self.colors) == 4 and self.blocked:
            self.color = self.colors[3]
        elif self.on and self.down:
            self.color = self.colors[2]
        elif self.on:
            self.color = self.colors[1]
        else:
            self.color = self.colors[0]

    def drawing(self, screen): # Нарисовать кнопку
        self.animation() # Запуск анимации

        # Рисование кнопки
        pygame.draw.rect(screen, self.color, self.rect, 0)
        # Отрисовка текста
        to_write = pygame.font.SysFont(FONT, int(self.text_size)).render(self.text, True, TEXT_COLOR)
        screen.blit(to_write, ((self.x + self.w / 2) - to_write.get_width() / 2,
                               (self.y + self.h / 2) - to_write.get_height() / 2))
        
    def block(self, value):
        self.blocked = value

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
        if not self.blocked:
            self.down = value

class Inventory():
    def __init__(self, inv_slots, wi, hi, player_slots, wp, hp, money_score):
        self.blocked = None
        self.show_info = False
        self.double_click = None
        self.first_click = None
        self.info = None
        
        self.selected = False
        self.pressed = False
        
        self.shop_icon = pygame.image.load(FILES_WAY + SHOP_NAME)
        self.shop_icon = pygame.transform.scale(self.shop_icon,
                                            (int(SHOP_HEIGHT / 2),
                                             int(SHOP_HEIGHT / 2)))        
        
        self.money_score = money_score
        self.shop_icon_color = SHOP_ICON_COLOR
        
        
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
                
        if self.info:
            self.info.drawing(screen)
    
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
    
    def go_to_skills_shop(self):
        pass
    
    def shop_color(self):
        if self.selected:
            if self.pressed:
                self.shop_icon_color = PRESSED_ICON_COLOR
            else:
                self.shop_icon_color = SELECTED_ICON_COLOR
        else:
            self.shop_icon_color = SHOP_ICON_COLOR
    
    def controller(self, event, screen):
        if not self.show_info:
            global global_pressed
            
            # Для панели магазина
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SHOP_HEIGHT > event.pos[0] > 0 and SHOP_HEIGHT > event.pos[1] > 0:
                    self.pressed = True
                    self.go_to_skills_shop()
            elif event.type == pygame.MOUSEMOTION:
                if SHOP_HEIGHT > event.pos[0] > 0 and SHOP_HEIGHT > event.pos[1] > 0:
                    self.selected = True
                else:
                    self.selected = False
                    self.pressed = False
            
            # Для инвентаря
            pressing = False
            
            if not global_pressed and self.square_clone:
                self.destroy_clone()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    for i in self.inv_slots:
                        x, y = i[1], i[2]
                        if self.items[x][y].down and global_pressed:
                            if self.items[x][y].count > 1:
                                self.minus_1(x, y, self.items, self.inv_slots, i)
                                pressing = True
                                self.double_click = None
                                break
                            elif self.items[x][y].count == 1:
                                self.items[x][y].down = False
                                pressing = False
                                break
                        elif not global_pressed:
                            if self.items[x][y].count > 1:
                                if self.items[x][y].on:
                                    self.minus_half(x, y, self.items, self.inv_slots, i)
                                    pressing = True
                                    self.double_click = None
                                    break
                                
                    for i in self.player_slots:
                        x, y = i[1], i[2]
                        if self.player_items[x][y].down and global_pressed:
                            if self.player_items[x][y].count > 1:
                                self.minus_1(x, y, self.player_items, self.player_slots, i)
                                pressing = True
                                self.double_click = None
                                break
                            elif self.player_items[x][y].count == 1:
                                self.player_items[x][y].down = False
                                pressing = False
                                break
                        elif not global_pressed:
                            if self.player_items[x][y].count > 1:
                                if self.player_items[x][y].on and not global_pressed:
                                    self.minus_half(x, y, self.player_items, self.player_slots, i)
                                    pressing = True
                                    self.double_click = None
                                    break
            
            if self.double_click:
                self.first_click = self.double_click
            self.double_click = None
            
            for i in self.inv_slots:
                x, y = i[1], i[2]
                if self.items[x][y].controller(event):
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
                if self.player_items[x][y].controller(event):
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
                if self.square_clone.controller(event):
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
                        print(self.get_free_slots(self.first_click[2]))
                        self.info = Information(name, self.money_score,
                                                self.get_free_slots(self.first_click[2]))
                    else:
                        self.info = Information(name, self.money_score)                        
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
            #self.first_click = None
            #self.double_click = None
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
                a = [i[0] for i in slots].index(image)
                if slots[a][3] == -1:
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
        
    def minus_1(self, x, y, arr, slots, elem):
        a = slots.index(elem)
        slots[a] = (slots[a][0], slots[a][1], slots[a][2], arr[x][y].count - 1)
        arr[x][y].count -= 1

        data = self.get_cell(event.pos, slots[a][0])
        if (data[1], data[2]) == (x, y) and data[3] == arr:
            self.add_square(screen, *data, False)
        else:
            self.add_square(screen, *data, True)
            
    def minus_half(self, x, y, arr, slots, elem):
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
    
    
    def controller(self, event): # Обработка событий мыши
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
    
# Пример
if __name__ == '__main__':
    pygame.init()
    size = width, height = SIZE[0], SIZE[1]
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('black'))

    inv = Inventory([('1.jpg', 4, 0, 5), ('2.jpg', 3, 1, -1)], 9, 3,
                    [('3.jpg', 4, 0, 100)], 8, 1,
                    1000)

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
