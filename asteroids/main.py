# Space Rocks! (asteroids)
# KidsCanCode 2016, 2017
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
        # all drawing is done to game_surface
        # then game surface blitted to screen
        self.game_surface = pg.Surface((WIDTH, HEIGHT))
        self.game_rect = self.game_surface.get_rect()
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        # rotation cache to store rotated images of sprites
        # rather than repeated transforms every frame
        self.rot_cache = {}
        self.rot_cache['player'] = {}
        self.rot_cache['rock'] = {}
        self.load_data()

    def draw_text(self, text, size, color, x, y, align='midtop'):
        # helper method to render/place text - use in game loop draw section
        font = pg.font.Font(path.join(img_dir, FONT_NAME), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.game_surface.blit(text_surface, text_rect)

    def draw_hyper(self, x, y):
        # draw charge indicator for hyperspace function
        box_width = 100
        box_height = 12
        if self.player.hyper_charge:
            pct = 1
        else:
            pct = (pg.time.get_ticks() - self.player.last_hyper) / HYPER_CHARGE_TIME
        fill = box_width * pct
        if pct < .50:
            col = RED
        elif pct < .95:
            col = YELLOW
        else:
            col = GREEN
        outline_rect = pg.Rect(x, y, box_width, box_height)
        fill_rect = pg.Rect(x, y + 3, fill, box_height - 4)
        pg.draw.rect(self.game_surface, col, fill_rect)
        pg.draw.rect(self.game_surface, WHITE, outline_rect, 2)

    def draw_shield_level(self, x, y):
        # draw shield indicator
        # TODO: add "warning" flash when shield empty
        box_width = 12
        box_height = 15
        spacer = 3
        offset = 25
        # icon
        img = self.shield_logo
        img_rect = img.get_rect()
        img_rect.topleft = (x, y)
        # outline
        outline_rect = pg.Rect(x + offset, y, box_width * 3 + spacer * 4, box_height + spacer * 2)
        pg.draw.rect(self.game_surface, GREY, outline_rect, 2)
        # fill
        fill_colors = [RED, YELLOW, GREEN]
        if self.player.shield:
            for i in range(self.player.shield.level + 1):
                r = pg.Rect(x + offset + spacer + (box_width + spacer) * i, y + spacer, box_width, box_height)
                pg.draw.rect(self.game_surface, fill_colors[self.player.shield.level], r)
        else:
            pass
        self.game_surface.blit(img, img_rect)

    def draw_lives(self, img, x, y, count):
        # draw lives indicator using given icon
        for i in range(count):
            img_rect = img.get_rect()
            img_rect.x = x + 40 * i
            img_rect.y = y
            self.game_surface.blit(img, img_rect)

    def draw_score(self, x, y):
        # draw score using image font
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
        # initialize all variables and do all the setup for a new game
        # various groups for collisions
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.rocks = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.bomb_explosions = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.aliens = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player = Player(self, PLAYER_IMG)
        for i in range(START_ROCKS):
            Rock(self, 3, None)
        self.score = 0
        self.level = 1
        # Experimental lighting
        # TODO: improve lighting functionality
        self.light = False
        # offset for screen shake function
        self.offset = repeat((0, 0))
        self.last_alien = pg.time.get_ticks()
        pg.mixer.music.load(path.join(snd_dir, 'SimpleBeat.ogg'))
        pg.mixer.music.play(loops=-1)

    def load_data(self):
        # load all game assets
        # TODO: loading bar (needed?)
        # TODO: improve lighting frame rate
        self.fog = pg.Surface((WIDTH, HEIGHT))  # , pg.SRCALPHA)
        self.fog.fill((255, 255, 255))
        self.player_light_img = pg.image.load(path.join(img_dir, 'circle_1000.png')).convert_alpha()
        self.player_light_rect = self.player_light_img.get_rect()
        self.bullet_light_img = pg.transform.scale(self.player_light_img, (300, 300))
        self.bullet_light_rect = self.bullet_light_img.get_rect()
        # spritesheets
        self.spritesheet = SpritesheetWithXML(path.join(img_dir, 'sheet'))
        self.beam_sheet = SpritesheetWithXML(path.join(img_dir, 'beams'))
        self.expl_sheet = SpritesheetWithXML(path.join(img_dir, 'spritesheet_regularExplosion'))
        self.expl_player_sheet = SpritesheetWithXML(path.join(img_dir, 'spritesheet_sonicExplosion'))
        self.ship_particle_img = pg.image.load(path.join(img_dir, PLAYER_THRUST_IMG)).convert_alpha()
        # rock images - 4 sizes
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
        # image font - numerals for 0-9
        self.numbers = []
        for i in range(10):
            self.numbers.append(self.spritesheet.get_image_by_name('numeral{}.png'.format(i)))
        self.background = pg.image.load(path.join(img_dir, 'starfield.png')).convert_alpha()
        self.background_rect = self.background.get_rect()
        # shield images
        self.shield_images = []
        for img in SHIELD_IMAGES:
            img = pg.transform.rotozoom(self.spritesheet.get_image_by_name(img), 0, PLAYER_SCALE - 0.1)
            self.shield_images.append(img)
        self.shield_logo = pg.transform.rotozoom(self.spritesheet.get_image_by_name(POW_IMAGES['shield']), 0, 0.6)
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
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        # TODO: clean up - move collisions to sep. functions?
        self.all_sprites.update()
        # spawn alien?
        # TODO: improve alien spawning
        now = pg.time.get_ticks()
        if now - self.last_alien > ALIEN_SPAWN_TIME + randint(1000, 5000):
            self.last_alien = now
            Alien(self)

        # bomb explosions take out rocks (player too?)
        hits = pg.sprite.groupcollide(self.mobs, self.bomb_explosions, False, False)
        for hit in hits:
            if isinstance(hit, Pow) or isinstance(hit, ABullet):
                pass
            else:
                hit.kill()
                self.score += 4 - hit.size
                if hit.size > 1:
                    Explosion(self, hit.rect.center, 'lg')
                else:
                    Explosion(self, hit.rect.center, 'sm')
                if hit.size > 0:
                    Rock(self, hit.size - 1, hit.rect.center)
                    Rock(self, hit.size - 1, hit.rect.center)

        # check for bullet hits
        # 1) with rocks 2) with aliens 3) with alien bullets
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, False, pg.sprite.collide_mask)
        for hit in hits.keys():
            for bullet in hits[hit]:
                if isinstance(bullet, Bomb):
                    bullet.explode()
                if isinstance(hit, Alien):
                    hit.hit()
                    bullet.kill()
                    if hit.health <= 0:
                        Explosion(self, hit.rect.center, 'sonic')
                        Pow(self, hit.pos)
                        hit.kill()
                        self.score += 10
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
                    if isinstance(bullet, Bullet):
                        bullet.kill()
            if isinstance(hit, ABullet):
                # TODO: decide whether player shots should hit alien shots
                # hit.kill()
                pass

        # check for collisions with player
        # 1) Rocks 2) alien shots 3) powerups 4) aliens
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
                    self.player.die()
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
                    self.player.die()
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

        # destroyed all rocks? next level
        # TODO: level change indication
        if len(self.rocks) == 0:
            self.level += 1
            for i in range(self.level + 2):
                Rock(self, choice([3, 2]), None)

        # game over
        if self.player.lives <= 0:
            self.playing = False

    def shake(self, amount=20, times=2):
        # implement screen shake
        d = -1
        for _ in range(0, times):
            for x in range(0, amount, 4):
                yield(x * d, x * d)
            for x in range(amount, 0, -4):
                yield(x * d, x * d)
            d *= -1
        while True:
            yield (0, 0)

    def render_fog(self):
        self.fog.fill((180, 180, 180))
        self.player_light_rect.center = self.player.pos
        self.fog.blit(self.player_light_img, self.player_light_rect)
        for sprite in self.all_sprites:
            if isinstance(sprite, Bullet) or isinstance(sprite, ABullet):
                self.bullet_light_rect.center = sprite.pos
                self.fog.blit(self.bullet_light_img, self.bullet_light_rect)
            if isinstance(sprite, Alien) or isinstance(sprite, Explosion):
                self.player_light_rect.center = sprite.pos
                self.fog.blit(self.player_light_img, self.player_light_rect)
        self.game_surface.blit(self.fog, (0, 0), special_flags=pg.BLEND_RGBA_SUB)

    # def render_fog(self):
    #     self.fog.fill((0, 0, 0, 255))
    #     steps = 250
    #     center = (int(self.player.pos.x), int(self.player.pos.y))
    #     for i in range(steps, 1, -5):
    #         pg.draw.circle(self.fog, (0, 0, 0, i * 255 / steps), center, i)
    #     self.game_surface.blit(self.fog, (0, 0))

    def draw(self):
        # draw everything to the screen
        # TODO: disable FPS counter
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.game_surface.blit(self.background, self.background_rect)
        #self.game_surface.fill((40, 40, 40))
        self.all_sprites.draw(self.game_surface)
        self.player.engine_emitter.draw()
        if self.light:
            self.render_fog()
        self.draw_text(str(self.score), 28, WHITE, WIDTH / 2, 15, align='midtop')
        self.draw_text("Level: " + str(self.level), 22, WHITE, 5, 15, align='topleft')
        self.draw_lives(self.player.life_image, WIDTH - 150, 15, self.player.lives)
        self.draw_shield_level(WIDTH - 150, 55)
        self.draw_hyper(WIDTH - 150, 105)
        # self.draw_score(WIDTH / 2, 15)
        self.screen.blit(self.game_surface, next(self.offset))
        pg.display.update()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.quit()
            # TODO: remove this
            if event.type == pg.KEYDOWN and event.key == pg.K_l:
                self.light = not self.light

    def show_start_screen(self):
        # show the start screen
        # TODO: add animation
        # TODO: combine with go_screen?
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
        # simple loop to wait for a keyup event
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
