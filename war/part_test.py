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
    def __init__(self, image, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = image
        self.base_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(0, 0)
        self.vel = pygame.math.Vector2(0, 0)
        self.rot = 0
        self.update()

    def update(self):
        self.thrust = 0
        self.rot = self.rot % 360
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.rot += 3
        if keystate[pygame.K_RIGHT]:
            self.rot -= 3
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
        self.part_img = pygame.image.load('img/ship_particle.png').convert()
        self.box_img = pygame.image.load('img/playerShip1_red.png').convert_alpha()
        self.bg_img = pygame.image.load('img/scrolling2.png').convert_alpha()

        self.all_sprites = pygame.sprite.Group()
        self.box = Box(self.box_img, self.all_sprites)
        self.OFFSET = OFFSET
        em_offset = pygame.math.Vector2(0, 15)
        part_vel = pygame.math.Vector2(0, 3)
        self.emitter = ParticleEmitter(self, self.box, em_offset, part_vel,
                                       self.part_img, 0, 1, 0, 35, 10)

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
        if self.box.thrust:
            self.emitter.count = 100
        self.all_sprites.update()
        self.emitter.update()
        self.emitter.print_state()

    def draw(self):
        fps_txt = "FPS: {:.2f}  dt: {:.3f}  rot: {:.2f}".format(self.clock.get_fps(), self.dt, self.box.rot)
        pygame.display.set_caption(fps_txt)
        self.screen.fill(BLACK)
        self.screen.blit(self.bg_img, [0, 0])
        self.all_sprites.draw(self.screen)
        self.emitter.draw()
        # pygame.draw.circle(self.screen, (0, 255, 0), (int(self.emitter.pos.x), int(self.emitter.pos.y)), 5)
        pygame.display.update()


g = Game()
g.run()
