from Classes.Player import *
pygame.init()


screen = pygame.display.set_mode((1900, 600))
player = Player()

update_event = pygame.USEREVENT + 1
pygame.time.set_timer(update_event, 10)

enemys = [Starship(800 + 100 * i, 500 + 20 * i, "Assets/Images/Ships/Starship1.png", 76, 40, 1000, 76, 40) for i in
          range(1)]


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
    draw(screen, player.get_info_for_drawing())
    for enemy in enemys:
        draw(screen, enemy.info_for_drawing())
        player.ship.check_intersection_with_ship(enemy)
        for enemy2 in enemys:
            if enemy2 != enemy:
                enemy.check_intersection_with_ship(enemy2)
    pygame.display.flip()
