import pygame
from Classes.Starship import *


class Player:
    def __init__(self):
        self.ship = Starship(20, 500, "Assets/Images/Ship1.png", 38, 20, 1000, 35, 18)
        self.camera = None

    def control(self, events):
        for event in events:
            if event.type == pygame.K_d:
                self.ship.set_acceleration(x=1)
            if event.type == pygame.K_w:
                self.ship.set_acceleration(y=-1)
            if event.type == pygame.K_a:
                self.ship.set_acceleration(x=-1)
            if event.type == pygame.K_s:
                self.ship.set_acceleration(y=1)

    def get_info_for_drawing(self):
        return self.ship.info_for_drawing()
