import pygame
from mode import RPTank
from settings import *


class UserInterface():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('RPTank')


        self.active_mode = 'game'
        self.game_mode = RPTank()


        self.clock = pygame.time.Clock()
        self.running = True


    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            if self.active_mode == 'game':
                 self.game_mode.run(self.screen)

            # Update display
            pygame.display.update()
            # print(self.clock.get_fps())
            self.clock.tick(60)


user_interface = UserInterface()
user_interface.run()

