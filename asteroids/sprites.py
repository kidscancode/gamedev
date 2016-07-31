import pygame as pg
from os import path
from random import choice, randint, uniform
from settings import *
from particles import *
import xml.etree.ElementTree as ET
vec = pg.math.Vector2
# TODO: organize (separate files?)
# TODO: consolidate common sprite parameters (base class?)

class SpritesheetWithXML:
    # utility class for loading and parsing spritesheets
    # xml filename should match png filename (Kenney format)
    # TODO: improve to work with other data formats
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename + '.png').convert_alpha()
        # self.spritesheet.set_colorkey(BLACK)
        # load XML (kenney format) if it exists
        if path.isfile(filename + '.xml'):
            tree = ET.parse(filename + '.xml')
            self.map = {}
            # read through XML and pull out image locations using the following structure:
            # self.map['image name'] = {'x':x, 'y':y, 'w':w, 'h':h}
            for node in tree.iter():
                if node.attrib.get('name'):
                    name = node.attrib.get('name')
                    self.map[name] = {}
                    self.map[name]['x'] = int(node.attrib.get('x'))
                    self.map[name]['y'] = int(node.attrib.get('y'))
                    self.map[name]['w'] = int(node.attrib.get('width'))
                    self.map[name]['h'] = int(node.attrib.get('height'))

    def get_image_by_rect(self, x, y, w, h):
        r = pg.Rect(x, y, w, h)
        return self.spritesheet.subsurface(r)

    def get_image_by_name(self, name):
        # TODO: error message if no xml exists
        r = pg.Rect(self.map[name]['x'], self.map[name]['y'],
                    self.map[name]['w'], self.map[name]['h'])
        return self.spritesheet.subsurface(r)

