from V2.Code.Entity import *


class Bullet(Entity):
    def __init__(self, groups, frames, world, state="main", width=100, height=100, rot=0, coords=None, speed=None,
                 acceleration=None, max_acceleration=None, max_speed=None, friction=None, mass=100, controller=None,
                 health=1000, master=None, damage=100):
        super().__init__(groups, frames, world, state=state, width=width, height=height, rot=rot, coords=coords,
                         speed=speed, acceleration=acceleration, max_acceleration=max_acceleration,
                         max_speed=max_speed, friction=friction, mass=mass, controller=controller, health=health)
        self.master = master
        self.damage = damage

    def update(self, mode):
        super().update(mode)
        if mode == "standart":
            self.health -= ACCELERATION

    def hit(self, other, force):
        if other is not None and other != self.master:
            other.health -= self.damage
        if other != self.master:
            self.health = 0

    def get_collision(self):
        return {"type": "point", "point": tuple(self.coords)}

    def check_intersection(self, other):
        pass


class Plasma(Bullet):

    def update(self, mode):
        super().update(mode)
        if mode == "standart":
            coeff = 0.98
            self.rot = 360 - to_point(0, 0, *self.speed) % 360
            self.health *= coeff
            self.damage *= coeff
            self.width *= coeff
            self.height *= coeff
            if self.width < 5 or self.height < 5:
                self.health = 0


class CopperShell(Bullet):
    pass


class SmallRocket(Bullet):
    def update(self, mode):
        self.flip = False
        self.flipped = False
        super().update(mode)

    def hit(self, other, force):
        if other is not None and other != self.master:
            other.health -= self.damage

        if other != self.master:
            self.health = 0
            r = 100
            Explosion(self.world.all_sprites, frames_tree2, self.world, health=150, coords=[*self.coords], width=r,
                      height=r)


class MediumRocket(Bullet):
    def __init__(self, group, frames, world, state="main", width=100, height=100, rot=0, coords=None, speed=None,
                 acceleration=None, max_acceleration=None, max_speed=None, friction=None, mass=100, controller=None,
                 health=1000, master=None, damage=0, target=None):
        super().__init__(group, frames, world, state=state, width=width, height=height, rot=rot, coords=coords,
                         speed=speed, acceleration=acceleration, max_acceleration=max_acceleration,
                         max_speed=max_speed, friction=friction, mass=mass, controller=controller, health=health,
                         damage=damage)
        self.master = master
        self.target = target
        self.params["acceleration"] = math.hypot(*self.acceleration)

    def hit(self, other, force):
        if other is not None and other != self.master:
            other.health -= self.damage

        if other != self.master:
            self.health = 0
            r = 200
            Explosion(self.world.all_sprites, frames_tree2, self.world, health=150, coords=[*self.coords], width=r,
                      height=r, damage=self.damage)

    def check_flip(self):
        pass

    def update(self, mode):
        if mode == "standart":
            self.flip = False
            self.flipped = False
            super().update(mode)
            speed = math.hypot(*self.speed)
            if self.target is not None:
                angle = get_angle(to_point(0, 0, *self.speed), to_point(*self.coords, *self.target.coords))
                if abs(angle) > 5:
                    direction = to_point(0, 0, *self.speed) + 180
                    self.acceleration = [math.cos(direction * math.pi / 180) * self.params["acceleration"],
                                         math.sin(direction * math.pi / 180) * self.params["acceleration"]]
                    if speed < 10:
                        direction = to_point(*self.coords, *self.target.coords)
                        self.acceleration = [math.cos(direction * math.pi / 180) * self.params["acceleration"],
                                             math.sin(direction * math.pi / 180) * self.params["acceleration"]]
                        self.rot = -direction
                else:
                    direction = to_point(*self.coords, *self.target.coords)
                    self.acceleration = [math.cos(direction * math.pi / 180) * self.params["acceleration"],
                                         math.sin(direction * math.pi / 180) * self.params["acceleration"]]
                    self.rot = -direction
                if self.health < 5:
                    self.health = 0
                    self.hit(None, 0)


class Laser(Bullet):
    def __init__(self, group, frames, world, state="main", width=100, height=100, rot=0, coords=None, speed=None,
                 acceleration=None, max_acceleration=None, max_speed=None, friction=None, mass=100, controller=None,
                 health=1000, master=None, damage=0):
        super().__init__(group, frames, world, state=state, width=width, height=height, rot=rot, coords=coords,
                         speed=speed, acceleration=acceleration, max_acceleration=max_acceleration,
                         max_speed=max_speed, friction=friction, mass=mass, controller=controller, health=health,
                         damage=damage)
        self.material = False
        self.image = pygame.Surface((1, 1))
        self.params["end"] = self.coords
        self.master = master

    def draw(self):
        sc = self.world.screen

        x = (self.coords[0] - self.world.cam.pos[0]) * self.world.cam.zoom + self.world.cam.size[0] // 2
        y = (self.coords[1] - self.world.cam.pos[1]) * self.world.cam.zoom + self.world.cam.size[1] // 2

        x2 = (self.params["end"][0] - self.world.cam.pos[0]) * self.world.cam.zoom + self.world.cam.size[0] // 2
        y2 = (self.params["end"][1] - self.world.cam.pos[1]) * self.world.cam.zoom + self.world.cam.size[1] // 2

        width = max(1, 5 * self.world.cam.zoom)

        pygame.draw.line(sc, LASER_OUTER_LAYER_COLOR, (int(x), int(y)), (int(x2), int(y2)), int(width))
        pygame.draw.circle(sc, LASER_OUTER_LAYER_COLOR, (int(x), int(y)), int(width * 2))

    def update(self, mode):
        if mode == "check":
            min_dist = []  # Obj, dist
            direction = to_point(0, 0, *self.speed)
            end_x = self.coords[0] + math.cos(direction * math.pi / 180) * LASER_MAX_LENGTH
            end_y = self.coords[1] + math.sin(direction * math.pi / 180) * LASER_MAX_LENGTH
            line = [(self.coords[0], self.coords[1]), (end_x, end_y)]
            for obj in self.world.all_sprites.sprites():
                if isinstance(obj, Starship) and obj != self.master:
                    intersection = False
                    dist = [0, (0, 0)]
                    for ln in obj.get_lines():
                        coords = line_intersection(ln, line, True)
                        if coords:
                            cur_dist = math.hypot(line[0][0] - coords[0], line[0][1] - coords[1])
                            if coords is not False and (dist[0] == 0 or cur_dist < dist[0]):
                                dist = [cur_dist, coords]
                                intersection = True
                    if intersection:
                        if len(min_dist) == 0:
                            min_dist = [obj, dist]
                        else:
                            if min_dist[1][0] > dist[0]:
                                min_dist = [obj, dist]

            self.params["end"] = [end_x, end_y]
            if len(min_dist) > 0:
                self.params["end"] = min_dist[1][1]
                min_dist[0].health -= self.damage
            self.draw()
            self.health = 0

