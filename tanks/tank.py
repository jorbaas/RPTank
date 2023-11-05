from .parts import *
from .tankScripts import *
from effects import Smoke, Flash
import pygame
from player.items import Inventory, Item


class Tank(pygame.sprite.Sprite):
    def __init__(self, game, sprite_group, pos, hull_name, turret_name, cannon_name, barrel_name, engine_name):
        super().__init__(sprite_group)
        # instance of game to call methods
        self.game = game
        # name for the sprite
        self.name = 'tank'

        # tank is build of these objects
        self.turret = Turret(turret_name, pos)
        self.barrel = Barrel(self.turret, barrel_name, pos)
        self.hull = Hull(hull_name, pos)
        self.engine = Engine(engine_name)
        self.cannon = Cannon(cannon_name)

        self.equipped_parts = [Item(self.barrel.name, 'barrel'),
                               Item(self.turret.name, 'turret'),
                               Item(self.hull.name, 'hull'),
                               Item(self.engine.name, 'engine'),
                               Item(self.cannon.name, 'cannon')]


        # set the turret and barrel offset
        self.turret.calculate_turret_offset(self.hull.rect, self.hull.turret_offset, self.hull.angle)
        self.barrel.calculate_barrel_offset(self.turret.rect, self.turret.barrel_offset, self.turret.angle)

        # total mass of the tanks
        self.mass = self.hull.mass + self.turret.mass + self.barrel.mass + self.engine.mass + self.cannon.mass

        self.health = 100
        self.acceleration = calculateAcceleration(self.mass, self.engine.power)
        self.speed = 0
        self.angle = self.hull.angle

        # for smoke effects etc
        self.particles = []
        self.flashes = []


        # ammo stuff
        self.allowed_caliber = self.cannon.caliber

        self.ammo_space = self.hull.ammo_space * (40 / self.cannon.caliber) # 40mm is standard for normal ammo_space
        self.ammo_inventory = Inventory()
        self.ammo_inventory.add_item(Item('AP_20', 'ammo'), 100)
        self.ammo_inventory.add_item(Item('AP_40', 'ammo'), 100)
        # self.ammo_inventory.add_item(Item('HE_40', 'ammo'), 100)


        self.ammo_order = []
        for bullet in self.ammo_inventory.ammo:
            bullet = self.ammo_inventory.ammo[bullet]
            self.ammo_order.append(bullet[0].name)

            if bullet[0].values['caliber'] == self.allowed_caliber:
                pass



        # self.active_ammo = next(iter(self.ammo_order))

        self.active_ammo = self.ammo_order[0]
        self.aim_loc = (0,0)

        self.shooting_speed = self.cannon.shooting_speed * 1000
        self.last_shot_time = pygame.time.get_ticks() - self.shooting_speed

        self.rect = self.hull.rect
        self.pos = pygame.Vector2(self.rect.center)

        self.mask = pygame.mask.from_surface(self.hull.image)
        self.front_mask = pygame.mask.from_surface(self.hull.image_hitbox_front)
        self.right_mask = pygame.mask.from_surface(self.hull.image_hitbox_right)
        self.left_mask = pygame.mask.from_surface(self.hull.image_hitbox_left)
        self.rear_mask = pygame.mask.from_surface(self.hull.image_hitbox_rear)

        self.target_lock = True
        self.colliding = False
        self.player = False


    # def calculate_maxspeed(self):
    #     max_speed = self.engine.max_speed


    def movement(self, direction):
        max_speed = self.engine.max_speed


        if direction == "R_UP":
            if self.speed <= max_speed:
                self.speed += self.acceleration
            self.hull.angle -= 1
            self.turret.angle -= 1
            self.turret.calculate_turret_offset(self.hull.rect, self.hull.turret_offset, self.hull.angle)
            self.barrel.calculate_barrel_offset(self.turret.rect, self.turret.barrel_offset, self.turret.angle)

        elif direction == "L_UP":
            if self.speed <= max_speed:
                self.speed += self.acceleration

            self.hull.angle += 1
            self.turret.angle += 1
            self.turret.calculate_turret_offset(self.hull.rect, self.hull.turret_offset, self.hull.angle)
            self.barrel.calculate_barrel_offset(self.turret.rect, self.turret.barrel_offset, self.turret.angle)

        elif direction == "UP":
            if self.speed <= max_speed:
                self.speed += self.acceleration

        elif direction == "DOWN":
            if self.speed >= -max_speed:
                self.speed -= self.acceleration

        elif direction == "RIGHT":
            self.speed = calcualteSpeed(self.speed, self.acceleration)
            self.hull.angle -= 1
            self.turret.angle -= 1
            self.turret.calculate_turret_offset(self.hull.rect, self.hull.turret_offset, self.hull.angle)
            self.barrel.calculate_barrel_offset(self.turret.rect, self.turret.barrel_offset, self.turret.angle)

        elif direction == "LEFT":
            self.speed = calcualteSpeed(self.speed, self.acceleration)
            self.hull.angle += 1
            self.turret.angle += 1
            self.turret.calculate_turret_offset(self.hull.rect, self.hull.turret_offset, self.hull.angle)
            self.barrel.calculate_barrel_offset(self.turret.rect, self.turret.barrel_offset, self.turret.angle)

        if direction == "NONE":
            if self.speed > 0:
                self.speed = max(0, self.speed - self.acceleration)
            elif self.speed < 0:
                self.speed = max(0, self.speed - self.acceleration)


    def turret_movement(self, mouse_pos, rotation_speed=1):
        # Calculate the angle to rotate the turret to point at the player
        turret_center = self.turret.rect.center

        dx = mouse_pos[0] - turret_center[0]
        dy = mouse_pos[1] - turret_center[1]

        """ below attempt at setting aim for loc for the gun"""
        # distance = math.sqrt(dx * dx + dy * dy)
        #
        # direction_vector = pygame.math.Vector2(0, 1)
        # target_angle = math.degrees(math.atan2(-dy, dx)) - 90
        #
        # rotated_vector = direction_vector.rotate(-target_angle)
        # self.aim_loc = self.turret.rect.center + rotated_vector * distance
        self.aim_loc = mouse_pos

        # Calculate the angle in degrees
        target_angle = math.degrees(math.atan2(-dy, dx)) - 90

        # Gradually rotate the turret towards the target angle
        angle_difference = (target_angle - self.turret.angle) % 360

        if angle_difference > 180:
            angle_difference -= 360

        if angle_difference < -180:
            angle_difference += 360

        # Calculate the maximum rotation amount based on rotation_speed
        max_rotation = rotation_speed  # Adjust this value for the desired rotation speed

        if abs(angle_difference) > max_rotation:
            if angle_difference > 0:
                self.turret.angle += max_rotation
                self.target_lock = False
            else:
                self.turret.angle -= max_rotation
                self.target_lock = False
        elif not self.target_lock:
            self.turret.angle = target_angle
            self.target_lock = True

        self.barrel.calculate_barrel_offset(self.turret.rect, self.turret.barrel_offset, self.turret.angle)

    def switch_ammo(self, num):
        max = len(self.ammo_order)
        if num <= max:
            self.active_ammo = self.ammo_order[num-1]

    def reset_active_ammo(self):
        self.active_ammo = self.ammo_order[0]

    def set_ammo_order(self):
        self.ammo_order = []
        for bullet in self.ammo_inventory.ammo:
            bullet = self.ammo_inventory.ammo[bullet]
            self.ammo_order.append(bullet[0].name)
            if bullet[0].values['caliber'] == self.allowed_caliber:
                pass

    def switch_part(self, part_name, type):
        pos = (self.rect.centerx, self.rect.centery)
        if type == 'hull':
            self.hull = Hull(part_name, pos, self.angle)
        elif type == 'turret':
            self.turret = Turret(part_name, pos)
            self.barrel.turret = self.turret
        elif type == 'barrel':
            self.barrel = Barrel(self.turret, part_name, pos)

        elif type == 'cannon':
            self.cannon = Cannon(part_name)
            self.shooting_speed = self.cannon.shooting_speed * 1000
            self.allowed_caliber = self.cannon.caliber

        elif type == 'engine':
            self.engine = Engine(part_name)

        self.equipped_parts = [Item(self.barrel.name, 'barrel'),
                               Item(self.turret.name, 'turret'),
                               Item(self.hull.name, 'hull'),
                               Item(self.engine.name, 'engine'),
                               Item(self.cannon.name, 'cannon')]

        self.mass = self.hull.mass + self.turret.mass + self.barrel.mass + self.engine.mass + self.cannon.mass
        self.acceleration = calculateAcceleration(self.mass, self.engine.power)




    def muzzle_flash(self):
        start_pos = calculateAngleOffset(self.barrel.rect, self.turret.angle, self.barrel.fire_offset)
        self.flashes.append(Flash(start_pos[0], start_pos[1], 10))

        particle = Smoke((start_pos[0], start_pos[1]), 2, 30, self.turret.angle, 160, 0.2, 0.03)
        self.particles.append(particle)



        if self.barrel.muzzle_break == 1:

            particle2 = Smoke((start_pos[0], start_pos[1]), 2, 10, self.turret.angle + 90, 120, 0.2,
                              0.025)
            particle3 = Smoke((start_pos[0], start_pos[1]), 2, 10, self.turret.angle - 90, 120, 0.2,
                              0.025)
            self.particles.append(particle2)
            self.particles.append(particle3)


    def shoot_main_gun(self):

        if len(self.ammo_inventory.ammo) > 0:
            if self.ammo_inventory.ammo[self.active_ammo][1] > 0:


                current_time = pygame.time.get_ticks()
                if current_time - self.last_shot_time >= self.shooting_speed:

                    start_pos = calculateAngleOffset(self.barrel.rect, self.turret.angle, self.barrel.fire_offset)

                    if self.target_lock:
                        self.game.create_bullet(start_pos, self.aim_loc, self.turret.angle, self.active_ammo, locked=True)
                    else:
                        self.game.create_bullet(start_pos, self.aim_loc, self.turret.angle, self.active_ammo, locked=False)



                    self.last_shot_time = current_time

                    self.recoil = True

                    self.muzzle_flash()

                    self.cannon.sound.play()

                    # self.gun_smoke(self.turret_angle)


                    # self.ammo[self.active_ammo] -= 1
                    self.ammo_inventory.remove_item(Item(self.active_ammo, 'ammo'), 1)


    def exhaust(self, size, dis_speed):
        pos = calculateAngleOffset(self.hull.rect, self.hull.angle, self.hull.exhaust_offset)
        particle = Smoke(pos, size, 1, 90, 100, 1, dis_speed)
        self.particles.append(particle)


    def handleCollision(self):
        if self.speed > 0:
            calculateMovement(-1, self.hull.angle, self.hull.rect, self.turret.rect, self.barrel.rect)
        elif self.speed <= 0:
            calculateMovement(1, self.hull.angle, self.hull.rect, self.turret.rect, self.barrel.rect)
        self.speed = 0


    def update(self):
        if not self.colliding:
            calculateMovement(self.speed, self.hull.angle, self.hull.rect, self.turret.rect, self.barrel.rect)
        self.hull.fuel_amount = calculate_fuel(self.hull.fuel_amount, self.mass, self.engine.power, self.speed)

        # sets the exhaust
        if self.speed > 0 or self.speed < 0:
            self.exhaust(4, 0.05)
        else:
            self.exhaust(2, 0.0045)

        for particle in self.particles:
            particle.update()

        for flash in self.flashes:
            flash.update()

        self.rect = self.hull.rect
        self.pos = pygame.Vector2(self.rect.center)
        self.angle = self.hull.angle

        # update parts
        self.hull.update()
        self.turret.update()
        self.barrel.update()

        self.tank_mask = pygame.mask.from_surface(self.hull.image)
        self.front_mask = pygame.mask.from_surface(self.hull.image_hitbox_front)
        self.right_mask = pygame.mask.from_surface(self.hull.image_hitbox_right)
        self.left_mask = pygame.mask.from_surface(self.hull.image_hitbox_left)
        self.rear_mask = pygame.mask.from_surface(self.hull.image_hitbox_rear)