class EmptySprite(pg.sprite.Sprite):
    # invisible placeholder, for testing safe teleport locations
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Shield(pg.sprite.Sprite):
    # TODO: make generic for use with non-player sprites
    def __init__(self, game, ship):
        self.groups = game.all_sprites
        self._layer = ship._layer + 1
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.ship = ship
        self.level = 2
        self.image = pg.transform.rotate(self.game.shield_images[0], self.ship.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.ship.pos
        self.pos = self.ship.pos
        self.ship.shield = self

    def update(self):
        self.image = pg.transform.rotate(self.game.shield_images[self.level], self.ship.rot)
        self.rect = self.image.get_rect()
        self.pos = self.ship.pos
        self.rect.center = self.ship.pos

class Player(pg.sprite.Sprite):
    def __init__(self, game, img):
        self.groups = game.all_sprites
        self._layer = PLAYER_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet.get_image_by_name(img)
        self.image = pg.transform.rotozoom(self.image, 0, PLAYER_SCALE)
        self.image_clean = self.image.copy()
        self.life_image = self.game.spritesheet.get_image_by_name(PLAYER_LIFE_IMG)
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.rot = 0
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.thrust_power = PLAYER_THRUST
        self.friction = PLAYER_FRICTION
        self.shoot_delay = BULLET_RATE
        self.last_shot = pg.time.get_ticks()
        self.hyper_charge = True
        self.last_hyper = pg.time.get_ticks()
        self.wpn2_type = WEAPON2_AT_SPAWN
        # TODO: remove
        self.bombs = 5
        self.last_bomb = 0
        self.gun_level = GUN_LEVEL_AT_SPAWN
        self.shield = None
        if SHIELD_AT_SPAWN:
            Shield(self.game, self)
        self.lives = LIVES_AT_SPAWN
        self.hidden = False
        self.hide_timer = 0
        self.beam_firing = False
        self.engine_emitter = ParticleEmitter(self.game, self, PLAYER_THRUST_OFFSET, PLAYER_THRUST_VEL,
                                              game.ship_particle_img, PLAYER_THRUST_COUNT, PLAYER_THRUST_LIFETIME,
                                              PLAYER_THRUST_FADE, PLAYER_THRUST_SIZE, PLAYER_THRUST_ANGLE)

    def unhide(self):
        # spawn safely (no obstacles at desired pos)
        self.placeholder = EmptySprite(self.dest.x, self.dest.y, self.rect.width * 2, self.rect.height * 2)

        hits = pg.sprite.spritecollideany(self.placeholder, self.game.mobs, False)
        if not hits:
            self.hidden = False
            self.pos = self.dest
            self.vel = vec(0, 0)

    def hide(self):
        # hide player temporarily (between deaths or when using hyper)
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.pos = vec(WIDTH + 1000, HEIGHT + 1000)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def get_keys(self):
        # TODO: add WASD?
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            if not self.beam_firing:
                self.rot_speed = PLAYER_ROT_SPEED
        if keystate[pg.K_RIGHT]:
            if not self.beam_firing:
                self.rot_speed = -PLAYER_ROT_SPEED
        if keystate[pg.K_UP]:
            self.acc = vec(0, -self.thrust_power).rotate(-self.rot)
            self.engine_emitter.count = 50
        if keystate[pg.K_SPACE]:
            self.shoot()
        if keystate[pg.K_z]:
            self.hyper()
        if keystate[pg.K_x]:
            self.shoot_wpn2()

    def shoot_wpn2(self):
        if self.wpn2_type == 'bomb':
            self.drop_bomb()
        elif self.wpn2_type == 'beam':
            self.fire_beam()
        elif self.wpn2_type is None:
            pass
            # TODO: play "click" sound

    def fire_beam(self):
        now = pg.time.get_ticks()
        if now - self.last_bomb > BEAM_RATE:
            self.last_bomb = now
            Beam(self, 0, 120)
            self.beam_firing = True

    def drop_bomb(self):
        # TODO: final decision on bomb ammo
        now = pg.time.get_ticks()
        if now - self.last_bomb > BOMB_RATE:
            # if self.bombs > 0:
            self.last_bomb = now
            Bomb(self, 0, -40)
            # self.bombs -= 1

    def die(self):
        self.lives -= 1
        self.hide()
        self.dest = vec(WIDTH / 2, HEIGHT / 2)
        self.gun_level = 1
        if SHIELD_AT_SPAWN:
            Shield(self.game, self)

    def hyper(self):
        if self.hyper_charge:
            self.game.hyper_sound.play()
            self.hide()
            self.dest = vec(randint(30, WIDTH - self.rect.width - 30),
                            randint(30, HEIGHT - self.rect.height - 30))
            self.hyper_charge = False
            self.last_hyper = pg.time.get_ticks()

    def shoot(self):
        # TODO: ugly - improve this
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.gun_level == 1:
                self.shoot_delay = BULLET_RATE
                Bullet(BULLET_IMG, self, 0, 30)
            if self.gun_level == 2:
                self.shoot_delay = BULLET_RATE
                Bullet(BULLET_IMG, self, 23, 18)
                Bullet(BULLET_IMG, self, -23, 18)
            if self.gun_level == 3:
                self.shoot_delay = BULLET_RATE
                Bullet(BULLET_IMG, self, 0, 30)
                Bullet(BULLET_IMG, self, 5, 30, rot=15)
                Bullet(BULLET_IMG, self, -5, 30, rot=-15)
            if self.gun_level == 4:
                self.shoot_delay = BULLET_RATE - 100
                Bullet(BULLET_IMG, self, 0, 30)
                Bullet(BULLET_IMG, self, 5, 30, rot=15)
                Bullet(BULLET_IMG, self, -5, 30, rot=-15)
                Bullet(BULLET_IMG, self, 8, 30, rot=25)
                Bullet(BULLET_IMG, self, -8, 30, rot=-25)

    def rotate(self):
        self.rot = (self.rot + self.rot_speed) % 360
        if self.rot in self.game.rot_cache['player']:
            image = self.game.rot_cache['player'][self.rot]
        else:
            image = pg.transform.rotate(self.image_clean, self.rot)
            self.game.rot_cache['player'][self.rot] = image
        old_center = self.rect.center
        self.image = image
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=old_center)

    def update(self):
        # unhide if hidden
        if self.hidden and pg.time.get_ticks() - self.hide_timer > 1000:
            self.unhide()

        # recharge hyperspace if not fully charged
        if not self.hyper_charge:
            now = pg.time.get_ticks()
            if now - self.last_hyper > HYPER_CHARGE_TIME:
                self.last_hyper = now
                self.hyper_charge = True

        self.rot_speed = 0
        self.acc = vec(0, 0)
        self.engine_emitter.count = 0
        if not self.hidden:
            self.get_keys()
        self.rotate()
        self.engine_emitter.update()
        self.acc += self.vel * -self.friction
        self.vel += self.acc * self.game.dt
        if self.vel.length_squared() > PLAYER_MAX_SPEED ** 2:
            self.vel = self.vel.normalize() * PLAYER_MAX_SPEED
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        if not self.hidden:
            if self.pos.x > WIDTH:
                self.pos.x = 0
            if self.pos.x < 0:
                self.pos.x = WIDTH
            if self.pos.y > HEIGHT:
                self.pos.y = 0
            if self.pos.y < 0:
                self.pos.y = HEIGHT
        self.rect.center = self.pos

