# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)

# game settings
WIDTH = 800
HEIGHT = 600
FPS = 60
TITLE = "Space Rocks!"
BGCOLOR = BLACK
FONT_NAME = 'KenVector Future.ttf'

# player settings
PLAYER_IMG = 'playerShip1_red.png'
PLAYER_SCALE = 0.5
PLAYER_THRUST = 0.2
PLAYER_ROT_SPEED = 3.5
PLAYER_MAX_SPEED = 3
PLAYER_FRICTION = 0.01
SHIELD_AT_START = True
HYPER_CHARGE_TIME = 8000
SHIELD_IMAGES = ['shield1.png', 'shield2.png', 'shield3.png']

# weapon settings
BULLET_IMG = 'laserBlue01.png'
BULLET_SCALE = 0.8
BULLET_SPEED = 8
BULLET_LIFETIME = 2000
BULLET_RATE = 350
BULLET_SOUNDS = ['sfx_wpn_laser8.wav']
BOMB_IMAGES = ['laserRed08.png', 'laserRed09.png']
BOMB_SCALE = 0.6
BOMB_SPEED = 0
BOMB_LIFETIME = 4000
BOMB_RATE = 1000
BOMB_LAUNCH_SOUND = 'sfx_wpn_laser6.wav'

# sounds
HYPER_SOUND = 'sfx_movement_portal4.wav'
SHIELD_DOWN_SOUND = 'sfx_sound_shutdown1.wav'
ROCK_EXPL_SOUNDS = ['sfx_exp_shortest_hard1.wav', 'sfx_exp_short_hard12.wav', 'sfx_exp_short_hard15.wav']
BOMB_EXPL_SOUNDS = ['sfx_exp_medium5.wav', 'sfx_exp_medium6.wav']
BOMB_TICK_SOUND = 'sfx_sounds_Blip10.wav'

# rock settings
ROCK_IMAGES = {}
ROCK_IMAGES[0] = ['meteorGrey_tiny1.png', 'meteorGrey_tiny2.png']
ROCK_IMAGES[1] = ['meteorGrey_small1.png', 'meteorGrey_small2.png']
ROCK_IMAGES[2] = ['meteorGrey_med1.png', 'meteorGrey_med2.png']
ROCK_IMAGES[3] = ['meteorGrey_big1.png', 'meteorGrey_big2.png']
ROCK_SPEED_MIN = 0.5
ROCK_SPEED_MAX = 2.5

# bad guys
ALIEN_IMAGE = 'ufoGreen.png'
ALIEN_SCALE = 0.6
ALIEN_SPEED_MIN = 0.5
ALIEN_SPEED_MAX = 1.5
ALIEN_SPAWN_TIME = 10000
ALIEN_FIRE_RATE = 2500
ALIEN_BULLET_SPEED = 12
ALIEN_BULLET_IMAGE = 'laserGreen03.png'
ALIEN_BULLET_LIFETIME = 3000
ALIEN_HITS = 2

# powerups
POW_SPAWN_PCT = 4
POW_IMAGES = {'shield': 'shield_gold.png',
              'gun': 'bolt_bronze.png'}
POW_SOUNDS = {'shield': 'sfx_sounds_powerup18.wav',
              'gun': 'sfx_sounds_fanfare2.wav'}
POW_LIFETIME = 3000

# layers
PLAYER_LAYER = 1
BULLET_LAYER = 2
ROCK_LAYER = 0
TEXT_LAYER = 3
EXPLOSION_LAYER = 3
POW_LAYER = 1
