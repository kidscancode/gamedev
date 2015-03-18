from particles import *
import pygame
import random
import sys

BLACK = [0, 0, 0]
RED = [255, 0, 0]
LIGHTBLUE = [0, 155, 155]
FPS = 60
WIDTH, HEIGHT = 800, 600
OFFSET = pygame.math.Vector2(int(WIDTH/2), int(HEIGHT/2))
OFFSETX = int(WIDTH / 2)
OFFSETY = int(HEIGHT / 2)

class Box(pygame.sprite.Sprite):
    def __init__(self, game, image, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = image
        self.game = game
        self.base_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(0, 0)
        self.vel = pygame.math.Vector2(0, 0)
        self.rot = 0
        self.update()

    def update(self):
        self.thrust = 0
        self.act_thrust = 0
        self.rot = self.rot % 360
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.rot += 3
            self.act_thrust = 3
        if keystate[pygame.K_RIGHT]:
            self.rot -= 3
            self.act_thrust = -3
        if keystate[pygame.K_UP]:
            self.thrust = 1

        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.base_image, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.rect.center = self.pos + OFFSET


class Game:
    def __init__(self):
        pygame.init()
        flags = pygame.DOUBLEBUF  # | pygame.HWSURFACE | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        self.clock = pygame.time.Clock()
        self.new()

    def new(self):
        self.part_img = pygame.image.load('../war/img/ship_particle.png').convert()
        self.box_img = pygame.image.load('../war/img/playerShip1_red.png').convert_alpha()
        self.bg_img = pygame.image.load('../war/img/scrolling2.png').convert_alpha()

        self.all_sprites = pygame.sprite.Group()
        self.box = Box(self, self.box_img, self.all_sprites)
        self.OFFSET = OFFSET
        em_offset = pygame.math.Vector2(0, 15)
        part_vel = pygame.math.Vector2(0, 4)
        self.emitter = ParticleEmitter(self, self.box, em_offset, part_vel,
                                       self.part_img, 0, .5, 0, 35, 8)
        act_em_offset_r = pygame.math.Vector2(23, 6)
        act_em_offset_l = pygame.math.Vector2(-23, 6)
        act_part_vel = pygame.math.Vector2(0, 2)
        self.act_emitter_r = ParticleEmitter(self, self.box, act_em_offset_r, act_part_vel,
                                             self.part_img, 0, 0.2, 0, 15, 5)
        self.act_emitter_l = ParticleEmitter(self, self.box, act_em_offset_l, act_part_vel,
                                             self.part_img, 0, 0.2, 0, 15, 5)

    def run(self):
        running = True
        while running:
            self.dt = self.clock.tick(FPS) * 0.001
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

    def update(self):
        self.emitter.count = 0
        self.act_emitter_r.count = 0
        self.act_emitter_l.count = 0
        if self.box.thrust:
            self.emitter.count = 100
        if self.box.act_thrust > 0:
            self.act_emitter_r.count = 25
        if self.box.act_thrust < 0:
            self.act_emitter_l.count = 25
        self.all_sprites.update()
        self.emitter.update()
        self.act_emitter_r.update()
        self.act_emitter_l.update()
        # self.emitter.print_state()

    def draw(self):
        fps_txt = "FPS: {:.2f}  dt: {:.3f}  rot: {:.2f}".format(self.clock.get_fps(), self.dt, self.box.rot)
        pygame.display.set_caption(fps_txt)
        self.screen.fill(BLACK)
        self.screen.blit(self.bg_img, [0, 0])
        self.all_sprites.draw(self.screen)
        self.emitter.draw()
        self.act_emitter_r.draw()
        self.act_emitter_l.draw()
        # pygame.draw.circle(self.screen, (0, 255, 0), (int(self.emitter.pos.x), int(self.emitter.pos.y)), 5)
        # pygame.draw.circle(self.screen, (0, 255, 0), (int(self.act_emitter_r.pos.x),
        #                                               int(self.act_emitter_r.pos.y)), 3)
        # pygame.draw.circle(self.screen, (0, 255, 0), (int(self.act_emitter_l.pos.x),
        #                                               int(self.act_emitter_l.pos.y)), 3)
        pygame.display.update()


g = Game()
g.run()
