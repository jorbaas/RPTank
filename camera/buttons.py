import pygame

class Button():
    def __init__(self, pos, size, text):
        self.pos = pos
        self.size = size
        self.text = text

        self.font = pygame.font.Font(None, 24)
        self.text_render = self.font.render(text, True, 'white')
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

        self.pressed = False


    def draw(self, screen):

        pygame.draw.rect(screen,'grey15', self.rect)
        screen.blit(self.text_render, (self.rect.x, self.rect.y))