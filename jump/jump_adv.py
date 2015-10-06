# Jump!
# by KidsCanCode 2015
# A Doodle Jump style game in Pygame
# For educational purposes only

# TODO: Sounds:
#   * Hit enemy
#   * Pow
#   * Heart
#   * Walk (step)
# TODO: More enemies - shooters, ?
# TODO: Background image / clouds
# TODO: Moving platforms
# TODO: Particle effects

import pygame
import sys
from os import path
import random

# define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE

WIDTH = 480
HEIGHT = 640
FPS = 30
GRAVITY = 1
TITLE = "Jump!"


class SpriteSheet:
    """Utility class to load and parse spritesheets"""
    def __init__(self, filename):
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pygame.Surface([width, height])
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        # image.set_colorkey([230, 230, 230])
        image.set_colorkey([0, 155, 155])
        return image


class Player(pygame.sprite.Sprite):
    speed = 12
    jump_speed = 20

    def __init__(self, game):
        # player init - create the sprite and set the starting location
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.life = 3
        self.speed_x = 0
        self.speed_y = 0
        self.walking = False
        self.jumping = False
        self.hit = False
        self.hit_time = 0
        self.current_frame = 0
        self.dir = 'l'
        self.last_update = 0
        self.load_images()
        self.image = self.frames_standing_l[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 48

    def load_images(self):
        self.frames_running_l = []
        self.frames_running_r = []
        self.frames_standing_r = []
        self.frames_standing_l = []
        self.frames_jumping_ul = []
        self.frames_jumping_ur = []
        self.frames_jumping_dl = []
        self.frames_jumping_dr = []
        self.frames_hit_l = []
        self.frames_hit_r = []

        # running frames
        for x in range(0, 476, 68):
            image = self.game.sprite_sheet.get_image(x, 0, 68, 100)
            self.frames_running_r.append(image)
            image = pygame.transform.flip(image, True, False)
            self.frames_running_l.append(image)
        # idle frames
        for x in range(0, 204, 68):
            image = self.game.sprite_sheet.get_image(x, 100, 68, 100)
            self.frames_standing_r.append(image)
            image = pygame.transform.flip(image, True, False)
            self.frames_standing_l.append(image)
        # jump frames
        image = self.game.sprite_sheet.get_image(136, 100, 68, 100)
        self.frames_jumping_ur.append(image)
        image = pygame.transform.flip(image, True, False)
        self.frames_jumping_ul.append(image)
        image = self.game.sprite_sheet.get_image(204, 100, 68, 100)
        self.frames_jumping_dr.append(image)
        image = pygame.transform.flip(image, True, False)
        self.frames_jumping_dl.append(image)
        # hit frame
        image = self.game.sprite_sheet.get_image(272, 100, 68, 100)
        self.frames_hit_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.frames_hit_l.append(image)

    def update(self):
        self.animate()
        if not self.hit:
            # keep moving as long as key is down
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.dir = 'l'
                self.speed_x = -self.speed
            if keystate[pygame.K_RIGHT]:
                self.dir = 'r'
                self.speed_x = self.speed
            if not keystate[pygame.K_LEFT] and not keystate[pygame.K_RIGHT]:
                self.walking = False
                self.speed_x = 0
        # update the player's position
        # add gravity
        self.speed_y += GRAVITY
        # move the sprite
        self.rect.x += self.speed_x
        # self.check_collisions('x')
        self.rect.y += self.speed_y
        # self.check_collisions('y')
        # stop at the left and right sides
        if self.rect.left < -8:
            self.rect.left = -8
            self.speed_x = 0
        if self.rect.right > WIDTH + 8:
            self.rect.right = WIDTH + 8
            self.speed_x = 0

    def check_collisions(self, dir):
        if dir == 'x':
            hit_list = pygame.sprite.spritecollide(self, g.platforms, False)
            if hit_list:
                if self.speed_x > 0:
                    self.speed_x = 0
                    self.rect.right = hit_list[0].rect.left
                elif self.speed_x < 0:
                    self.speed_x = 0
                    self.rect.left = hit_list[0].rect.right
        elif dir == 'y':
            hit_list = pygame.sprite.spritecollide(self, g.platforms, False)
            if hit_list:
                self.speed_y = 0
                self.jumping = False
                self.rect.bottom = hit_list[0].rect.top

    def animate(self):
        now = pygame.time.get_ticks()
        if self.hit:
            if now - self.hit_time < 300:
                if self.dir == 'l':
                    self.image = self.frames_hit_l[0]
                else:
                    self.image = self.frames_hit_r[0]
                return
            else:
                self.hit = False
                self.last_update = self.hit_time
        if self.speed_x != 0 and not self.jumping:
            self.walking = True
        if self.speed_y > 0 and not self.jumping:
            self.jumping = True
            self.walking = False
        # first, if we're not moving, just idle
        if not self.walking and not self.jumping:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % 2
                if self.dir == 'l':
                    self.image = self.frames_standing_l[self.current_frame]
                else:
                    self.image = self.frames_standing_r[self.current_frame]
            return
        # if we're walking, animate in the proper direction
        if self.walking:
            if now - self.last_update > 75:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % 6
                if self.dir == 'r':
                    self.image = self.frames_running_r[self.current_frame]
                else:
                    self.image = self.frames_running_l[self.current_frame]
        # not walking, but jumping or falling
        else:
            if self.speed_y > 0:
                if self.dir == 'l':
                    self.image = self.frames_jumping_ul[0]
                else:
                    self.image = self.frames_jumping_ur[0]
            else:
                if self.dir == 'l':
                    self.image = self.frames_jumping_dl[0]
                else:
                    self.image = self.frames_jumping_dr[0]

    def hit_enemy(self):
        # if you just hit, can't immediately hit again
        if not self.hit:
            self.hit = True
            self.jumping = True
            self.life -= 1
            self.hit_time = pygame.time.get_ticks()
            if self.dir == 'l':
                self.speed_x = self.speed
            else:
                self.speed_x = -self.speed
            # could hit from above or below
            if self.speed_y >= 0:
                self.speed_y = -12
            else:
                self.speed_y = 8

    def jump(self):
        # need to see if there's a platform under us.  If not, can't jump
        # move down a little bit and see if there's a collision
        self.rect.y += 1
        hit_list = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hit_list and not self.jumping:
            self.game.player_jump_snd.play()
            self.jumping = True
            self.walking = False
            self.speed_y -= self.jump_speed


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, game, kind, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.kind = kind
        self.frames = []
        self.current_frame = 0
        self.last_update = 0
        self.last_shimmer = 0
        self.shimmer = False
        if kind == 'heart':
            for x in range(450, 850, 50):
                image = self.game.sprite_sheet.get_image(x, 45, 50, 45)
                self.frames.append(image)
        elif kind == 'boost':
            for x in range(400, 900, 50):
                image = self.game.sprite_sheet.get_image(x, 100, 50, 50)
                self.frames.append(image)
        self.image = self.frames[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_shimmer > 10000:
            self.shimmer = not self.shimmer
            self.last_shimmer = now
            self.image = self.frames[0]
            self.current_frame = 0
        if self.shimmer:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame += 1
                if self.current_frame == len(self.frames) - 1:
                    self.shimmer = False
                    self.image = self.frames[0]
                else:
                    self.image = self.frames[self.current_frame]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, mid_x, bottom):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.current_frame = 0
        self.frames_l = []
        self.frames_r = []
        self.last_update = 0
        for y in range(240, 336, 48):
            for x in range(0, 395, 79):
                image = self.game.sprite_sheet.get_image(x, y, 79, 48)
                self.frames_r.append(image)
                image = pygame.transform.flip(image, True, False)
                self.frames_l.append(image)
        if random.randrange(2) == 0:
            self.dir = 'l'
            self.current_frame = random.randrange(len(self.frames_l))
            self.image = self.frames_l[self.current_frame]
        else:
            self.dir = 'r'
            self.current_frame = random.randrange(len(self.frames_r))
            self.image = self.frames_r[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = mid_x
        self.rect.bottom = bottom

    def update(self):
        self.animate()

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 175:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % 10
            if self.dir == 'l':
                self.image = self.frames_l[self.current_frame]
            else:
                self.image = self.frames_r[self.current_frame]


class Platform(pygame.sprite.Sprite):
    # platform objects - green rectangles
    def __init__(self, game, x, y, size):
        # platform init - set location and size (width)
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = game.sprite_sheet.get_image(0, 384, size*48, 48)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def offscreen(self):
        # check to see if the platform has moved off the bottom of the screen
        if self.rect.top > HEIGHT + 5:
            return True
        return False


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        game_dir = path.dirname(__file__)
        img_dir = path.join(game_dir, 'img')
        snd_dir = path.join(game_dir, 'snd')
        self.sprite_sheet = SpriteSheet(path.join(img_dir, "jump_sprites_sm.png"))
        self.player_jump_snd = pygame.mixer.Sound(path.join(snd_dir, 'jump_10.wav'))
        self.player_jump_snd.set_volume(0.5)
        pygame.mixer.music.load(path.join(snd_dir, "Casual game track.ogg"))
        pygame.mixer.music.set_volume(0.5)

    def new(self):
        # initialize for a new game
        self.running = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player, layer=1)
        self.score = 0
        self.create_start_layout()
        pygame.mixer.music.play(loops=-1)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.stop()

    def quit(self):
        pygame.quit()
        sys.exit()

    def events(self):
        # handle all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key in [pygame.K_UP, pygame.K_SPACE]:
                    self.player.jump()

    def draw(self):
        # TODO: always draw player on top
        self.screen.fill(BGCOLOR)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        self.draw_hearts()
        fps_txt = "{:.2f}".format(self.clock.get_fps())
        self.draw_text(str(fps_txt), 18, WIDTH-50, 10)
        # draw score
        pygame.display.flip()

    def draw_text(self, text, size, x, y):
        # utility function to draw text at a given location
        # TODO: move font matching to beginning of file (don't repeat)
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def create_start_layout(self):
        # create the starting platforms
        platform_list = [[0, HEIGHT-48, 10],
                         [25, 448, 2],
                         [220, 305, 3],
                         [25, 120, 4],
                         [320, 10, 3]]
        for loc in platform_list:
            plat = Platform(self, loc[0], loc[1], loc[2])
            self.all_sprites.add(plat)
            self.platforms.add(plat)
        # one enemy
        enemy = Enemy(self, 111, 120)
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)
        # a powerup
        pow = PowerUp(self, 'boost', 10, 10)
        self.powerups.add(pow)
        self.all_sprites.add(pow)

    def update(self):
        # shift all platforms down when player jumps into the top 1/4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            for sprite in self.all_sprites:
                sprite.rect.y += max(abs(self.player.speed_y), 8)

        # only collide with the platforms if falling down
        if self.player.speed_y > 0:
            hit_list = pygame.sprite.spritecollide(self.player,
                                                   self.platforms, False)
                                                   # pygame.sprite.collide_mask)
            if hit_list:
                plat = self.find_lowest(hit_list)
                if self.player.rect.bottom < plat.rect.bottom:
                    if self.player.rect.right > plat.rect.left+24 and self.player.rect.left < plat.rect.right-24:
                        self.player.speed_y = 0
                        self.player.jumping = False
                        self.player.rect.bottom = plat.rect.top

        # hit enemies
        hit_list = pygame.sprite.spritecollide(self.player, self.enemies,
                                               False, pygame.sprite.collide_mask)
        if hit_list:
            # bounce in the air and change briefly to hit image
            self.player.hit_enemy()

        # hit powerups
        hit_list = pygame.sprite.spritecollide(self.player, self.powerups,
                                               True, pygame.sprite.collide_mask)
        if hit_list:
            if hit_list[0].kind == 'heart':
                # self.heart_snd.play()
                self.player.life += 1
                if self.player.life > 3:
                    self.player.life = 3
            elif hit_list[0].kind == 'boost':
                # self.boost_snd.play()
                self.player.speed_y -= 75

        # delete platforms and enemies that fall off the screen
        # and create new ones to replace
        for enemy in self.enemies:
            if enemy.rect.top > HEIGHT + 5:
                enemy.kill()
        for plat in self.platforms:
            if plat.offscreen():
                plat.kill()
                # new platform is created off the top of the screen
                delta = 180 + random.randrange(10, 30)
                newplat = Platform(self, random.randrange(-10, WIDTH-40),
                                   self.player.rect.y-delta,
                                   random.randrange(2, 5))
                self.all_sprites.add(newplat)
                self.platforms.add(newplat)
                self.score += 10
                if random.random() > 0.9:
                    kind = random.choice(['boost', 'heart'])
                    pow = PowerUp(self, kind, random.randrange(5, WIDTH-55),
                                  -50)
                    self.powerups.add(pow)
                    self.all_sprites.add(pow)

        # die
        if self.player.life == 0:
            self.running = False
        if self.player.rect.bottom > HEIGHT-20:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.speed_y, 10)
                if sprite.rect.bottom < -100:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.running = False

    def find_lowest(self, sprites):
        # find the lowest (highest y) sprite in a list of sprites
        lowest = None
        y = 0
        for sprite in sprites:
            if sprite.rect.y > y:
                y = sprite.rect.y
                lowest = sprite
        return lowest

    def start_screen(self):
        pass

    def go_screen(self):
        pass

    def draw_hearts(self):
        img = self.sprite_sheet.get_image(450, 45, 50, 45)
        rect = img.get_rect()
        for i in range(self.player.life):
            rect.x = i * 50
            rect.y = 10
            self.screen.blit(img, rect)

g = Game()
while True:
    g.start_screen()
    g.new()
    g.run()
    g.go_screen()
