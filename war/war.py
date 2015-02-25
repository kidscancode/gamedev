# Spacewar!
# by KidsCanCode 2015
# For educational purposes only
# TODO:
# Sounds
# Enemy AI
# Other weapons (missile, beam)
# Shields
# Fuel
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
WIDTH = 1280
HEIGHT = 720
FPS = 60
OFFSETX = int(WIDTH / 2)
OFFSETY = int(HEIGHT / 2)
PLANET_SIZE = 70
G = -4500


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
    def __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.rot_cache = {}
        self.pos = pygame.math.Vector2(0, 0)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.thrust = pygame.math.Vector2(0, 0)
        self.rot = 0
        self.thrust_power = 0.05
        self.rot_speed = 3
        self.health = 100
        self.shield = 100
        self.fire_delay = 250
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
                Bullet(self, [g.bullets, g.bodies, g.all_sprites])

    def rotate(self):
        if self.rot in self.rot_cache:
            image = self.rot_cache[self.rot]
        else:
            image = pygame.transform.rotate(self.image0, self.rot)
            self.rot_cache[self.rot] = image
        old_center = self.rect.center
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def animate(self):
        pass

    def hit(self, hit):
        if self.shield > 0:
            self.shield -= hit.damage
            if self.shield < 0:
                self.health += self.shield
                self.shield = 0
        else:
            self.health -= hit.damage

    def update(self):
        self.animate()
        self.rot = self.rot % 360
        # use key controls
        # TODO: ai controls
        if self.player:
            # self.get_key_accel()
            self.get_keys()
        # rotate image
        self.rotate()
        # check edges - wrap around
        if self.pos.y > HEIGHT / 2:
            self.pos.y = -HEIGHT / 2
        if self.pos.y < -HEIGHT / 2:
            self.pos.y = HEIGHT / 2
        if self.pos.x > WIDTH / 2:
            self.pos.x = -WIDTH / 2
        if self.pos.x < -WIDTH / 2:
            self.pos.x = WIDTH / 2
        # move the sprite
        self.rect.centerx = self.pos.x + OFFSETX
        self.rect.centery = self.pos.y + OFFSETY


class Player(Ship):
    def __init__(self, *groups):
        super(Player, self).__init__(*groups)
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
        self.stats_pos = (10, 10)

    # def animate(self):
    #     if self.thrust.length == 0:
    #         return
    #     now = pygame.time.get_ticks()
    #     if now - self.last_update > 100:
    #         self.


class Enemy(Ship):
    def __init__(self, *groups):
        Ship.__init__(self, *groups)
        self.image = g.sprite_sheet.get_image(222, 0, 103, 84)
        self.image = pygame.transform.smoothscale(self.image, (51, 42))
        self.radius = 200
        self.image0 = self.image
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(0, -250)
        self.vel = pygame.math.Vector2(-3.5, 0)
        self.player = False
        self.stats_pos = (10, WIDTH - 110)

    def animate(self):
        # find dir to player and then rotate toward it
        pass


class Bullet(pygame.sprite.Sprite):
    def __init__(self, ship, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.rot_cache = {}
        self.ship = ship
        if isinstance(self.ship, Player):
            self.image = g.sprite_sheet.get_image(858, 475, 9, 37)
        elif isinstance(self.ship, Enemy):
            pass
        self.rect = self.image.get_rect()
        self.image0 = self.image
        self.pos = ship.pos - pygame.math.Vector2(0, 45).rotate(-ship.rot)
        self.vel = -pygame.math.Vector2(0, 6).rotate(-ship.rot)
        self.acc = pygame.math.Vector2(0, 0)
        self.thrust = pygame.math.Vector2(0, 0)
        self.spawn_time = pygame.time.get_ticks()
        self.damage = 10
        self.update()

    def rotate(self):
        # rotate image
        old_center = self.rect.center
        self.rot = self.vel.angle_to(pygame.math.Vector2(0, 0)) + 90
        if self.rot in self.rot_cache:
            image = self.rot_cache[self.rot]
        else:
            image = pygame.transform.rotate(self.image0, self.rot)
            self.rot_cache[self.rot] = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.spawn_time > 4000:
            self.kill()
        self.rotate()
        # check edges - wrap around
        if self.pos.y > HEIGHT / 2:
            self.pos.y = -HEIGHT / 2
        if self.pos.y < -HEIGHT / 2:
            self.pos.y = HEIGHT / 2
        if self.pos.x > WIDTH / 2:
            self.pos.x = -WIDTH / 2
        if self.pos.x < -WIDTH / 2:
            self.pos.x = WIDTH / 2
        self.rect.centerx = self.pos.x + OFFSETX
        self.rect.centery = self.pos.y + OFFSETY


class RenderText(pygame.sprite.Sprite):
    def __init__(self, size, color, pos, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        font_name = pygame.font.match_font('arial')
        self.font = pygame.font.Font(font_name, size)
        self.color = color
        self.image = None
        self.rect = None
        self.pos = pos
        self.update_text("0.0")

    def update_text(self, text):
        self.image = self.font.render(text, 0, self.color)
        self.rect = self.image.get_rect(topleft=self.pos)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE  # | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        self.bg_img = pygame.image.load('img/space_bg.png').convert_alpha()
        self.sprite_sheet = SpriteSheet("img/sheet.png")

    def new(self):
        self.running = True
        self.all_sprites = pygame.sprite.RenderUpdates()
        self.bullets = pygame.sprite.Group()
        self.bodies = pygame.sprite.Group()
        self.player = Player([self.all_sprites, self.bodies])
        self.enemy = Enemy([self.all_sprites, self.bodies])
        self.screen.blit(self.bg_img, [0, 0])
        pygame.display.update()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()  # check for events
            self.update()  # update the game state
            self.draw_test()    # draw the next frame

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
        for body in self.bodies:
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
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self.player, self.bullets, True, pygame.sprite.collide_circle)
        for hit in hits:
            self.player.hit(hit)

    def draw(self):
        self.all_sprites.clear(self.screen, self.bg_img)
        self.draw_planet()
        self.draw_stats()
        dirty = self.all_sprites.draw(self.screen)
        pygame.display.update(dirty)

    def draw_test(self):
        self.screen.fill(BGCOLOR)
        # self.screen.blit(self.bg_img, [0, 0])
        self.draw_planet()
        # dirty = self.draw_stats()
        # self.all_sprites.clear(self.screen, self.clear_cb)
        # dirty += self.all_sprites.draw(self.screen)
        self.all_sprites.draw(self.screen)
        fps_txt = "FPS: {:.2f}".format(self.clock.get_fps())
        pygame.display.set_caption(fps_txt)
        pygame.display.update()

    def clear_cb(self, surf, rect):
        surf.fill(BGCOLOR, rect)

    def draw_stats(self):
        for ship in [self.player]:
            h_surf = pygame.Surface([ship.health, 20])
            h_surf.fill(GREEN)
            h_rect = h_surf.get_rect()
            h_rect.topleft = ship.stats_pos
            g.screen.blit(h_surf, h_rect)
            s_surf = pygame.Surface([ship.shield, 20])
            s_surf.fill(BLUE)
            s_rect = s_surf.get_rect()
            s_rect.topleft = (ship.stats_pos[0], ship.stats_pos[1]+25)
            g.screen.blit(s_surf, s_rect)
        return [h_rect, s_rect]

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
        return self.screen.blit(text_surface, text_rect)

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
