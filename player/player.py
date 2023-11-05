import pygame
from tanks import Tank
from .person import Person
from camera import Window
from .statusWindow import Status_window
from .inventory_window import Inventory_window
from .items import Item, Inventory




class Player():
    def __init__(self, game, sprite_group, pos):

        # self.tank = Tank(game, sprite_group, pos,'panser2_hull', 'panser2_turret', 'panser2_cannon', 'panser2_barrel', 'test_engine_2')
        self.tank = Tank(game, sprite_group, pos,'T34_hull', 'panser2_turret', '40mm_cannon', 'T34_barrel', 'test_engine_2')

        self.person = Person(sprite_group)

        self.mode = 'tank'

        self.click_time = 100
        self.last_click_time = pygame.time.get_ticks() - self.click_time


        self.inventory = Inventory()
        self.inventory.add_item(Item('T34_hull', 'hull'))
        self.inventory.add_item(Item('T34_turret', 'turret'))
        self.inventory.add_item(Item('panser2_hull', 'hull'))
        self.inventory.add_item(Item('panser2_barrel', 'barrel'))
        self.inventory.add_item(Item('20mm_cannon', 'cannon'))
        self.inventory.add_item(Item('test_engine', 'engine'))
        self.inventory.add_item(Item('tiger1_hull', 'hull'))
        self.inventory.add_item(Item('tiger1_turret', 'turret'))
        self.inventory.add_item(Item('tiger1_barrel', 'barrel'))
        self.inventory.add_item(Item('88mm_cannon', 'cannon'))
        self.inventory.add_item(Item('AP_40', 'ammo'), 100)
        self.inventory.add_item(Item('HE_40', 'ammo'), 100)
        self.inventory.add_item(Item('AP_88', 'ammo'), 100)

        self.status_window = Status_window(self.tank, (100, 100), (200, 300), 'status')
        self.inventory_window = Inventory_window(self, (500, 100), (400, 300), 'inv')

        self.sight_image = pygame.image.load(f'C:\\Users\\jorba\\PycharmProjects\\RPTank\\assets\\sights\\sight2.png').convert_alpha()
        self.sight_rect = self.sight_image.get_rect(center=(0,0))


    def movement(self, keys, mouse_pos_offset, mouse_pos, mouse_pressed):

        if self.mode == 'tank':
            if keys[pygame.K_d] and keys[pygame.K_w]:
                self.tank.movement("R_UP")
            elif keys[pygame.K_a] and keys[pygame.K_w]:
                self.tank.movement("L_UP")

            elif keys[pygame.K_a]:
                self.tank.movement("LEFT")
            elif keys[pygame.K_d]:
                self.tank.movement("RIGHT")
            elif keys[pygame.K_w]:
                self.tank.movement("UP")
            elif keys[pygame.K_s]:
                self.tank.movement("DOWN")
            else:
                self.tank.movement("NONE")

            if (keys[pygame.K_SPACE] or mouse_pressed[0]) and not self.inventory_window.active:
                self.tank.shoot_main_gun()

            if keys[pygame.K_1]:
                self.tank.switch_ammo(1)
            elif keys[pygame.K_2]:
                self.tank.switch_ammo(2)
            elif keys[pygame.K_3]:
                self.tank.switch_ammo(3)
            elif keys[pygame.K_4]:
                self.tank.switch_ammo(4)

            if keys[pygame.K_ESCAPE]:
                self.mode = 'person'
                self.person.active = True
                self.person.rect = self.tank.rect


            self.tank.turret_movement(mouse_pos_offset)

        elif self.mode == 'person':
            if keys[pygame.K_a]:
                self.person.movement("LEFT")
            elif keys[pygame.K_d]:
                self.person.movement("RIGHT")
            elif keys[pygame.K_w]:
                self.person.movement("UP")
            elif keys[pygame.K_s]:
                self.person.movement("DOWN")
            else:
                self.person.movement("NONE")

            if keys[pygame.K_e] and self.person.rect.colliderect(self.tank.hull.rect):
                self.mode = 'tank'
                self.person.active = False


        current_time = pygame.time.get_ticks()

        if current_time - self.last_click_time >= self.click_time:

            if keys[pygame.K_u] and not self.status_window.active:
                self.status_window.active = True
            elif keys[pygame.K_u] and self.status_window.active:
                self.status_window.active = False

            if keys[pygame.K_i] and not self.inventory_window.active:
                self.inventory_window.active = True

            elif keys[pygame.K_i] and self.inventory_window.active:
                self.inventory_window.active = False

            self.last_click_time = current_time



        # self.status_window.move_window(mouse_pos, mouse_pressed)
        self.inventory_window.move_window(mouse_pos, mouse_pressed)
        self.inventory_window.press_button(mouse_pos, mouse_pressed)


    def update_mouse_sight(self, mouse_pos):
        self.sight_rect.center = mouse_pos


    def update(self):
        self.tank.update()
        self.person.update()


    def draw(self, screen):
        if self.mode == 'tank':
            screen.blit(self.sight_image, self.sight_rect)


        self.status_window.draw(screen)
        self.inventory_window.draw(screen)


