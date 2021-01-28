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
goals = ["Уничтожить все командные пункты", "Уничтожить все корабли противника"]


def generate_level(level_name):
    data = json.load(open("Data/Levels/" + level_name + ".json", "r"))
    player_data = json.load(open("Data/PlayerData.json", "r"))
    save = True
    array = [None] * player_data["player_inv_width"]
    for skill in player_data["player_inv"]:
        array[skill[1]] = {"skill": skill[0].rstrip(".png").rstrip(".jpg"), "number": skill[3]}
    if data["player_skills"]:
        array = data["player_skills"]
        save = False
    world = World(array)
    player_pos = data["player_pos"]
    world.create_ship("Inquisitor", player_pos[0], player_pos[1], world.player)
    for ship in data["ships"]:
        world.create_ship(ship["class"], *ship["coords"])
    for nexus in data["nexuses"]:
        world.create_nexus(nexus["class"], *nexus["coords"])
    world.goal = goals[data["goal"]]
    world.income = data["reward"]
    world.ranges = data["ranges"]

    return world, save


class World:
    def __init__(self, skills):
        self.all_sprites = pygame.sprite.Group()
        self.screen = pygame.display.set_mode(SIZE)
        self.events = []

        self.acceleration = 1

        self.player = Player(self, skills=skills)
        self.controllers = [self.player]
        self.planet = Planet(0, "Assets/Images/Planets/Planet1.png", 1000, 377, self)
        self.cam = Camera()

        self.nexuses = []
        self.state = "play"
        self.goal = goals[0]
        self.running = True
        self.start = True
        self.step = -1
        self.warning_step = 0
        self.ranges = [-2000, 5000]

        self.stars = [(random.randint(0, STAR_RANGE),
                       random.randint(0, STAR_RANGE),
                       STAR_COLOR, random.randint(STAR_MIN_SIZE, STAR_MAX_SIZE)) for _ in range(STAR_COUNT)]

        self.income = 1000

    def update(self):
        self.events = []
        self.events = pygame.event.get()
        self.warning_step += 5
        self.warning_step %= 510
        if not self.start:
            self.screen.fill(BACKGROUND_COLOR)
            self.draw_sky()
            self.draw_range()

            if self.warning_step < 5 and (self.player.managed.coords[0] < self.ranges[0] or
                                          self.player.managed.coords[0] > self.ranges[1]):
                self.player.managed.health -= PLAYGROUND_DAMAGE * self.player.managed.max_health / 100

            if self.state == "play":
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

            if self.step != -1:
                self.step += 1

            self.nexuses = list(filter(lambda n: n.health > 0, self.nexuses))
            if self.player.managed.health <= 0 and self.state == "play":
                self.state = "defeat"
                self.step = 0

            if self.goal == goals[0]:
                if len(self.nexuses) == 0 and self.state == "play":
                    self.state = "victory"
                    self.step = 0

            elif self.goal == goals[1]:
                if len([sprite for sprite in self.all_sprites.sprites() if isinstance(sprite, Starship)]) == 1 and \
                        self.state == "play" and self.player.managed.health > 0:
                    self.state = "victory"
                    self.step = 0

    def draw_sky(self):
        zoom = self.cam.zoom
        pos = self.cam.pos
        w, h = STAR_RANGE * zoom, STAR_RANGE * zoom
        y_numb = SIZE[1] // h
        x_numb = SIZE[0] // w + 1
        x_shift = (pos[0] % STAR_RANGE) * zoom
        y_shift = (pos[1] % STAR_RANGE) * zoom
        for i in range(-int(x_numb), int(x_numb) + 2):
            for j in range(-int(y_numb), int(y_numb) + 2):
                for star in self.stars:

                    x = SIZE[0] / 2 - x_shift + star[0] * zoom - STAR_RANGE * zoom / 2 + i * w
                    y = SIZE[1] / 2 - y_shift + star[1] * zoom - STAR_RANGE * zoom / 2 + j * h
                    self.draw_star(x, y, star[2], star[3] * zoom)

    def draw_range(self):
        zoom = self.cam.zoom
        pos = self.cam.pos
        for rng in self.ranges:
            x = (rng - pos[0]) * zoom + SIZE[0] / 2
            pygame.draw.line(self.screen, RANGE_LINE_COLOR2, (x, 0), (x, SIZE[1]), int(RANGE_LINE_WIDTH * zoom * 3))
            pygame.draw.line(self.screen, RANGE_LINE_COLOR, (x, 0), (x, SIZE[1]), int(RANGE_LINE_WIDTH * zoom))

    def draw_star(self, x, y, col, size):
        if size >= 1:
            pygame.draw.circle(self.screen, col, (int(x), int(y)), int(size))

    def draw(self):
        if self.state == "play":
            self.cam.posite(self.all_sprites.sprites()[0])
        self.all_sprites.draw(self.screen)

        fps = clock.get_fps()
        self.planet.draw(self.screen)
        self.draw_health()
        if self.player.managed.health > 0:

            self.controllers[0].skills.draw()

        self.draw_player_health()
        self.draw_fps(fps, 0, 300)
        self.draw_sprites_number(0, 300)
        self.draw_player_coords(0, 300)
        self.draw_minimap()

        if self.player.managed.coords[0] < self.ranges[0] or self.player.managed.coords[0] > self.ranges[1]:
            self.draw_warning(self.player.managed.coords[0] < self.ranges[0])

        if self.step > 0:
            self.draw_end_banner()

        if self.start:
            self.draw_start_banner()

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

    def draw_warning(self, left):

        font = pygame.font.SysFont('Arial', 20)
        string = "ВЕРНИТЕСЬ В БЕЗОПАСНУЮ ЗОНУ (ДВИГАЙТЕСЬ "
        if left:
            string += "ВПРАВО)"
        else:
            string += "ВЛЕВО)"
        image_text = font.render(string, True, pygame.Color('red'))
        image_text.set_alpha(min(255, (255 - self.warning_step) * 2))
        width = image_text.get_width()
        i_t_x = SIZE[0] // 2 - width // 2
        i_t_y = 10

        self.screen.blit(image_text, (i_t_x, i_t_y))

    def draw_start_banner(self):
        surf = pygame.Surface(SIZE)
        surf.fill((0, 0, 0))
        img = load_image("Assets/Images/Ships/Nexus/Nexus.png")
        img = pygame.transform.scale(img, (349, 315))
        width = img.get_width()
        i_x = SIZE[0] // 2 - width // 2
        i_y = 50

        font = pygame.font.SysFont('Arial', 20)
        string = "Так выглядит командный пункт:"
        image_text = font.render(string, True, pygame.Color('white'))
        width = image_text.get_width()
        i_t_x = SIZE[0] // 2 - width // 2
        i_t_y = 10

        font = pygame.font.SysFont('Arial', 40)
        string = "Цель: " + self.goal
        text = font.render(string, True, pygame.Color('white'))
        width = text.get_width()
        height = text.get_height()
        x = SIZE[0] // 2 - width // 2
        y = SIZE[1] // 2 - height // 2

        self.screen.blit(surf, (0, 0))
        self.screen.blit(text, (x, y))

        if self.goal == goals[0]:
            self.screen.blit(img, (i_x, i_y))
            self.screen.blit(image_text, (i_t_x, i_t_y))

        font = pygame.font.SysFont('Arial', 30)
        string = "ПОНЯЛ"
        text = font.render(string, True, pygame.Color('white'))
        width = text.get_width()
        height = text.get_height()
        padding = 10
        x = SIZE[0] // 2 - width // 2
        y = SIZE[1] // 4 * 3 - height // 2
        col = (50, 50, 50)
        m_x, m_y = pygame.mouse.get_pos()
        if x - padding <= m_x <= x + width + padding and y - padding <= m_y <= y + height + padding:
            col = (70, 70, 70)
            for event in self.events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.start = False
                        pygame.event.set_grab(True)
        pygame.draw.rect(self.screen, col, (x - padding, y - padding, width + padding * 2,
                                            height + padding * 2))
        self.screen.blit(text, (x, y))

    def draw_minimap(self):
        scale = MINIMAP_SIZE[0] / (self.ranges[1] - self.ranges[0])
        y = MINIMAP_SIZE[1] / scale
        x = self.ranges[0]
        x2 = self.ranges[1]

        pygame.draw.rect(self.screen, (0, 0, 0), (*MINIMAP_COORDS, *MINIMAP_SIZE))

        for sprite in self.all_sprites.sprites():
            if isinstance(sprite, Starship):
                if x < sprite.coords[0] < x2:
                    spr_x = (sprite.coords[0] - x) * scale + MINIMAP_COORDS[0]
                    spr_y = (sprite.coords[1] + y) * scale + MINIMAP_COORDS[1]
                    if self.goal == goals[0] and isinstance(sprite, Nexus):
                        pygame.draw.circle(self.screen, (255, 0, 0), (int(spr_x), int(spr_y)), 1)
                    else:
                        pygame.draw.circle(self.screen, (255, 255, 255), (int(spr_x), int(spr_y)), 1)
                    if self.player.managed == sprite:
                        pygame.draw.circle(self.screen, (255, 255, 0), (int(spr_x), int(spr_y)), 1)

    def draw_end_banner(self):
        start = 100
        if self.step > start:
            surf = pygame.Surface(SIZE)
            surf.fill((0, 0, 0))
            surf.set_alpha(min((self.step - start) * 4, 255))
            font = pygame.font.SysFont('Arial', 40)
            string = "Вы победили" if self.state == "victory" else "Вы проиграли"
            text = font.render(string, True, pygame.Color('white'))
            width = text.get_width()
            height = text.get_height()
            x = SIZE[0] // 2 - width // 2
            y = SIZE[1] // 2 - height // 2

            self.screen.blit(surf, (0, 0))
            self.screen.blit(text, (x, y))

            if self.state == "victory":
                font = pygame.font.SysFont('Arial', 30)
                income = ""
                for i in range(len(str(self.income)), 0, -1):
                    income += str(self.income)[i - 1]
                    if (len(str(self.income)) - i) % 3 == 2:
                        income += " "
                income = "".join(reversed(list(income)))
                string = "Награда за бой: " + income + "$"
                text = font.render(string, True, pygame.Color('#ffa929'))
                width = text.get_width()
                height2 = text.get_height()
                x = SIZE[0] // 2 - width // 2
                y = SIZE[1] // 2 - height2 // 2 + height + 20
                self.screen.blit(text, (x, y))

            font = pygame.font.SysFont('Arial', 30)
            string = "В МЕНЮ"
            text = font.render(string, True, pygame.Color('white'))
            width = text.get_width()
            height = text.get_height()
            padding = 10
            x = SIZE[0] // 2 - width // 2
            y = SIZE[1] // 4 * 3 - height // 2
            col = (50, 50, 50)
            m_x, m_y = pygame.mouse.get_pos()
            if x - padding <= m_x <= x + width + padding and y - padding <= m_y <= y + height + padding:
                col = (70, 70, 70)
                for event in self.events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.running = False
            pygame.draw.rect(self.screen, col, (x - padding, y - padding, width + padding * 2,
                                                         height + padding * 2))
            self.screen.blit(text, (x, y))

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

    def draw_player_health(self):
        sprite = self.player.managed
        health = max(0, sprite.health / sprite.max_health)
        w = self.player.skills.get_width()
        h = HEALTH_BAR_HEIGHT2
        w = max(HEALTH_BAR_MIN_WIDTH, w)
        x = 0
        y = 0
        pygame.draw.rect(self.screen, HEALTH_BAR_BACKGROUND, (x, y, w, h))
        pygame.draw.rect(self.screen, HEALTH_BAR_COLOR, (x, y, int(w * health), h))

    def remove_sprite(self, sprite):
        if sprite.controller is not None:
            controller = self.controllers.index(sprite.controller)
            self.controllers.pop(controller)
        x, y = sprite.coords
        if isinstance(sprite, Starship):
            r = max(250, sprite.width)
            Explosion(self.all_sprites, frames_tree2, self, health=150, coords=[x, y], width=r, height=r, damage=0)
            for skill in sprite.controller.skills.skills:
                if isinstance(skill, AntimatterShot):
                    if skill.number > 0:
                        r = 1500
                        AnnihilationExplosion(self.all_sprites, frames_tree2, self, health=500,
                                              coords=[*sprite.coords],
                                              width=r, height=r, damage=0)
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
            controller = Enemy(self.controllers[0], self, skills=skills, beh=d["behaviour"])
            self.controllers.append(controller)

        Starship(self.all_sprites, d["anim"], self, coords=[x, y], max_speed=[d["msx"], d["msy"]],
                 max_acceleration=[d["ax"], d["ay"]], friction=[d["fx"], d["fy"]], mass=d["mass"], health=d["hp"],
                 width=d["width"], height=d["height"], controller=controller)

    def create_station(self, cls, x, y, controller=None, skills=None):
        d = ships_data[cls]

        if skills is None:
            skills = []
            eq = d["equipment"]
            for skill in eq:
                skills.append({"skill": skill, "number": eq[skill]})
        if controller is None:
            controller = Enemy(self.controllers[0], self, skills=skills, beh="station")
            self.controllers.append(controller)

        Station(self.all_sprites, d["anim"], self, coords=[x, y], mass=d["mass"], health=d["hp"],
                width=d["width"], height=d["height"], controller=controller)

    def create_nexus(self, cls, x, y):
        d = ships_data[cls]

        skills = []
        eq = d["equipment"]
        for skill in eq:
            skills.append({"skill": skill, "number": eq[skill]})

        controller = Enemy(self.controllers[0], self, skills=skills, beh=d["behaviour"])
        self.controllers.append(controller)

        n = Nexus(self.all_sprites, d["anim"], self, coords=[x, y], max_speed=[d["msx"], d["msy"]],
                  max_acceleration=[d["ax"], d["ay"]], friction=[d["fx"], d["fy"]], mass=d["mass"], health=d["hp"],
                  width=d["width"], height=d["height"], controller=controller)
        self.nexuses.append(n)

if __name__ == "__main__":
    world = generate_level("level1")
    """world = World()
    world.create_ship("Inquisitor", -1000, -80, world.player)
    for i in range(1):
        for j in range(1):
            world.create_ship("Bug", i * 500, j * 300 - 1200)
    
    for i in range(2):
        world.create_ship("Hindenburg",  -200 - 100 * i, -MIN_AIR_ATTACK_HEIGHT-100)
    world.create_nexus("Nexus",  0, -NEXUS_HEIGHT)"""

    while world.running:
        world.update()
        world.draw()
