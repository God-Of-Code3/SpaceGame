from V2.Code.Constants import *
from V2.Code.Methods import *
from V2.Code.Entity import *
from V2.Code.Bullet import *

import pygame


class SkillList:
    def __init__(self, x, y, master, world, skills):
        self.x = x
        self.y = y
        self.master = master
        self.skills = [eval(s["skill"])(world, s["number"], self.master) if s is not None else None for s in skills]
        self.length = len(self.skills)
        self.world = world
        self.selected = 2

    def draw(self):
        sc = self.world.screen

        pygame.draw.rect(sc, SKILL_BACKGROUND, (self.x, self.y, self.length * SKILL_TILE_SIZE, SKILL_TILE_SIZE))
        for i, skill in enumerate(self.skills):
            x = self.x + i * SKILL_TILE_SIZE
            y = self.y
            x2 = x + SKILL_TILE_PADDING
            y2 = y + SKILL_TILE_PADDING
            col = SKILL_BORDER_COLOR
            if skill is not None:
                if self.selected == i:

                    pygame.draw.rect(sc, SKILL_BACKGROUND_ACTIVE, (x, y, SKILL_TILE_SIZE, SKILL_TILE_SIZE))
                if skill.type == "passive":
                    pygame.draw.rect(sc, SKILL_BACKGROUND_PASSIVE, (x, y, SKILL_TILE_SIZE, SKILL_TILE_SIZE))
                sc.blit(skill.image, (x2, y2))
                if skill.recharge_timer != 0 or skill.number == 0:
                    shade = pygame.Surface((SKILL_TILE_SIZE, SKILL_TILE_SIZE))
                    shade.fill((0, 0, 0))
                    shade.set_alpha(100)
                    sc.blit(shade, (x, y))
                if skill.number > 0 or skill.number == -1:
                    if skill.recharge_timer != 0:
                        percent = max(0, 1 - (skill.recharge_timer / skill.recharge_time))
                        percent = int(percent * SKILL_TILE_SIZE)
                        y3 = y + SKILL_TILE_SIZE + SKILL_BAR_MARGIN

                        pygame.draw.rect(sc, SKILL_RECHARGE_BAR_BACKGROUND,
                                         (x, y3, SKILL_TILE_SIZE, SKILL_BAR_HEIGHT))
                        pygame.draw.rect(sc, SKILL_RECHARGE_BAR_COLOR,
                                         (x, y3, percent, SKILL_BAR_HEIGHT))

                    if skill.using_timer != 0:
                        percent = max(0, 1 - (skill.using_timer / skill.using_time))
                        percent = int(percent * SKILL_TILE_SIZE)
                        y3 = y + SKILL_TILE_SIZE + SKILL_BAR_MARGIN * 2 + SKILL_BAR_HEIGHT
                        pygame.draw.rect(sc, SKILL_USING_BAR_BACKGROUND,
                                         (x, y3, SKILL_TILE_SIZE, SKILL_BAR_HEIGHT))
                        pygame.draw.rect(sc, SKILL_USING_BAR_COLOR,
                                         (x, y3, percent, SKILL_BAR_HEIGHT))

                col = SKILL_BORDER_COLOR if skill.type == "active" else SKILL_BORDER_COLOR_PASSIVE

                if skill.number != -1 and skill.type == "active":
                    font = pygame.font.SysFont('Arial', 20)
                    string_rendered = font.render(str(skill.number), True, pygame.Color('black'))
                    sc.blit(string_rendered, (x + SKILL_TILE_PADDING, y + SKILL_TILE_PADDING))

            pygame.draw.rect(sc, col, (x, y, SKILL_TILE_SIZE, SKILL_TILE_SIZE - 1),
                             SKILL_BORDER_WIDTH)

    def select(self, i):
        if self.skills[i] is not None and self.skills[i].type == "active":
            self.selected = i

    def control(self):
        for event in self.world.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = event.pos
                    if self.x <= pos[0] <= self.x + self.length * SKILL_TILE_SIZE \
                       and self.y <= pos[1] <= self.y + SKILL_TILE_SIZE:
                        x = min((pos[0] - self.x) // SKILL_TILE_SIZE, self.length - 1)
                        self.select(x)

    def update(self, args):
        for i, skill in enumerate(self.skills):
            if skill is not None:
                if self.selected == i:
                    skill.selected = True
                else:
                    skill.selected = False
                skill.update(args)

    def check_pos(self, pos):
        if self.x <= pos[0] <= self.x + self.length * SKILL_TILE_SIZE \
                and self.y <= pos[1] <= self.y + SKILL_TILE_SIZE:
            return True
        return False

    def get_width(self):
        return self.length * SKILL_TILE_SIZE

    def get_skills(self):
        array = []
        for i, skill in enumerate(self.skills):
            if skill is not None:
                array.append((skill.origin, i, 0, skill.number))
        return array


class Skill:
    def __init__(self, world, name, number, master):
        self.world = world
        self.master = master
        self.number = number
        self.name = name
        self.recharge_timer = 0
        self.using_timer = 0
        self.using_process = False

        skill_data = skills_data[name]
        self.origin = skill_data["image"]
        self.image = load_image("./Assets/Images/Skills/" + skill_data["image"])
        self.image = pygame.transform.scale(self.image, (SKILL_TILE_SIZE - 2 * SKILL_TILE_PADDING,
                                                         SKILL_TILE_SIZE - 2 * SKILL_TILE_PADDING))
        self.type = skill_data["type"]
        self.selected = False
        self.recharge_time = skill_data["recharge_time"]
        self.using_time = skill_data["using_time"]
        self.auto_using = skill_data["auto_using"]

    def use(self, args):
        if self.type == "passive":
            return False
        if not (self.recharge_timer == 0 or (self.using_time != -1 and self.using_timer > 0)):
            return False
        self.use_code(args)
        self.start_using()
        if self.using_time == -1:
            self.number -= 1
            self.recharge_timer = self.recharge_time
        if self.using_time != -1 and self.using_timer == 0 and self.recharge_timer == 0:
            self.using_timer = self.using_time
        return True

    def using(self, args):
        if self.type == "passive":
            return False
        if self.using_timer > 0 and (self.auto_using or args["using"]):
            self.using_code(args)
            self.using_timer = max(self.using_timer - ACCELERATION, 0)
            return True
        return False

    def use_code(self, args):
        pass

    def using_code(self, args):
        pass

    def passive_code(self):
        pass

    def start_using(self):
        self.using_process = True

    def end_using(self):
        self.using_process = False

    def update(self, args):
        self.number = max(-1, self.number)
        if self.type == "active" and (self.number == -1 or self.number > 0):
            self.recharge_timer = max(self.recharge_timer - ACCELERATION, 0)
            if self.using_process and self.recharge_timer == 0:
                if self.auto_using or self.selected:
                    self.using(args)
                if self.using_timer == 0 and self.using_time != -1:
                    self.using_process = False
                    self.number -= 1
                    self.recharge_timer = self.recharge_time

            if self.selected:
                if args["use"]:
                    self.use(args)
        elif self.type == "passive":
            self.passive_code()


class PlasmaShot(Skill):
    def __init__(self, world, number, master):
        super().__init__(world, "PlasmaShot", number, master)

    def use_code(self, args):
        data = guns_data["Plasma"]
        coords = self.master.managed.coords
        coords2 = args["using_coords"]
        angle = to_point(*coords, *coords2)
        speed = [math.cos(angle * math.pi / 180) * data["speed"], math.sin(angle * math.pi / 180) * data["speed"]]
        spawn_coords = [*self.master.managed.coords]
        Plasma(self.world.all_sprites, data["anim"], self.world, speed=speed, coords=spawn_coords,
               width=data["width"], height=data["height"], master=self.master.managed, friction=[0, 0],
               max_speed=[data["speed"], data["speed"]], damage=data["damage"], health=data["health"],
               rot=-angle, controller=None)


class CopperShellShot(Skill):
    def __init__(self, world, number, master):
        super().__init__(world, "CopperShellShot", number, master)

    def use_code(self, args):
        data = guns_data["CopperShell"]
        coords = self.master.managed.coords
        coords2 = args["using_coords"]
        angle = to_point(*coords, *coords2)
        speed = [math.cos(angle * math.pi / 180) * data["speed"], math.sin(angle * math.pi / 180) * data["speed"]]
        spawn_coords = [*self.master.managed.coords]
        CopperShell(self.world.all_sprites, data["anim"], self.world, speed=speed, coords=spawn_coords,
                    width=data["width"], height=data["height"], master=self.master.managed, friction=[0, 0],
                    max_speed=[data["speed"], data["speed"]], damage=data["damage"], health=data["health"],
                    rot=-angle, controller=None)


class AntimatterShot(Skill):
    def __init__(self, world, number, master):
        super().__init__(world, "AntimatterShot", number, master)

    def use_code(self, args):
        data = guns_data["Antimatter"]
        coords = self.master.managed.coords
        coords2 = args["using_coords"]
        angle = to_point(*coords, *coords2)
        speed = [math.cos(angle * math.pi / 180) * data["speed"], math.sin(angle * math.pi / 180) * data["speed"]]
        spawn_coords = [*self.master.managed.coords]
        Antimatter(self.world.all_sprites, data["anim"], self.world, speed=speed,
                   coords=spawn_coords,
                    width=data["width"], height=data["height"], master=self.master.managed, friction=[0, 0],
                    max_speed=[data["speed"], data["speed"]], damage=data["damage"], health=data["health"],
                    rot=-angle, controller=None)


class AntirocketDeviceLaunch(Skill):
    def __init__(self, world, number, master):
        super().__init__(world, "AntirocketDeviceLaunch", number, master)

    def using_code(self, args):
        if self.using_timer % 10 == 0:
            data = guns_data["AntirocketDevice"]
            coords = self.master.managed.coords
            coords2 = args["using_coords"]
            angle = to_point(*coords, *coords2)
            acceleration = [math.cos(angle * math.pi / 180) * data["acceleration"],
                            math.sin(angle * math.pi / 180) * data["acceleration"]]
            d = max(self.master.managed.width, self.master.managed.height) + data["width"]
            spawn_coords = [self.master.managed.coords[0] + math.cos(angle * math.pi / 180) * d,
                            self.master.managed.coords[1] + math.sin(angle * math.pi / 180) * d]
            AntirocketDevice(self.world.all_sprites, data["anim"], self.world, mass=data["mass"], coords=spawn_coords,
                        width=data["width"], height=data["height"], master=self.master.managed, friction=[0, 0],
                        max_speed=[100, 100], health=data["health"], acceleration=acceleration,
                        rot=0, controller=None, rot_speed=data["rot_speed"], damage=data["damage"],
                        direction=angle + 90)


class SmallRocketLaunch(Skill):
    def __init__(self, world, number, master):
        super().__init__(world, "SmallRocketLaunch", number, master)

    def use_code(self, args):
        data = guns_data["SmallRocket"]
        coords = self.master.managed.coords
        coords2 = args["using_coords"]
        angle = to_point(*coords, *coords2)
        acceleration = [math.cos(math.pi / 180 * angle) * data["acceleration"],
                        math.sin(math.pi / 180 * angle) * data["acceleration"]]

        speed = [*self.master.managed.speed]
        spawn_coords = [*self.master.managed.coords]
        rot = -angle
        SmallRocket(self.world.all_sprites, data["anim"], self.world, speed=speed, coords=spawn_coords,
                    width=data["width"], height=data["height"], master=self.master.managed, friction=[0, 0],
                    max_speed=[90, 90], damage=data["damage"], health=data["health"],
                    rot=rot, acceleration=acceleration)


class MediumRocketLaunch(Skill):
    def __init__(self, world, number, master):
        super().__init__(world, "MediumRocketLaunch", number, master)

    def use_code(self, args):
        data = guns_data["MediumRocket"]
        coords = self.master.managed.coords
        coords2 = args["using_coords"]
        angle = to_point(*coords, *coords2)
        acceleration = [math.cos(math.pi / 180 * angle) * data["acceleration"],
                        math.sin(math.pi / 180 * angle) * data["acceleration"]]
        speed = [*self.master.managed.speed]
        spawn_coords = [*self.master.managed.coords]
        rot = -angle
        target = None
        for obj in self.world.all_sprites.sprites():
            if isinstance(obj, Starship):
                if obj.coords[0] - obj.width / 2 <= coords2[0] <= obj.coords[0] + obj.width / 2 and \
                        obj.coords[1] - obj.height / 2 <= coords2[1] <= obj.coords[1] + obj.height / 2:
                    target = obj
                    break
        r = MediumRocket(self.world.all_sprites, data["anim"], self.world, speed=speed, coords=spawn_coords,
                    width=data["width"], height=data["height"], master=self.master.managed, friction=[0, 0],
                    max_speed=[90, 90], damage=data["damage"], health=data["health"],
                    rot=rot, acceleration=acceleration, target=target)


class LaserShot(Skill):
    def __init__(self, world, number, master):
        super().__init__(world, "LaserShot", number, master)

    def using_code(self, args):
        speed = [args["using_coords"][0] - self.master.managed.coords[0],
                 args["using_coords"][1] - self.master.managed.coords[1]]
        data = guns_data["Laser"]
        Laser(self.world.all_sprites, frames_tree2, self.world, master=self.master.managed,
              coords=self.master.managed.coords, speed=speed, damage=data["damage"])


class HealthBoost(Skill):
    def __init__(self, world, number, master):
        super().__init__(world, "HealthBoost", number, master)

    def use_code(self, args):
        d = guns_data["HealthBoost"]
        self.master.managed.health = min(self.master.managed.max_health, d["health"] + self.master.managed.health)