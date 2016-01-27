# Pygame Template (advanced)
# Use this to start a new Pygame project
# KidsCanCode 2016
import pygame as pg
import random

# define some colors (R, G, B)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FUCHSIA = (255, 0, 255)
GRAY = (128, 128, 128)
LIME = (0, 128, 0)
MAROON = (128, 0, 0)
NAVYBLUE = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
CYAN = (0, 255, 255)

# basic constants to set up your game
WIDTH = 360
HEIGHT = 480
FPS = 30
TITLE = "My Game"
BGCOLOR = BLACK

class Game:
    # The Game object will initialize the game, run the game loop,
    # and display start/end screens

    def __init__(self):
        # initialize the game and create the window
        # initialize pygame
        pg.init()
        # initialize sound - uncomment if you're using sound
        # pygame.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # start the clock
        self.clock = pg.time.Clock()
        self.load_data()
        self.running = True

    def new(self):
        # initialize all your variables and do all the setup for a new game
        self.run()

    def load_data(self):
        # load all your assets (sounds, images, etc.)
        pass

    def run(self):
        # The Game loop - set self.running to False to end the game
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # the update part of the game loop
        pass

    def draw(self):
        # draw everything to the screen
        self.screen.fill(BGCOLOR)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            # this one checks for the window being closed
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # add any other events here (keys, mouse, etc.)

    def show_start_screen(self):
        # show the start screen
        pass

    def show_go_screen(self):
        # show the game over screen
        pass

# create the game object
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
