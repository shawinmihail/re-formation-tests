# coding=utf8

import pygame
import time
import Copter
import numpy as np
import pid
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

x_desired = np.array([10, 10])


copter = Copter.Copter(0, np.array([0, 0]), np.array([0, 0]), 1, 20)
copterPainter = Copter.CopterPainter(copter, green, gameDisplay, (px_ratio, display_width, display_height), True)


def update(dt):

    accel = pid.get_prop_diff_control(copter.x, x_desired, copter.v)
    copter.move(accel, dt)
    copterPainter.draw()


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
