from V2.Code.Constants import *
from V2.Code.Methods import *

import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, group, frames, world, state="main", width=100, height=100, rot=0, coords=None, speed=None,
                 acceleration=None, max_acceleration=None, max_speed=None, friction=None, mass=100, controller=None,
                 health=1000):
        super().__init__(group)

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
        self.max_acceleration = max_acceleration
        self.max_speed = max_speed
        self.friction = friction
        if acceleration is None:
            self.acceleration = [0, 0]
        if max_acceleration is None:
            self.max_acceleration = [0.1, 0.1]
        if speed is None:
            self.speed = [0, 0]
        if max_speed is None:
            self.max_speed = [15, 15]
        if friction is None:
            self.friction = [0.01, 0.01]
        if coords is None:
            self.coords = [0, 0]
        self.last_acceleration = self.acceleration.copy()
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

        # Материальность
        self.material = True

        # Объект мира
        self.world = world

        # Некоторые параметры, которые могут использовать дочерние классы
        self.params = dict()

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

    def set_acceleration(self, x=0, y=0):  # Изменение ускорения корабля
        self.acceleration[0] += self.max_acceleration[0] * x
        self.acceleration[1] += self.max_acceleration[1] * y
        if abs(self.acceleration[0]) > abs(self.max_acceleration[0]):

            self.acceleration[0] = self.max_acceleration[0] * (self.acceleration[0] / abs(self.acceleration[0]))
        if abs(self.acceleration[1]) > abs(self.max_acceleration[1]):
            self.acceleration[1] = self.max_acceleration[1] * (self.acceleration[1] / abs(self.acceleration[1]))

    def get_lines(self):
        x1 = self.coords[0] - self.width / 2
        x2 = self.coords[0] + self.width / 2

        y1 = self.coords[1] - self.height / 2
        y2 = self.coords[1] + self.height / 2

        lines = [[(x1, y1), (x2, y2)],
                 [(x2, y1), (x1, y2)]]
        return lines

    def get_collision(self):
        return {"type": "circle", "r": max(self.width, self.height)}

    def check_intersection(self, other):
        if other.material and self.material:
            col = other.get_collision()
            if col["type"] == "point":

                if self.coords[0] - self.width / 2 < col["point"][0] < self.coords[0] + self.width / 2 and \
                        self.coords[1] - self.height / 2 < col["point"][1] < self.coords[1] + self.height / 2:
                    self.hit(other, 0)
                    other.hit(self, 89)
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

    def check_flip(self):
        if self.flip != self.flipped:
            self.origin = pygame.transform.flip(self.origin, True, False)
            self.flipped = self.flip
        self.flip_timer = max(0, self.flip_timer - 1)

    def draw(self):
        self.check_flip()
        self.rect.center = tuple([int(coord) for coord in self.coords])
        img = pygame.transform.scale(self.origin, (int(self.width * self.world.cam.zoom),
                                                   int(self.height * self.world.cam.zoom)))
        img = pygame.transform.rotate(img, int(self.rot) % 360)
        self.world.cam.apply(self)
        self.image = img

    def stop(self, x=False, y=False):
        if x:
            self.acceleration[0] = 0

        if y:
            self.acceleration[1] = 0

    def update(self, mode):
        if mode == "standart":
            for i in range(2):
                self.coords[i] += self.speed[i] * ACCELERATION * self.world.acceleration
                self.speed[i] += self.acceleration[i] * ACCELERATION * self.world.acceleration

            if abs(self.speed[0]) > self.max_speed[0]:
                self.speed[0] = self.max_speed[0] * (abs(self.speed[0]) / self.speed[0])

            if abs(self.speed[1]) > self.max_speed[1]:
                self.speed[1] = self.max_speed[1] * (abs(self.speed[1]) / self.speed[1])

            if abs(self.last_acceleration[0]) < abs(self.acceleration[0]):
                self.set_state("start_x")
            if self.acceleration[0] == 0:
                if self.state in ["moving", "start_x"]:
                    self.set_state("stop_x")

            self.last_acceleration[0] = self.acceleration[0]
            self.last_acceleration[1] = self.acceleration[1]

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
            if max(self.width, self.height) / 2 + self.coords[1] > self.world.planet.y and not isinstance(self, Station):

                self.speed[1] = -self.speed[1]
                self.coords[1] = self.world.planet.y - max(self.width, self.height) / 2
                self.hit(None, abs(self.speed[1]))
            objects = self.world.all_sprites.sprites()
            for obj in objects:
                if obj != self:
                    if obj.material and obj.health > 0:
                        self.check_intersection(obj)
                    if self.controller is not None:
                        self.controller.control_object(obj)


class Starship(Entity):
    pass


