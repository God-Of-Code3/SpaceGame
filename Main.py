from Classes.Player import *
from Classes.Camera import *
from Classes.AI import *
from Classes.Animation import *
from Classes.Level import *
from Classes.VisualHandler import *
import random

import time

pygame.init()

screen = pygame.display.set_mode(SIZE)
cam = Camera(pygame.Color('blue'), screen, 0.15, 2, 1.2)
world = World(6000)
player = Player(world, cam, all_sprites, "Inquisitor")

update_event = pygame.USEREVENT + get_counter()
pygame.time.set_timer(update_event, 10)

FPS = 55
clock = pygame.time.Clock()

enemys = []
ais = []

for i in range(0):
    ship, skills = create_ship(world, cam, all_sprites, i * 900 + 600, -200, "Hindenburg")
    enemys.append(ship)
    ais.append(AI(ship, player, skills))

for i in range(15):
    ship, skills = create_ship(world, cam, all_sprites, i * 900 + 600, -400, "Bug")
    enemys.append(ship)
    ais.append(AI(ship, player, skills))

planet = Planet(0, "Assets/Images/Planets/Planet1.png", 1000, 377, cam)
bullets = []


def draw(screen, info):
    img = info["img"]
    img = pygame.transform.scale(img, (info["width"], info['height']))  # Изменение размера картинки
    img = pygame.transform.rotate(img, info['rot'])  # Поворот картинки
    screen.blit(img, (info['x'] - info['width'] / 2, info['y'] - info['height'] / 2))


expls = []
last_health = player.ship.health
shaking = 0


world_data = {"enemys_ships": enemys, "enemys_ai": ais, "bullets": bullets, "expls": expls, "player": player,
              "cam": cam, "screen": screen, "all_sprites": all_sprites, "planet": planet}


class Level:
    def __init__(self, data):
        self.world_data = data

    def get(self, obj):
        return self.world_data[obj]

    def set(self, obj, value):
        self.world_data[obj] = value


level = Level(world_data)
visual_handler = VisualHandler(level)

running = True
while running:

    events = pygame.event.get()
    drawing = []
    start_time = time.time()
    print("-------")
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    for ai in level.get("enemys_ai"):
        ai.control(events, level)
        ai.update()
    dels = []

    other_ships = [ship for ship in [*level.get("enemys_ships"), level.get("player").ship]]
    for i, enemy in enumerate(level.get("enemys_ships")):

        if not enemy.update(other_ships.copy(), i):
            dels.append(i)
    for i, el in enumerate(dels):
        en = enemys[el - i]
        level.get("all_sprites").remove_internal(en.sprite)
        level.get("expls").append(Explosion(en.x, en.y, max(en.image_width / 2, 250), cam))
        level.get("enemys_ships").pop(el - i)
        level.get("enemys_ai").pop(el - i)
    dels = []
    for i, bullet in enumerate(level.get("bullets")):
        if not bullet.update():
            dels.append(i)
        else:
            for enemy in [*level.get("enemys_ships"), level.get("player").ship]:
                if bullet.check_intersection(enemy):
                    if not bullet.hit(enemy):
                        dels.append(i)

    for i, el in enumerate(dels):
        level.get("bullets").pop(el - i)
    if level.get("player").ship.health > 0:
        level.get("player").update()
        level.get("player").ship.update(level.get("enemys_ships"), -1)
    else:
        if level.get("all_sprites").has(level.get("player").ship.sprite):
            ship = level.get("player").ship
            level.get("all_sprites").remove(ship.sprite)
            level.get("expls").append(Explosion(ship.x, ship.y, max(ship.image_width / 2, 250),
                                                level.get("cam")))
    for expl in level.get("expls"):
        expl.update([*level.get("enemys_ships"), level.get("player").ship])
    level.set("expls", list(filter(lambda x: x.size > 1 or len(x.circles) > 0 or len(x.particles) >
                                                      0, level.get("expls"))))
    #player.laser.check_intersection(enemys, screen)
    #player.skills_list.draw(screen)
    if level.get("player").ship.health > 0:
        level.get("player").control(events, level)

    cam.control(events)

    #print(1 / (time.time() - start_time))
    # ----------
    level.get("all_sprites").update()
    visual_handler.draw()
    print(clock.get_fps())
    pygame.display.flip()
    clock.tick(FPS)
