from .cannon_types import all_cannons
import pygame

class Cannon():
    def __init__(self, cannon_name):
        self.cannon_values = all_cannons[cannon_name]
        self.name = self.cannon_values['name']

        self.caliber = self.cannon_values['caliber']
        self.size = self.cannon_values['size']
        self.mass = self.cannon_values['mass']
        self.shooting_speed = self.cannon_values['shooting_speed']

        self.sound = pygame.mixer.Sound(f"assets/sound/cannon/{self.cannon_values['sound']}.wav")