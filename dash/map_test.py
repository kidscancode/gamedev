import pygame
import pytmx
import sys
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BGCOLOR = BLACK

WIDTH = 640
HEIGHT = 320
FPS = 60

class Renderer:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        tw = self.tmxdata.tilewidth
        th = self.tmxdata.tileheight
        gt = self.tmxdata.get_tile_image_by_gid

        if self.tmxdata.background_color:
            surface.fill(self.tmxdata.background_color)

        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = gt(gid)
                    if tile:
                        surface.blit(tile, (x*tw, y*th))
            elif isinstance(layer, pytmx.TiledObjectGroup):
                pass
            elif isinstance(layer, pytmx.TiledImageLayer):
                image = gt(layer.gid)
                if image:
                    surface.blit(image, (0, 0))

    def make_map(self):
        temp_surface = pygame.Surface(self.size)
        self.render(temp_surface)
        return temp_surface

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface([22, 22])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (50, HEIGHT-32)
        self.vx, self.vy = 0, 0
        self.jumping = False

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if not self.jumping:
                # self.rect.y -= 1
                self.vy = -16
                self.jumping = True

        self.vy += 1
        # self.rect.x += self.vx
        # hit = pygame.sprite.spritecollide(self, self.game.blockers, False)
        # if hit:
        #     if self.vx > 0:
        #         self.rect.right = hit[0].rect.left
        #         self.vx = 0
        #     elif self.vx < 0:
        #         self.rect.left = hit[0].rect.right
        #         self.vx = 0
        self.rect.y += self.vy
        hit = pygame.sprite.spritecollide(self, self.game.blockers, False)
        if hit:
            if self.vy > 0:
                self.rect.bottom = hit[0].rect.top
                self.vy = 0
            elif self.vy < 0:
                self.rect.top = hit[0].rect.bottom
                self.vy = 0
            self.jumping = False

        if self.rect.bottom >= HEIGHT - 32:
            self.rect.bottom = HEIGHT - 32
            self.vy = 0
            self.jumping = False

class Blocker(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.game = game
        self.rect = pygame.Rect(x, y, width, height)

    def update(self):
        self.rect.x -= self.game.speed

class Game:
    def __init__(self):
        pygame.init()
        os.environ['SDL_VIDEODRIVER'] = 'fbcon'
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE  # | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Map Test")
        self.clock = pygame.time.Clock()
        self.load_data()

    def new(self):
        self.map_surface = self.tile_renderer.make_map()
        self.map_rect = self.map_surface.get_rect()
        self.speed = 4
        self.blockers = pygame.sprite.Group()
        for tile_object in self.tile_renderer.tmxdata.objects:
            properties = tile_object.__dict__
            if properties['type'] == 'platform':
                x = properties['x']
                y = properties['y']
                w = properties['width']
                h = properties['height']
                Blocker(self, x, y, w, h, [self.blockers])

        self.player = Player(self)

    def load_data(self):
        self.tile_renderer = Renderer('img/dash.tmx')

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        self.player.update()
        self.map_rect.x -= self.speed
        self.blockers.update()

    def draw(self):
        fps_txt = "FPS: {:.2f}".format(self.clock.get_fps())
        pygame.display.set_caption(fps_txt)
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_surface, self.map_rect)
        self.player.draw()
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()

