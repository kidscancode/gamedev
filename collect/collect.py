# Collect the Blocks
# by KidsCanCode 2015
# Run around and collect the blocks before the time runs out!

import pygame
import sys
import random
import math

# define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

WIDTH = 800
HEIGHT = 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collect the Blocks")
clock = pygame.time.Clock()

def draw_text(text, size, x, y):
    # utility function to draw text on screen
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        x = self.x * other
        y = self.y * other
        return vec2(x, y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return vec2(x, y)

    def __str__(self):
        return "({:.2f},{:.2f})".format(self.x, self.y)

    def mag(self):
        return math.sqrt(self.x*self.x + self.y*self.y)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pos = vec2(WIDTH/2, HEIGHT/2)
        self.vel = vec2(0, 0)
        self.accel = vec2(0, 0)
        self.image = pygame.Surface((36, 36))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

    def update(self):
        self.accel = vec2(0, 0)
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.accel.x = -.7
        if keystate[pygame.K_RIGHT]:
            self.accel.x = .7
        if keystate[pygame.K_UP]:
            self.accel.y = -.7
        if keystate[pygame.K_DOWN]:
            self.accel.y = .7
        if self.accel.x != 0 and self.accel.y != 0:
            self.accel *= 0.7071

        # friction (based on vel)
        self.accel += self.vel * -0.1
        # grav
        # self.accel.y += .3

        # equations of motion
        # p' = 0.5 at**2 + vt + p
        # v' = at + v
        self.pos += self.accel * 0.5 + self.vel
        self.vel += self.accel

        # move the sprite
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)
        # don't move offscreen
        if self.rect.left < 0:
            self.pos.x = 0
            self.vel.x = 0
        if self.rect.right > WIDTH:
            self.pos.x = WIDTH - self.rect.width
            self.vel.x = 0
        if self.rect.top < 0:
            self.pos.y = 0
            self.vel.y = 0
        if self.rect.bottom > HEIGHT:
            self.pos.y = HEIGHT - self.rect.height
            self.vel.y = 0

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

running = True
while running:
    clock.tick(FPS)
    # handle all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    screen.fill(BLACK)
    draw_text(str(player.pos), 18, 10, 10)
    draw_text(str(player.vel), 18, 10, 50)
    draw_text(str(player.accel), 18, 10, 90)
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
