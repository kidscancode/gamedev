# Flap
# KidsCanCode 2014
# Flappy bird in pygame - Simple version (no graphics)
import pygame
import sys
import random

# define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE

# basic constants for your game options
WIDTH = 480
HEIGHT = 320
FPS = 30

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flap")
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(FPS)
    # check for events
    for event in pygame.event.get():
        # this one checks for the window being closed
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # now check for keypresses
        elif event.type == pygame.KEYDOWN:
            # this one quits if the player presses Esc
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    ##### Draw/update screen #########
    screen.fill(BGCOLOR)
    # after drawing, flip the display
    pygame.display.flip()
