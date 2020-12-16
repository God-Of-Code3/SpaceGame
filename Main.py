from Classes.Player import *
from Classes.Bullet import *
import random
pygame.init()


screen = pygame.display.set_mode((1900, 600))
player = Player()

update_event = pygame.USEREVENT + 1
pygame.time.set_timer(update_event, 10)

enemys = [Starship(700 + 100 * i, 250, "Assets/Images/Ships/Starship1.png", 38, 20, 1000, 38, 20) for i in
          range(10)]

bullets = [Bullet(0, 0, i * 10, 10, "Assets/Images/Bullets/Bullet1.png", 28, 10) for i in range(10)]


def draw(screen, info):
    img = info["img"]
    img = pygame.transform.scale(img, (info["width"], info['height'])) # Изменение размера картинки
    img = pygame.transform.rotate(img, info['rot'])  # Поворот картинки
    screen.blit(img, (info['x'] - info['width'] / 2, info['y'] - info['height'] / 2))


while True:
    screen.fill((0, 0, 0))
    events = pygame.event.get()
    player.control(events)
    for event in events:
        if event.type == update_event:
            player.ship.update()
            for enemy in enemys:
                enemy.update()
            dels = []
            for i, bullet in enumerate(bullets):
                bullet.update()
                for enemy in enemys:
                    if bullet.check_intersection(enemy):
                        enemy.speed_x += math.cos(bullet.direction * math.pi / 180) * bullet.speed
                        enemy.speed_y += math.sin(bullet.direction * math.pi / 180) * bullet.speed
                        dels.append(i)
            for i, el in enumerate(dels):
                bullets.pop(el - i)
    draw(screen, player.get_info_for_drawing())
    for enemy in enemys:
        draw(screen, enemy.info_for_drawing())
        player.ship.check_intersection_with_ship(enemy)
        for enemy2 in enemys:
            if enemy2 != enemy:
                enemy.check_intersection_with_ship(enemy2)
    for bullet in bullets:
        draw(screen, bullet.info_for_drawing())
    pygame.display.flip()
