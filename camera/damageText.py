import pygame


class DamageRender():
    def __init__(self, damage, pos):
        self.text = damage
        self.pos = pos
        self.original_pos = pos
        self.font = pygame.font.Font(None, 14)
        self.alpha = 255

        self.render_text()

        self.timer = 2000
        self.start_time = pygame.time.get_ticks()

        self.alive = True




    def render_text(self):
        self.text_render = self.font.render(str(self.text), True, 'white').convert_alpha()
        self.text_outline = self.font.render(str(self.text), True, 'black').convert_alpha()


    def move_text(self):
        self.original_pos = (self.original_pos[0], self.original_pos[1] - 0.5)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time <= self.start_time + self.timer:
            self.move_text()
            self.text_render.set_alpha(self.alpha)
            self.alpha -= 2

        else:
            self.alive = False


    def draw(self, screen):
        outline_thickness = 2  # Adjust this to change the outline thickness
        # Draw the outline first
        for dx in range(-outline_thickness, outline_thickness + 1):
            for dy in range(-outline_thickness, outline_thickness + 1):
                if dx != 0 or dy != 0:
                    screen.blit(self.text_outline, (self.pos[0] + dx, self.pos[1] + dy))

        # Draw the actual text on top
        screen.blit(self.text_render, self.pos)
