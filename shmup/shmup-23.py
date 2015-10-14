# Shmup - Part 23
#   add graphical score font
# by KidsCanCode 2015
# A space shmup in multiple parts
# For educational purposes only
# Art from Kenney.nl
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3

import pygame as pg
import random
from os import path
import sys

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

def draw_text(surf, text, size, x, y):
    # generic function to draw some text
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def wait_for_key():
    # utility function to pause waiting for a keypress
    # still allow Esc to exit
    # Actually, we look for KEYUP event, not KEYPRESS
    if len(pg.event.get(pg.QUIT)) > 0:
        pg.quit()
        sys.exit()
    keyup_events = pg.event.get(pg.KEYUP)
    if len(keyup_events) == 0:
        return None
    if keyup_events[0].key == pg.K_ESCAPE:
        pg.quit()
        sys.exit()
    return keyup_events[0].key

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, img, x, y, lives):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_score(surf, images, x, y, score):
    num_rect = images[0].get_rect()
    width = len(str(score)) * num_rect.width
    score_surf = pg.Surface([width, num_rect.height])
    score_surf.set_colorkey(BLACK)
    score_rect = score_surf.get_rect()
    score_rect.midtop = (x, y)
    for pos, char in enumerate(str(score)):
        digit_img = images[int(char)]
        digit_rect = digit_img.get_rect()
        digit_rect.topleft = (pos * num_rect.width, 0)
        score_surf.blit(digit_img, digit_rect)
    surf.blit(score_surf, score_rect)


