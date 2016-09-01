# Steering Behavior Examples
# Flee
# KidsCanCode 2016
import pygame as pg
from random import randint, uniform
vec = pg.math.Vector2

WIDTH = 1000
HEIGHT = 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)

# Mob properties
MOB_SIZE = 32
MAX_SPEED = 5
MAX_FORCE = 0.1
SEEK_RADIUS = 300
WALL_LIMIT = 80

class SteeringManager:
    def __init__(self, host):
        self.host = host
        self.steering = vec(0, 0)

    def update(self):
        if self.steering.length() > MAX_FORCE:
            self.steering.scale_to_length(MAX_FORCE)
        self.host.acc = self.steering
        # equations of motion
        self.host.vel += self.host.acc
        if self.host.vel.length() > MAX_SPEED:
            self.host.vel.scale_to_length(MAX_SPEED)
        self.host.pos += self.host.vel
        if self.host.pos.x > WIDTH:
            self.host.pos.x = 0
        if self.host.pos.x < 0:
            self.host.pos.x = WIDTH
        if self.host.pos.y > HEIGHT:
            self.host.pos.y = 0
        if self.host.pos.y < 0:
            self.host.pos.y = HEIGHT
        self.steering_tmp = vec(self.steering)
        self.steering = vec(0, 0)

    def seek(self, target):
        dist = target - self.host.pos
        if dist.length() < SEEK_RADIUS:
            desired = dist.normalize() * MAX_SPEED
            steer = (desired - self.host.vel)
            # if steer.length() > MAX_FORCE:
            #     steer.scale_to_length(MAX_FORCE)
            self.steering += steer

    def avoid_walls(self):
        steer = vec(0, 0)
        near_wall = False
        if self.host.pos.x < WALL_LIMIT:
            desired = vec(MAX_SPEED, self.host.vel.y)
            near_wall = True
        if self.host.pos.x > WIDTH - WALL_LIMIT:
            desired = vec(-MAX_SPEED, self.host.vel.y)
            near_wall = True
        if self.host.pos.y < WALL_LIMIT:
            desired = vec(self.host.vel.x, MAX_SPEED)
            near_wall = True
        if self.host.pos.y > HEIGHT - WALL_LIMIT:
            desired = vec(self.host.vel.x, -MAX_SPEED)
            near_wall = True
        if near_wall:
            steer = (desired - self.host.vel)
            # if steer.length() > MAX_FORCE:
            #     steer.scale_to_length(MAX_FORCE)
        self.steering += steer

    def wander(self):
        pass

    def approach(self, target):
        # seek + easing
        pass

    def evade(self, target):
        pass

    def pursue(self, target):
        pass

    def flock(self, group):
        pass

    def draw_vectors(self):
            scale = 25
            # vel
            pg.draw.line(screen, GREEN, self.host.pos, (self.host.pos + self.host.vel * scale), 5)
            # desired
            pg.draw.line(screen, RED, self.host.pos, (self.host.pos + self.steering_tmp * scale**2), 5)

class Mob(pg.sprite.Sprite):
    def __init__(self):
        self.groups = all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((MOB_SIZE, MOB_SIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(randint(0, WIDTH), randint(0, HEIGHT))
        self.vel = vec(MAX_SPEED, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.steering = SteeringManager(self)

    def update(self):
        self.steering.seek(pg.mouse.get_pos())
        self.steering.avoid_walls()
        self.steering.update()
        self.rect.center = self.pos

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

all_sprites = pg.sprite.Group()
Mob()
paused = False
show_vectors = False
running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_SPACE:
                paused = not paused
            if event.key == pg.K_v:
                show_vectors = not show_vectors
            if event.key == pg.K_m:
                Mob()

    if not paused:
        all_sprites.update()
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGRAY)
    all_sprites.draw(screen)
    if show_vectors:
        for sprite in all_sprites:
            sprite.steering.draw_vectors()
    pg.display.flip()
