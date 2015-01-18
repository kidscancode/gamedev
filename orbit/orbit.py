# Orbital simulation, using real physical values
# by KidsCanCode 2015
# For educational purposes only
import pygame
import sys
import math

# define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)

WIDTH = 800
HEIGHT = 600
FPS = 60

# Physical constants
G = 6.67428e-11  # Newton's Grav. Constant
AU = (149.6e6 * 1000)  # in meters
SCALE = WIDTH / (4 * AU)  # Pixels per AU.  1 AU is 1/4 screen width
OFFSETX = WIDTH / 2  # places origin at center of screen
OFFSETY = HEIGHT / 2
TIMESTEP = 24 * 3600  # one day, in sec

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbits")
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

    def __sub__(self, other):
        # subtract one vector from another
        x = self.x - other.x
        y = self.y - other.y
        return vec2(x, y)

    def __str__(self):
        # the __str__ function defines how an object appears with print()
        return "({:.4f},{:.4f})".format(self.x, self.y)

    def mag(self):
        # return the magnitude (length) of the vector
        return math.sqrt(self.x*self.x + self.y*self.y)


class Body(pygame.sprite.Sprite):
    # a generic astronomical body
    # requires radius (in pixels) and color for drawing
    def __init__(self, rad, col):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((rad*2, rad*2))
        pygame.draw.circle(self.image, col, (rad, rad), rad)
        self.mass = 1
        self.rad = rad
        self.col = col
        self.rect = self.image.get_rect()
        self.pos = vec2(0, 0)
        self.vel = vec2(0, 0)
        self.accel = vec2(0, 0)
        self.rect.x = self.pos.x * SCALE + OFFSETX - rad
        self.rect.y = self.pos.y * SCALE + OFFSETY - rad

    def update(self):
        # move the sprite
        self.rect.x = self.pos.x * SCALE + OFFSETX - self.rad
        self.rect.y = self.pos.y * SCALE + OFFSETY - self.rad


bodies = pygame.sprite.Group()

# planetary data from http://ssd.jpl.nasa.gov/horizons.cgi
sun = Body(25, YELLOW)
sun.name = "Sun"
sun.mass = 1.98892e30  # kg
bodies.add(sun)

earth = Body(8, BLUE)
earth.name = "Earth"
earth.mass = 5.9742e24  # kg
earth.pos.x = -1 * AU
earth.vel.y = 29.783e3  # km/s
bodies.add(earth)

venus = Body(7, YELLOW)
venus.name = "Venus"
venus.mass = 4.8685e24
venus.pos.x = 0.723 * AU
venus.vel.y = -35.02e3
bodies.add(venus)

mars = Body(5, RED)
mars.name = "Mars"
mars.mass = 6.4185e23
mars.pos.x = 1.3812 * AU
mars.vel.y = -24.1309e3
bodies.add(mars)

mercury = Body(3, RED)
mercury.name = "Mercury"
mercury.mass = 3.302e23
mercury.pos.x = -0.3075 * AU
mercury.vel.y = 47.362e3
bodies.add(mercury)

# Jupiter is *really* far from the sun.  You'll need to make the window bigger
# and/or change the SCALE value to even see it. Try WIDTH / (12 * AU)
# jup = Body(12, ORANGE)
# jup.name = "Jupiter"
# jup.mass = 1898.13e24
# jup.pos.y = 4.9470 * AU
# jup.vel.x = 13.0697e3
# bodies.add(jup)

step = 1
running = True
while running:
    # uncomment to print out each body's data each step
    # print('Step #{}'.format(step))
    # for body in bodies:
    #     s = '{:<8}  Pos.={:>6.4f} {:>6.4f} Vel.={:>10.4f} {:>10.4f}'.format(
    #         body.name, body.pos.x/AU, body.pos.y/AU, body.vel.x, body.vel.y)
    #     print(s)
    # print()
    # use this if you want to slow the animation down
    # pygame.time.wait(1000)
    step += 1
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

    # find sun's force on each body
    for body in bodies:
        if body is sun:
            continue
        body.accel = vec2(0, 0)
        d = (sun.pos - body.pos).mag()
        dir = (sun.pos - body.pos) * (1/d)
        a = G * sun.mass / (d**2)
        body.accel += dir * a

    # move each body
    for body in bodies:
        if body is sun:
            continue
        # equations of motion
        body.vel += body.accel * TIMESTEP
        body.pos += body.vel * TIMESTEP

    # comment this to make the planets leave trails!
    screen.fill(BLACK)
    # uncomment to show current FPS
    # fps_txt = "{:.2f}".format(clock.get_fps())
    # draw_text(str(fps_txt), 18, WIDTH-50, 10)
    bodies.update()
    bodies.draw(screen)
    pygame.display.flip()
