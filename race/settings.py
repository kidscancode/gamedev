import pygame as pg

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 1200   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 800  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Race!"
BGCOLOR = DARKGREY

# Layers
PLAYER_LAYER = 2
EFFECTS_LAYER = 3
BG_LAYER = 1
POW_LAYER = 2

# Player 1 settings
PLAYER1 = {'name': 'player1',
           'img': 'car_blue_small_1.png',
           'heading': 45,
           'pos': (WIDTH / 2, HEIGHT * 3 / 4),
           'accel': 1000,
           'braking': 350,
           'friction': 0.05,
           'drag': 0.05 / 30,
           'steering_fast': 12,
           'steering_slow': 25,
           'max_speed': 500,
           'wheelbase': 30}
PLAYER1['controls'] = {'TurnLeft': pg.K_LEFT,
                       'TurnRight': pg.K_RIGHT,
                       'Accelerate': pg.K_UP,
                       'Brake': pg.K_DOWN}
