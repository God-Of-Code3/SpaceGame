from Classes.Player import *
from Classes.Camera import *
from Classes.AI import *
from Classes.Animation import *
from Classes.Level import *
import random
pygame.init()

screen = pygame.display.set_mode(SIZE)
cam = Camera(pygame.Color('blue'), screen, 0.2, 2, 1.2)
world = World(6000)
player = Player(world, cam, all_sprites, "Inquisitor")

update_event = pygame.USEREVENT + get_counter()
pygame.time.set_timer(update_event, 10)

enemys = [create_ship(world, cam, all_sprites, i * 100 + 400, -700, "Bug") for i in range(10)]

ais = [AI(en, player) for en in enemys]
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
while True:
    screen.fill((46, 29, 140))
    events = pygame.event.get()
    drawing = []
    for event in events:
        if event.type == update_event:
            player.ship.update(enemys)
            dels = []
            for i, enemy in enumerate(enemys):
                if not enemy.update(enemys):
                    dels.append(i)
            for i, el in enumerate(dels):
                en = enemys[el - i]
                all_sprites.remove_internal(en.sprite)
                expls.append(Explosion(en.x, en.y, 200, cam))
                enemys.pop(el - i)
                ais.pop(el - i)

            dels = []
            for i, bullet in enumerate(bullets):
                if not bullet.update():
                    dels.append(i)
                else:
                    for enemy in [*enemys, player.ship]:
                        if bullet.check_intersection(enemy):
                            enemy.health -= bullet.damage
                            dels.append(i)
            for i, el in enumerate(dels):
                bullets.pop(el - i)
            player.update()
            for ai in ais:
                ai.update()
            all_sprites.update()
            for expl in expls:
                expl.update([*enemys, player.ship])
            expls = list(filter(lambda x: x.size > 1 or len(x.circles) > 0 or len(x.particles) > 0, expls))
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_coords_to_real(cam, event.pos)
    cam.control(events)
    for bullet in bullets:
        drawing.append(bullet.info_for_drawing())
    for spr in all_sprites.sprites():
        if isinstance(spr.master, Starship):
            w, h = 100 * cam.zoom_value, 20 * cam.zoom_value
            x = spr.rect.center[0] - w / 2
            y = spr.rect.y - h - 10

            percent = max(int(spr.master.health / spr.master.max_health * w), 0)
            pygame.draw.rect(screen, (41, 255, 62), (x, y, percent, h))
            pygame.draw.rect(screen, (255, 255, 255), (x, y, w, h), 2)

    cam.drawing(drawing, cam.cam_pos, cam.zoom_value)
    cam.cam_pos = (player.ship.x, player.ship.y)
    if shaking != 0:
        sh_lvl = 5
        cam.cam_pos = (cam.cam_pos[0] + random.randint(-sh_lvl, sh_lvl),
                       cam.cam_pos[1] + random.randint(-sh_lvl, sh_lvl))

    #player.laser.check_intersection(enemys, screen)
    #player.skills_list.draw(screen)
    all_sprites.draw(screen)
    player.draw(screen, cam)
    player.control(events, bullets, cam, enemys)
    for ai in ais:
        ai.control(events, bullets, cam, [*enemys, player.ship])
    planet.draw(screen)
    for expl in expls:
        expl.draw(screen)
    if last_health > player.ship.health:
        shaking = 2
        last_health = player.ship.health
    shaking = max(0, shaking - 1)
    pygame.display.flip()
