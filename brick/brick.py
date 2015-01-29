# Brick breaker example
# by KidsCanCode 2015
# For educational purposes only

import pygame
import sys
import random
import math

# define some colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BGCOLOR = BLACK

# basic constants for your game options
TITLE = "Bricks!"
WIDTH = 800
HEIGHT = 600
FPS = 30

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15

class vec2:
    # a class to do vector math
    # includes operator overloading
    # TODO: more operations
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        # multiplying a vector by a scalar
        x = self.x * other
        y = self.y * other
        return vec2(x, y)

    def __add__(self, other):
        # adding two vectors
        x = self.x + other.x
        y = self.y + other.y
        return vec2(x, y)

    def __str__(self):
        # the __str__ function defines how an object appears with print()
        return "({:.2f},{:.2f})".format(self.x, self.y)

    def mag(self):
        # return the magnitude (length) of the vector
        return math.sqrt(self.x*self.x + self.y*self.y)

    def normalize(self):
        # return a normalized vector (unit vector)
        return self * self.mag()**-1


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.xspeed = 0
        self.speed = 15
        self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT - 20
        self.rect.centerx = WIDTH / 2

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.xspeed = -self.speed
        if keystate[pygame.K_RIGHT]:
            self.xspeed = self.speed
        if not keystate[pygame.K_LEFT] and not keystate[pygame.K_RIGHT]:
            self.xspeed = 0
        # update position
        self.rect.x += self.xspeed
        if self.rect.left < 0:
            self.rect.left = 0
            self.xspeed = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.xspeed = 0

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 5
        # self.vel = vec2(random.randrange(-10, 10),
        #                 random.randrange(-5, -1))
        self.vel = vec2(0, -1)
        self.vel = self.vel.normalize() * self.speed
        self.image = pygame.Surface([10, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT / 2

    def update(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.vel.x *= -1
        if self.rect.top < 0:
            self.vel.y *= -1

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        pass

    def new(self):
        # initialize for a new game
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.paddle = Paddle()
        self.all_sprites.add(self.paddle)
        ball = Ball()
        self.balls.add(ball)
        self.all_sprites.add(ball)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()  # check for events
            self.update()  # update the game state
            self.draw()    # draw the next frame

    def quit(self):
        pygame.quit()
        sys.exit()

    def events(self):
        # handle all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

    def update(self):
        self.all_sprites.update()
        # bounce paddle
        hit_ball = pygame.sprite.spritecollide(self.paddle, self.balls, False)
        if hit_ball:
            hit_ball[0].vel.y *= -1
            diff = hit_ball[0].rect.centerx - self.paddle.rect.centerx
            hit_ball[0].vel.x += diff * 0.12
            hit_ball[0].vel = hit_ball[0].vel.normalize() * hit_ball[0].speed

        for ball in self.balls:
            if ball.rect.bottom >= HEIGHT:
                ball.kill()

        if len(self.balls) == 0:
            self.running = False

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        # uncommment to show FPS (useful for troubleshooting)
        fps_txt = "{:.2f}".format(self.clock.get_fps())
        self.draw_text(str(fps_txt), 18, WIDTH-50, 10)
        pygame.display.flip()

    def draw_text(self, text, size, x, y):
        # utility function to draw text at a given location
        # TODO: move font matching to beginning of file (don't repeat)
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def start_screen(self):
        pass

    def go_screen(self):
        pass

g = Game()
while True:
    g.start_screen()
    g.new()
    g.run()
    g.go_screen()