class Explosion(pg.sprite.Sprite):
    def __init__(self, game, center, size):
        self.groups = game.all_sprites
        self._layer = EXPLOSION_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = center
        self.size = size
        if self.size == 'sonic':
            self.game.bomb_explosions.add(self)
            self.frame_rate = 75
            sound = choice(self.game.bomb_exp_sounds)
            if sound.get_num_channels() < 2:
                sound.play()
            self.game.offset = self.game.shake(amount=12, times=2)

        else:
            self.frame_rate = 55
            choice(self.game.rock_exp_sounds).play()
            self.game.offset = self.game.shake(amount=8, times=2)
        self.image = self.game.expl_frames[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.game.expl_frames[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.game.expl_frames[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Pow(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.powerups, game.mobs
        self._layer = POW_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.type = choice(list(POW_IMAGES.keys()))
        self.game = game
        self.image = game.spritesheet.get_image_by_name(POW_IMAGES[self.type])
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.pos = pos
        self.vel = vec(uniform(POW_MIN_SPEED, POW_MAX_SPEED), 0).rotate(uniform(0, 360))
        self.rect.center = self.pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > POW_LIFETIME:
            self.kill()
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if self.rect.right < 0:
            self.pos.x = WIDTH + self.rect.width / 2
        if self.rect.left > WIDTH:
            self.pos.x = -self.rect.width / 2
        if self.rect.bottom < 0:
            self.pos.y = HEIGHT + self.rect.height / 2
        if self.rect.top > HEIGHT:
            self.pos.y = -self.rect.height / 2

class Alien(pg.sprite.Sprite):
    # TODO: different types
    # TODO: different movement patterns
    def __init__(self, game):
        self.groups = game.all_sprites, game.aliens, game.mobs
        self._layer = PLAYER_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.spritesheet.get_image_by_name(ALIEN_IMAGE)
        self.image = pg.transform.rotozoom(self.image, 0, ALIEN_SCALE)
        self.image_orig = self.image.copy()
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        # create a white image from mask for damage flash
        self.dmg_flash = self.image.copy()
        for x in range(self.rect.width):
            for y in range(self.rect.height):
                if self.mask.get_at((x, y)):
                    pg.draw.circle(self.dmg_flash, WHITE, (x, y), 1)
        self.pos = vec(-self.rect.width * 2, randint(50, HEIGHT - 50))
        self.vel = vec(uniform(ALIEN_SPEED_MIN, ALIEN_SPEED_MAX), 0).rotate(uniform(-15, 15))
        self.rect.center = self.pos
        self.last_shot = pg.time.get_ticks()
        self.health = ALIEN_HITS
        self.spawn_time = pg.time.get_ticks()
        self.size = 0
        self.fire_rate = max(500, ALIEN_FIRE_RATE - 500 * game.level // 3)
        self.hit_time = 0

    def hit(self):
        self.hit_time = pg.time.get_ticks()
        self.image = self.dmg_flash
        self.health -= 1

    def update(self):
        now = pg.time.get_ticks()
        if now - self.hit_time > 100:
            self.image = self.image_orig
        if now - self.last_shot > self.fire_rate:
            # TODO: ugly - clean this up
            self.last_shot = now
            self.game.alien_fire_sound.play()
            if self.game.level < 5:
                ABullet(self.game, self)
            elif self.game.level < 10:
                ABullet(self.game, self, 25)
                ABullet(self.game, self)
                ABullet(self.game, self, -25)
            else:
                ABullet(self.game, self, 30)
                ABullet(self.game, self, 15)
                ABullet(self.game, self)
                ABullet(self.game, self, -15)
                ABullet(self.game, self, -30)

        self.pos += self.vel * self.game.dt
        # sine wave pattern
        # self.pos.y = 50 * math.sin((pg.time.get_ticks() - self.spawn_time) / 1000 * 0.5 * math.pi)
        self.rect.center = self.pos
        if self.rect.left > WIDTH:
            self.game.last_alien = pg.time.get_ticks()
            self.kill()

class Rock(pg.sprite.Sprite):
    # rock sizes 0-3 (3 biggest)
    def __init__(self, game, size, center):
        self.groups = game.all_sprites, game.rocks, game.mobs
        self._layer = ROCK_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size = size
        self.game = game
        self.img_name = choice(ROCK_IMAGES[size])
        self.image = game.spritesheet.get_image_by_name(self.img_name)
        self.image_clean = self.image.copy()
        self.rect = self.image.get_rect()
        self.pos = vec(0, 0)
        self.vel = vec(uniform(ROCK_SPEED_MIN, ROCK_SPEED_MAX), 0).rotate(uniform(0, 360))
        self.rot = 0
        self.rot_speed = choice([-1.5, -1, -0.5, 0.5, 1, 1.5])
        if center is None:
            edge = choice(['h', 'v'])
            if edge == 'h':
                self.pos.x = -self.rect.width
                self.pos.y = randint(0, HEIGHT)
            elif edge == 'v':
                self.pos.y = -self.rect.height
                self.pos.x = randint(0, WIDTH)
        else:
            self.pos = center
        self.rect.center = self.pos

    def rotate(self):
        self.rot = (self.rot + self.rot_speed) % 360
        if self.rot in self.game.rot_cache['rock'][self.img_name]:
            image = self.game.rot_cache['rock'][self.img_name][self.rot]
        else:
            image = pg.transform.rotate(self.image_clean, self.rot)
            self.game.rot_cache['rock'][self.img_name][self.rot] = image
        old_center = self.rect.center
        self.image = image
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=old_center)

    def update(self):
        self.rotate()
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if self.rect.right < 0:
            self.pos.x = WIDTH + self.rect.width / 2
        if self.rect.left > WIDTH:
            self.pos.x = -self.rect.width / 2
        if self.rect.bottom < 0:
            self.pos.y = HEIGHT + self.rect.height / 2
        if self.rect.top > HEIGHT:
            self.pos.y = -self.rect.height / 2

class Bomb(pg.sprite.Sprite):
    def __init__(self, ship, dx, dy):
        self.groups = ship.game.all_sprites, ship.game.bullets
        self._layer = BULLET_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = ship.game
        self.frames = []
        for img in BOMB_IMAGES:
            img = ship.game.spritesheet.get_image_by_name(img)
            img = pg.transform.rotozoom(img, 0, BOMB_SCALE)
            self.frames.append(img)
        self.pos = ship.pos - vec(dx, dy).rotate(-ship.rot)
        self.vel = vec(0, BOMB_SPEED).rotate(-ship.rot)
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.frame = 0
        self.frame_rate = 1000
        self.rot = 0
        self.rot_speed = 1
        self.rot_cache = {}
        self.spawn_time = pg.time.get_ticks()
        self.last_update = pg.time.get_ticks()
        self.game.bomb_launch_sound.play()

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.spawn_time > BOMB_LIFETIME * 2 / 3:
            self.frame_rate = 200
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.game.bomb_tick_sound.play()
            self.frame = (self.frame + 1) % len(self.frames)
            self.image = self.frames[self.frame]
        self.rot = (self.rot + self.rot_speed) % 360
        if self.rot in self.rot_cache:
            image = self.rot_cache[self.rot]
        else:
            image = pg.transform.rotate(self.frames[self.frame], self.rot)
            self.rot_cache[self.rot] = image
        old_center = self.rect.center
        self.image = image
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=old_center)

    def explode(self):
        Explosion(self.game, self.rect.center, 'sonic')
        self.kill()

    def update(self):
        self.animate()
        now = pg.time.get_ticks()
        if now - self.spawn_time > BOMB_LIFETIME:
            self.explode()
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

class Beam(pg.sprite.Sprite):
    # TODO: find good art for this
    # TODO: allow/disallow move/rotate while firing?
    def __init__(self, ship, dx, dy):
        self.groups = ship.game.all_sprites, ship.game.bullets
        self._layer = BULLET_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.ship = ship
        self.offset = vec(dx, dy)
        self.images = [pg.transform.scale(ship.game.spritesheet.get_image_by_name('laserRed14.png'), (13, 200)),
                       pg.transform.scale(ship.game.spritesheet.get_image_by_name('laserRed15.png'), (13, 200))]
        self.image = pg.transform.rotate(self.images[0], self.ship.rot)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = self.ship.pos - self.offset.rotate(-self.ship.rot)
        self.spawn_time = pg.time.get_ticks()
        choice(ship.game.bullet_sounds).play()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.spawn_time > BEAM_LIFETIME:
            self.ship.beam_firing = False
            self.kill()
        self.image = pg.transform.rotate(self.images[0], self.ship.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.ship.pos - self.offset.rotate(-self.ship.rot)

class Bullet(pg.sprite.Sprite):
    def __init__(self, img, ship, dx, dy, rot=0):
        self.groups = ship.game.all_sprites, ship.game.bullets
        self._layer = BULLET_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = ship.game
        # self.image = ship.game.spritesheet.get_image_by_name(img)
        self.image = pg.transform.scale(ship.game.beam_sheet.get_image_by_rect(135, 309, 54, 97), (41, 73))  # lt blue
        # TODO: all these colors - customize?
        # self.image = ship.game.beam_sheet.get_image_by_rect(227, 210, 48, 85)  # purple
        # self.image = ship.game.beam_sheet.get_image_by_rect(294, 26, 71, 120)  # dk blue
        # self.image = ship.game.beam_sheet.get_image_by_rect(38, 168, 17, 33)  # sm red
        # self.image = ship.game.beam_sheet.get_image_by_rect(39, 53, 17, 33)  # sm green
        # self.image = ship.game.beam_sheet.get_image_by_rect(118, 58, 17, 33)  # sm purple
        self.image = pg.transform.rotozoom(self.image, 0, BULLET_SCALE)
        self.image = pg.transform.rotate(self.image, ship.rot + rot)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.pos = ship.pos - vec(dx, dy).rotate(-ship.rot)
        self.vel = ship.vel + -vec(0, BULLET_SPEED).rotate(-ship.rot - rot)
        self.rect.center = self.pos
        self.spawn_time = pg.time.get_ticks()
        choice(ship.game.bullet_sounds).play()

    def update(self):
        # TODO: should bullets wrap?
        now = pg.time.get_ticks()
        if now - self.spawn_time > BULLET_LIFETIME:
            self.kill()
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

class ABullet(pg.sprite.Sprite):
    def __init__(self, game, ship, angle=0):
        self.groups = game.all_sprites, game.mobs
        self._layer = ROCK_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = ship.pos + vec(0, 0)
        self.image = self.game.spritesheet.get_image_by_name(ALIEN_BULLET_IMAGE)
        self.image = self.game.beam_sheet.get_image_by_rect(236, 6, 49, 83)
        self.image = pg.transform.rotozoom(self.image, 0, BULLET_SCALE)
        self.dir = vec(self.game.player.pos.x - self.pos.x, self.game.player.pos.y - self.pos.y).as_polar()[1] + 90
        self.dir += angle
        self.image = pg.transform.rotate(self.image, -self.dir)
        self.vel = ship.vel + -vec(0, ALIEN_BULLET_SPEED).rotate(self.dir)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = self.pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.spawn_time > ALIEN_BULLET_LIFETIME:
            self.kill()
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
