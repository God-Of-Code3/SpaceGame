import pygame

SIZE = (1500, 800)
SENSITIVITY = 2


class Camera:
    def __init__(self, color, screen, min_zoom, max_zoom, zoom_step):  # Определения класса
        self.color = color
        self.cam_pos = (0, 0)
        self.zoom_value = 1
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.zoom_step = zoom_step
        self.screen = screen
        self.size = SIZE

    def control(self, get):
        for event in get:
            if event.type == pygame.MOUSEBUTTONDOWN:  # Изменение зума
                if event.button == 4:
                    self.zoom(self.zoom_step)
                elif event.button == 5:
                    self.zoom(1 / self.zoom_step)

    def set_position(self, x, y):  # Движение камеры
        self.cam_pos = (self.cam_pos[0] + x, self.cam_pos[1] + y)

    def get_position(self):  # Взять позицию
        return self.cam_pos

    def zoom(self, value):  # Приближение
        if self.max_zoom > self.zoom_value * value > self.min_zoom:
            self.zoom_value *= value

    def get_zoom(self):  # Взять приближение
        return self.zoom_value

    def fill(self):
        self.screen.fill(self.color)  # Установка цвета фона

    def render(self):
        pygame.display.flip()  # Обновление экрана

    def point_in_zone(self, point):  # Проверяет, лежит ли точка внутри камеры
        if -50 < point[0] < SIZE[0] and\
           -50 < point[1] < SIZE[1]:
            return True
        else:
            return False

    def drawing(self, objects, center, zoom):  # center - кортеж с x и y камеры
        # Отрисовка списков словарей
        for v in objects:
            x = SIZE[0] / 2 + (v['x'] - v['width'] / 2 - center[0]) * zoom
            y = SIZE[1] / 2 + (v['y'] - v['height'] / 2 - center[1]) * zoom
            w = int(v['width'] * zoom)
            h = int(v['height'] * zoom)
            if self.point_in_zone((x, y)) or self.point_in_zone((x + w, y)) or\
               self.point_in_zone((x + w, y + h)) or self.point_in_zone((x, y + h)):  # Отрисовка того, что на экране
                img = v['img']
                img = pygame.transform.scale(img, (w, h))  # Изменение размера картинки
                img = pygame.transform.rotate(img, -v['rot'])  # Поворот картинки
                self.screen.blit(img, (x, y))

    def drawing_planet(self, planet, center, zoom):  # center - кортеж с x и y камеры
        # Отрисовка списков словарей
        pygame.draw.circle(self.screen, planet.color, (int(SIZE[0] / 2 + (planet.x - center[0]) * zoom),
                                                  int(SIZE[1] / 2 + (planet.y - center[1]) * zoom)), int(planet.radius *
                                                                                                         zoom))

    def drawing_polygon(self, screen, polygon, center, zoom):  # center - кортеж с x и y камеры
        # Отрисовка списков словарей
        new_pol = []
        in_camera = False
        for point in polygon:  # Проверка на то, что объект в камере
            x = int(SIZE[0] / 2 + (point[0] - center[0]) * zoom)
            y = int(SIZE[1] / 2 + (point[1] - center[1]) * zoom)
            if self.point_in_zone((x, y)):
                in_camera = True
                break

        if in_camera:  # Отрисовка
            for point in polygon:
                x = int(SIZE[0] / 2 + (point[0] - center[0]) * zoom)
                y = int(SIZE[1] / 2 + (point[1] - center[1]) * zoom)
                new_pol.append([x, y])
            pygame.draw.polygon(screen, (255, 255, 255), new_pol, 3)


"""# Дальше типа пример
if __name__ == '__main__':
    pygame.init()
    size = width, height = SIZE[0], SIZE[1]
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('black'))
    W = A = S = D = False # Зажаты ли клавиши
    cam = Camera(pygame.Color('blue'), screen, 0.05, 2, 1.2) # Создание камеры
    running = True
    i = 0
    while running:
       #cam.control(pygame.event.get()) 2 цикла не работают вместе
       for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN: # Зажатие клавиш
                if event.key == ord('w'):
                   W = True
                if event.key == ord('a'):
                   A = True
                if event.key == ord('s'):
                   S = True
                if event.key == ord('d'):
                   D = True
            if event.type == pygame.KEYUP: # Отжатие клавиш
                if event.key == ord('w'):
                   W = False
                if event.key == ord('a'):
                   A = False
                if event.key == ord('s'):
                   S = False
                if event.key == ord('d'):
                   D = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    cam.zoom(1.2)
                if event.button == 5:
                    cam.zoom(0.8)
       cam.fill()
       if W: # Движение
           cam.set_position(0, -SENSITIVITY)
       if A:
           cam.set_position(-SENSITIVITY, 0)
       if S:
           cam.set_position(0, SENSITIVITY)
       if D:
           cam.set_position(SENSITIVITY, 0)
       cam.drawing([{"x": -100, "y": 100, "image": "../Assets/Images/Ships/Starship1.png", "width": 120,
                     "height": 70, "rot": 45 + i},
                    {"x": 100, "y": -100, "image": "../Assets/Images/Ships/Starship1.png", "width": 120, "height": 70,
                     "rot": 15 + i}],
                   cam.get_position(), cam.get_zoom())
       i += 1
       cam.render()
pygame.quit()"""