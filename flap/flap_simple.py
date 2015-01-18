# Flap - prototype (no graphics)
# KidsCanCode 2014
# Flappy bird in pygame - Simple version (no graphics)
# For educational purposes only
import pygame
import sys
import random

# define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE

# basic constants for your game options
WIDTH = 480
HEIGHT = 320
FPS = 30
# change this to change how quickly the bird falls
GRAVITY = 1
# how big the gaps between the pipes are
GAP = 100
# how frequently the pipes spawn (sec)
FREQ = 3.5
# how fast the bird flies at the pipes
PIPE_SPEED = 3
# how powerful is a flap?
FLAP_SPEED = 15

class Bird(pygame.sprite.Sprite):
    # player controlled bird, can only flap
    width = 36
    height = 24
    def __init__(self):
        # when you make a Pygame Sprite object, you have to call the
        # Sprite init function
        pygame.sprite.Sprite.__init__(self)
        self.speed_y = 0
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # start in the middle of the screen
        self.rect.centerx = WIDTH / 2
        self.rect.y = HEIGHT / 2

    def update(self):
        # gravity pulls downward
        self.speed_y += GRAVITY
        # move
        self.rect.y += self.speed_y
        # stop at the top/bottom
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed_y = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed_y = 0

    def flap(self):
        # player hit SPACEBAR
        self.speed_y -= FLAP_SPEED

class Pipe(pygame.sprite.Sprite):
    # pipe segment objects
    # all pipes move at the same speed and are the same width
    # only the height will vary
    speed_x = -PIPE_SPEED
    width = 36
    def __init__(self, height, y):
        # height = size of the pipe block
        # y = where to place it
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.width, height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        # start offscreen to the right
        self.rect.x = WIDTH + 50
        self.rect.y = y
        # has the bird passed this pipe?
        self.passed = False

    def update(self):
        # move
        self.rect.x += self.speed_x

    def offscreen(self):
        # test to see if the pipe has moved offscreen
        if self.rect.right < 0:
            return True
        else:
            return False

def new_pipe():
    # create a new pair of pipes segments(upper and lower)
    size = random.randrange(20, HEIGHT-20-GAP)
    pipe_u = Pipe(size, 0)
    pipe_l = Pipe(HEIGHT - GAP - size, size + GAP)
    return pipe_u, pipe_l

def draw_text(text, size, x, y):
    # utility function to draw text at a given location
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flap")

while True:
    clock = pygame.time.Clock()
    # timer to generate new pipes
    pygame.time.set_timer(pygame.USEREVENT, int(FREQ*1000))
    # groups to hold sprites (all sprites & a group of just the pipes)
    active_sprite_list = pygame.sprite.Group()
    pipe_sprite_list = pygame.sprite.Group()
    # create the player object
    player = Bird()
    active_sprite_list.add(player)
    score = 0
    # create a pair of pipes
    upper, lower = new_pipe()
    active_sprite_list.add(upper)
    pipe_sprite_list.add(upper)
    active_sprite_list.add(lower)
    pipe_sprite_list.add(lower)
    running = True
    while running:
        clock.tick(FPS)
        # check for events
        for event in pygame.event.get():
            # this one checks for the window being closed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # # every FREQ seconds, make a new pipe
            elif event.type == pygame.USEREVENT:
                upper, lower = new_pipe()
                active_sprite_list.add(upper)
                pipe_sprite_list.add(upper)
                active_sprite_list.add(lower)
                pipe_sprite_list.add(lower)
            # now check for keypresses
            elif event.type == pygame.KEYDOWN:
                # this one quits if the player presses Esc
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    player.flap()

        # delete old pipes
        for pipe in pipe_sprite_list:
            if pipe.offscreen():
                active_sprite_list.remove(pipe)
                pipe_sprite_list.remove(pipe)
            elif pipe.rect.right < player.rect.x and not pipe.passed:
                # if the pipe is past the player and hasn't yet been marked
                score += 0.5
                pipe.passed = True
        # check for collisions
        hit_list = pygame.sprite.spritecollide(player, pipe_sprite_list, False)
        if len(hit_list) > 0:
            # too bad!
            running = False

        ##### Draw/update screen #########
        screen.fill(BGCOLOR)
        active_sprite_list.update()
        active_sprite_list.draw(screen)
        score_text = 'Score: %s' % int(score)
        draw_text(score_text, 18, 40, 10)
        # after drawing, flip the display
        pygame.display.flip()
