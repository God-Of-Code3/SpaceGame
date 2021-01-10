from V2.Code.Constants import *
from V2.Code.Methods import *

import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, frames, world, state="main", width=100, height=100, rot=0, coords=None, speed=None,
                 acceleration=None, max_speed=None, friction=None, mass=100, controller=None, health=1000):
        super().__init__(*groups)

        # Размер
        self.width = width
        self.height = height

        # Анимация
        self.frames = self.upload_frames(frames)
        self.state = state
        self.frame = 0
        self.timer = 0
        self.step = 10

        # Изображение
        self.origin = self.get_current_image()
        self.rot = rot
        self.image = pygame.Surface((width, height))

        # Отражение изображения
        self.flip_timer = 0
        self.flip = False
        self.flipped = False

        # Свойства координат, скорости, ускорения, трения, макс. скорости, массы
        self.coords = coords
        self.speed = speed
        self.acceleration = acceleration
        self.max_speed = max_speed
        self.friction = friction
        if acceleration is None:
            self.acceleration = [0, 0]
        if speed is None:
            self.speed = [0, 0]
        if max_speed is None:
            self.max_speed = [15, 15]
        if friction is None:
            self.friction = [0.01, 0.01]
        if coords is None:
            self.coords = [0, 0]
        self.mass = mass

        # Прямоугольник
        self.rect = self.image.get_rect()
        self.rect.center = tuple([int(coord) for coord in self.coords])

        # Контроллер
        self.controller = controller
        if self.controller is not None:
            self.controller.set_managed(self)

        # Прочность
        self.health = health
        self.max_health = health
        self.material = True

        # Объект мира
        self.world = world

    # Загрузить кадры картинками
    def upload_frames(self, frames):
        frames_images = dict()
        for st in frames:
            state = frames[st]
            current_state = dict()
            current_state["next"] = state["next"]
            current_state["frames"] = list()
            for frame in state["frames"]:
                img = load_image(frame[0])
                img = pygame.transform.scale(img, (self.width, self.height))
                current_state["frames"].append([img, frame[1]])
            frames_images[st] = current_state

        return frames_images

    # Текущее изображение
    def get_current_image(self):
        return self.frames[self.state]["frames"][self.frame][0]

    # Текущее время кадра
    def get_current_time(self):
        return self.frames[self.state]["frames"][self.frame][1]

    # Проверка на переход к следующему кадру
    def check_next(self):
        return self.frame >= len(self.frames[self.state]["frames"])

    # Установить стадию анимации
    def set_state(self, state):
        if state in self.frames:
            self.timer = 0
            self.frame = 0
            self.state = state

    # Переход к следующей стадии
    def set_next_state(self):
        next_state = self.frames[self.state]["next"]
        self.timer = 0
        self.frame = 0
        self.state = next_state

    # Установить текущее изображение
    def set_current_image(self):
        self.origin = self.get_current_image()
        self.timer = 0
        self.flipped = False

    def get_collision(self):
        return {"type": "circle", "r": max(self.width, self.height)}

    def check_intersection(self, other):
        col = other.get_collision()
        if col["type"] == "point":
            if self.rect.collidepoint(*col["point"]):
                pass
        if col["type"] == "circle":
            d = math.hypot(self.coords[0] - other.coords[0], self.coords[1] - other.coords[1])
            min_d = (max(self.width, self.height) + col["r"]) / 2
            if d < min_d:
                self.speed, other.speed, force = collision(self.coords, other.coords, self.speed, other.speed,
                                                           self.mass, other.mass)
                self.hit(other, force)
                other.hit(self, force)

                other.update("standart")
                self.update("standart")

                d = math.hypot(self.coords[0] - other.coords[0], self.coords[1] - other.coords[1])
                if d < min_d:
                    a = to_point(*self.coords, *other.coords)
                    other.coords = [math.cos(a * math.pi / 180) * min_d +
                                    self.coords[0],
                                    math.sin(a * math.pi / 180) * min_d +
                                    self.coords[1]]

    def hit(self, other, force):
        if other is not None:
            damage = force * HIT_DAMAGE_COEFFICIENT * other.mass / (self.mass + other.mass)
            self.health -= damage
        else:
            damage = force * HIT_DAMAGE_COEFFICIENT
            self.health -= damage

    def draw(self):
        if self.flip != self.flipped:
            self.origin = pygame.transform.flip(self.origin, True, False)
            self.flipped = self.flip
        self.flip_timer = max(0, self.flip_timer - 1)
        self.rect.center = tuple([int(coord) for coord in self.coords])

        img = pygame.transform.rotate(self.origin, int(self.rot) % 360)
        rect = img.get_rect()
        img = pygame.transform.scale(img, (int(rect.width * self.world.cam.zoom),
                                           int(rect.height * self.world.cam.zoom)))
        rect = img.get_rect()
        self.world.cam.apply(self)
        self.rect.width = rect.width
        self.rect.height = rect.height
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill((0, 0, 0))
        self.image.blit(img, (0, 0))
        self.image.set_colorkey((0, 0, 0))

    def update(self, mode):
        if mode == "standart":
            for i in range(2):
                self.coords[i] += self.speed[i] * ACCELERATION * self.world.acceleration
                self.speed[i] += self.acceleration[i] * ACCELERATION * self.world.acceleration

            if max(self.width, self.height) / 2 + self.coords[1] > self.world.planet.y:

                self.speed[1] = -self.speed[1]
                self.coords[1] = self.world.planet.y - max(self.width, self.height) / 2
                self.hit(None, abs(self.speed[1]))

            if abs(self.speed[0]) > self.max_speed[0]:
                self.speed[0] = self.max_speed[0] * (abs(self.speed[0]) / self.speed[0])

            if abs(self.speed[1]) > self.max_speed[1]:
                self.speed[1] = self.max_speed[1] * (abs(self.speed[1]) / self.speed[1])

            # Трение
            if self.acceleration[0] == 0 and self.speed[0] != 0:
                if abs(self.speed[0]) < 0.01:
                    self.speed[0] = 0
                elif abs(self.speed[0]) < self.friction[0]:
                    self.speed[0] = 0
                else:
                    self.speed[0] -= self.friction[0] * abs(self.speed[0]) / self.speed[0]

            if self.acceleration[1] == 0 and self.speed[1] != 0:
                if abs(self.speed[1]) < 0.01:
                    self.speed[1] = 0
                elif abs(self.speed[1]) < self.friction[1]:
                    self.speed[1] = 0
                else:
                    self.speed[1] -= self.friction[1] * abs(self.speed[1]) / self.speed[1]
            
            if self.timer >= self.get_current_time():
                self.frame += 1
                if self.check_next():
                    self.set_next_state()
                self.set_current_image()
            else:
                self.timer += self.step * self.world.acceleration * ACCELERATION

            if self.acceleration[0] < 0 and self.flip_timer == 0:
                self.flip = True
                self.flip_timer = 20
            if self.flip:
                if self.acceleration[0] > 0 and self.flip_timer == 0:
                    self.flip = False
                    self.flip_timer = 20

            self.draw()

        elif mode == "check":
            objects = self.world.all_sprites.sprites()

            for obj in objects:
                if obj != self:
                    if obj.material:
                        self.check_intersection(obj)
                    if self.controller is not None:
                        self.controller.control_object(obj)


class Bullet(Entity):
    def hit(self, other, force):
        self.rot = 360 - to_point(0, 0, *self.speed) % 360

    def get_collision(self):
        return {"type": "circle", "r": max(self.width, self.height)}
