import pygame
from settings import BLACK
from player import Player
from tanks import Bullet, calculateDistance, calculateAngle
import math
from camera import CameraGroup, HUD
from enemy import EnemySimple
from effects import Explosion

class RPTank():
    def __init__(self):
        self.camera_group = CameraGroup()

        self.player = Player(self, self.camera_group, (300,300))

        self.enemies = []
        enemy = EnemySimple(self, self.camera_group, (400, 400))
        self.enemies.append(enemy)

        self.hud = HUD(self.player)

        self.bullets = []
        self.explosions = []


        self.ground_mask = pygame.mask.from_surface(self.camera_group.ground_image)
        self.ground_overlay_mask = pygame.mask.from_surface(self.camera_group.ground_collision_image)




    def input(self):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        offset = self.offset_mouse_pos()

        mouse_pos_offset = ((mouse_pos[0] + offset[0]), (mouse_pos[1] + offset[1]))

        self.player.movement(keys, mouse_pos_offset, mouse_pos, mouse_pressed)
        self.player.update_mouse_sight(mouse_pos)



    def offset_mouse_pos(self):
        offset = (self.player.tank.rect.centerx - 800), (self.player.tank.rect.centery - 450)
        return offset

    def create_bullet(self, pos, target_pos, angle, name = 'AP_40', locked=True):
        bullet = Bullet(self.camera_group, self, pos, target_pos, angle, name, locked)
        if bullet.caliber == self.player.tank.cannon.caliber:
            self.bullets.append(bullet)



    def create_explosion(self, rect, size, type):
        explosion = Explosion(self.camera_group, rect, size)
        if type == 'AP_S':
            explosion.small_impact()
            self.explosions.append(explosion)
        if type == 'AP':
            explosion.impact()
            self.explosions.append(explosion)
        elif type == 'HE':
            explosion.he_small_explosion()
            self.explosions.append(explosion)

    def hit_angle_calculation(self, bullet, enemy, side):
        print(f'side hit: {side}')
        shot_angle = calculateAngle(self.player.tank.rect.center, bullet.rect.center)

        if side == 'front':
            hit_angle =   (shot_angle + (enemy.tank.hull.angle)) % 180
        elif side == 'right':
            hit_angle =   (shot_angle + (enemy.tank.hull.angle + 90)) % 180
        elif side == 'left':
            hit_angle =   (shot_angle + (enemy.tank.hull.angle - 90)) % 180
        elif side == 'rear':
            hit_angle =   (shot_angle + (enemy.tank.hull.angle - 180)) % 180

        if hit_angle - 90 >= 0:
            hit_angle = 90 - (hit_angle - 90)

        print(f'hit angle: {hit_angle}')
        return hit_angle


    def damage_calculation(self, bullet, enemy, side):
        angle = self.hit_angle_calculation(bullet, enemy, side)


        if angle <= bullet.values['ricochet_angle']:
            print('RICOCHET!')
            return

        if side == 'front':
            armor_thickness = enemy.tank.hull.front_armor
        if side in ['left', 'right']:
            armor_thickness = enemy.tank.hull.side_armor
        if side == 'rear':
            armor_thickness = enemy.tank.hull.rear_armor

        # Convert the cutting angle from degrees to radians
        angle_radians = math.radians(90-angle)

        # Calculate the effective thickness
        effective_thickness = armor_thickness / math.cos(angle_radians)
        print(armor_thickness, effective_thickness)

        if bullet.values['max_thickness'] >= effective_thickness:
            damage = bullet.damage - (effective_thickness - armor_thickness + ((armor_thickness/10)**2))
            damage = round(damage, 1)

            enemy.tank.health -= damage
            print(enemy.tank.health)
            self.camera_group.renderDamage(damage, bullet.rect.center)

        else:
            self.camera_group.renderDamage(0, bullet.rect.center)



    def collision(self):
        # collision with ground alpha and ground_collision_overlay
        pos = (self.player.tank.rect.x, self.player.tank.rect.y)
        if not self.ground_mask.overlap(self.player.tank.mask, pos) or self.ground_overlay_mask.overlap(self.player.tank.mask, pos):
            self.player.tank.handleCollision()
            self.player.tank.colliding = True
        else:
            self.player.tank.colliding = False

        # bullet collisions
        for bullet in self.bullets:
            pos = (bullet.rect.x, bullet.rect.y)
            # with enemies
            for enemy in self.enemies:
                pos = (bullet.rect.x - enemy.tank.rect.x, bullet.rect.y - enemy.tank.rect.y)
                if enemy.tank.front_mask.overlap(bullet.mask, pos):
                    self.damage_calculation(bullet, enemy, 'front')
                    bullet.create_explosion()
                    self.bullets.remove(bullet)
                    self.camera_group.remove(bullet)
                    break
                elif enemy.tank.right_mask.overlap(bullet.mask, pos):
                    self.damage_calculation(bullet, enemy, 'right')
                    bullet.create_explosion()
                    self.bullets.remove(bullet)
                    self.camera_group.remove(bullet)
                    break
                elif enemy.tank.left_mask.overlap(bullet.mask, pos):
                    self.damage_calculation(bullet, enemy, 'left')
                    bullet.create_explosion()
                    self.bullets.remove(bullet)
                    self.camera_group.remove(bullet)
                    break
                elif enemy.tank.rear_mask.overlap(bullet.mask, pos):
                    self.damage_calculation(bullet, enemy, 'rear')
                    bullet.create_explosion()
                    self.bullets.remove(bullet)
                    self.camera_group.remove(bullet)
                    break

            # with the world collision overlay
            if  self.ground_overlay_mask.overlap(bullet.mask, bullet.rect.center):
                # explosion = Explosion(self.camera_group, bullet.rect, 20)
                # explosion.small_impact()
                # self.explosions.append(explosion)
                bullet.create_explosion()
                self.bullets.remove(bullet)
                self.camera_group.remove(bullet)


    def sound_render(self):
        for enemy in self.enemies:
            d = calculateDistance(self.player.tank.rect, enemy.tank.rect)
            if d > 300:
                enemy.tank.engine.sound.set_volume(0)



    def update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for bullet in self.bullets:
            bullet.update()
            if not bullet.alive:
                bullet.create_explosion()
                self.bullets.remove(bullet)
                self.camera_group.remove(bullet)

        for explosion in self.explosions:
            explosion.update()

        self.collision()
        self.sound_render()
        self.hud.update()

    def draw(self, screen):
        screen.fill('blue')

        self.camera_group.custom_draw(self.player.tank)
        self.player.draw(screen)
        self.hud.draw(screen)

    def run(self, screen):
        self.input()
        self.update()
        self.draw(screen)