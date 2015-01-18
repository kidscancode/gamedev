# Pokemon example
# by KidsCanCode 2014
# An example of using Tiled editor to create tilemaps and load in Python
# For educational purposes only
import pygame
import sys
import tmx

# define some colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BGCOLOR = BLACK

# basic constants for your game options
WIDTH = 640
HEIGHT = 480
FPS = 30

class Player(pygame.sprite.Sprite):
    def __init__(self, location, orientation, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = pygame.image.load('img/player.png')
        self.image_default = self.image.copy()
        self.rect = pygame.Rect(location, (64, 64))
        self.dir = orientation
        self.hold_time = 0
        self.walking = False
        self.dx = 0
        self.step = 'rightFoot'
        self.set_sprite()

    def set_sprite(self):
        self.image = self.image_default.copy()
        if self.dir == 'up':
            self.image.scroll(0, -64)
        elif self.dir == 'down':
            self.image.scroll(0, 0)
        elif self.dir == 'left':
            self.image.scroll(0, -128)
        elif self.dir == 'right':
            self.image.scroll(0, -192)

    def update(self, dt):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            if not self.walking:
                if self.dir != 'up':
                    self.dir = 'up'
                    self.set_sprite()
                self.hold_time += dt
        elif key[pygame.K_DOWN]:
            if not self.walking:
                if self.dir != 'down':
                    self.dir = 'down'
                    self.set_sprite()
                self.hold_time += dt
        elif key[pygame.K_LEFT]:
            if not self.walking:
                if self.dir != 'left':
                    self.dir = 'left'
                    self.set_sprite()
                self.hold_time += dt
        elif key[pygame.K_RIGHT]:
            if not self.walking:
                if self.dir != 'right':
                    self.dir = 'right'
                    self.set_sprite()
                self.hold_time += dt
        else:
            self.hold_time = 0
            self.step = 'rightFoot'
        # walking happens if key is held longer than 0.1 sec
        if self.hold_time >= 100:
            self.walking = True
        last_rect = self.rect.copy()
        # walk at 8 pixels per frame in the dir
        if self.walking and self.dx < 64:
            if self.dir == 'up':
                self.rect.y -= 8
            elif self.dir == 'down':
                self.rect.y += 8
            elif self.dir == 'left':
                self.rect.x -= 8
            elif self.dir == 'right':
                self.rect.x += 8
            self.dx += 8
        # check for collisions
        # reset to the previous rect if collides w/foreground layer
        if len(tilemap.layers['triggers'].collide(self.rect, 'solid')) > 0:
            self.rect = last_rect
        # switch to walking sprite after 32 pixels
        if self.dx == 32:
            # step keeps track of when to flip (so it looks like stepping
            # with different feet)
            if (self.dir == 'up' or self.dir == 'down') and self.step == 'leftFoot':
                self.image = pygame.transform.flip(self.image, True, False)
                self.step = 'rightFoot'
            else:
                self.image.scroll(-64, 0)
                self.step = 'leftFoot'

        # after walking 64 pixels, animation is done
        if self.dx == 64:
            self.walking = False
            self.set_sprite()
            self.dx = 0

        tilemap.set_focus(self.rect.x, self.rect.y)

class SpriteLoop(pygame.sprite.Sprite):
    def __init__(self, location, cell, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = pygame.image.load(cell['src'])
        self.image_default = self.image.copy()
        self.width = int(cell['width'])
        self.height = int(cell['height'])
        self.rect = pygame.Rect(location, (self.width, self.height))
        self.frames = int(cell['frames'])
        self.frame_count = 0
        self.mspf = int(cell['mspf'])
        self.time_count = 0

    def update(self, dt):
        self.time_count += dt
        if self.time_count > self.mspf:
            # advance to the next frame
            self.image = self.image_default.copy()
            self.image.scroll(-1 * self.width * self.frame_count, 0)
            self.time_count = 0
            self.frame_count += 1
            if self.frame_count == self.frames:
                self.frame_count = 0

# initialize pygame
pygame.init()
# initialize sound - remove if you're not using sound
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

tilemap = tmx.load("town.tmx", screen.get_size())
players = tmx.SpriteLayer()
objects = tmx.SpriteLayer()
# animated sprites here
for cell in tilemap.layers['sprites'].find('src'):
    SpriteLoop((cell.px, cell.py), cell, objects)
tilemap.layers.append(objects)
# player sprite
start_cell = tilemap.layers['triggers'].find('playerStart')[0]
player = Player((start_cell.px, start_cell.py), start_cell['playerStart'], players)
tilemap.layers.append(players)
tilemap.set_focus(player.rect.x, player.rect.y)

running = True
while running:
    dt = clock.tick(FPS)
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
    tilemap.update(dt)
    ##### Draw/update screen #########
    screen.fill(BGCOLOR)
    tilemap.draw(screen)
    # after drawing, flip the display
    pygame.display.flip()
