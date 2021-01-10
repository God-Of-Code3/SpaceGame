from V2.Code.Constants import *
from V2.Code.Methods import *

from V2.Code.Entity import *
from V2.Code.Camera import *
from V2.Code.Controller import *
from V2.Code.Planet import *
from V2.Code.Skills import *
import random

clock = pygame.time.Clock()

frames_tree = {
    "main": {
        "frames": [["./Assets/Images/Ships/Inquisitor/Starship1_frame1.png", 20],
                   ["./Assets/Images/Ships/Inquisitor/Starship1_frame2.png", 20],
                   ["./Assets/Images/Ships/Inquisitor/Starship1_frame3.png", 20],
                   ["./Assets/Images/Ships/Inquisitor/Starship1_frame2.png", 20],
                   ["./Assets/Images/Ships/Inquisitor/Starship1_frame1.png", 20]],
        "next": "main"
    }
}

frames_tree2 = {
    "main": {
        "frames": [["./Assets/Images/Bullets/Bullet1.png", 20]],
        "next": "main"
    }
}

font = pygame.font.Font(None, 32)


class World:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.screen = pygame.display.set_mode(SIZE)
        self.events = []

        self.acceleration = 1

        self.player = Player(self)
        self.controllers = [self.player]
        self.planet = Planet(0, "Assets/Images/Planets/Planet1.png", 1000, 377, self)
        self.cam = Camera()

    def update(self):
        self.events = pygame.event.get()
        for controller in self.controllers:
            controller.control()
        skills_list.control()

        self.cam.control(self.events)

        self.all_sprites.update(mode="standart")
        self.all_sprites.update(mode="check")

    def draw(self):

        self.screen.fill(BACKGROUND_COLOR)

        self.cam.posite(self.all_sprites.sprites()[0])
        self.all_sprites.draw(self.screen)

        fps = clock.get_fps()
        self.planet.draw(self.screen)

        self.draw_fps(fps)
        self.draw_sprites_number()
        self.draw_player_coords()
        self.draw_health()
        skills_list.draw()

        pygame.display.flip()
        clock.tick(REAL_FPS)

        if fps != 0 and abs(REAL_FPS - fps) > 5:
            self.acceleration = REAL_FPS / fps
        else:
            self.acceleration = 1

    def draw_fps(self, fps):

        col = (0, 0, 0)
        if fps != 0:
            col = (int(max(0, min(255, 255 * (1 - fps / REAL_FPS)))), int(max(0, min(255, 255 * (fps / REAL_FPS)))), 0)
        text2 = font.render("FPS: " + str(int(fps)), True,
                            col)
        self.screen.blit(text2, (40, 40))

    def draw_sprites_number(self):

        col = (0, 255, 0)

        text2 = font.render("SPRITES: " + str(int(len(self.all_sprites.sprites()))), True,
                            col)
        self.screen.blit(text2, (40, 80))

    def draw_player_coords(self):

        col = (0, 255, 0)

        text2 = font.render("X: " + str(int(self.player.managed.coords[0])) + "; Y: " + str(int(
            self.player.managed.coords[1])), True, col)
        self.screen.blit(text2, (40, 120))

    def draw_health(self):
        for sprite in self.all_sprites.sprites():
            if "health" in dir(sprite):
                health = max(0, sprite.health / sprite.max_health)
                w = HEALTH_BAR_WIDTH
                h = HEALTH_BAR_HEIGHT
                w = max(HEALTH_BAR_MIN_WIDTH, w * self.cam.zoom)
                h = max(HEALTH_BAR_MIN_HEIGHT, h * self.cam.zoom)
                x = sprite.rect.center[0] - (w // 2)
                y = sprite.rect.y - h - 10
                pygame.draw.rect(self.screen, HEALTH_BAR_BACKGROUND, (x, y, w, h),
                                 border_radius=HEALTH_BAR_BORDER_RADIUS)
                pygame.draw.rect(self.screen, HEALTH_BAR_COLOR, (x, y, int(w * health), h),
                                 border_radius=HEALTH_BAR_BORDER_RADIUS)

    def remove_sprite(self, sprite):
        if sprite.controller is not None:
            controller = self.controllers.index(sprite.controller)
            self.controllers.pop(controller)
            sprite.kill()

    def add(self, x, y, controller=None, mass=100, width=76, height=40):
        Entity([self.all_sprites], frames_tree, self, width=width, height=height, coords=[x, y], controller=controller,
               mass=mass)

    def add_bullet(self, x, y, direction):
        speed = 10
        speeds = [
            math.cos(direction * math.pi / 180) * speed,
            math.sin(direction * math.pi / 180) * speed
        ]
        Bullet([self.all_sprites], frames_tree2, self, width=56, height=20, coords=[x, y], speed=speeds, mass=0,
               rot=direction)


world = World()
skills_list = SkillList(0, 200, None, world, [1, None, 1, None, 1, 1, 1])
world.add(-100, -700, world.player, 10000, 304, 160)
world.add_bullet(-300, -900, 0)
for i in range(2):
    for j in range(2):
        world.controllers.append(Enemy(world))
        world.add(i * 160, j * 160 - 1000, mass=1000, width=152, height=80, controller=world.controllers[-1])

while True:
    world.update()
    world.draw()
