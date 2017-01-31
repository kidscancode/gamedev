import pygame as pg

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
LIGHTGREY = (90, 90, 90)
BGCOLOR = (129, 245, 59)

TITLE = "Snake!"
FPS = 60
WIDTH = 1024
HEIGHT = 768
CELLSIZE = 32
GRIDWIDTH = 40
GRIDHEIGHT = 30

SNAKE_SPEED = 50
SNAKE_LENGTH = 3
# SNAKE_HEAD = (2 * 384, 0, 384, 384)
# SNAKE_BODY = (384, 0, 384, 384)
# SNAKE_TAIL = (0, 0, 384, 384)
SNAKE_HEAD = "snake_head_64.png"
SNAKE_BODY = "snake_body_64.png"
APPLE_IMAGE = (3 * 384, 0, 384, 384)
WALL_IMAGE = (4 * 384, 384, 384, 384)
CONTROLS = {pg.K_LEFT: 'l',
            pg.K_RIGHT: 'r',
            pg.K_UP: 'u',
            pg.K_DOWN: 'd'}
DIRECTIONS = {'l': (-1, 0),
              'r': (1, 0),
              'u': (0, -1),
              'd': (0, 1)}
ROTATIONS = {'l': -90,
             'r': 90,
             'u': 180,
             'd': 0}
# ROTATIONS = {'l': 180,
#              'r': 0,
#              'u': 90,
#              'd': -90}

SPRITESHEET = 'Textures.png'

LEVEL1_WALLS = [(x, 0) for x in range(GRIDWIDTH)]
LEVEL1_WALLS += [(0, y) for y in range(GRIDHEIGHT)]
LEVEL1_WALLS += [(x, GRIDHEIGHT - 1) for x in range(GRIDWIDTH)]
LEVEL1_WALLS += [(GRIDWIDTH - 1, y) for y in range(GRIDHEIGHT)]
LEVEL1_WALLS += [(12, y) for y in range(8, GRIDHEIGHT - 8)]
LEVEL1_WALLS += [(GRIDWIDTH - 12, y) for y in range(8, GRIDHEIGHT - 8)]
