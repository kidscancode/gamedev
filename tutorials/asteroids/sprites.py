import pygame as pg
from random import choice, randint, uniform
from settings import *
import xml.etree.ElementTree as ET
vec = pg.math.Vector2

class SpritesheetWithXML:
    # utility class for loading and parsing spritesheets
    # xml filename should match png filename
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename + '.png').convert_alpha()
        # self.spritesheet.set_colorkey(BLACK)
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

    def get_image_by_name(self, name):
        #print("getting image {}".format(name))
        r = pg.Rect(self.map[name]['x'], self.map[name]['y'],
                    self.map[name]['w'], self.map[name]['h'])
        return self.spritesheet.subsurface(r)

class Shield(pg.sprite.Sprite):
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
        self.ship.shield = self

    def update(self):
        self.image = pg.transform.rotate(self.game.shield_images[self.level], self.ship.rot)
        self.rect = self.image.get_rect()
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
        self.last_hyper = 0
        self.bombs = 5
        self.last_bomb = 0
        self.gun_level = 1
        self.shield = None

    def get_keys(self):
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keystate[pg.K_RIGHT]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keystate[pg.K_UP]:
            self.acc = vec(0, -self.thrust_power).rotate(-self.rot)
        if keystate[pg.K_SPACE]:
            self.shoot()
        if keystate[pg.K_z]:
            self.hyper()
        if keystate[pg.K_x]:
            self.drop_bomb()

    def drop_bomb(self):
        now = pg.time.get_ticks()
        if now - self.last_bomb > BOMB_RATE:
            if self.bombs > 0:
                self.last_bomb = now
                Bomb(self, 0, -40)
                self.bombs -= 1

    def hyper(self):
        if self.hyper_charge:
            self.game.hyper_sound.play()
            self.vel = vec(0, 0)
            self.pos = vec(randint(0, WIDTH - self.rect.width),
                           randint(0, HEIGHT - self.rect.height))
            self.hyper_charge = False

    def shoot(self):
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
        # recharge hyperspace if not charged
        if not self.hyper_charge:
            now = pg.time.get_ticks()
            if now - self.last_hyper > HYPER_CHARGE_TIME:
                self.last_hyper = now
                self.hyper_charge = True

        self.rot_speed = 0
        self.acc = vec(0, 0)
        self.get_keys()
        self.rotate()
        self.acc += self.vel * -self.friction
        self.vel += self.acc
        if self.vel.length_squared() > PLAYER_MAX_SPEED ** 2:
            self.vel = self.vel.normalize() * PLAYER_MAX_SPEED
        self.pos += self.vel + 0.5 * self.acc
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
        self.size = size
        if self.size == 'sonic':
            self.game.bomb_explosions.add(self)
            self.frame_rate = 75
            choice(self.game.bomb_exp_sounds).play()
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
        self.groups = game.all_sprites, game.powerups
        self._layer = POW_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.type = choice(list(POW_IMAGES.keys()))
        self.game = game
        self.image = game.spritesheet.get_image_by_name(POW_IMAGES[self.type])
        self.rect = self.image.get_rect()
        self.pos = pos
        self.vel = vec(uniform(0.5, 1.5), 0).rotate(uniform(0, 360))
        self.rect.center = self.pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > POW_LIFETIME:
            self.kill()
        self.pos += self.vel
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
    def __init__(self, game):
        self.groups = game.all_sprites, game.aliens
        self._layer = PLAYER_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.spritesheet.get_image_by_name(ALIEN_IMAGE)
        self.image = pg.transform.rotozoom(self.image, 0, ALIEN_SCALE)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.pos = vec(-self.rect.width * 2, randint(50, HEIGHT - 50))
        self.vel = vec(uniform(ALIEN_SPEED_MIN, ALIEN_SPEED_MAX), 0).rotate(uniform(-10, 10))
        self.rect.center = self.pos
        self.last_shot = pg.time.get_ticks()
        self.health = ALIEN_HITS

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > ALIEN_FIRE_RATE:
            self.last_shot = now
            ABullet(self.game, self)
        self.pos += self.vel
        self.rect.center = self.pos
        if self.rect.left > WIDTH:
            self.game.last_alien = pg.time.get_ticks()
            self.kill()

class Rock(pg.sprite.Sprite):
    # rock sizes 0-3 (3 biggest)
    def __init__(self, game, size, center):
        self.groups = game.all_sprites, game.rocks
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
        self.pos += self.vel
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
        self.vel = -vec(0, BOMB_SPEED).rotate(-ship.rot)
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
        self.pos += self.vel
        self.rect.center = self.pos

class Bullet(pg.sprite.Sprite):
    def __init__(self, img, ship, dx, dy, rot=0):
        self.groups = ship.game.all_sprites, ship.game.bullets
        self._layer = BULLET_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = ship.game.spritesheet.get_image_by_name(img)
        self.image = pg.transform.rotozoom(self.image, 0, BULLET_SCALE)
        self.image = pg.transform.rotate(self.image, ship.rot + rot)
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = ship.pos - vec(dx, dy).rotate(-ship.rot)
        self.vel = ship.vel + -vec(0, BULLET_SPEED).rotate(-ship.rot - rot)
        self.rect.center = self.pos
        # self.vel = -pg.math.Vector2(0, 12).rotate(-self.ship.rot)
        self.spawn_time = pg.time.get_ticks()
        choice(ship.game.bullet_sounds).play()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.spawn_time > BULLET_LIFETIME:
            self.kill()
        self.pos += self.vel
        self.rect.center = self.pos

class ABullet(pg.sprite.Sprite):
    def __init__(self, game, ship):
        self.groups = game.all_sprites, game.alien_bullets
        self._layer = ROCK_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = ship.pos + vec(0, 0)
        self.image = self.game.spritesheet.get_image_by_name(ALIEN_BULLET_IMAGE)
        self.image = pg.transform.rotozoom(self.image, 0, BULLET_SCALE)
        # self.dir = degrees(atan2(self.game.player.pos.y - self.pos.y, self.game.player.pos.x - self.pos.x)) + 90
        # self.dir = 90
        self.dir = vec(self.game.player.pos.x - self.pos.x, self.game.player.pos.y - self.pos.y).as_polar()[1] + 90
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
        self.pos += self.vel
        self.rect.center = self.pos
