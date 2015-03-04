# Dash!
# by KidsCanCode 2015
# For educational purposes only
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
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
CYAN = (0, 255, 255)
BGCOLOR = BLACK

# basic constants for your game options
WIDTH = 640
HEIGHT = 360
FPS = 60
# Game settings
GRAVITY = 1
PLAYER_JUMP = 15
WORLD_SPEED = 10

# initialize pygame
pygame.init()
# initialize sound - remove if you're not using sound (always use sound!)
pygame.mixer.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.vx, self.vy = 0, 0
        self.image = pygame.Surface([24, 24])
        pygame.draw.rect(self.image, GREEN, [0, 0, 23, 23], 2)
        # self.image.fill(GREEN)
        self.image_orig = self.image.copy()
        self.rot = 0
        self.rot_speed = 0
        self.rot_cache = {}
        self.jumping = False
        self.rect = self.image.get_rect()
        self.rect.center = (50, HEIGHT-50)

    def update(self):
        self.get_keys()

        self.rot = self.rot % 360
        self.vy += GRAVITY

        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.top <= 0:
            self.rect.top = 0
            self.vy = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vy = 0
            self.jumping = False

    def get_keys(self):
        keystate = pygame.key.get_pressed()
        mousestate = pygame.mouse.get_pressed()
        if keystate[pygame.K_SPACE] or mousestate[0]:
            if not self.jumping:
                self.vy = -PLAYER_JUMP
                self.jumping = True

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

class Stage:
    pass

class Object:
    pass

class Game:
    def __init__(self):
        # initialize game settings
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.load_data()

    def new(self):
        # initialize all your variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self.all_sprites)

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
        self.all_sprites.update()

    def draw(self):
        # draw everything to the screen
        fps_txt = "FPS: {:.2f}".format(self.clock.get_fps())
        pygame.display.set_caption(fps_txt)
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
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
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
