import pygame

class Person(pygame.sprite.Sprite):
    def __init__(self, sprite_group):
        super().__init__(sprite_group)

        self.name = 'person'

        self.direction = pygame.math.Vector2()

        self.image = pygame.image.load('assets/persons/person.png').convert_alpha()
        self.rect = self.image.get_rect()

        self.active = False

    def movement(self, direction):
        keys = pygame.key.get_pressed()

        # movement
        if direction == "UP":
            self.direction.y = -1
        elif direction == "DOWN":
            self.direction.y = 1
        else:
            self.direction.y = 0

        if direction == "LEFT":
            self.direction.x = -1
        elif direction == "RIGHT":
            self.direction.x = 1
        else:
            self.direction.x = 0

        # interact/talk
        if keys[pygame.K_SPACE]:
            print('helle.')

    def move(self, speed):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        self.rect.center += self.direction * speed

    def update(self):
        self.move(1)

