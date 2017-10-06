# coding=utf8

import pygame
import time
import Copter
import numpy as np
import pid

import loop2
""" ------------------ pygame constants ------------------------"""

# from meters to px (1m = px_ratio)
px_ratio = 30.0
display_width = 1200
display_height = 980
frame_freq = 50

pygame.init()
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Simple copter 2d simulation')
clock = pygame.time.Clock()

surface = pygame.display.get_surface()

crashed = False

green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)


t_prev = time.time()

x_desired1 = np.array([10, 10])
x_desired2 = np.array([10, -10])


copter1 = Copter.Copter(0, np.array([0, 0, 0]), np.array([10, 10, 0]), 1, 10)
copterPainter1 = Copter.CopterPainter(copter1, green, gameDisplay, (px_ratio, display_width, display_height), True)

loop = loop2.Loop(copter1, 0.3, 20)

# copter2 = Copter.Copter(1, np.array([0, 0]), np.array([0, 0]), 1, 20)
# copterPainter2 = Copter.CopterPainter(copter2, red, gameDisplay, (px_ratio, display_width, display_height), True)


def update(dt):

    # accel1 = pid.get_prop_diff_control(copter1.x, x_desired1, copter1.v)
    # accel2 = pid.get_prop_diff_control(copter2.x, x_desired2, copter2.v)

    copter1.move_vel(loop.get_speed(), dt)
    # copter2.move(accel2, dt)
    copterPainter1.draw()
    # copterPainter2.draw()


while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.fill(white)

    dt = time.time() - t_prev
    t_prev = time.time()

    update(dt)

    pygame.display.update()
    clock.tick(frame_freq)

pygame.quit()


quit()
