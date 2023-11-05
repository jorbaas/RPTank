import pygame
from .turret_types import all_turrets
from tanks.tankScripts import calculateAngleOffset



class Turret():
    def __init__(self, turret_name, pos):

        self.name = turret_name
        # get values
        self.turret_values = all_turrets[turret_name]
        armor_values = self.turret_values['armor_values']

        # armor
        self.turret_front_armor = armor_values[0]
        self.turret_side_armor = armor_values[1]
        self.turret_rear_armor = armor_values[2]

        self.size = self.turret_values['size']
        self.mass = self.turret_values['mass']
        self.name = turret_name
        self.image_name = self.turret_values['image_name']

        # movement
        self.angle = 0
        self.barrel_offset = self.turret_values['barrel_offset']

        self.image = pygame.image.load(f'assets/turret_images/{self.image_name}.png').convert_alpha()
        self.original_image = self.image.copy()

        self.rect = self.image.get_rect(center=pos)


    def calculate_turret_offset(self, rect, offset, angle):
        self.rect.center = calculateAngleOffset(rect, angle, -offset)

    def update(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)






