import pygame
from tanks import Tank
import math
import random
import copy
from tanks import *

class EnemySimple():
    def __init__(self, game, sprite_group, pos):

        self.tank = Tank(game, sprite_group, pos,'T34_hull', 'T34_turret', '40mm_cannon', 'T34_barrel', 'test_engine')
        self.mode = 'tank'
        self.tank.hull.angle = 0
        self.rand_move_loc = pygame.Rect(0, 0, 0, 0)
        self.last_rand_move_time = pygame.time.get_ticks() - 5000

        self.turning = False
        self.target_lock = True

    def random_movement(self):


        current_time = pygame.time.get_ticks()

        if current_time - self.last_rand_move_time >= (8000 / 1):
            self.rand_move_loc = (random.randint(0, 1080), random.randint(0, 900))
            self.rand_move_loc = pygame.Rect(self.rand_move_loc[0], self.rand_move_loc[1],0,0)

            self.last_rand_move_time = current_time

        self.rotate_to_loc(self.rand_move_loc)


        # moves only if there is no object infornt

        if not self.turning:
            self.tank.movement("UP")


    def rotate_to_loc(self, rect, rotation_speed=1):
        # Calculate the angle to rotate the turret to point at the player
        center = rect.center
        hull_center = copy.copy(self.tank.hull.rect.center)

        dx = center[0] - hull_center[0]
        dy = center[1] - hull_center[1]

        # Calculate the angle in degrees
        hull_angle = math.degrees(math.atan2(-dy, dx)) - 90

        # Gradually rotate the turret towards the target angle
        angle_difference = (hull_angle - self.tank.hull.angle) % 360

        if angle_difference > 180:
            angle_difference -= 360

        if angle_difference < -180:
            angle_difference += 360

        # Calculate the maximum rotation amount based on rotation_speed
          # Adjust this value for the desired rotation speed

        if abs(angle_difference) > rotation_speed:
            if angle_difference > 0:
                self.tank.hull.angle += rotation_speed
                self.tank.turret.angle += rotation_speed
                self.target_lock = False
                self.turning = True

            elif angle_difference < 0:
                self.tank.hull.angle -= rotation_speed
                self.tank.turret.angle -= rotation_speed
                self.target_lock = False
                self.turning = True

        elif not self.target_lock:

            self.target_lock = True
            self.turning = False

        self.tank.turret.calculate_turret_offset(self.tank.hull.rect, self.tank.hull.turret_offset, self.tank.hull.angle)

        self.tank.barrel.calculate_barrel_offset(self.tank.turret.rect, self.tank.turret.barrel_offset, self.tank.turret.angle)


    def move_to_player(self):
        if self.target_lock:

            self.tank.movement("UP")
        else:
            self.tank.movement("NONE")


    def look_at_player(self, player_rect, rotation_speed=1.0):
        # Calculate the angle to rotate the turret to point at the player
        player_center = player_rect.center
        turret_center = self.tank.turret.rect.center

        dx = player_center[0] - turret_center[0]
        dy = player_center[1] - turret_center[1]

        # Calculate the angle in degrees
        target_angle = math.degrees(math.atan2(-dy, dx)) -90

        # Gradually rotate the turret towards the target angle
        angle_difference = (target_angle - self.tank.turret.angle) % 360

        if angle_difference > 180:
            angle_difference -= 360

        if angle_difference < -180:
            angle_difference += 360

        # Calculate the maximum rotation amount based on rotation_speed
        max_rotation = rotation_speed  # Adjust this value for the desired rotation speed

        if abs(angle_difference) > max_rotation:
            if angle_difference > 0:
                self.tank.turret.angle += max_rotation
                self.target_lock = False
            else:
                self.turret_angle -= max_rotation
                self.target_lock = False
        elif not self.target_lock:
            self.turret_angle = target_angle
            self.target_lock = True


    def update(self):

        if self.tank.health >= 0:
            self.random_movement()
            self.tank.update()




