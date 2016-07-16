import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
GREY = (100, 100, 100)

# game settings
WIDTH = 800
HEIGHT = 600
FPS = 60
TITLE = "Space Rocks!"
BGCOLOR = BLACK
FONT_NAME = 'KenVector Future.ttf'

# player settings
PLAYER_IMG = 'playerShip1_red.png'
PLAYER_LIFE_IMG = 'playerLife1_red.png'
PLAYER_SCALE = 0.4
PLAYER_THRUST = 500
PLAYER_ROT_SPEED = 3.5
PLAYER_MAX_SPEED = 300
PLAYER_FRICTION = 0.75
LIVES_AT_SPAWN = 3
GUN_LEVEL_AT_SPAWN = 1
SHIELD_AT_SPAWN = True
# TODO: set to None
WEAPON2_AT_SPAWN = 'beam'
HYPER_CHARGE_TIME = 8000
SHIELD_IMAGES = ['shield1.png', 'shield2.png', 'shield3.png']
# thrust particles
PLAYER_THRUST_OFFSET = vec(0, 25)
PLAYER_THRUST_VEL = vec(0, 3)
PLAYER_THRUST_IMG = 'ship_particle.png'
PLAYER_THRUST_COUNT = 0
PLAYER_THRUST_LIFETIME = 0.2
PLAYER_THRUST_FADE = 0
PLAYER_THRUST_SIZE = 50
PLAYER_THRUST_ANGLE = 10

# weapon settings
BULLET_IMG = 'laserBlue01.png'
BULLET_SCALE = 0.8
BULLET_SPEED = 500
BULLET_LIFETIME = 2000
BULLET_RATE = 350
BULLET_SOUNDS = ['sfx_wpn_laser8.wav']
BOMB_IMAGES = ['laserRed08.png', 'laserRed09.png']
BOMB_SCALE = 0.6
BOMB_SPEED = 25
BOMB_LIFETIME = 4000
BOMB_RATE = 2000
BOMB_LAUNCH_SOUND = 'sfx_wpn_laser6.wav'
BEAM_WIDTH = 20
BEAM_RATE = 2000
BEAM_LIFETIME = 1000

# sounds
HYPER_SOUND = 'sfx_movement_portal4.wav'
SHIELD_DOWN_SOUND = 'sfx_sound_shutdown1.wav'
ROCK_EXPL_SOUNDS = ['sfx_exp_shortest_hard1.wav', 'sfx_exp_short_hard12.wav', 'sfx_exp_short_hard15.wav']
BOMB_EXPL_SOUNDS = ['sfx_exp_medium5.wav', 'sfx_exp_medium6.wav']
BOMB_TICK_SOUND = 'sfx_sounds_Blip10.wav'

# rock settings
START_ROCKS = 3
ROCK_IMAGES = {}
ROCK_IMAGES[0] = ['meteorGrey_tiny1.png', 'meteorGrey_tiny2.png']
ROCK_IMAGES[1] = ['meteorGrey_small1.png', 'meteorGrey_small2.png']
ROCK_IMAGES[2] = ['meteorGrey_med1.png', 'meteorGrey_med2.png']
ROCK_IMAGES[3] = ['meteorGrey_big1.png', 'meteorGrey_big2.png', 'meteorGrey_big3.png', 'meteorGrey_big4.png']
ROCK_SPEED_MIN = 25
ROCK_SPEED_MAX = 100

# bad guys
ALIEN_IMAGE = 'ufoGreen.png'
ALIEN_SCALE = 0.6
ALIEN_SPEED_MIN = 40
ALIEN_SPEED_MAX = 75
ALIEN_SPAWN_TIME = 15000
ALIEN_FIRE_RATE = 2500
ALIEN_BULLET_SPEED = 450
ALIEN_BULLET_IMAGE = 'laserGreen03.png'
ALIEN_BULLET_SOUND = 'sfx_wpn_laser7.wav'
ALIEN_BULLET_LIFETIME = 3000
ALIEN_HITS = 3

# powerups
POW_SPAWN_PCT = 4
POW_IMAGES = {'shield': 'shield_gold.png',
              'gun': 'bolt_bronze.png'}
POW_SOUNDS = {'shield': 'sfx_sounds_powerup18.wav',
              'gun': 'sfx_sounds_fanfare2.wav'}
POW_LIFETIME = 3000
POW_MIN_SPEED = 10
POW_MAX_SPEED = 50

# layers
PLAYER_LAYER = 2
BULLET_LAYER = 3
ROCK_LAYER = 1
TEXT_LAYER = 4
EXPLOSION_LAYER = 4
POW_LAYER = 2
