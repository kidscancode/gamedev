# Shmup - Part 17
#   re-organize code by adding a game object (see adv. pygame template)
#   TODO: fix quit
# by KidsCanCode 2015
# A space shmup in multiple parts
# For educational purposes only
# Art from Kenney.nl
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3

import pygame as pg
import random

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

def draw_text(screen, text, size, x, y):
    # generic function to draw some text
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def draw_shield_bar(screen, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(screen, GREEN, fill_rect)
    pg.draw.rect(screen, WHITE, outline_rect, 2)


############  DEFINE SPRITES  ############
class Player(pg.sprite.Sprite):
    # player sprite - moves left/right, shoots
    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = pg.transform.scale(g.player_image, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 22
        # uncomment to test the radius
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pg.time.get_ticks()
        self.power = 1
        self.power_time = pg.time.get_ticks()

    def update(self):
        # timeout for powerups
        if self.power >= 2 and pg.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pg.time.get_ticks()
        # only move if arrow key is pressed
        self.speedx = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.speedx = -5
        if keystate[pg.K_RIGHT]:
            self.speedx = 5
        if keystate[pg.K_SPACE]:
            self.shoot()

        # move the sprite
        self.rect.x += self.speedx
        # stop at the edges
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        g.power_sound.play()
        self.power += 1
        self.power_time = pg.time.get_ticks()

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                self.shoot_delay = 250
                Bullet(self.rect.centerx, self.rect.top, [g.all_sprites, g.bullets])
                g.pew_sound.play()
            if self.power == 2:
                self.shoot_delay = 250
                Bullet(self.rect.left, self.rect.centery, [g.all_sprites, g.bullets])
                Bullet(self.rect.right, self.rect.centery, [g.all_sprites, g.bullets])
                g.pew_sound.play()
            if self.power >= 3:
                self.shoot_delay = 150
                Bullet(self.rect.left, self.rect.centery, [g.all_sprites, g.bullets])
                Bullet(self.rect.right, self.rect.centery, [g.all_sprites, g.bullets])
                Bullet(self.rect.centerx, self.rect.top, [g.all_sprites, g.bullets])
                g.pew_sound.play()

class Mob(pg.sprite.Sprite):
    # mob sprite - spawns above top and moves downward
    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image0 = random.choice(g.meteor_images)
        self.image0.set_colorkey(BLACK)
        self.image = self.image0.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # uncomment to test the radius
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-80, -50)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 8)
        self.rot = 0
        self.rot_speed = random.randrange(-10, 10)
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image0, self.rot)
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

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = g.bullet_image
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

class Powerup(pg.sprite.Sprite):
    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.type = random.choice(['shield', 'gun'])
        self.image = g.powerup_images[self.type]
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

# initialize pg
pg.init()
pg.mixer.init()


class Game:
    # The Game object will initialize the game, run the game loop,
    # and display start/end screens

    def __init__(self):
        # initialize the game and create the window
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # start the clock
        self.clock = pg.time.Clock()
        self.load_data()

    def new(self):
        # initialize all your variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.powerups = pg.sprite.Group()

        self.player = Player(self.all_sprites)
        for i in range(15):
            # spawn a new mob and add it to sprite groups
            Mob([self.all_sprites, self.mobs])
        self.score = 0
        self.last_powerup = pg.time.get_ticks()
        pg.mixer.music.play(loops=-1)

    def load_data(self):
        # load all your assets (sounds, images, etc.)
        # load graphics and sounds
        self.pew_sound = pg.mixer.Sound('snd/pew.wav')
        self.shield_sound = pg.mixer.Sound('snd/pow4.wav')
        self.power_sound = pg.mixer.Sound('snd/pow5.wav')
        self.expl_sounds = []
        for snd in ['snd/expl3.wav', 'snd/expl6.wav']:
            self.expl_sounds.append(pg.mixer.Sound(snd))
        pg.mixer.music.load('snd/tgfcoder-FrozenJam-SeamlessLoop.ogg')
        pg.mixer.music.set_volume(0.4)
        self.background = pg.image.load("img/starfield.png").convert()
        self.background_rect = self.background.get_rect()
        self.player_image = pg.image.load('img/playerShip1_orange.png').convert()
        self.bullet_image = pg.image.load('img/laserRed16.png').convert()
        meteor_list = ['img/meteorBrown_med3.png', 'img/meteorBrown_med1.png',
                       'img/meteorBrown_small2.png', 'img/meteorBrown_tiny1.png']
        self.meteor_images = []
        for img in meteor_list:
            self.meteor_images.append(pg.image.load(img).convert())
        self.powerup_images = {}
        self.powerup_images['shield'] = pg.image.load('img/shield_gold.png').convert()
        self.powerup_images['gun'] = pg.image.load('img/bolt_gold.png').convert()

    def run(self):
        # The Game loop - set self.running to False to end the game
        self.running = True
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        self.running = False
        pg.quit()

    def update(self):
        # the update part of the game loop
        self.all_sprites.update()
        # check if bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, True, True)
        for hit in hits:
            # more points for smaller hits
            self.score += 25 - hit.radius
            random.choice(self.expl_sounds).play()
            # spawn a new mob and add it to sprite groups
            Mob([self.all_sprites, self.mobs])

        # check if mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, True, pg.sprite.collide_circle)
        for hit in hits:
            self.player.shield -= hit.radius * 2
            # spawn a new mob and add it to sprite groups
            Mob([self.all_sprites, self.mobs])
            if self.player.shield <= 0:
                self.running = False

        # check if player hits powerup
        hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for hit in hits:
            if hit.type == 'shield':
                self.player.shield += 20
                self.shield_sound.play()
                if self.player.shield > 100:
                    self.player.shield = 100
            if hit.type == 'gun':
                self.player.powerup()

        # spawn a powerup (maybe)
        now = pg.time.get_ticks()
        if now - self.last_powerup > 3000 and random.random() > 0.99:
            self.last_powerup = now
            Powerup([self.all_sprites, self.powerups])

    def draw(self):
        # Draw/update screen
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.background, self.background_rect)
        self.all_sprites.draw(self.screen)
        score_text = str(self.score)
        draw_text(self.screen, score_text, 18, WIDTH / 2, 10)
        draw_shield_bar(self.screen, 5, 5, self.player.shield)
        # after drawing, flip the display
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            # this one checks for the window being closed
            if event.type == pg.QUIT:
                self.quit()

    def show_start_screen(self):
        # show the start screen
        pass

    def show_go_screen(self):
        # show the game over screen
        pass

# create the game object
g = Game()
while True:
    g.show_start_screen()
    g.new()
    g.run()
    g.show_go_screen()
