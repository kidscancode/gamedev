# Cross!
# A "Crossy Road" style game
# Template for new Pygame project
# KidsCanCode 2015
import pygame
import sys
import time
import random

# define some colors (R, G, B)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FUCHSIA = (255, 0, 255)
GRAY = (128, 128, 128)
DARKGRAY = (40, 40, 40)
LIME = (0, 128, 0)
MAROON = (128, 0, 0)
NAVYBLUE = (0, 0, 128)
LIGHTBLUE = (0, 155, 155)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
CYAN = (0, 255, 255)
BGCOLOR = FUCHSIA

# basic constants for your game options
WIDTH = 540
HEIGHT = 720
FPS = 10
TILESIZE = 30
TILEWIDTH = WIDTH // TILESIZE
TILEHEIGHT = HEIGHT // TILESIZE
PLAYERSIZE = 20
SPEED = 0

LANE_TYPES = ['Road', 'River', 'Grass', 'Road']
LANE_COLORS = {'Road': GRAY, 'River': LIGHTBLUE, 'Grass': GREEN}

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pygame.draw.line(screen, DARKGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pygame.draw.line(screen, DARKGRAY, (0, y), (WIDTH, y))

def draw_board(lanes):
    for y, type in enumerate(lanes):
        lane_rect = pygame.Rect(0, y*TILESIZE, WIDTH, TILESIZE)
        pygame.draw.rect(screen, LANE_COLORS[type], lane_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.tile_x = TILEWIDTH // 2
        self.tile_y = TILEHEIGHT - 4
        self.image = pygame.Surface((PLAYERSIZE, PLAYERSIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x = self.tile_x * TILESIZE + (TILESIZE - PLAYERSIZE) / 2
        self.rect.y = self.tile_y * TILESIZE + (TILESIZE - PLAYERSIZE) / 2
        self.rect.y += SPEED

    def jump(self, dir):
        if dir == 'f':
            self.tile_y -= 1
            if self.tile_y < 0:
                self.tile_y = 0
        elif dir == 'b':
            self.tile_y += 1
            if self.tile_y > TILEHEIGHT - 1:
                self.tile_y = TILEHEIGHT - 1
        elif dir == 'l':
            self.tile_x -= 1
            if self.tile_x < 0:
                self.tile_x = 0
        elif dir == 'r':
            self.tile_x += 1
            if self.tile_x > TILEWIDTH - 1:
                self.tile_x = TILEWIDTH - 1

class Mob(pygame.sprite.Sprite):
    def __init__(self, lane):
        pygame.sprite.Sprite.__init__(self)
        self.tile_x = random.choice([0, TILEWIDTH-1])
        self.speed_x = random.randrange(4, 10)
        if self.tile_x == 0:
            self.speed_x *= 1
        else:
            self.speed_x *= -1
        self.image = pygame.Surface((40, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = self.tile_x * TILESIZE
        self.rect.y = lane * TILESIZE + 5

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.left > WIDTH:
            self.rect.left = 0
        if self.rect.right < 0:
            self.rect.right = WIDTH

# initialize pygame
pygame.init()
# initialize sound - remove if you're not using sound (always use sound!)
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cross!")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
fg_sprites = pygame.sprite.Group()
bg_sprites = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
fg_sprites.add(player)
lanes = []
for y in range(TILEHEIGHT):
    lanes.append(random.choice(LANE_TYPES))
    mob = Mob(y)
    all_sprites.add(mob)
    fg_sprites.add(mob)

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
            if event.key == pygame.K_UP:
                player.jump('f')
            if event.key == pygame.K_DOWN:
                player.jump('b')
            if event.key == pygame.K_LEFT:
                player.jump('l')
            if event.key == pygame.K_RIGHT:
                player.jump('r')
    ##### Game logic goes here  #########

    ##### Draw/update screen #########
    screen.fill(BGCOLOR)
    # draw_grid()
    draw_board(lanes)
    all_sprites.update()
    bg_sprites.draw(screen)
    fg_sprites.draw(screen)
    # after drawing, flip the display
    pygame.display.flip()
