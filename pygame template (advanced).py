# Template for new Pygame project
# KidsCanCode 2014
import pygame
import sys

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
BGCOLOR = BLACK

# basic constants for your game options
WIDTH = 360
HEIGHT = 480
FPS = 30
TITLE = "My Game"
# initialize pygame
pygame.init()
# initialize sound - remove if you're not using sound (always use sound!)
pygame.mixer.init()

class Game:
    def __init__(self):
        # initialize game settings
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()

    def new(self):
        # initialize all your variables and do all the setup for a new game
        pass

    def load_data(self):
        # load all your assets (sound, images, etc.)
        pass

    def run(self):
        # The Game Loop
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
        # the update part of the game loop
        pass

    def draw(self):
        # draw everything to the screen
        self.screen.fill(BGCOLOR)
        pygame.display.flip()

    def events(self):
        # catch all events here
        for event in pygame.event.get():
            # this one checks for the window being closed
            if event.type == pygame.QUIT:
                self.quit()
            # now check for keypresses
            elif event.type == pygame.KEYDOWN:
                # this one quits if the player presses Esc
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                # add any other key events here

    def show_start_screen(self):
        # show the start screen
        pass

    def show_go_screen(self):
        # show the game over screen
        pass

g = Game()
while True:
    g.show_start_screen()
    g.new()
    g.run()
    g.show_go_screen()
