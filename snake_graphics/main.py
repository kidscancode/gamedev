# Snake w/Graphics
# by KidsCanCode 2017
# A pg snake clone
# For educational purposes only
import pygame as pg
import sys
from os import path
from settings import *
from tools import *
from snake import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        img_dir = path.join(path.dirname(__file__), 'img')
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.apple_img = self.spritesheet.get_image_by_rect(*APPLE_IMAGE)
        self.apple_img = pg.transform.scale(self.apple_img, (CELLSIZE, CELLSIZE))
        self.wall_img = self.spritesheet.get_image_by_rect(*WALL_IMAGE)
        self.wall_img = pg.transform.scale(self.wall_img, (CELLSIZE, CELLSIZE))
        self.snake_images = []
        # img = self.spritesheet.get_image_by_rect(*SNAKE_HEAD)
        img = pg.image.load(path.join(img_dir, SNAKE_HEAD)).convert_alpha()
        self.snake_images.append(pg.transform.scale(img, (CELLSIZE, CELLSIZE)))
        # img = self.spritesheet.get_image_by_rect(*SNAKE_BODY)
        img = pg.image.load(path.join(img_dir, SNAKE_BODY)).convert_alpha()
        self.snake_images.append(pg.transform.scale(img, (CELLSIZE, CELLSIZE)))
        # img = self.spritesheet.get_image_by_rect(*SNAKE_TAIL)
        # self.snake_images.append(pg.transform.scale(img, (CELLSIZE, CELLSIZE)))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.tilemap = Tilemap(GRIDWIDTH, GRIDHEIGHT, self.wall_img)
        self.camera = Camera(CELLSIZE * GRIDWIDTH, CELLSIZE * GRIDHEIGHT)
        start = self.tilemap.get_random_tile(5)
        self.snake = Snake(self, start, SNAKE_LENGTH, self.snake_images)
        self.apple = self.tilemap.get_random_tile(1)
        self.paused = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.snake.move()
        self.camera.update(self.snake.head)
        if self.snake.hit_self():
            self.playing = False
        if self.snake.hit_walls():
            self.playing = False
        pg.display.set_caption('a:{} s:{}'.format(self.apple, self.snake.head))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.tilemap.draw(self.screen, self.camera)
        self.snake.draw(self.screen, self.camera)
        self.apple.draw(self.screen, self.camera, self.apple_img)
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
                if event.key in CONTROLS:
                    self.snake.dir = CONTROLS[event.key]

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
