from V2.Code.Constants import *
from V2.Code.Methods import *

from V2.Code.Entity import *
from V2.Code.Camera import *
from V2.Code.Controller import *
from V2.Code.Planet import *
from V2.Code.Skills import *

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

        self.player = Player(self, skills=[None, None, {"skill": "PlasmaShot", "number": 200},
                                           {"skill": "CopperShellShot", "number": 200},
                                           {"skill": "LaserShot", "number": -1},
                                           {"skill": "MediumRocketLaunch", "number": 200},
                                           {"skill": "SmallRocketLaunch", "number": 200}])
        self.controllers = [self.player]
        self.planet = Planet(0, "Assets/Images/Planets/Planet1.png", 1000, 377, self)
        self.cam = Camera()

    def update(self):

        self.screen.fill(BACKGROUND_COLOR)
        self.events = []
        self.events = pygame.event.get()

        for controller in self.controllers:
            controller.control()
            controller.update()

        self.cam.control(self.events)

        self.all_sprites.update(mode="check")
        self.all_sprites.update(mode="standart")

        killing = []
        for sprite in self.all_sprites.sprites():
            if isinstance(sprite, Entity):
                if sprite.health <= 0:
                    killing.append(sprite)

        for sprite in killing:
            self.remove_sprite(sprite)

    def draw(self):

        self.cam.posite(self.all_sprites.sprites()[0])
        self.all_sprites.draw(self.screen)

        fps = clock.get_fps()
        self.planet.draw(self.screen)
        self.controllers[0].skills.draw()

        self.draw_fps(fps, 0, 300)
        self.draw_sprites_number(0, 300)
        self.draw_player_coords(0, 300)
        self.draw_health()

        """print("--------------")
        for sprite in self.all_sprites.sprites():
            print(sprite.__class__.__name__)"""

        pygame.display.flip()
        clock.tick(REAL_FPS)

        if fps != 0 and abs(REAL_FPS - fps) > 5:
            self.acceleration = REAL_FPS / fps
        else:
            self.acceleration = 1

    def draw_fps(self, fps, x, y):

        col = (0, 0, 0)
        if fps != 0:
            col = (int(max(0, min(255, 255 * (1 - fps / REAL_FPS)))), int(max(0, min(255, 255 * (fps / REAL_FPS)))), 0)
        text2 = font.render("FPS: " + str(int(fps)), True,
                            col)
        self.screen.blit(text2, (x + 40, y + 40))

    def draw_sprites_number(self, x, y):

        col = (0, 255, 0)

        text2 = font.render("SPRITES: " + str(int(len(self.all_sprites.sprites()))), True,
                            col)
        self.screen.blit(text2, (x + 40, y + 80))

    def draw_player_coords(self, x, y):

        col = (0, 255, 0)

        text2 = font.render("X: " + str(int(self.player.managed.coords[0])) + "; Y: " + str(int(
            self.player.managed.coords[1])), True, col)
        self.screen.blit(text2, (x + 40, y + 120))

    def draw_health(self):
        for sprite in self.all_sprites.sprites():
                if isinstance(sprite, Starship):
                    health = max(0, sprite.health / sprite.max_health)
                    w = HEALTH_BAR_WIDTH
                    h = HEALTH_BAR_HEIGHT
                    w = max(HEALTH_BAR_MIN_WIDTH, w * self.cam.zoom)
                    h = max(HEALTH_BAR_MIN_HEIGHT, h * self.cam.zoom)
                    x = sprite.rect.center[0] - (w // 2)
                    y = sprite.rect.y - h - 10
                    pygame.draw.rect(self.screen, HEALTH_BAR_BACKGROUND, (x, y, w, h))
                    pygame.draw.rect(self.screen, HEALTH_BAR_COLOR, (x, y, int(w * health), h))

    def remove_sprite(self, sprite):
        if sprite.controller is not None:
            controller = self.controllers.index(sprite.controller)
            self.controllers.pop(controller)
        x, y = sprite.coords
        if isinstance(sprite, Starship):
            r = max(250, sprite.width)
            Explosion(self.all_sprites, frames_tree2, self, health=150, coords=[x, y], width=r, height=r)
        sprite.kill()

    def add(self, x, y, controller=None, mass=100, width=76, height=40):
        Entity(self.all_sprites, frames_tree, self, width=width, height=height, coords=[x, y], controller=controller,
               mass=mass)

    def create_ship(self, cls, x, y, controller=None, skills=None):
        d = ships_data[cls]

        if skills is None:
            skills = []
            eq = d["equipment"]
            for skill in eq:
                skills.append({"skill": skill, "number": eq[skill]})
        if controller is None:
            controller = Enemy(world.controllers[0], world, skills=skills, beh=d["behaviour"])
            self.controllers.append(controller)

        Starship(self.all_sprites, d["anim"], self, coords=[x, y], max_speed=[d["msx"], d["msy"]],
                 max_acceleration=[d["ax"], d["ay"]], friction=[d["fx"], d["fy"]], mass=d["mass"], health=d["hp"],
                 width=d["width"], height=d["height"], controller=controller)


world = World()
world.create_ship("Inquisitor", -200, -80, world.player)
for i in range(0):
    for j in range(0):
        world.create_ship("Bug", i * 500, j * 300 - 1200)


world.create_ship("Hindenburg",  -200, -MIN_AIR_ATTACK_HEIGHT-100)

while True:
    world.update()
    world.draw()
