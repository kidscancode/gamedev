# Template for new Pygame project
# KidsCanCode 2014
import pygame
import sys

# define some colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BGCOLOR = BLACK

# basic constants for your game options
WIDTH = 360
HEIGHT = 480
FPS = 30

# initialize pygame
pygame.init()
# initialize sound - remove if you're not using sound
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(FPS)
    # check for all your events
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
            # add any other key events here

    ##### Game logic goes here  #########

    ##### Draw/update screen #########
    screen.fill(BGCOLOR)
    # after drawing, flip the display
    pygame.display.flip()
