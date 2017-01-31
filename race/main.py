# KidsCanCode -
import pygame as pg
import sys
from os import path
from settings import *
from tools import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.img_cache = {}
        self.load_data()

    def load_data(self):
        self.font_name = pg.font.match_font('hack')
        img_dir = path.join(path.dirname(__file__), 'img')
        snd_dir = path.join(path.dirname(__file__), 'snd')
        self.map_dir = path.join(path.dirname(__file__), 'maps')
        self.vehicle_sheet = SpritesheetWithXML(path.join(img_dir, 'spritesheet_vehicles'))
        self.objects_sheet = SpritesheetWithXML(path.join(img_dir, 'spritesheet_objects'))

    def draw_text(self, text, size, color, x, y, align="topleft"):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.paused = False
        self.draw_debug = False
        self.all_sprites = pg.sprite.Group()
        self.map = TiledMap(path.join(self.map_dir, 'test.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        self.camera = Camera(self.map.width, self.map.height)
        self.player1 = Vehicle(self, PLAYER1)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        if not self.paused:
            self.all_sprites.update()
            self.camera.update(self.player1)
            # self.paused = True

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        if self.draw_debug:
            for sprite in self.all_sprites:
                sprite.draw_debug()
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_SPACE:
                    self.paused = not self.paused
                if event.key == pg.K_v:
                    self.draw_debug = not self.draw_debug

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
