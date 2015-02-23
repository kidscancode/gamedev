# Spacewar!
# by KidsCanCode 2015
# For educational purposes only
# TODO:
# Sounds
# Enemy AI
# Other weapons (missile, beam)
# Shields
# Planet graphics
# Menu/start/end screens

import pygame
import sys
import random

# define some colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = BLACK

# basic constants for your game options
TITLE = "War!"
WIDTH = 1080
HEIGHT = 720
FPS = 60
OFFSETX = int(WIDTH / 2)
OFFSETY = int(HEIGHT / 2)
PLANET_SIZE = 70
G = -3500


class SpriteSheet:
    """Utility class to load and parse spritesheets"""
    def __init__(self, filename):
        self.sprite_sheet = pygame.image.load(filename)

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pygame.Surface([width, height], pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        # image.set_colorkey(image.get_at((0, 0)))
        return image


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rot_cache = {}
        self.pos = pygame.math.Vector2(0, 0)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.thrust = pygame.math.Vector2(0, 0)
        self.rot = 0
        self.thrust_power = 0.02
        self.rot_speed = 3
        self.health = 100
        self.shield = 100
        self.fire_delay = 300
        self.next_shot = 0
        self.last_update = 0

    def get_keys(self):
        self.thrust = pygame.math.Vector2(0, 0)
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.rot += self.rot_speed
        if keystate[pygame.K_RIGHT]:
            self.rot -= self.rot_speed
        if keystate[pygame.K_UP]:
            self.thrust = pygame.math.Vector2(0, -self.thrust_power)
        # rotate thrust vector to facing dir
        self.thrust = self.thrust.rotate(-self.rot)
        if keystate[pygame.K_SPACE]:
            if self.next_shot > pygame.time.get_ticks():
                return
            else:
                self.next_shot = pygame.time.get_ticks() + self.fire_delay
                bullet = Bullet(self)
                g.bullets.add(bullet)
                g.all_sprites.add(bullet)

    def make_image(self):
        if self.rot in self.rot_cache:
            image = self.rot_cache[self.rot]
        else:
            image = pygame.transform.rotozoom(self.image0, self.rot, 1.0)
            self.rot_cache[self.rot] = image
        return image

    def animate(self):
        pass

    def draw_stats(self):
        pass

    def update(self):
        self.animate()
        self.rot = self.rot % 360
        # use key controls
        # TODO: ai controls
        if self.player:
            # self.get_key_accel()
            self.get_keys()
        # rotate image
        old_center = self.rect.center
        self.image = self.make_image()
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        # move the sprite
        self.rect.centerx = self.pos.x + OFFSETX
        self.rect.centery = self.pos.y + OFFSETY


class Player(Ship):
    def __init__(self):
        super(Player, self).__init__()
        # self.image = pygame.image.load("img/playerShip1_red.png").convert_alpha()
        self.image = g.sprite_sheet.get_image(224, 832, 99, 75)
        self.image = pygame.transform.smoothscale(self.image, (50, 38))
        self.radius = 20
        self.image0 = self.image
        self.rect = self.image.get_rect()
        # debug collision circle
        # pygame.draw.circle(self.image, RED, self.rect.center, 20)
        self.pos = pygame.math.Vector2(0, 250)
        self.vel = pygame.math.Vector2(3.5, 0)
        self.player = True

    # def animate(self):
    #     if self.thrust.length == 0:
    #         return
    #     now = pygame.time.get_ticks()
    #     if now - self.last_update > 100:
    #         self.


class Enemy(Ship):
    def __init__(self):
        Ship.__init__(self)
        self.image = g.sprite_sheet.get_image(222, 0, 103, 84)
        self.image = pygame.transform.smoothscale(self.image, (51, 42))
        self.radius = 200
        self.image0 = self.image
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(0, -250)
        self.vel = pygame.math.Vector2(-3.5, 0)
        self.player = False

    def animate(self):
        # find dir to player and then rotate toward it
        pass


class Bullet(pygame.sprite.Sprite):
    def __init__(self, ship):
        pygame.sprite.Sprite.__init__(self)
        self.ship = ship
        if isinstance(self.ship, Player):
            self.image = g.sprite_sheet.get_image(858, 475, 9, 37)
        elif isinstance(self.ship, Enemy):
            pass
        self.rect = self.image.get_rect()
        self.image0 = self.image
        self.pos = ship.pos - pygame.math.Vector2(0, 45).rotate(-ship.rot)
        self.vel = -pygame.math.Vector2(0, 5).rotate(-ship.rot)
        self.acc = pygame.math.Vector2(0, 0)
        self.thrust = pygame.math.Vector2(0, 0)
        self.spawn_time = pygame.time.get_ticks()
        self.update()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_time > 6000:
            self.kill()
        # rotate image
        old_center = self.rect.center
        self.rot = self.vel.angle_to(pygame.math.Vector2(0, 0)) + 90
        self.image = pygame.transform.rotozoom(self.image0, self.rot, 1.0)
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.rect.centerx = self.pos.x + OFFSETX
        self.rect.centery = self.pos.y + OFFSETY


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        self.sprite_sheet = SpriteSheet("img/sheet.png")

    def new(self):
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.enemy = Enemy()
        self.all_sprites.add(self.enemy)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()  # check for events
            self.update()  # update the game state
            self.draw()    # draw the next frame

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

    def update(self):
        for body in self.all_sprites:
            dist = body.pos.length()
            if dist < PLANET_SIZE:
                body.kill()
                continue
            dir = body.pos.normalize()
            a = G * dist**-2
            body.acc = dir * a + body.thrust
            body.vel += body.acc
            body.pos += body.vel
        self.all_sprites.update()
        hits = pygame.sprite.spritecollide(self.player, self.bullets, True, pygame.sprite.collide_circle)
        for hit in hits:
            self.player.health -= 10

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_planet()
        self.draw_stats()
        self.all_sprites.draw(self.screen)
        # uncommment to show FPS (useful for troubleshooting)
        fps_txt = "{:.2f}".format(self.clock.get_fps())
        self.draw_text(str(fps_txt), 18, WIDTH-50, 10)
        pygame.display.flip()

    def draw_stats(self):
        for ship in [self.player]:
            h_surf = pygame.Surface([ship.health, 20])
            h_surf.fill(GREEN)
            h_rect = h_surf.get_rect()
            h_rect.topleft = (10, 10)
            g.screen.blit(h_surf, h_rect)
    def draw_planet(self):
        pygame.draw.circle(self.screen, BLUE, (OFFSETX, OFFSETY), PLANET_SIZE)

    def draw_text(self, text, size, x, y):
        # utility function to draw text at a given location
        # TODO: move font matching to beginning of file (don't repeat)
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def start_screen(self):
        pass

    def go_screen(self):
        pass

g = Game()
while True:
    g.start_screen()
    g.new()
    g.run()
    g.go_screen()
