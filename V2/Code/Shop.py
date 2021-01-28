import pygame
import json
from V2.Code.InventoryConstants import *
from V2.Code.Button import Button
from V2.Code.Information import Information



FILES_WAY = 'Assets/Images/Skills/'  # Путь для файлов
HIGH_FILES_WAY = 'Assets/Images/Skills/'  # Путь для файлов в высоком разрешении

ICON_SIZE = (100, 100)  # Размер квадрата для предмета
DISTANCE_X = 300  # Расстояние между предметами
DISTANCE_Y = 200  # Расстояние между предметами

FONT = None  # Шрифт
TEXT_SIZE = 24
TEXT_COLOR = pygame.Color(255, 255, 255)
BTN_SIZE = (120, 30)
BTN_CLR1 = pygame.Color(150, 150, 150)
BTN_CLR2 = pygame.Color(100, 100, 100)
BTN_CLR3 = pygame.Color(50, 50, 50)
BTN_PAD = 5  # отступ кнопки от предмета

# Константы магазина

SHOP_COLOR = pygame.Color(150, 150, 150)  # цвета
SHOP_SQUARE_COLOR = pygame.Color(255, 255, 255)
SHOP_ICON_COLOR = pygame.Color(255, 255, 255)
SELECTED_ICON_COLOR = pygame.Color(50, 50, 50)
PRESSED_ICON_COLOR = pygame.Color(100, 100, 100)

TO_SHOP_NAME = 'shopping-basket.png'  # имя файла иконки магазина
SHOP_HEIGHT = 80  # размер панели магазина
# Отступы магазина
PAD5 = 30  # панель магазина от инвентаря (-PAD2)
PAD6 = 10  # кол-во денег
PAD7 = 2  # кнопка магазина
# Текст кол-ва денег
MONEY_SIZE = 32
MONEY_COLOR = pygame.Color(0, 0, 0)
file = open("./Data/Skills.json", "r", encoding="utf-8")
skills_data = json.load(file)


def get_products():

    skills = []
    i = 0
    for skill in skills_data:
        if i % 4 == 0:
            skills.append([])
        skills[-1].append(skills_data[skill]["image"])
        i += 1
    return skills


def get_info(image_name):
    inf = None
    for key in skills_data:
        if skills_data[key]["image"] == image_name:
            inf = skills_data[key]
            if "indivisible" not in inf:
                inf["indivisible"] = False
    if inf:
        return {'image': HIGH_FILES_WAY + image_name,
            'name': inf["name"],
            'description': inf["description"],
            'cost': inf["cost"],
            "specifications": {},
            "indivisible": inf["indivisible"]}

    return {'image': HIGH_FILES_WAY + image_name,
            'name': "Супер мега пушка Сокрушитель миров 3000 ультра экстрим круть",
            'description': [
                "Слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова",
                "Слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова слова"],
            'cost': 100,
            'specifications': {'spec1': "Значение свойства spec1",
                               'spec2': "Значение свойства spec2",
                               'spec3': "Значение свойства spec3"},
            "indivisible": False}


