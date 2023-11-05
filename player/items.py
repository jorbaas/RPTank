
from tanks.bullets import all_ammo
import pygame
from tanks.parts import all_turrets, all_hulls, all_barrels, all_engines, all_cannons



class Item():
    def __init__(self, name, type):

        self.name = name
        self.type = type

        self.setup()

        self.rect = None


    def setup(self):
        if self.type == 'hull':
            self.values = all_hulls[self.name]
            self.image = pygame.image.load(f'assets/items/hull_images/{self.values["image_name"]}.png')
            self.rect = self.image.get_rect()
        elif self.type == 'turret':
            self.values = all_turrets[self.name]
            self.image = pygame.image.load(f'assets/items/turret_images/{self.values["image_name"]}.png')
            self.rect = self.image.get_rect()
        elif self.type == 'barrel':

            self.values = all_barrels[self.name]
            self.image = pygame.image.load(f'assets/items/barrel_images/{self.values["image_name"]}.png')
            self.rect = self.image.get_rect()
        elif self.type == 'engine':
            self.values = all_engines[self.name]
            self.image = pygame.image.load(f'assets/items/engine_images/{self.values["image_name"]}.png')
            self.rect = self.image.get_rect()
        elif self.type == 'cannon':
            self.values = all_cannons[self.name]
            self.image = pygame.image.load(f'assets/items/cannon_images/{self.values["image_name"]}.png')
            self.rect = self.image.get_rect()
        elif self.type == 'ammo':
            self.values = all_ammo[self.name]
            self.image = pygame.image.load(f'assets/items/ammo_images/{self.values["image_name"]}.png')
            self.rect = self.image.get_rect()

class Inventory():
    def __init__(self):

        # {'item1': [item, amount]}
        self.items = {}
        self.ammo = {}

    def add_item(self, item, amount=1):

        if item.values['name'] in self.items and item.type != 'ammo':
            self.items[item.values['name']][1] += amount
        elif item.type != 'ammo':
            self.items[item.values['name']] = [item, amount]
        elif item.values['name'] in self.ammo and item.type == 'ammo':
            self.ammo[item.values['name']][1] += amount

        elif item.type == 'ammo':

            self.ammo[item.values['name']] = [item, amount]


    def add_item_by_name(self, name, amount=1):
        items = [all_cannons, all_engines, all_barrels, all_hulls, all_turrets, all_ammo]
        for item_dict in items:
            if name in item_dict:
                item = Item(name, item_dict[name]['type'])
                self.add_item(item, amount)


    def remove_item(self, item, amount=1):
        if item.values['name'] in self.items:
            self.items[item.values['name']][1] -= amount
            if self.items[item.values['name']][1] <= 0:
                self.items.pop(item.values['name'])
        elif item.values['name'] in self.ammo:
            self.ammo[item.values['name']][1] -= amount
            if self.ammo[item.values['name']][1] <= 0:
                self.ammo.pop(item.values['name'])





