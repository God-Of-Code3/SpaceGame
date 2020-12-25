from Classes.Player import *
from Classes.Bullet import *
from Classes.Skill import *
from Classes.Camera import *
from Classes.AI import *
from Classes.Animation import *
import random
pygame.init()

screen = pygame.display.set_mode(SIZE)
cam = Camera(pygame.Color('blue'), screen, 0.05, 2, 1.2)
player = Player(cam, all_sprites, frames_tree)

update_event = pygame.USEREVENT + get_counter()
pygame.time.set_timer(update_event, 10)

enemys = [Starship(700 + 100 * i, 250 + random.randint(-100, 100), "Assets/Images/Ships/Starship1_enemy.png", 152, 80,
                   1000, cam, all_sprites, frames_tree) for i in range(10)]

ai = AI(enemys[0], player)

bullets = []

#anim = Anim(all_sprites, cam, frames_tree, enemys[0], 152, 80, )


def draw(screen, info):
    img = info["img"]
    img = pygame.transform.scale(img, (info["width"], info['height']))  # Изменение размера картинки
    img = pygame.transform.rotate(img, info['rot'])  # Поворот картинки
    screen.blit(img, (info['x'] - info['width'] / 2, info['y'] - info['height'] / 2))


while True:
    screen.fill((46, 29, 140))
    events = pygame.event.get()
    drawing = []
    for event in events:
        if event.type == update_event:
            player.ship.update(enemys)
            for enemy in enemys:
                enemy.update(enemys)
            dels = []
            for i, bullet in enumerate(bullets):
                if not bullet.update():
                    dels.append(i)
                else:
                    for enemy in [*enemys, player.ship]:
                        if bullet.check_intersection(enemy):
                            enemy.speed_x += math.cos(bullet.direction * math.pi / 180) * bullet.speed * 100 / \
                                             enemy.mass
                            enemy.speed_y += math.sin(bullet.direction * math.pi / 180) * bullet.speed * 100 / \
                                             enemy.mass
                            dels.append(i)
            for i, el in enumerate(dels):
                bullets.pop(el - i)
            player.update()
            ai.update()
            all_sprites.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_coords_to_real(cam, event.pos)
    cam.control(events)
    for bullet in bullets:
        drawing.append(bullet.info_for_drawing())
    cam.cam_pos = (player.ship.x + random.randint(-2, 2) * 0, player.ship.y + random.randint(-2, 2) * 0)
    #player.laser.check_intersection(enemys, screen)
    #player.skills_list.draw(screen)
    all_sprites.draw(screen)
    player.draw(screen, cam)
    player.control(events, bullets, cam, enemys)
    #ai.control(events, bullets, cam, enemys)

    pygame.display.flip()
