import random

import pygame
import math
import copy

class SimpleParticle():
    def __init__(self, center, radius, move_speed, fade_speed):

        self.center = center
        self.x = center[0]
        self.y = center[1]
        self.radius = radius

        self.angle = 0
        self.leaf_moved = False
        self.moves_stepped = 0
        self.original_center = copy.copy(center)
        self.color = pygame.Color(f'grey1')
        self.start_radius = copy.copy(radius)

        self.move_speed = move_speed
        self.fade_speed = fade_speed

        self.alive = True

    def move_angle(self, angle, move_speed):
        movement_angle = math.radians(angle)
        move_x = move_speed * math.sin(movement_angle)
        move_y = move_speed * math.cos(movement_angle)  # Negative because pygame's y-axis is inverted

        fade_factor = self.radius / self.start_radius

        # Update the tank's position

        self.x -= move_x * fade_factor
        self.y -= move_y * fade_factor
        self.center = (self.x, self.y)


    def deflate(self):
        self.radius -= self.fade_speed
        if self.radius <= 0:
            self.alive = False


    def color_fade(self):

        fade_factor = self.radius / self.start_radius
        grey_num = int(20 / fade_factor)

        if grey_num > 60:
            grey_num = 60
        if grey_num < 0:
            grey_num = 0
        self.color = pygame.Color(f'grey{grey_num}')

