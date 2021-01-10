import pygame
import random
from Functions.Math import *
from Classes.Bullet import *


TILE_MARGIN = 10
SKILL_RECHARGE_MARGIN = 4


class SkillList:
    def __init__(self, x, y, size, master):
        self.x = x
        self.y = y
        self.size = size
        self.master = master
        self.tile_size = 50
        self.skills = []
        self.selected = 0

    def add(self, skill_class):
        self.skills.append(skill_class(self.master, self))

    def draw(self, screen):
        pygame.draw.rect(screen, (80, 80, 80), (self.x, self.y,
                                                self.size * (self.tile_size + TILE_MARGIN) + TILE_MARGIN,
                                                self.tile_size + TILE_MARGIN * 2))
        [self.skills[i].draw(screen, self.x + i * (self.tile_size + TILE_MARGIN) + TILE_MARGIN,
                             self.y + TILE_MARGIN) for i in range(len(self.skills))]
        for i in range(self.size):
            color = (180, 180, 180) if i != self.selected else (255, 255, 255)
            width = 1 if i != self.selected else 3
            pygame.draw.rect(screen, color, (self.x + i * (self.tile_size + TILE_MARGIN) + TILE_MARGIN
                                                       / 2, self.y + TILE_MARGIN / 2, self.tile_size + TILE_MARGIN,
                                                       self.tile_size
                                                       + TILE_MARGIN), width)

    def check_click(self):
        pos = pygame.mouse.get_pos()
        if self.x + TILE_MARGIN <= pos[0] <= self.x + self.size * (self.tile_size + TILE_MARGIN) + TILE_MARGIN and \
                self.y + TILE_MARGIN <= pos[1] <= self.y + self.tile_size + TILE_MARGIN * 2:
            for i, skill in enumerate(self.skills):
                rect = skill.image.get_rect()
                rect.x, rect.y = self.x + i * (self.tile_size + TILE_MARGIN) + TILE_MARGIN, self.y + TILE_MARGIN
                if rect.collidepoint(pos):
                    self.selected = i
            return True

    def update(self):
        for skill in self.skills:
            skill.update()

    def use(self, args):
        self.skills[self.selected].use(args)


class Skill:
    def __init__(self, master, skills_list):
        self.master = master
        self.timer = 0
        self.recharge_time = 100
        self.image = pygame.image.load("Assets/Images/Skills/PlasmaShot.png")
        self.skills_list = skills_list
        self.image = pygame.transform.scale(self.image, (self.skills_list.tile_size, self.skills_list.tile_size))
        self.shade = pygame.Surface((self.skills_list.tile_size, self.skills_list.tile_size))
        self.shade.fill((0, 0, 0))
        self.shade.set_alpha(180)
        self.number = 125
        self.active = True

    def update(self):
        if self.timer > 0:
            self.timer -= 1
        self.active = self.timer == 0

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))

        if self.timer != 0 or self.number == 0:
            screen.blit(self.shade, (x, y))
            percent = (self.recharge_time - self.timer) / self.recharge_time
            width = int(self.skills_list.tile_size * percent)
            height = 10
            pygame.draw.rect(screen, (94, 231, 255), (x, y + self.skills_list.tile_size + TILE_MARGIN * 2,
                                                      width, height))
            pygame.draw.rect(screen, (200, 200, 200), (x, y + self.skills_list.tile_size + TILE_MARGIN * 2,
                                                       self.skills_list.tile_size, height), 1)
        if self.number != -1:
            font = pygame.font.Font(None, 30)
            string_rendered = font.render(str(self.number), 1, pygame.Color('black'))
            rect = string_rendered.get_rect()
            rect.bottom = y + self.image.get_rect().height
            rect.left = x + 2
            screen.blit(string_rendered, rect)

    def use(self, args):
        pass


class PlasmaShot(Skill):

    def use(self, args):
        if self.timer == 0 and self.number > 0:
            self.number -= 1
            direction = to_point(self.master.x, self.master.y, args["real_click_x"], args["real_click_y"])
            dist = math.hypot(self.master.width, self.master.height) / 2
            x = self.master.x + math.cos(math.pi / 180 * direction) * dist
            y = self.master.y + math.sin(math.pi / 180 * direction) * dist
            args["level"].get("bullets").append(Plasma(x, y, direction, 50, "Assets/Images/Bullets/Bullet1.png",
                                                       56, 20, 520))
            self.timer = self.recharge_time


