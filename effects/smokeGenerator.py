from .particle import SimpleParticle
import random

class Smoke():
    def __init__(self, pos, size, amount, angle, off_set, move_speed, fade_speed):

        self.pos = pos
        self.size = size
        self.amount = amount
        self.angle = angle
        self.off_set = off_set
        self.move_speed = move_speed
        self.fade_speed = fade_speed

        self.alive = True
        self.particles = []

        self.setup()


    def setup(self):

        for i in range(self.amount):
            random_fade_speed = self.fade_speed + (random.randint(0,300) / 10000)
            particle = SimpleParticle(self.pos, self.size, self.move_speed, random_fade_speed)
            self.particles.append(particle)


    def move_in_angle(self):

        for particle in self.particles:
            left_off_set = self.angle - self.off_set
            right_off_set = self.angle + self.off_set
            particle_angle = random.randint(int(left_off_set), int(right_off_set))
            particle.move_angle(particle_angle, self.move_speed)


    def update(self):

        for particle in self.particles:
            particle.color_fade()
            particle.deflate()

            if not particle.alive:
                self.alive = False
                self.particles.remove(particle)

            self.move_in_angle()


