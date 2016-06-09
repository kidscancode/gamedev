import pygame as pg
import random as rand
from brick_settings import *
vec = pg.math.Vector2

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
        
    def get_image(self, x, y, w, h):
        image = pg.Surface((w, h))  
        image.blit(self.spritesheet, (0, 0), (x, y, w, h))
        return image
        
class Brick(pg.sprite.Sprite):
    def __init__(self, x, y, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.image = pg.transform.scale(self.image, (BRICK_WIDTH, BRICK_HEIGHT))
        self.rect = self.image.get_rect()  
        self.rect.midtop = (x, y)
        self.hit = False
        self.vy = -5
        self.vx = rand.randrange(-4, 5)
        
    def update(self):
        if self.hit:
            self.fall_away()
        if self.rect.top > HEIGHT:
            self.kill()
        
    def fall_away(self):
        self.vy += 0.5
        self.rect.y += self.vy
        self.rect.x += self.vx
        
class Paddle(pg.sprite.Sprite):
    def __init__(self, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.image = pg.transform.scale(self.image, (PADDLE_WIDTH, PADDLE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 30)
        
    def update(self):
        pos = pg.mouse.get_pos()
        self.rect.centerx = pos[0]
        
class Ball(pg.sprite.Sprite):
    def __init__(self, game, image):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = image
        self.image = pg.transform.scale(self.image, (BALL_SIZE, BALL_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.vel = vec(rand.randrange(-3, 4), -1)
        self.vel = self.vel.normalize() * BALL_SPEED
        
    def update(self):
        self.rect.center += self.vel
        # bounce off 3 walls
        if self.rect.left < 0:
            self.game.screen_shake(8)
            self.game.wall_sound.play()
            self.rect.left = 0
            self.vel.x *= -1
        if self.rect.right > WIDTH:
            self.game.screen_shake(8)
            self.game.wall_sound.play()
            self.rect.right = WIDTH
            self.vel.x *= -1
        if self.rect.top < 0:
            self.game.screen_shake(8)
            self.game.wall_sound.play()
            self.rect.top = 0
            self.vel.y *= -1