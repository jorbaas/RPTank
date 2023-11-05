import pygame
from .barrel_types import all_barrels
from tanks.tankScripts import calculateAngleOffset



class Barrel():
    def __init__(self, turret, barrel_name, pos):

        self.barrel_values = all_barrels[barrel_name]

        self.turret = turret
        self.caliber = self.barrel_values['caliber']
        self.mass = self.barrel_values['mass']
        self.name = self.barrel_values['image_name']
        self.muzzle_break = self.barrel_values['muzzle_break']

        # movement
        self.angle = 0
        self.fire_offset = self.barrel_values['fire_offset']

        self.image = pygame.image.load(f'assets/barrel_images/{self.name}.png').convert_alpha()
        self.original_image = self.image.copy()

        self.rect = self.image.get_rect(center=pos)


    def calculate_barrel_offset(self, rect, offset, angle):
        self.rect.center = calculateAngleOffset(rect, angle, -offset)


    def update(self):
        self.angle = self.turret.angle

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)


