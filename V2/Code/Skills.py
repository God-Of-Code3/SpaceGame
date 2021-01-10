from V2.Code.Constants import *
from V2.Code.Methods import *

import pygame


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
            if skill is not None:
                # sc.blit(skill.image, (x2, y2))
                pass
            if self.selected == i:
                pygame.draw.rect(sc, SKILL_BACKGROUND_ACTIVE, (x, y, SKILL_TILE_SIZE, SKILL_TILE_SIZE))

            pygame.draw.rect(sc, SKILL_BORDER_COLOR, (x, y, SKILL_TILE_SIZE, SKILL_TILE_SIZE - 1),
                             SKILL_BORDER_WIDTH)

    def select(self, i):
        if self.skills[i] is not None:
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



class Skill:
    def __init__(self, name):
        pass