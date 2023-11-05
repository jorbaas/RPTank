from camera import Window
import pygame

class Status_window(Window):
    def __init__(self, tank, pos, size, name):


        self.tank = tank
        self.pos = pos
        self.rect = pygame.rect.Rect(pos[0], pos[1], size[0], size[1])
        self.border_rect = pygame.rect.Rect(pos[0], pos[1], size[0], 15)
        self.name = name
        self.font_size = 13
        self.font = pygame.font.Font(None, 14)

        self.active = False

        self.moving = False
        self.first_mouse_pos = ()

        self.buttons = []
        self.create_stats_text()
        self.create_tabs()

    def create_stats_text(self):
        hull = self.tank.hull.hull_values

        turret = self.tank.turret.turret_values
        barrel = self.tank.barrel.barrel_values
        engine = self.tank.engine.engine_values

        armor_values = hull['armor_values']
        self.hull_text = f'Hull Armor\n front: {armor_values[0]}\n sides: {armor_values[1]}\n rear: {armor_values[2]}'

    def create_tabs(self):
        tab_names = ('overv.', 'hull', 'turret', 'engine')
        x_offset = 0
        for name in tab_names:
            self.create_button((self.pos[0] + x_offset, self.pos[1] + 15), (50,30), name)
            x_offset += 50



    def draw_text(self, screen):
        # screen.blit(self.hull_text, (self.rect.x + 50, self.rect.y + 100))
        self.print_text(screen, self.hull_text, (self.rect.x + 50, self.rect.y + 100))

