# Shmup - Part 20
#   improve asset loading by adding full path to img & snd folders
#   try it - go to folder above and run 'python3 shmup-19.py'
# by KidsCanCode 2015
# A space shmup in multiple parts
# For educational purposes only
# Art from Kenney.nl
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3

import pygame
import random
from os import path

sound_dir = path.join(path.dirname(__file__), 'snd')
img_dir = path.join(path.dirname(__file__), 'img')

# define some colors (R, G, B)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 480
HEIGHT = 600
FPS = 60
TITLE = "SHMUP"
BGCOLOR = BLACK
POWERUP_TIME = 5000

def draw_text(text, size, x, y):
    # generic function to draw some text
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def draw_shield_bar(x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(screen, GREEN, fill_rect)
    pygame.draw.rect(screen, WHITE, outline_rect, 2)

def draw_lives(x, y, lives):
    for i in range(lives):
        img_rect = player_mini_image.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        screen.blit(player_mini_image, img_rect)

############  DEFINE SPRITES  ############
class Player(pygame.sprite.Sprite):
    # player sprite - moves left/right, shoots
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_image, (50, 38))
        self.rect = self.image.get_rect()
        self.radius = 22
        # uncomment to test the radius
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def hide(self):
        # hide player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.loc = self.rect.center
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def update(self):
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.center = self.loc
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        # only move if arrow key is pressed
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()

        # move the sprite
        self.rect.x += self.speedx
        # stop at the edges
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        power_sound.play()
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if not self.hidden and now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                self.shoot_delay = 250
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                pew_sound.play()
            if self.power == 2:
                self.shoot_delay = 250
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                pew_sound.play()
            if self.power >= 3:
                self.shoot_delay = 150
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                pew_sound.play()

class Mob(pygame.sprite.Sprite):
    # mob sprite - spawns above top and moves downward
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image0 = random.choice(meteor_images)
        self.image0.set_colorkey(BLACK)
        self.image = self.image0.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # uncomment to test the radius
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-80, -50)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 8)
        self.rot = 0
        self.rot_speed = random.randrange(-10, 10)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image0, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.y = random.randrange(-80, -50)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if off top of screen
        if self.rect.bottom < 0:
            self.kill()

class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = -20
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        # kill if off bottom of screen
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# initialize pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# load graphics and sounds
pew_sound = pygame.mixer.Sound(path.join(sound_dir, 'pew.wav'))
shield_sound = pygame.mixer.Sound(path.join(sound_dir, 'pow4.wav'))
player_die_sound = pygame.mixer.Sound(path.join(sound_dir, 'rumble1.ogg'))
power_sound = pygame.mixer.Sound(path.join(sound_dir, 'pow5.wav'))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(sound_dir, snd)))
pygame.mixer.music.load(path.join(sound_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()
player_image = pygame.image.load(path.join(img_dir, 'playerShip1_orange.png')).convert()
player_image.set_colorkey(BLACK)
player_mini_image = pygame.transform.scale(player_image, (25, 19))
bullet_image = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()
meteor_list = ['meteorBrown_med3.png', 'meteorBrown_med1.png',
               'meteorBrown_small2.png', 'meteorBrown_tiny1.png']
meteor_images = []
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    img = pygame.image.load(path.join(img_dir, 'regularExplosion0{}.png'.format(i))).convert()
    img.set_colorkey(BLACK)
    img1 = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img1)
    img2 = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img2)
    img = pygame.image.load(path.join(img_dir, 'sonicExplosion0{}.png'.format(i))).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

# set up new game
def newmob():
    # spawn a new mob and add it to sprite groups
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
for i in range(15):
    newmob()
score = 0
last_powerup = pygame.time.get_ticks()
pygame.mixer.music.play(loops=-1)

running = True
while running:
    clock.tick(FPS)
    # check for events
    for event in pygame.event.get():
        # this one checks for the window being closed
        if event.type == pygame.QUIT:
            running = False

    ##### Game logic goes here  #########
    all_sprites.update()
    # check if bullets hit mobs
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        # more points for smaller hits
        score += 25 - hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        random.choice(expl_sounds).play()
        newmob()

    # check if mobs hit player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            # spawn a player explosion and delete the player sprite
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100
            player.power = 1
    # if player died and explosion finished
    if player.lives == 0 and not death_explosion.alive():
        running = False
        pygame.mixer.music.stop()

    # check if player hits powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += 20
            shield_sound.play()
            if player.shield > 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()

    # spawn a powerup (maybe)
    now = pygame.time.get_ticks()
    if now - last_powerup > 3000 and random.random() > 0.99:
        last_powerup = now
        powerup = Powerup()
        all_sprites.add(powerup)
        powerups.add(powerup)

    ##### Draw/update screen #########
    screen.fill(BGCOLOR)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    score_text = str(score)
    draw_text(score_text, 18, WIDTH / 2, 10)
    draw_shield_bar(5, 5, player.shield)
    draw_lives(WIDTH - 100, 5, player.lives)
    # after drawing, flip the display
    pygame.display.flip()
