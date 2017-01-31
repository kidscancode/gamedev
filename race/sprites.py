import pygame as pg
from settings import *
vec = pg.math.Vector2

class Vehicle(pg.sprite.Sprite):
    def __init__(self, game, config):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.config = config
        game.img_cache[config['name']] = {}
        self.image_clean = pg.transform.rotate(game.vehicle_sheet.get_image_by_name(config['img']), -90)
        self.heading = config['heading']
        self.image = pg.transform.rotate(self.image_clean, self.heading)
        self.rect = self.image.get_rect()
        self.pos = config['pos']
        # self.vel = vec(150, 0).rotate(-self.heading)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.steering = 0
        self.rect.center = self.pos

    def rotate_image(self):
        if self.heading in self.game.img_cache[self.config['name']]:
            image = self.game.img_cache[self.config['name']][self.heading]
        else:
            image = pg.transform.rotate(self.image_clean, self.heading)
            self.game.img_cache[self.config['name']][self.heading] = image
        old_center = self.rect.center
        self.image = image
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=old_center)

    def get_keys(self):
        if self.vel.length_squared() > 90000:
            steering = self.config['steering_fast']
        else:
            steering = self.config['steering_slow']
        keystate = pg.key.get_pressed()
        if keystate[self.config['controls']['Accelerate']]:
            self.acc = vec(self.config['accel'], 0).rotate(-self.heading)
        if keystate[self.config['controls']['Brake']]:
            self.acc = vec(-self.config['braking'], 0).rotate(-self.heading)
        if keystate[self.config['controls']['TurnLeft']]:
            self.steering = steering
        if keystate[self.config['controls']['TurnRight']]:
            self.steering = -steering

    def apply_friction(self):
        # apply friction forces
        friction = -self.config['friction'] * self.vel
        drag = -self.config['drag'] * self.vel * self.vel.length()
        if self.vel.length_squared() < 10000:
            friction *= 10
        self.acc += drag + friction

    def update(self):
        # get acc & steering from player input
        self.acc = vec(0, 0)
        self.steering = 0
        self.get_keys()
        self.apply_friction()
        self.vel += self.acc * self.game.dt
        if self.vel.length_squared() < 100:
            self.vel = vec(0, 0)
        # calculate steering (bicycle model)
        self.front_wheel = self.pos + vec(self.config['wheelbase'], 0).rotate(-self.heading)
        self.rear_wheel = self.pos - vec(self.config['wheelbase'], 0).rotate(-self.heading)
        self.rear_wheel += self.vel * self.game.dt
        self.front_wheel += self.vel.rotate(-self.steering) * self.game.dt
        self.pos = (self.front_wheel + self.rear_wheel) / 2
        self.heading = (self.front_wheel - self.rear_wheel).angle_to(vec(1, 0))
        self.vel = vec(1, 0).rotate(-self.heading) * self.vel.length()
        self.rotate_image()
        self.rect.center = self.pos

    def draw_debug(self):
        txt = 'pos:({},{})'.format(int(self.pos.x), int(self.pos.y))
        self.game.draw_text(txt, 20, WHITE, 10, 10, align="topleft")
        txt = 'head:{}'.format(int(self.heading))
        self.game.draw_text(txt, 20, WHITE, 10, 30, align="topleft")
        txt = 'vel:({},{}) mag: {}'.format(int(self.vel.x), int(self.vel.y), int(self.vel.length()))
        self.game.draw_text(txt, 20, WHITE, 10, 50, align="topleft")
        txt = 'acc:({},{}) mag: {}'.format(int(self.acc.x), int(self.acc.y), int(self.acc.length()))
        self.game.draw_text(txt, 20, WHITE, 10, 70, align="topleft")
        txt = 'steer: {}'.format(self.steering)
        self.game.draw_text(txt, 20, WHITE, 10, 90, align="topleft")

        scale = 0.5
        pos = self.game.camera.apply_point(self.pos)
        # vel
        pg.draw.line(self.game.screen, GREEN, pos, (pos + self.vel * scale), 5)
        # acc
        pg.draw.line(self.game.screen, RED, pos, (pos + self.acc * scale), 5)