############  DEFINE SPRITES  ############
class Player(pg.sprite.Sprite):
    # player sprite - moves left/right, shoots
    def __init__(self, game, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.game = game
        self.image = pg.transform.scale(game.player_image, (50, 38))
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
        self.lives = 3
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()

    def hide(self):
        # hide player temporarily
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.loc = self.rect.center
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def update(self):
        # unhide if hidden
        if self.hidden and pg.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.center = self.loc
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
        self.game.power_sound.play()
        self.power += 1
        self.power_time = pg.time.get_ticks()

    def shoot(self):
        now = pg.time.get_ticks()
        if not self.hidden and now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                self.shoot_delay = 250
                Bullet(self.game.bullet_image, self.rect.centerx, self.rect.top,
                       [self.game.all_sprites, self.game.bullets])
                self.game.pew_sound.play()
            if self.power == 2:
                self.shoot_delay = 250
                Bullet(self.game.bullet_image, self.rect.left, self.rect.centery,
                       [self.game.all_sprites, self.game.bullets])
                Bullet(self.game.bullet_image, self.rect.right, self.rect.centery,
                       [self.game.all_sprites, self.game.bullets])
                self.game.pew_sound.play()
            if self.power >= 3:
                self.shoot_delay = 150
                Bullet(self.game.bullet_image, self.rect.left, self.rect.centery,
                       [self.game.all_sprites, self.game.bullets])
                Bullet(self.game.bullet_image, self.rect.right, self.rect.centery,
                       [self.game.all_sprites, self.game.bullets])
                Bullet(self.game.bullet_image, self.rect.centerx, self.rect.top,
                       [self.game.all_sprites, self.game.bullets])
                self.game.pew_sound.play()

class Mob(pg.sprite.Sprite):
    # mob sprite - spawns above top and moves downward
    def __init__(self, images, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image0 = random.choice(images)
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
    def __init__(self, img, x, y, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = img
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
    def __init__(self, images, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.type = random.choice(['shield', 'gun'])
        self.image = images[self.type]
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

class Explosion(pg.sprite.Sprite):
    def __init__(self, anim, center, size, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.anim = anim
        self.size = size
        self.image = anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

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

        self.player = Player(self, [self.all_sprites])
        for i in range(15):
            Mob(self.meteor_images, [self.all_sprites, self.mobs])
        self.score = 0
        self.last_powerup = pg.time.get_ticks()
        pg.mixer.music.play(loops=-1)

    def load_data(self):
        # load all your assets (sounds, images, etc.)
        self.pew_sound = pg.mixer.Sound(path.join(sound_dir, 'pew.wav'))
        self.shield_sound = pg.mixer.Sound(path.join(sound_dir, 'pow4.wav'))
        self.power_sound = pg.mixer.Sound(path.join(sound_dir, 'pow5.wav'))
        self.player_die_sound = pg.mixer.Sound(path.join(sound_dir, 'rumble1.ogg'))
        self.expl_sounds = []
        for snd in ['expl3.wav', 'expl6.wav']:
            self.expl_sounds.append(pg.mixer.Sound(path.join(sound_dir, snd)))
        pg.mixer.music.load(path.join(sound_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
        pg.mixer.music.set_volume(0.4)
        self.background = pg.image.load(path.join(img_dir, 'starfield.png')).convert()
        self.background_rect = self.background.get_rect()
        self.player_image = pg.image.load(path.join(img_dir, 'playerShip1_orange.png')).convert()
        self.player_image.set_colorkey(BLACK)
        self.player_mini_image = pg.transform.scale(self.player_image, (25, 19))
        self.bullet_image = pg.image.load(path.join(img_dir, 'laserRed16.png')).convert()
        meteor_list = ['meteorBrown_med3.png', 'meteorBrown_med1.png',
                       'meteorBrown_small2.png', 'meteorBrown_tiny1.png']
        self.meteor_images = []
        for img in meteor_list:
            self.meteor_images.append(pg.image.load(path.join(img_dir, img)).convert())
        self.powerup_images = {}
        self.powerup_images['shield'] = pg.image.load(path.join(img_dir, 'shield_gold.png')).convert()
        self.powerup_images['gun'] = pg.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
        self.explosion_anim = {}
        self.explosion_anim['lg'] = []
        self.explosion_anim['sm'] = []
        self.explosion_anim['player'] = []
        for i in range(9):
            img = pg.image.load(path.join(img_dir, 'regularExplosion0{}.png'.format(i))).convert()
            img.set_colorkey(BLACK)
            img1 = pg.transform.scale(img, (75, 75))
            self.explosion_anim['lg'].append(img1)
            img2 = pg.transform.scale(img, (32, 32))
            self.explosion_anim['sm'].append(img2)
            img = pg.image.load(path.join(img_dir, 'sonicExplosion0{}.png'.format(i))).convert()
            img.set_colorkey(BLACK)
            self.explosion_anim['player'].append(img)
        self.num_images = []
        for i in range(10):
            img = pg.image.load(path.join(img_dir, 'numeral{}.png'.format(i))).convert()
            img.set_colorkey(BLACK)
            self.num_images.append(img)

    def run(self):
        # The Game loop - set self.running to False to end the game
        self.running = True
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # the update part of the game loop
        self.all_sprites.update()

        # check if bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, True, True)
        for hit in hits:
            # more points for smaller hits
            self.score += 25 - hit.radius
            Explosion(self.explosion_anim, hit.rect.center, 'lg', [self.all_sprites])
            random.choice(self.expl_sounds).play()
            Mob(self.meteor_images, [self.all_sprites, self.mobs])

        # check if mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, True, pg.sprite.collide_circle)
        for hit in hits:
            self.player.shield -= hit.radius * 2
            Explosion(self.explosion_anim, hit.rect.center, 'sm', [self.all_sprites])
            Mob(self.meteor_images, [self.all_sprites, self.mobs])

            if self.player.shield <= 0:
                # spawn a player explosion and delete the player sprite
                self.player_die_sound.play()
                self.death_explosion = Explosion(self.explosion_anim, self.player.rect.center, 'player', [self.all_sprites])
                self.player.hide()
                self.player.lives -= 1
                self.player.shield = 100
                self.player.power = 1
        # if player died and explosion finished
        if self.player.lives == 0 and not self.death_explosion.alive():
            self.running = False
            pg.mixer.music.stop()

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
            Powerup(self.powerup_images, [self.all_sprites, self.powerups])

    def draw(self):
        # draw everything to the screen
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.background, self.background_rect)
        self.all_sprites.draw(self.screen)
        # score_text = str(self.score)
        # draw_text(self.screen, score_text, 18, WIDTH / 2, 10)
        draw_score(self.screen, self.num_images, WIDTH / 2, 10, self.score)
        draw_shield_bar(self.screen, 5, 5, self.player.shield)
        draw_lives(self.screen, self.player_mini_image, WIDTH - 100, 5, self.player.lives)
        # for testing purposes
        # fps_txt = "FPS: {:.2f}".format(self.clock.get_fps())
        # pg.display.set_caption(fps_txt)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            # this one checks for the window being closed
            if event.type == pg.QUIT:
                self.quit()

    def show_start_screen(self):
        # show the start screen
        self.screen.blit(self.background, self.background_rect)
        draw_text(self.screen, "Shmup!", 72, WIDTH / 2, HEIGHT / 4)
        draw_text(self.screen, "Move with the arrow keys", 24, WIDTH / 2, HEIGHT / 2)
        draw_text(self.screen, "Shoot the meteors", 24, WIDTH / 2, HEIGHT * 5 / 8)
        draw_text(self.screen, "Press a key to begin", 24, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.update()
        # wait for a keypress to start
        wait_for_key()
        while True:
            if wait_for_key():
                pg.event.get()
                return

    def show_go_screen(self):
        # show the game over screen
        self.screen.blit(self.background, self.background_rect)
        draw_text(self.screen, "GAME OVER", 58, WIDTH / 2, HEIGHT / 4)
        text = "Score: %s" % self.score
        draw_text(self.screen, text, 24, WIDTH / 2, HEIGHT / 2)
        draw_text(self.screen, "Press a key to begin", 24, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.update()
        # pause for a moment and then wait for key
        pg.time.wait(500)
        wait_for_key()
        while True:
            if wait_for_key():
                pg.event.get()
                return

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
