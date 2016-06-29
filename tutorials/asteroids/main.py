# Space Rocks! (asteroids)
# KidsCanCode 2016
# Art by kenney.nl
# SimpleBeat by http://opengameart.org/users/3uhox
import pygame as pg
import sys
from os import path
from random import choice, randrange
from itertools import repeat
from sprites import *
from settings import *

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        pg.mixer.set_num_channels(16)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.game_surface = pg.Surface((WIDTH, HEIGHT))
        self.game_rect = self.game_surface.get_rect()
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.rot_cache = {}
        self.load_data()

    def draw_text(self, text, size, color, x, y, align='m'):
        font = pg.font.Font(path.join(img_dir, FONT_NAME), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == 'm':
            text_rect.midtop = (x, y)
        elif align == 'r':
            text_rect.topright = (x, y)
        elif align == 'l':
            text_rect.topleft = (x, y)
        self.game_surface.blit(text_surface, text_rect)

    def draw_score(self, x, y):
        digit_rect = self.numbers[0].get_rect()
        width = len(str(self.score)) * digit_rect.width
        score_surf = pg.Surface([width, digit_rect.height])
        score_rect = score_surf.get_rect()
        score_rect.midtop = (x, y)
        for pos, char in enumerate(str(self.score)):
            digit_img = self.numbers[int(char)]
            digit_rect.topleft = (pos * digit_rect.width, 0)
            score_surf.blit(digit_img, digit_rect)
        self.game_surface.blit(score_surf, score_rect)

    def new(self):
        # initialize all your variables and do all the setup for a new game
        self.rot_cache['player'] = {}
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.rocks = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.bomb_explosions = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.aliens = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player = Player(self, PLAYER_IMG)
        if SHIELD_AT_START:
            Shield(self, self.player)
        for i in range(2):
            Rock(self, 3, None)
        self.score = 0
        self.level = 1
        self.offset = repeat((0, 0))
        self.last_alien = pg.time.get_ticks()
        pg.mixer.music.load(path.join(snd_dir, 'SimpleBeat.ogg'))
        pg.mixer.music.play(loops=-1)

    def load_data(self):
        # spritesheets
        self.spritesheet = SpritesheetWithXML(path.join(img_dir, 'sheet'))
        self.expl_sheet = SpritesheetWithXML(path.join(img_dir, 'spritesheet_regularExplosion'))
        self.expl_player_sheet = SpritesheetWithXML(path.join(img_dir, 'spritesheet_sonicExplosion'))
        # rock images - 4 sizes
        self.rot_cache['rock'] = {}
        for size in ROCK_IMAGES.keys():
            for img in ROCK_IMAGES[size]:
                self.rot_cache['rock'][img] = {}
        # explosions - 3 kinds
        self.expl_frames = {}
        self.expl_frames['lg'] = []
        self.expl_frames['sm'] = []
        self.expl_frames['sonic'] = []
        for i in range(9):
            img_name = 'sonicExplosion0{}.png'.format(i)
            img = self.expl_player_sheet.get_image_by_name(img_name)
            img.set_colorkey(BLACK)
            self.expl_frames['sonic'].append(img)
            img_name = 'regularExplosion0{}.png'.format(i)
            img = self.expl_sheet.get_image_by_name(img_name)
            img.set_colorkey(BLACK)
            img_lg = pg.transform.rotozoom(img, 0, 0.6)
            self.expl_frames['lg'].append(img_lg)
            img_sm = pg.transform.rotozoom(img, 0, 0.3)
            self.expl_frames['sm'].append(img_sm)
        # numerals for 0-9
        self.numbers = []
        for i in range(10):
            self.numbers.append(self.spritesheet.get_image_by_name('numeral{}.png'.format(i)))
        self.background = pg.image.load(path.join(img_dir, 'starfield.png'))
        self.background_rect = self.background.get_rect()
        # shield images
        self.shield_images = []
        for img in SHIELD_IMAGES:
            img = pg.transform.rotozoom(self.spritesheet.get_image_by_name(img), 0, PLAYER_SCALE - 0.1)
            self.shield_images.append(img)
        # sounds
        self.shield_down_sound = pg.mixer.Sound(path.join(snd_dir, SHIELD_DOWN_SOUND))
        self.shield_down_sound.set_volume(1.0)
        self.alien_fire_sound = pg.mixer.Sound(path.join(snd_dir, ALIEN_BULLET_SOUND))
        self.alien_fire_sound.set_volume(1.0)
        self.hyper_sound = pg.mixer.Sound(path.join(snd_dir, HYPER_SOUND))
        self.bomb_tick_sound = pg.mixer.Sound(path.join(snd_dir, BOMB_TICK_SOUND))
        self.bomb_tick_sound.set_volume(0.5)
        self.bullet_sounds = []
        for sound in BULLET_SOUNDS:
            snd = pg.mixer.Sound(path.join(snd_dir, sound))
            snd.set_volume(0.5)
            self.bullet_sounds.append(snd)
        self.bomb_launch_sound = pg.mixer.Sound(path.join(snd_dir, BOMB_LAUNCH_SOUND))
        self.rock_exp_sounds = []
        for sound in ROCK_EXPL_SOUNDS:
            self.rock_exp_sounds.append(pg.mixer.Sound(path.join(snd_dir, sound)))
        self.bomb_exp_sounds = []
        for sound in BOMB_EXPL_SOUNDS:
            self.bomb_exp_sounds.append(pg.mixer.Sound(path.join(snd_dir, sound)))
        self.pow_sounds = {}
        for pow_type in POW_SOUNDS.keys():
            self.pow_sounds[pow_type] = pg.mixer.Sound(path.join(snd_dir, POW_SOUNDS[pow_type]))

    def run(self):
        # The Game loop - set self.running to False to end the game
        self.playing = True
        while self.playing:
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
        # spawn alien?
        now = pg.time.get_ticks()
        if now - self.last_alien > ALIEN_SPAWN_TIME + randint(1000, 5000):
            self.last_alien = now
            Alien(self)

        # bomb explosions take out rocks (player too?)
        hits = pg.sprite.groupcollide(self.rocks, self.bomb_explosions, True, False)
        for hit in hits:
            self.score += 4 - hit.size
            if hit.size > 1:
                Explosion(self, hit.rect.center, 'lg')
            else:
                Explosion(self, hit.rect.center, 'sm')
            if hit.size > 0:
                Rock(self, hit.size - 1, hit.rect.center)
                Rock(self, hit.size - 1, hit.rect.center)

        # check for bullet hits
        # 1) with rocks 2) with aliens
        # collide bullets with aliens
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits.keys():
            for bullet in hits[hit]:
                if isinstance(bullet, Bomb):
                    bullet.explode()
                if isinstance(hit, Alien):
                    hit.health -= 1
                    if hit.health <= 0:
                        Explosion(self, hit.rect.center, 'sonic')
                        Pow(self, hit.pos)
                        hit.kill()
                    else:
                        Explosion(self, bullet.rect.center, 'sm')
            if isinstance(hit, Rock):
                if randrange(100) < POW_SPAWN_PCT and len(self.powerups) <= 2:
                    Pow(self, hit.pos)
                self.score += 4 - hit.size
                if hit.size > 1:
                    Explosion(self, hit.rect.center, 'lg')
                else:
                    Explosion(self, hit.rect.center, 'sm')
                if hit.size > 0:
                    Rock(self, hit.size - 1, hit.rect.center)
                    Rock(self, hit.size - 1, hit.rect.center)
                hit.kill()

        # check for collisions with player
        hits = pg.sprite.spritecollide(self.player, self.mobs, True, pg.sprite.collide_mask)
        for hit in hits:
            # type of object
            if isinstance(hit, Rock):
                # decrease shield / lives
                if self.player.shield:
                    if self.player.shield.level > 0:
                        self.player.shield.level -= 1
                    else:
                        self.shield_down_sound.play()
                        self.player.shield.kill()
                        self.player.shield = None
                    Explosion(self, self.player.rect.center, 'sonic')
                else:
                    self.playing = False
            elif isinstance(hit, ABullet):
                # decrease shield / lives
                if self.player.shield:
                    if self.player.shield.level > 0:
                        self.player.shield.level -= 1
                    else:
                        self.shield_down_sound.play()
                        self.player.shield.kill()
                        self.player.shield = None
                    Explosion(self, hit.rect.center, 'sm')
                else:
                    self.playing = False
            elif isinstance(hit, Pow):
                if hit.type == 'shield':
                    if not self.player.shield:
                        Shield(self, self.player)
                    else:
                        self.player.shield.level = 2
                    self.pow_sounds[hit.type].play()
                elif hit.type == 'gun':
                    if self.player.gun_level < 4:
                        self.player.gun_level += 1
                        self.pow_sounds[hit.type].play()
            elif isinstance(hit, Alien):
                pass

        if len(self.rocks) == 0:
            self.level += 1
            for i in range(self.level + 2):
                Rock(self, choice([3, 2]), None)

    def shake(self, amount=20, times=2):
        d = -1
        for _ in range(0, times):
            for x in range(0, amount, 4):
                yield(x * d, x * d)
            for x in range(amount, 0, -4):
                yield(x * d, x * d)
            d *= -1
        while True:
            yield (0, 0)

    def draw(self):
        # draw everything to the screen
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.game_surface.blit(self.background, self.background_rect)
        self.all_sprites.draw(self.game_surface)
        self.draw_text(str(self.score), 28, WHITE, WIDTH / 2, 15, align='m')
        self.draw_text("Level: " + str(self.level), 22, WHITE, 5, 15, align='l')
        # self.draw_score(WIDTH / 2, 15)
        self.screen.blit(self.game_surface, next(self.offset))
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            # this one checks for the window being closed
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.quit()

    def show_start_screen(self):
        # show the start screen
        self.game_surface.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to fire", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.screen.blit(self.game_surface, self.game_rect)
        pg.display.flip()
        self.wait_for_key(0)

    def show_go_screen(self):
        # show the game over screen
        self.game_surface.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.screen.blit(self.game_surface, self.game_rect)
        pg.display.flip()
        self.wait_for_key(2000)

    def wait_for_key(self, delay):
        start = pg.time.get_ticks()
        pg.event.get()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP and pg.time.get_ticks() - start > delay:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                    else:
                        waiting = False

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
