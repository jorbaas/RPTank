import pygame
from .smokeGenerator import Smoke
import math
import random



class Flash():
    def __init__(self, x, y, size):
        self.x = x
        self.y = y

        self.flash_particles = []

        self.flash_color = 'yellow'
        self.flash_max_radius = size
        self.flash_min_radius = 2
        self.flash_duration = 400  # milliseconds
        self.flash_start_time = 0

        self.flash_particles.append([self.x, self.y, self.flash_max_radius, self.flash_duration])


    def create_flash(self):
        self.flash_particles.append([self.x, self.y, self.flash_max_radius, self.flash_duration])


    def update(self):
        # Update the position, size, and lifetime of each smoke particle
        for flash_particle in self.flash_particles:

            flash_particle[2] -= 2  # Decrease the radius over time
            flash_particle[3] -= 1  # Decrease the lifetime over time

        # Remove smoke particles that have faded away
        self.flash_particles[:] = [sp for sp in self.flash_particles if sp[3] > 0]


    def draw(self, screen):
        # Draw each smoke particle as a gray circle
        for flash_particle in self.flash_particles:
            x, y, radius, _ = flash_particle
            pygame.draw.circle(screen, 'yellow', (x, y), radius)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, sprite_group, pos, size):
        super().__init__(sprite_group)
        self.center = pos
        self.x = pos[0]
        self.y = pos[1]
        self.size = size
        self.rect = pygame.rect.Rect(self.y, self.y ,0 ,0)

        self.particles = []
        self.flashes = []

        self.name = 'explosion'

        self.shockwave_start_time = 0
        self.shockwave_radius = 0

        self.sound = pygame.mixer.Sound("assets/sound/cannon/explosion1.mp3")

    def small_impact(self):
        self.particles.append(Smoke(self.center, 2, 10, 0, 180, 0.8, 0.04))
        self.flashes.append([self.x, self.y, self.size, 2000])
        self.sound.play()

    def impact(self):
        self.particles.append(Smoke(self.center, 3, 20, 0, 180, 0.8, 0.04))
        self.flashes.append([self.x, self.y, self.size, 4000])
        self.sound.play()

    def he_small_explosion(self):
        circle_radius = 25
        circle_radius2 = 50
        num_positions = 60

        for n in range(num_positions):
            angle = random.uniform(0, 2 * math.pi)  # Random angle in radians
            size = random.randint(2, 4)
            x = self.center[0] + circle_radius * math.cos(angle)
            y = self.center[1] + circle_radius * math.sin(angle)
            pos = (x,y)
            self.particles.append(Smoke(pos, size, 1, 90, 180, 0.8, 0.04))

            # second smoke ring
            if (n % 2) == 0:
                offset = random.randint(-15, 15)
                x = self.center[0] + circle_radius2 * math.cos(angle)
                y = self.center[1] + circle_radius2 * math.sin(angle)
                pos = (x + offset, y + offset)
                self.particles.append(Smoke(pos, 2, 1, 90, 90, 0.2, 0.01))

            self.sound.play()

        self.flashes.append([self.x, self.y, circle_radius, 2000])

    def update(self):
        for particle in self.particles:
            particle.update()
            if not particle.alive:
                self.particles.remove(particle)

        for flash in self.flashes:
            try:
                flash[2] -= 3  # Decrease the radius over time
                flash[3] -= 0.1  # Decrease the lifetime over time

                # Remove smoke particles that have faded away
                self.flashes[:] = [sp for sp in self.flashes if sp[3] > 0]

            except:
                break


    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
        for flash in self.flashes:
            flash.draw(screen)

