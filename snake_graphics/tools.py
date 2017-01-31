import pygame as pg
from random import randrange
from settings import *

class Spritesheet:
    # utility class for loading and cutting spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image_by_rect(self, x, y, w, h):
        r = pg.Rect(x, y, w, h)
        return self.spritesheet.subsurface(r)

def draw_grid(surf):
    for x in range(0, WIDTH, CELLSIZE):
        pg.draw.line(surf, LIGHTGREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELLSIZE):
        pg.draw.line(surf, LIGHTGREY, (0, y), (WIDTH, y))

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surf, camera, img):
        x = self.x * CELLSIZE
        y = self.y * CELLSIZE
        r = pg.Rect(x, y, CELLSIZE, CELLSIZE)
        surf.blit(img, camera.apply(r))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)

class Tilemap:
    def __init__(self, width, height, wall_img):
        self.width = width
        self.height = height
        self.walls = [Coord(wall[0], wall[1]) for wall in LEVEL1_WALLS]
        self.wall_img = wall_img

    def draw(self, surf, camera):
        for wall in self.walls:
            wall.draw(surf, camera, self.wall_img)

    def get_random_tile(self, buffer=0):
        safe = False
        while not safe:
            tile = Coord(randrange(buffer, self.width - buffer),
                         randrange(buffer, self.height - buffer))
            if tile not in self.walls:
                safe = True
        return tile

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.x * CELLSIZE + int(WIDTH / 2)
        y = -target.y * CELLSIZE + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
