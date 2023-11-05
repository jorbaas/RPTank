from .engine_types import all_engines
import pygame

class Engine():
    def __init__(self, engine_name):

        self.engine_values = all_engines[engine_name]

        self.name = self.engine_values['name']

        self.power = self.engine_values['power']
        self.max_speed = self.engine_values['max_speed']
        self.size = self.engine_values['size']

        self.mass = self.engine_values['mass']

        self.sound = pygame.mixer.Sound('assets/sound/engine/engine_sound.wav')


        self.sound.set_volume(0.3)
        self.sound.play(-1)






