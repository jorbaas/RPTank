from tanks.parts import *

def changePart(item, tank):
    if item.type == ['turret']:
        tank.turret = Turret(item.name, (tank.rect.x, tank.rect.y))
    if item.type == ['barrel']:
        tank.barrel = Barrel(item.name, (tank.rect.x, tank.rect.y))
    if item.type == ['hull']:
        tank.hull = Hull(item.name, (tank.rect.x, tank.rect.y))
    if item.type == ['engine']:
        tank.engine = Engine(item.name)
    if item.type == ['cannon']:
        tank.cannon = Cannon(item.name)