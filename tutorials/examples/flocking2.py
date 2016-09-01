# pg template - skeleton for a new pg project
import pygame as pg
from random import randint, uniform
vec = pg.math.Vector2

WIDTH = 1024
HEIGHT = 800
FPS = 30
GRIDSIZE = 32
NUM_MOBS = 20
NEIGHBOR_RADIUS = 25
ALIGN_WEIGHT = .5
COHERE_WEIGHT = 1
SEPARATE_WEIGHT = 2
MAX_SPEED = 5
MAX_FORCE = 0.3
APPROACH_RADIUS = 100

WANDER_RADIUS = 150
WANDER_DISTANCE = 255
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTGREY = (40, 40, 40)

# initialize pg and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Flocking Example")
clock = pg.time.Clock()

def draw_text(text, size, color, x, y, align="nw"):
    font_name = pg.font.match_font('hack')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "nw":
        text_rect.topleft = (x, y)
    if align == "ne":
        text_rect.topright = (x, y)
    if align == "sw":
        text_rect.bottomleft = (x, y)
    if align == "se":
        text_rect.bottomright = (x, y)
    if align == "n":
        text_rect.midtop = (x, y)
    if align == "s":
        text_rect.midbottom = (x, y)
    if align == "e":
        text_rect.midright = (x, y)
    if align == "w":
        text_rect.midleft = (x, y)
    if align == "center":
        text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_grid():
    for x in range(0, WIDTH, GRIDSIZE):
        pg.draw.line(screen, LIGHTGREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRIDSIZE):
        pg.draw.line(screen, LIGHTGREY, (0, y), (WIDTH, y))

def draw_vectors():
    # future vector
    draw_arrow(p1.pos, p1.draw_data[0], GREEN, 5)
    # circle
    cx = int(p1.draw_data[0].x)
    cy = int(p1.draw_data[0].y)
    pg.draw.circle(screen, WHITE, (cx, cy), WANDER_RADIUS, 2)
    # target vector
    draw_arrow((cx, cy), p1.draw_data[1], RED, 4)


def draw_arrow(p1, p2, col, size):
    # line portion
    pg.draw.line(screen, col, p1, p2, size)

class Predator(pg.sprite.Sprite):
    def __init__(self):
        self.groups = all_sprites, predators
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((16, 16))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(randint(25, WIDTH - 25), randint(25, HEIGHT - 25))
        self.vel = vec(3, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos

    def wander(self):
        steer = vec(0, 0)
        future = self.pos + self.vel.normalize() * WANDER_DISTANCE
        target = future + vec(WANDER_RADIUS, 0).rotate(uniform(0, 360))
        steer = self.seek(target)
        self.draw_data = [future, target]
        return steer

    def seek(self, target):
        desired = (target - self.pos).normalize() * MAX_SPEED
        steer = (desired - self.vel)
        if steer.length_squared() > 0.2**2:
            steer.scale_to_length(0.2)
        return steer

    def update(self):
        wander = self.wander()
        seek = vec(0, 0)

        self.acc = seek + wander
        self.vel += self.acc
        self.pos += self.vel
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT

        self.rect.center = self.pos

class Mob(pg.sprite.Sprite):
    def __init__(self):
        self.groups = all_sprites, mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((16, 16))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(randint(25, WIDTH - 25), randint(25, HEIGHT - 25))
        self.vel = vec(MAX_SPEED, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos

    def seek(self, target):
        desired = (target - self.pos).normalize() * MAX_SPEED
        steer = (desired - self.vel)
        if steer.length_squared() > MAX_FORCE**2:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def separation(self, count, a_dist):
        # move away from other mobs
        steer = vec(0, 0)
        desired = a_dist
        if count > 0:
            desired.scale_to_length(MAX_SPEED)
            steer = (desired - self.vel)
            if steer.length_squared() > MAX_FORCE**2:
                steer.scale_to_length(MAX_FORCE)
        return steer * SEPARATE_WEIGHT

    def alignment(self, count, a_vel):
        steer = vec(0, 0)
        desired = a_vel
        if count > 0:
            desired.scale_to_length(MAX_SPEED)
            steer = (desired - self.vel)
            if steer.length_squared() > MAX_FORCE**2:
                steer.scale_to_length(MAX_FORCE)
        return steer * ALIGN_WEIGHT

    def cohesion(self, count, a_pos):
        steer = vec(0, 0)
        desired = a_pos
        if count > 0:
            steer = self.seek(desired)
        return steer * COHERE_WEIGHT

    def get_averages(self):
        count = 0
        a_pos = vec(0, 0)
        a_dist = vec(0, 0)
        a_vel = vec(0, 0)
        for mob in mobs:
            if mob != self:
                d = self.pos.distance_to(mob.pos)
                if d < NEIGHBOR_RADIUS:
                    a_pos += mob.pos
                    a_vel += mob.vel
                    a_dist += (self.pos - mob.pos).normalize()
                    count += 1
        if count > 0:
            a_pos /= count
            a_vel /= count
            a_dist /= count
        return count, a_pos, a_dist, a_vel

    def update(self):
        # avoid multiple loops, get averages
        count, a_pos, a_dist, a_vel = self.get_averages()
        # seek = self.seek(pg.mouse.get_pos())
        # seek = vec(0, 0)
        seek = self.seek(p1.pos)
        sep = self.separation(count, a_dist)
        ali = self.alignment(count, a_vel)
        coh = self.cohesion(count, a_pos)

        self.acc = seek + sep + ali + coh
        self.vel += self.acc
        self.pos += self.vel
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT

        self.rect.center = self.pos


all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()
predators = pg.sprite.Group()
p1 = Predator()
for i in range(NUM_MOBS):
    Mob()
paused = False
show_vectors = False

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pg.event.get():
        # check for closing window
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            paused = not paused
        if event.type == pg.KEYDOWN and event.key == pg.K_m:
            Mob()
        if event.type == pg.KEYDOWN and event.key == pg.K_v:
            show_vectors = not show_vectors

    # Update
    if not paused:
        mobs.update()
        predators.update()

    # Draw / render
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(BLACK)
    draw_grid()
    all_sprites.draw(screen)
    if show_vectors:
        draw_vectors()
    pg.display.flip()

pg.quit()
