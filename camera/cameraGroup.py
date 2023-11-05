import pygame
from .damageText import DamageRender


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_screen = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()
        self.half_w = self.display_screen.get_size()[0] // 2
        self.half_h = self.display_screen.get_size()[1] // 2

        self.damage_renders = []

        self.ground_image = pygame.image.load('assets/maps/map1.png').convert_alpha()
        self.ground_rect = self.ground_image.get_rect(topleft=(0, 0))

        self.ground_overlay_image = pygame.image.load('assets/maps/map1_overlay.png').convert_alpha()
        self.ground_collision_image = pygame.image.load('assets/maps/map1_collision.png').convert_alpha()

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h


    def renderDamage(self, damage, pos):
        text_render = DamageRender(damage, pos)
        self.damage_renders.append(text_render)



    def custom_draw(self, target):

        self.center_target_camera(target)

        ground_offset = self.ground_rect.topleft - self.offset
        self.display_screen.blit(self.ground_image, ground_offset)

        for sprite in self.sprites():
            if sprite.name == 'tank':
                offset_hull = sprite.hull.rect.topleft - self.offset
                offset_turret = sprite.turret.rect.topleft - self.offset
                offset_barrel = sprite.barrel.rect.topleft - self.offset

                self.display_screen.blit(sprite.hull.image, offset_hull)
                self.display_screen.blit(sprite.turret.image, offset_turret)
                self.display_screen.blit(sprite.barrel.image, offset_barrel)

                for particle in sprite.particles:
                    for p in particle.particles:
                        pygame.draw.circle(self.display_screen, p.color, p.center - self.offset, p.radius)

                for flashes in sprite.flashes:
                    for flash in flashes.flash_particles:
                        offset_explosion = (flash[0] - self.offset[0], flash[1] - self.offset[1])

                        try:
                            x, y, radius, _ = flash

                            pygame.draw.circle(self.display_screen, 'yellow', offset_explosion, radius)
                        except:
                            break

            elif sprite.name == 'person':
                if sprite.active:
                    offset_person = sprite.rect.center - self.offset
                    self.display_screen.blit(sprite.image, offset_person)

            elif sprite.name == 'bullet':
                offset_bullet = sprite.rect.center - self.offset
                self.display_screen.blit(sprite.image, offset_bullet)
            # self.display_screen.blit(sprite.sight_image, sprite.sight_rect.center)

            elif sprite.name == 'explosion':

                offset_explosion = (sprite.x - self.offset[0], sprite.y - self.offset[1])
                for flash in sprite.flashes:
                    try:
                        x, y, radius, _ = flash
                        pygame.draw.circle(self.display_screen, 'yellow', offset_explosion, radius)
                    except:
                        break

                for smoke in sprite.particles:
                    for p in smoke.particles:

                        try:
                            pygame.draw.circle(self.display_screen, p.color, p.center - self.offset, p.radius)
                        except:
                            break


        self.display_screen.blit(self.ground_overlay_image, ground_offset)

        for text_render in self.damage_renders:
            text_render.pos = text_render.original_pos - self.offset
            text_render.update()
            text_render.draw(self.display_screen)

            if not text_render.alive:
                self.damage_renders.remove(text_render)

