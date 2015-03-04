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
PLAYER_JUMP = 16
WORLD_SPEED = 8

class Player(pygame.sprite.Sprite):
    def __init__(self, game, image, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.game = game
        self.vx, self.vy = 0, 0
        self.image = image
        # self.image = pygame.Surface([24, 24])
        # pygame.draw.rect(self.image, GREEN, [0, 0, 23, 23], 2)
        # self.image.fill(GREEN)
        self.image_orig = self.image.copy()
        self.rot = 0
        self.rot_speed = 0
        self.rot_cache = {0: self.image}
        self.jumping = False
        self.rect = self.image.get_rect()
        self.rect.center = (50, HEIGHT-50)
        self.layer = 5

    def update(self):
        self.get_keys()
        self.rotate()
        self.rot = self.rot % 360
        self.vy += GRAVITY

        # move SPEED pixels forward just to see if we're going to hit something
        self.rect.x += self.game.speed / 2
        hits = pygame.sprite.spritecollide(self, self.game.obstacles, False)
        self.rect.x -= self.game.speed / 2
        if hits:
            self.game.speed = 0
            self.kill()
        # now move in y and see if we need to land on something
        self.rect.y += self.vy
        hits = pygame.sprite.spritecollide(self, self.game.obstacles, False)
        if hits:
            if hits[0].type == 'plat':
                self.rect.bottom = hits[0].rect.top # - 1
                self.vy = 0
                self.jumping = False
            elif hits[0].type == 'spike':
                self.game.speed = 0
                self.kill()

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
                self.rect.y -= 1
                self.vy = -PLAYER_JUMP
                self.jumping = True
                self.jump_time = pygame.time.get_ticks()

    def rotate(self):
        if self.jumping:
            self.rot -= 5
        else:
            self.rot = 0
        if self.rot in self.rot_cache:
            image = self.rot_cache[self.rot]
        else:
            image = pygame.transform.rotate(self.image_orig, self.rot)
            self.rot_cache[self.rot] = image
        old_center = self.rect.center
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = old_center

class Background(pygame.sprite.Sprite):
    def __init__(self, game, image, x, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0
        self.layer = 0

    def update(self):
        if self.game.speed > 0:
            self.rect.x -= (self.game.speed - 6)

class Stage:
    pass

class Object(pygame.sprite.Sprite):
    def __init__(self, game, x, object_type, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.game = game
        self.type = object_type
        self.image = pygame.Surface([188, 32])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + x
        self.rect.bottom = HEIGHT
        self.layer = 1

    def update(self):
        self.rect.x += -self.game.speed
        if self.rect.right <= 0:
            self.kill()

class Game:
    def __init__(self):
        # initialize game settings
        # initialize pygame
        pygame.init()
        # initialize sound
        # pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.load_data()

    def new(self):
        # initialize all your variables and do all the setup for a new game
        self.speed = WORLD_SPEED
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.obstacles = pygame.sprite.Group()
        self.bg1 = Background(self, self.background, 0, self.all_sprites)
        self.bg2 = Background(self, self.background, self.background.get_width(), self.all_sprites)
        self.player = Player(self, self.player_image, self.all_sprites)
        for i in range(8):
            Object(self, i * 300, "plat", [self.all_sprites, self.obstacles])

    def load_data(self):
        # load all your assets (sound, images, etc.)
        self.background = pygame.image.load('img/game_bg_01_001.png').convert()
        self.background = pygame.transform.scale(self.background, [640, 640])
        self.player_image = pygame.image.load('img/element_green_square.png').convert_alpha()

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
        if self.bg1.rect.right <= 0:
            self.bg1.rect.left = self.bg2.rect.right
        if self.bg2.rect.right <= 0:
            self.bg2.rect.left = self.bg1.rect.right
        self.all_sprites.update()

    def draw(self):
        # draw everything to the screen
        fps_txt = "FPS: {:.2f}".format(self.clock.get_fps())
        pygame.display.set_caption(fps_txt)
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