class Explosion(Entity):
    def __init__(self, group, frames, world, state="main", width=100, height=100, rot=0, coords=None, speed=None,
                 acceleration=None, max_acceleration=None, max_speed=None, friction=None, mass=100, controller=None,
                 health=1000, damage=100):
        super().__init__(group, frames, world, state=state, width=width, height=height, rot=rot, coords=coords,
                         speed=speed, acceleration=acceleration, max_acceleration=max_acceleration,
                         max_speed=max_speed, friction=friction, mass=mass, controller=controller, health=health)
        self.material = False
        self.params["circles"] = []
        self.image = pygame.Surface((1, 1))
        self.draw()
        if damage > 0:
            for sprite in world.all_sprites.sprites():
                if isinstance(sprite, Starship):
                    dist = math.hypot(coords[0] - sprite.coords[0], coords[1] - sprite.coords[1])
                    if dist < self.width * 2:
                        sprite.health -= (1 - (dist / (self.width * 2))) * damage

    def draw(self):
        sc = self.world.screen
        r = int(self.width * self.health / self.max_health * self.world.cam.zoom)
        col = interpolate_color(EXPL_SECOND_COLOR, EXPL_CENTER_COLOR, self.health, self.max_health)
        x = (self.coords[0] - self.world.cam.pos[0]) * self.world.cam.zoom + self.world.cam.size[0] // 2
        y = (self.coords[1] - self.world.cam.pos[1]) * self.world.cam.zoom + self.world.cam.size[1] // 2
        pygame.draw.circle(sc, col, (x, y), r)

        if "particles" in self.params:
            for particle in self.params["particles"]:
                pygame.draw.line(sc, (255, 255, 255),
                                  [x + particle["x"] * self.world.cam.zoom,
                                   y + particle["y"] * self.world.cam.zoom],
                                  [x + (particle["x"] - particle["speed"][0] * 15) * self.world.cam.zoom,
                                   y + (particle["y"] - particle["speed"][1] * 15) * self.world.cam.zoom], 2)

        for circle in self.params["circles"]:
            size = circle["size"]
            x1, y1 = circle["x"] * self.world.cam.zoom, circle["y"] * self.world.cam.zoom
            if size > 1:
                s_circle = max(2, int(size * 0.6 * self.world.cam.zoom))
                t_circle = max(3, int(size * self.world.cam.zoom))
                circle_pos = (int((x + x1)),
                              int((y + y1)))

                pygame.draw.circle(sc, EXPL_THIRD_COLOR, circle_pos, t_circle)
                pygame.draw.circle(sc, EXPL_SECOND_COLOR, circle_pos, s_circle)

        self.world.cam.apply(self)

    def add_circle(self):
        if self.health > 10:
            direction = random.randint(0, 360)
            r = int(self.width * self.health / self.max_health)
            dist = r + random.randint(-int(r * 0.1), int(r * 0.2))
            x = math.cos(direction * math.pi / 180) * dist
            y = math.sin(direction * math.pi / 180) * dist
            self.params["circles"].append({"x": x, "y": y, "size": max(random.randint(int(self.health * 0.4),
                                                                                      int(self.health * 0.6)), 1) // 2,
                                 "max_size": max(random.randint(int(self.health * 0.4), int(self.health * 0.6)), 1),
                                 "step": 2, "expansion": 1})

    def add_particle(self):
        if self.health > 10:
            direction = random.randint(0, 360)
            speed = random.randint(0, 20) / 2
            speed_x = math.cos(direction * math.pi / 180) * speed
            speed_y = math.sin(direction * math.pi / 180) * speed
            self.params["particles"].append({"x": 0, "y": 0, "speed": (speed_x, speed_y),
                                             "age": random.randint(10, 100)})

    def update(self, mode):
        self.material = False
        if mode == "standart":
            if "particles" not in self.params:
                self.params["particles"] = []
                for _ in range(40):
                    self.add_particle()
            else:
                for particle in self.params["particles"]:
                    particle["x"] += particle["speed"][0]
                    particle["y"] += particle["speed"][1]
                self.params["particles"] = list(filter(lambda x: math.hypot(x["x"], x["y"]) < self.width, self.params[
                    "particles"]))

                if random.randint(0, 1000) < 200:
                    self.add_circle()

                for i in range(len(self.params["circles"])):
                    self.params["circles"][i]["size"] += self.params["circles"][i]["step"] * \
                                                         self.params["circles"][i]["expansion"]
                    if self.params["circles"][i]["size"] > self.params["circles"][i]["max_size"]:
                        self.params["circles"][i]["expansion"] = -1
                    if self.params["circles"][i]["size"] < 1:
                        self.params["circles"][i]["size"] = 1
            self.draw()
            self.health -= 1


class Station(Starship):
    def __init__(self, group, frames, world, state="main", width=100, height=100, rot=0, coords=None, speed=None,
                 acceleration=None, max_acceleration=None, max_speed=None, friction=None, mass=100, controller=None,
                 health=1000):
        super().__init__(group, frames, world, state=state, width=width, height=height, rot=rot, coords=coords,
                         speed=speed, acceleration=acceleration, max_acceleration=max_acceleration,
                         max_speed=max_speed, friction=friction, mass=mass, controller=controller, health=health)
        self.params["direction"] = 0

    def update(self, mode):
        self.speed = [0, 0]
        self.acceleration = [0, 0]
        coords = self.coords.copy()
        super().update(mode)
        self.coords = coords.copy()


class Nexus(Starship):
    pass