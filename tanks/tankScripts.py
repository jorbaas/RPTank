import pygame
import math



def calculateMovement(speed, angle, hull_rect, turret_rect, barrel_rect):

    # direction = pygame.Vector2(0, speed).rotate(-angle)
    # pos += direction
    #
    # hull_rect.center = round(pos[0]), round(pos[1])
    # turret_rect.center = round(pos[0]), round(pos[1])
    # barrel_rect.center = round(pos[0]), round(pos[1])


    # Calculate the horizontal and vertical components of the movement
    movement_angle = math.radians(-angle)
    move_x = speed * math.sin(movement_angle)
    move_y = speed * math.cos(movement_angle)  # Negative because pygame's y-axis is inverted


    # Update the tank's position

    hull_rect.x += move_x
    hull_rect.y -= move_y

    turret_rect.x += move_x
    turret_rect.y -= move_y

    barrel_rect.x += move_x
    barrel_rect.y -= move_y

    return


def calculateAcceleration(mass, power):
    acceleration = power / (mass*1000)
    return acceleration


def calculate_fuel(fuel, mass, power, speed):
    usage = power * speed / (mass * 5000)
    fuel -= usage
    return fuel


def calculateTurretAngle(mouse_pos, turret_rect):
    # Calculate the vector from the turret's position to the player's position
    dx = mouse_pos[0] - turret_rect.centerx
    dy = mouse_pos[1] - turret_rect.centery

    # Calculate the angle in radians between the turret's direction and the player
    turret_angle = math.atan2(-dy, dx)  # The negative dy is because the y-axis is often inverted in games

    # Convert the angle from radians to degrees (optional, depends on your angle units)
    turret_angle = math.degrees(turret_angle) - 90

    return turret_angle


def calcualteSpeed(speed, acceleration):
    if speed > 0:
        speed = max(0, speed - acceleration)
    elif speed < 0:
        speed = max(0, speed - acceleration)
    return speed


def calculateDistance(pos1, pos2):
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    distance = math.sqrt(dx * dx + dy * dy)
    return distance

def calculateAngle(pos1, pos2):
    angle = math.atan2(pos2[1] - pos1[1], pos2[0] - pos1[0])
    angle = math.degrees(angle)
    return angle%360



def calculateAngleOffset(start_rect, angle, offset):
    direction_vector = pygame.math.Vector2(0, 1)
    rotated_vector = direction_vector.rotate(-angle)
    end_position = start_rect.center + rotated_vector * offset
    return end_position


def handleCollision(speed, hull_angle, hull_rect, turret_rect):
    if speed > 0:
        calculateMovement(-1, hull_angle, hull_rect, turret_rect)
    elif speed <= 0:
        calculateMovement(1, hull_angle, hull_rect, turret_rect)
    speed = 0
    return speed



