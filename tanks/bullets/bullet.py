import pygame
import math
from .bullet_types import all_ammo
from effects import Explosion

class Bullet(pygame.sprite.Sprite):
    def __init__(self, sprite_group, game, pos, target_pos, angle, bullet_name, locked):
        super().__init__(sprite_group)

        self.game = game
        # location of where the bullet needs to travel to
        self.target_pos = target_pos
        self.angle = angle


        self.values = all_ammo[bullet_name]
        self.bullet_name = bullet_name
        self.caliber = self.values['caliber']

        self.name = 'bullet'
        self.type = 'ammo'

        self.image = pygame.image.load(f'assets/shells/{self.values["image_name"]}.png').convert_alpha()  # Adjust the size of the bullet image as needed

        self.image = pygame.transform.rotate(self.image, self.angle)  # Rotate the image
        self.rect = self.image.get_rect(center=(pos[0], pos[1]))
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = 10  # Adjust the speed of the bullet as needed
        self.damage = self.values['damage']

        self.alive = True
        self.locked = locked



    def create_explosion(self):
        if self.bullet_name == 'AP_40':
            self.game.create_explosion(self.rect, 15, 'AP_S')
        if self.bullet_name == 'HE_40':
            self.game.create_explosion(self.rect, 100, 'HE')
        if self.bullet_name == 'AP_88':
            self.game.create_explosion(self.rect, 20, 'AP')





    def update(self):

        if self.locked:
            dx = self.target_pos[0] - self.rect.centerx
            dy = self.target_pos[1] - self.rect.centery
            self.angle = math.degrees(math.atan2(dy, dx))

            # Update the bullet's velocity based on the calculated angle
            self.rect.x += self.speed * math.cos(math.radians(self.angle))
            self.rect.y += self.speed * math.sin(math.radians(self.angle))

            # Check if the bullet has reached the target position
            if math.hypot(dx, dy) < self.speed:
                self.alive = False

        else:
            dx = self.target_pos[0] - self.rect.centerx
            dy = self.target_pos[1] - self.rect.centery
            # Update the bullet's velocity based on the calculated angle
            self.rect.x -= self.speed * math.sin(math.radians(self.angle))
            self.rect.y -= self.speed * math.cos(math.radians(self.angle))

            # Check if the bullet has reached the target position
            if math.hypot(dx, dy) < self.speed:
                self.alive = False



