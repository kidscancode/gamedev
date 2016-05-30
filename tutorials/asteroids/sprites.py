import pygame as pg
from random import choice, randint
from settings import *
import xml.etree.ElementTree as ET

class SpritesheetWithXML:
    # utility class for loading and parsing spritesheets
    # xml filename should match png filename
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename + '.png').convert()
        tree = ET.parse(filename + '.xml')
        self.map = {}
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
        x = self.map[name]['x']
        y = self.map[name]['y']
        w = self.map[name]['w']
        h = self.map[name]['h']
        return self.get_image(x, y, w, h)

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game, img, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.game = game
        self.image = self.game.spritesheet.get_image_by_name(img)
        self.image = pg.transform.rotozoom(self.image, 0, PLAYER_SCALE)
        self.image.set_colorkey(BLACK)
        self.image_clean = self.image.copy()
        self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.rot = 0
        self.rot_cache = {}
        self.pos = pg.math.Vector2(WIDTH / 2, HEIGHT / 2)
        self.vel = pg.math.Vector2(0, 0)
        self.acc = pg.math.Vector2(0, 0)
        self.thrust_power = 0.2
        self.friction = 0.02
        self.shoot_delay = 250
        self.last_shot = pg.time.get_ticks()

    def get_keys(self):
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.rot_speed = 2
        if keystate[pg.K_RIGHT]:
            self.rot_speed = -2
        if keystate[pg.K_UP]:
            self.acc = pg.math.Vector2(0, -self.thrust_power).rotate(-self.rot)
        if keystate[pg.K_SPACE]:
            self.shoot()

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            Bullet(BULLET_IMG, self, [self.game.all_sprites, self.game.bullets])

    def rotate(self):
        self.rot = (self.rot + self.rot_speed) % 360
        if self.rot in self.rot_cache:
            image = self.rot_cache[self.rot]
        else:
            image = pg.transform.rotate(self.image_clean, self.rot)
            self.rot_cache[self.rot] = image
        old_center = self.rect.center
        self.image = image
        self.rect = self.image.get_rect(center=old_center)

    def update(self):
        self.rot_speed = 0
        self.acc = pg.math.Vector2(0, 0)
        self.get_keys()
        self.rotate()
        self.acc += self.vel * -self.friction
        self.vel += self.acc
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

class Pow(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        # if size ==
        self.image = explosion_anim[self.size][0]
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
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Rock(pg.sprite.Sprite):
    # rock sizes 0-3 (3 biggest)
    def __init__(self, game, size, center, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.size = size
        self.game = game
        self.image = game.spritesheet.get_image_by_name(choice(game.rock_images[size]))
        self.image.set_colorkey(BLACK)
        self.image_clean = self.image.copy()
        self.rect = self.image.get_rect()
        self.rot_cache = {}
        self.rot = 0
        self.rot_speed = choice([-1.5, -1, -0.5, 0.5, 1, 1.5])
        if self.size == 3:
            edge = choice(['h', 'v'])
            if edge == 'h':
                self.rect.x = -self.rect.width
                self.rect.y = randint(0, HEIGHT)
            elif edge == 'v':
                self.rect.y = -self.rect.height
                self.rect.x = randint(0, WIDTH)
        else:
            self.rect.center = center
        self.vx, self.vy = randint(-3, 3), randint(-3, 3)

    def rotate(self):
        self.rot = (self.rot + self.rot_speed) % 360
        if self.rot in self.rot_cache:
            image = self.rot_cache[self.rot]
        else:
            image = pg.transform.rotate(self.image_clean, self.rot)
            self.rot_cache[self.rot] = image
        old_center = self.rect.center
        self.image = image
        self.rect = self.image.get_rect(center=old_center)

    def update(self):
        # self.rotate()
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

class Bullet(pg.sprite.Sprite):
    def __init__(self, img, ship, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = ship.game.spritesheet.get_image_by_name(img)
        self.image = pg.transform.rotozoom(self.image, 0, BULLET_SCALE)
        self.image = pg.transform.rotate(self.image, ship.rot)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = ship.pos - pg.math.Vector2(0, 20).rotate(-ship.rot)
        self.vel = ship.vel + -pg.math.Vector2(0, 8).rotate(-ship.rot)
        self.rect.center = self.pos
        # self.vel = -pg.math.Vector2(0, 12).rotate(-self.ship.rot)
        self.spawn_time = pg.time.get_ticks()
        self.lifetime = 2000

    def update(self):
        now = pg.time.get_ticks()
        if now - self.spawn_time > self.lifetime:
            self.kill()
        self.pos += self.vel
        self.rect.center = self.pos
        # wrap around?