class LaserShot(Skill):
    def __init__(self, *args):
        super().__init__(*args)
        self.recharge_time = 200
        self.number = -1
        self.image = pygame.image.load("Assets/Images/Skills/LaserRay.png")
        self.image = pygame.transform.scale(self.image, (self.skills_list.tile_size, self.skills_list.tile_size))

    def use(self, args):
        if self.timer == 0:
            self.master.effects["laser"] = Laser(self.master.x, self.master.y,
                                                 to_point(self.master.x, self.master.y, args["real_click_x"],
                                                          args["real_click_y"]), self.master)


class CopperShellShot(Skill):
    def __init__(self, *args):
        super().__init__(*args)
        self.recharge_time = 50
        self.image = pygame.image.load("Assets/Images/Skills/CopperShell.png")
        self.image = pygame.transform.scale(self.image, (self.skills_list.tile_size, self.skills_list.tile_size))

    def use(self, args):
        if self.timer == 0 and self.number > 0:
            self.number -= 1
            direction = to_point(self.master.x, self.master.y, args["real_click_x"], args["real_click_y"])
            dist = math.hypot(self.master.width, self.master.height) / 2
            x = self.master.x + math.cos(math.pi / 180 * direction) * dist
            y = self.master.y + math.sin(math.pi / 180 * direction) * dist
            args["level"].get("bullets").append(CopperShell(x, y, direction, 50, "Assets/Images/Bullets/Bullet2.png",
                                                            32, 12, 520))
            self.timer = self.recharge_time


class SmallRocketLaunch(Skill):
    def __init__(self, *args):
        super().__init__(*args)
        self.recharge_time = 5
        self.number = 125
        self.image = pygame.image.load("Assets/Images/Skills/SmallRocket.png")
        self.image = pygame.transform.scale(self.image, (self.skills_list.tile_size, self.skills_list.tile_size))

    def use(self, args):
        if self.timer == 0 and self.number > 0:
            self.number -= 1
            direction = to_point(self.master.x, self.master.y, args["real_click_x"], args["real_click_y"])
            dist = math.hypot(self.master.width, self.master.height) / 2+ 10
            x = self.master.x + math.cos(math.pi / 180 * direction) * dist
            y = self.master.y + math.sin(math.pi / 180 * direction) * dist
            """n = 30
            for i in range(-n, n * 2, n):"""
            args["level"].get("bullets").append(SmallRocket(x, y, direction, 50,
                                                            "Assets/Images/Bullets/SmallRocket.png",
                                                            82, 20, 520, None,
                                                            self.master.speed_x, self.master.speed_y, args["level"]))
            self.timer = self.recharge_time


class MediumRocketLaunch(Skill):
    def __init__(self, *args):
        super().__init__(*args)
        self.recharge_time = 5
        self.number = 125
        self.image = pygame.image.load("Assets/Images/Skills/MediumRocket.png")
        self.image = pygame.transform.scale(self.image, (self.skills_list.tile_size, self.skills_list.tile_size))

    def use(self, args):
        if self.timer == 0 and self.number > 0:
            self.number -= 1
            direction = to_point(self.master.x, self.master.y, args["real_click_x"], args["real_click_y"])
            dist = math.hypot(self.master.width, self.master.height) / 2 + 10
            x = self.master.x + math.cos(math.pi / 180 * direction) * dist
            y = self.master.y + math.sin(math.pi / 180 * direction) * dist
            target = None
            for obj in [args["level"].get("player").ship, *args["level"].get("enemys_ships")]:
                if obj.check_intersection_with_point((args["real_click_x"], args["real_click_y"])):
                    target = obj
            """n = 30
            for i in range(-n, n * 2, n):"""
            args["level"].get("bullets").append(MediumRocket(x, y, direction, 50,
                                                             "Assets/Images/Bullets/MediumRocket.png",
                                                             140, 20, 520, target,
                                                             self.master.speed_x, self.master.speed_y, args["level"]))
            self.timer = self.recharge_time