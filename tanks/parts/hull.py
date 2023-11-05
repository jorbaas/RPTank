import pygame
from .hull_types import all_hulls



class Hull():
    def __init__(self, hull_name, pos, angle=0):

        self.name = hull_name
        
        self.hull_values = all_hulls[hull_name]
        armor_values = self.hull_values['armor_values']

        # armor
        self.front_armor = armor_values[0]
        self.side_armor = armor_values[1]
        self.rear_armor = armor_values[2]

        # movement
        self.angle = angle
        self.turret_offset = self.hull_values['turret_offset']
        self.exhaust_offset = self.hull_values['exhaust_offset']

        self.hull_size = self.hull_values['size']
        self.fuel_tank_size = self.hull_values['fuel_size']
        self.fuel_amount = 100
        self.mass = self.hull_values['mass']

        self.ammo_space = self.hull_values['ammo_space']
        self.ammo_list = []

        self.image_name = self.hull_values['image_name']

        self.image = pygame.image.load(f'assets/hull_images/{self.image_name}.png').convert_alpha()
        # self.image = pygame.transform.scale(self.image, (86, 86))
        self.original_image = self.image.copy()

        self.image_hitbox_front = pygame.image.load(f'assets/hull_images/{self.image_name}_FHB.png').convert_alpha()
        self.original_image_hitbox_front = self.image_hitbox_front.copy()
        self.image_hitbox_right = pygame.image.load(f'assets/hull_images/{self.image_name}_RHB.png').convert_alpha()
        self.original_image_hitbox_right = self.image_hitbox_right.copy()
        self.image_hitbox_left = pygame.image.load(f'assets/hull_images/{self.image_name}_LHB.png').convert_alpha()
        self.original_image_hitbox_left = self.image_hitbox_left.copy()
        self.image_hitbox_rear = pygame.image.load(f'assets/hull_images/{self.image_name}_BHB.png').convert_alpha()
        self.original_image_hitbox_rear = self.image_hitbox_rear.copy()

        self.rect = self.image.get_rect(center=pos)
        self.rect_hitbox_front = self.image_hitbox_front.get_rect(center=pos)


    def update(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.image_hitbox_front = pygame.transform.rotate(self.original_image_hitbox_front, self.angle)
        self.image_hitbox_right = pygame.transform.rotate(self.original_image_hitbox_right, self.angle)
        self.image_hitbox_left = pygame.transform.rotate(self.original_image_hitbox_left, self.angle)
        self.image_hitbox_rear = pygame.transform.rotate(self.original_image_hitbox_rear, self.angle)

        self.rect = self.image.get_rect(center=self.rect.center)



