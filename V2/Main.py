from V2.Code.World import *
from V2.Code.Inventory import *
from V2.Code.MainMenu import *
import os


pygame.init()
size = width, height = SIZE[0], SIZE[1]
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))

menu = MainMenu(BACKGROUND, SPEED)

# fps = FPS


clock = pygame.time.Clock()
running = True
while running:
    screen.fill(pygame.Color('black'))
    res = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            res = menu.controller(event, screen)
    menu.drawing(screen)
    pygame.display.flip()
    if res:
        size = width, height = SIZE[0], SIZE[1]
        screen = pygame.display.set_mode(size)
        screen.fill(pygame.Color('black'))

        data = open("./Data/PlayerData.json", "r", encoding="utf-8")
        inv_data = json.load(data)
        level = inv_data["level"]
        data2 = open(f"./Data/Levels/{level}.json", "r", encoding="utf-8")
        level_data = json.load(data2)
        if not level_data["player_skills"]:
            items = []
            for d in inv_data["inv"]:
                if d[3] != 0:
                    items.append(tuple(d))

            items2 = []
            for d in inv_data["player_inv"]:
                if d[3] != 0:
                    items2.append(tuple(d))

            inv = Inventory(screen, items, inv_data["inv_width"], inv_data["inv_height"],
                            items2, inv_data["player_inv_width"], inv_data["player_inv_height"],
                            inv_data["money"])

            running = True
            bg = pygame.image.load("Assets/Images/Other/SpaceBg.jpg")
            centerx = bg.get_rect().width // 2 - SIZE[0] // 2
            centery = bg.get_rect().height // 2 - SIZE[1] // 2

            while inv.running:
                screen.fill(pygame.Color('black'))
                x, y = pygame.mouse.get_pos()
                x -= SIZE[0] // 2
                y -= SIZE[1] // 2
                if inv.show_info:
                    x, y = 0, 0
                screen.blit(bg, (int(-centerx - x * 0.02), int(-centery - y * 0.02)))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        running = False
                    else:
                        inv.controller(event, screen)
                inv.drawing(screen)
                pygame.display.flip()
            inv_data["inv"] = inv.get_inventory_slots2()
            inv_data["player_inv"] = inv.get_player_slots2()
            inv_data["money"] = inv.money_score
            open("Data/PlayerData.json", "w").write(json.dumps(inv_data))

        player_data = json.load(open("Data/PlayerData.json", "r"))
        level = player_data["level"]
        world, save_inventary = generate_level(level)

        while world.running:
            world.update()
            world.draw()
            for event in world.events:
                if event.type == pygame.QUIT:
                    world.running = False
                    running = False

        if save_inventary:
            skills = world.player.skills.get_skills()
            player_data["player_inv"] = skills
        if world.state == "victory":
            player_data["money"] += world.income
            new_level = level_data["next_level"]
            if os.access(f"./Data/Levels/{new_level}.json", os.F_OK):
                player_data["level"] = new_level
        open("Data/PlayerData.json", "w").write(json.dumps(player_data))
    # clock.tick(fps)
pygame.quit()