import pygame


class TextBox():
    def __init__(self, pos, item_dict):
        self.pos = pos
        self.item_dict = item_dict

        self.font_size = 16
        self.font = pygame.font.Font(None, self.font_size)

        h = (self.font_size) * len(self.item_dict)
        w = 96
        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], h, w)

        self.text_renders = []
        self.text_pos = ()
        self.makeTextRender()

        self.active = False


    def makeTextRender(self):
        y = self.pos[1]
        x = self.pos[0] + 2

        if self.item_dict['type'] == 'hull':
            name = self.font.render(self.item_dict['name'], True, 'white')
            mass = self.font.render('mass: ' + str(self.item_dict['mass']), True, 'white')
            armor = self.font.render("armor f, s ,r: " + ', '.join(map(str, self.item_dict['armor_values'])), True, 'white')
            ammo_space = self.font.render('max ammo: ' + str(self.item_dict['ammo_space']), True, 'white')
            self.text_pos = (x, y)
            self.text_renders.append([name, mass, armor, ammo_space])

        elif self.item_dict['type'] == 'turret':
            name = self.font.render(self.item_dict['name'], True, 'white')
            mass = self.font.render('mass: ' + str(self.item_dict['mass']), True, 'white')
            armor = self.font.render("armor f, s ,r: " + ', '.join(map(str, self.item_dict['armor_values'])), True, 'white')
            self.text_pos = (x, y)
            self.text_renders.append([name, mass, armor])

        elif self.item_dict['type'] == 'cannon':
            name = self.font.render(self.item_dict['name'], True, 'white')
            mass = self.font.render('mass: ' + str(self.item_dict['mass']), True, 'white')
            caliber = self.font.render('caliber: ' + (str(self.item_dict['caliber'])), True, 'white')
            self.text_pos = (x, y)
            self.text_renders.append([name, mass, caliber])

        elif self.item_dict['type'] == 'barrel':
            name = self.font.render(self.item_dict['name'], True, 'white')
            mass = self.font.render('mass: ' + str(self.item_dict['mass']), True, 'white')
            caliber = self.font.render('caliber: ' + (str(self.item_dict['caliber'])), True, 'white')
            self.text_pos = (x, y)
            self.text_renders.append([name, mass, caliber])

        elif self.item_dict['type'] == 'engine':
            name = self.font.render(self.item_dict['name'], True, 'white')
            mass = self.font.render('mass: ' + str(self.item_dict['mass']), True, 'white')
            power = self.font.render('power: ' + (str(self.item_dict['power'])), True, 'white')
            max_speed = self.font.render('max speed: ' + (str(self.item_dict['max_speed'])), True, 'white')
            self.text_pos = (x, y)
            self.text_renders.append([name, mass, power, max_speed])

        elif self.item_dict['type'] == 'ammo':
            name = self.font.render(self.item_dict['name'], True, 'white')
            caliber = self.font.render('caliber: ' + (str(self.item_dict['caliber'])), True, 'white')
            damage = self.font.render('damage: ' + (str(self.item_dict['damage'])), True, 'white')
            max_pen = self.font.render('max pen: ' + (str(self.item_dict['max_thickness'])), True, 'white')
            ricochet_angle = self.font.render('ricochet <: ' + (str(self.item_dict['ricochet_angle'])), True, 'white')
            self.text_pos = (x, y)
            self.text_renders.append([name, caliber, damage, max_pen, ricochet_angle])


    def draw(self, screen):

        if self.active:
            pygame.draw.rect(screen, 'grey10', self.rect)
            x = self.text_pos[0]
            y = self.text_pos[1]
            for text_render in self.text_renders:

                for text in text_render:
                    y += self.font_size
                    screen.blit(text, (x, y))









