import pygame
from V2.Code.Constants import *


SPEED = 0.1 # скорость прокрутки фона в (пикселей в кадр)
BACKGROUND = 'Assets/Images/Other/SpaceBg.jpg' # файл фона

# Кнопка
START_BTN_SIZE = (200, 100)

FONT = None # Шрифт
FILES_WAY = 'Assets/Images/Skills/' # Путь для файлов
HIGH_FILES_WAY = 'Assets/Images/Skills/' # Путь для файлов в высоком разрешении
HIGH_QUALITY = (400, 400) # Разрешение картинок в описании


# ИНВЕНТАРЬ

TO_BATTLE_BTN_SIZE = (500, 50)

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

TO_SHOP_NAME = 'PlasmaShot.jpg' # имя файла иконки магазина
SHOP_HEIGHT = 80 # размер панели магазина
# Отступы магазина
PAD5 = 30 # панель магазина от инвентаря (-PAD2)
PAD6 = 10 # кол-во денег
PAD7 = 2 # кнопка магазина
# Текст кол-ва денег
MONEY_SIZE = 32
MONEY_COLOR = pygame.Color(0, 0, 0)


# ОПИСАНИЕ

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


# Кнопка "В бой"

BTN_SIZE = (500, 50)
BTN_CLR1 = pygame.Color(150, 150, 150)
BTN_CLR2 = pygame.Color(100, 100, 100)
BTN_CLR3 = pygame.Color(50, 50, 50)
BTN_PAD = 5 # отступ от нижних слотов


# МАГАЗИН

ICON_SIZE = (100, 100) # Размер квадрата для предмета
DISTANCE_X = 300 # Расстояние между предметами
DISTANCE_Y = 200 # Расстояние между предметами

SHOP_TEXT_SIZE = 24
SHOP_BTN_SIZE = (120, 30)
SHOP_BTN_PAD = 5 # отступ кнопки от предмета

# Константы магазина

SHOP_NAME = 'CopperShellShot.png' # имя файла иконки магазина
# Отступы магазина
PAD12 = 30 # от панели до магазина
PAD13 = 10 # кол-во денег
PAD14 = 2 # кнопка магазина