class Shop():
    def __init__(self, inventory):
        self.inv = inventory
        self.purchased_name = None
        print(FILES_WAY, SHOP_NAME)
        self.shop_icon = pygame.image.load(FILES_WAY + SHOP_NAME)
        self.shop_icon = pygame.transform.scale(self.shop_icon,
                                                (int(SHOP_HEIGHT / 2),
                                                 int(SHOP_HEIGHT / 2)))

        self.money_score = self.inv.money_score
        self.shop_icon_color = SHOP_ICON_COLOR
        self.selected = False
        self.pressed = True

        self.info = None
        self.show_info = False

        self.image_names = get_products()

        self.images = [None] * len(self.image_names)
        for i in range(len(self.image_names)):
            self.images[i] = [None] * len(self.image_names[i])

        for i in range(len(self.images)):
            for j in range(len(self.images[i])):
                self.images[i][j] = pygame.image.load(FILES_WAY + self.image_names[i][j])
                self.images[i][j] = pygame.transform.scale(self.images[i][j],
                                                           ICON_SIZE)

        self.pad_x = (SIZE[0] - DISTANCE_X * (len(self.images[0]) + 1)) / 2
        self.pad_y = (SIZE[1] - DISTANCE_Y * (len(self.images) + 1)) / 2

        self.buttons = [None] * len(self.image_names)
        for i in range(len(self.image_names)):
            self.buttons[i] = [None] * len(self.image_names[i])

        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                self.buttons[i][j] = Button(str(get_info(self.image_names[i][j])['cost']) + '$',
                                            TEXT_COLOR, SHOP_TEXT_SIZE, FONT,
                                            self.pad_x + (j + 1) * DISTANCE_X - SHOP_BTN_SIZE[0] / 2,
                                            self.pad_y + (i + 1) * DISTANCE_Y + ICON_SIZE[1] / 2 + SHOP_BTN_PAD,
                                            *SHOP_BTN_SIZE,
                                            (BTN_CLR1, BTN_CLR2, BTN_CLR3), True)

    def shop_color(self):
        if self.selected:
            if self.pressed:
                self.shop_icon_color = PRESSED_ICON_COLOR
            else:
                self.shop_icon_color = SELECTED_ICON_COLOR
        else:
            self.shop_icon_color = SHOP_ICON_COLOR

    def drawing(self, screen):
        # Рисование панели магазина
        pygame.draw.rect(screen, SHOP_COLOR, (0, 0, SIZE[0], SHOP_HEIGHT))

        self.shop_color()
        pygame.draw.rect(screen, SHOP_SQUARE_COLOR,
                         (0, 0, SHOP_HEIGHT, SHOP_HEIGHT))
        pygame.draw.circle(screen, self.shop_icon_color,
                           (SHOP_HEIGHT / 2, SHOP_HEIGHT / 2),
                           SHOP_HEIGHT / 2 - PAD14 * 2)
        screen.blit(self.shop_icon, (SHOP_HEIGHT / 4, SHOP_HEIGHT / 4))

        text = pygame.font.Font(FONT, MONEY_SIZE).render(str(self.money_score) + '$',
                                                         True, MONEY_COLOR)
        screen.blit(text, (SHOP_HEIGHT + PAD13, (SHOP_HEIGHT - MONEY_SIZE / 2) / 2))

        for i in range(len(self.images)):
            for j in range(len(self.images[i])):
                screen.blit(self.images[i][j], (self.pad_x + (j + 1) * DISTANCE_X - ICON_SIZE[0] / 2,
                                                self.pad_y + (i + 1) * DISTANCE_Y - ICON_SIZE[1] / 2))

        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                self.buttons[i][j].drawing(screen)

        if self.info:
            self.info.drawing(screen)

    def controller(self, event, screen):
        if not self.show_info:
            # Для панели магазина
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SHOP_HEIGHT > event.pos[0] > 0 and SHOP_HEIGHT > event.pos[1] > 0:
                    self.pressed = True
                    return False
            elif event.type == pygame.MOUSEMOTION:
                if SHOP_HEIGHT > event.pos[0] > 0 and SHOP_HEIGHT > event.pos[1] > 0:
                    self.selected = True
                else:
                    self.selected = False
                    self.pressed = False

            if event.type == pygame.MOUSEMOTION:
                for i in range(len(self.buttons)):
                    for j in range(len(self.buttons[i])):
                        if self.buttons[i][j].on_button(event.pos):
                            self.buttons[i][j].selected(True)
                        else:
                            self.buttons[i][j].selected(False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(self.buttons)):
                    for j in range(len(self.buttons[i])):
                        if self.buttons[i][j].on_button(event.pos):
                            self.buttons[i][j].pressed(True)

                            self.purchased_name = self.image_names[i][j]
                            if get_info(self.purchased_name)['indivisible']:
                                self.info = Information(self.purchased_name,
                                                        self.money_score,
                                                        get_info(self.purchased_name),
                                                        self.inv.get_free_slots(
                                                            self.inv.items) + self.inv.get_free_slots(
                                                            self.inv.player_items))
                            else:
                                self.info = Information(self.purchased_name,
                                                        self.money_score,
                                                        get_info(self.purchased_name))
                            self.show_info = True
                        else:
                            self.buttons[i][j].pressed(False)


        else:
            if not self.info.controller(event, screen):
                if self.info.buy:
                    if self.inv.in_arrays(self.purchased_name):
                        for _ in range(self.info.count):
                            cell = self.inv.get_cell((0, 0), self.purchased_name)
                            self.inv.add_square(screen, *cell, True)
                    else:
                        for _ in range(self.info.count):
                            cell = self.inv.get_cell((0, 0), self.purchased_name)
                            self.inv.add_square(screen, *cell, True)
                    self.money_score -= self.info.count * self.info.info['cost']
                self.show_info = False
                self.info = None

                for i in range(len(self.buttons)):
                    for j in range(len(self.buttons[i])):
                        self.buttons[i][j].selected(False)
        return True