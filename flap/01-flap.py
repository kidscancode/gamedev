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
# tweak this to change how quickly the bird falls
GRAVITY = 1
# how powerful is a flap?
FLAP_SPEED = 15

class Bird(pygame.sprite.Sprite):
    # player controlled bird, can only flap
    width = 36
    height = 24
    def __init__(self):
        # when you make a Pygame Sprite object, you have to call the
        # Sprite init function
        pygame.sprite.Sprite.__init__(self)
        self.speed_y = 0
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # start in the middle of the screen
        self.rect.centerx = WIDTH / 2
        self.rect.y = HEIGHT / 2

    def update(self):
        # gravity pulls downward
        self.speed_y += GRAVITY
        # move
        self.rect.y += self.speed_y
        # stop at the top/bottom
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed_y = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed_y = 0

    def flap(self):
        # player hit SPACEBAR
        self.speed_y -= FLAP_SPEED

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flap")
clock = pygame.time.Clock()

# group to hold sprites
active_sprite_list = pygame.sprite.Group()
# create the player object
player = Bird()
active_sprite_list.add(player)

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
            if event.key == pygame.K_SPACE:
                    player.flap()

    ##### Draw/update screen #########
    screen.fill(BGCOLOR)
    active_sprite_list.update()
    active_sprite_list.draw(screen)
    # after drawing, flip the display
    pygame.display.flip()
