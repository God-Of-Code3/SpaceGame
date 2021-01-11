from V2.Code.Constants import *
from V2.Code.Methods import *

import pygame
import json

file = open("Data/Skills.json", "r", encoding="utf-8")
skills_data = json.load(file)


class SkillList:
    def __init__(self, x, y, master, world, skills):
        self.x = x
        self.y = y
        self.master = master
        self.skills = skills  # [Skill, None, None, Skill, Skill, Skill, None]
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
            if self.selected == i:

                pygame.draw.rect(sc, SKILL_BACKGROUND_ACTIVE, (x, y, SKILL_TILE_SIZE, SKILL_TILE_SIZE))
            if skill.type == "passive":
                pygame.draw.rect(sc, SKILL_BACKGROUND_PASSIVE, (x, y, SKILL_TILE_SIZE, SKILL_TILE_SIZE))
            if skill is not None:
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
            pygame.draw.rect(sc, col, (x, y, SKILL_TILE_SIZE, SKILL_TILE_SIZE - 1),
                             SKILL_BORDER_WIDTH)
            if skill.number != -1 and skill.type == "active":
                font = pygame.font.SysFont('Calibri', 20)
                string_rendered = font.render(str(skill.number), True, pygame.Color('black'))
                sc.blit(string_rendered, (x + SKILL_TILE_PADDING, y + SKILL_TILE_PADDING))

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
            if self.selected == i:
                skill.selected = True
            else:
                skill.selected = False
            if skill is not None:
                skill.update(args)

    def check_pos(self, pos):
        if self.x <= pos[0] <= self.x + self.length * SKILL_TILE_SIZE \
                and self.y <= pos[1] <= self.y + SKILL_TILE_SIZE:
            return True
        return False


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
            self.using_timer = max(self.using_timer - 1, 0)
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
        if self.type == "active" and (self.number == -1 or self.number > 0):
            self.recharge_timer = max(self.recharge_timer - 1, 0)
            if self.using_process and self.recharge_timer == 0:
                if self.auto_using or self.selected:
                    self.using(args)
                if self.using_timer == 0 and self.using_time != -1:
                    self.using_process = False
                    self.recharge_timer = self.recharge_time

            if self.selected:
                if args["use"]:
                    self.use(args)
        else:
            self.passive_code()
