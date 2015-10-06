# Flap
# KidsCanCode 2014
# Flappy bird in pygame
# For educational purposes only
# Art from http://lanica.co/flappy-clone/
# Music from opengameart.org (http://opengameart.org/content/cheerful-1-choro-bavario-happy-loop)
#   Copyright 2009 MSTR "Choro Bavario" <http://www.jamendo.com/en/artist/349242/mstr>
#   Copyright 2012 Iwan Gabovitch "Choro Bavario (happy loop)" (simple editing to make it loop)
# TODO:
# combine sprites into one spritesheet
import pygame
import sys
from os import path
import random

# define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE

# basic constants for your game options
WIDTH = 480
HEIGHT = 320
FPS = 30
# tweak this to change how quickly the bird falls
GRAVITY = 1
# how big the gaps between the pipes are
GAP = 100
# how frequently the pipes spawn (sec)
FREQ = 2
# how fast the bird flies at the pipes
PIPE_SPEED = 3
# how powerful is a flap?
FLAP_SPEED = 15

# set up asset folders
game_dir = path.dirname(__file__)
img_dir = path.join(game_dir, 'img')
snd_dir = path.join(game_dir, 'snd')

class SpriteSheet:
    """Utility class to load and parse spritesheets"""
    def __init__(self, filename):
        self.sprite_sheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey([0, 0, 0])
        return image

class Bird(pygame.sprite.Sprite):
    # player controlled bird, can only flap
    width = 36
    height = 24
    def __init__(self):
        # when you make a Pygame Sprite object, you have to call the
        # Sprite init function
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed_x = 0
        self.speed_y = 0
        self.flap_snd = pygame.mixer.Sound(path.join(snd_dir, "bird_flap.wav"))
        self.flap_snd.set_volume(0.2)
        self.frames = []
        sprite_sheet = SpriteSheet(path.join(img_dir, "bird_sprites.png"))
        image = sprite_sheet.get_image(3, 7, 34, 24)
        image.set_colorkey(BLACK)
        self.frames.append(image)
        self.image_dead = pygame.transform.rotate(image, -90)
        image = sprite_sheet.get_image(59, 7, 34, 24)
        image.set_colorkey(BLACK)
        self.frames.append(image)
        image = sprite_sheet.get_image(115, 7, 34, 24)
        image.set_colorkey(BLACK)
        self.frames.append(image)
        self.index = 0
        self.image = self.frames[self.index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        # start in the middle of the screen
        self.rect.centerx = WIDTH / 2
        self.rect.y = HEIGHT / 2

    def update(self):
        # gravity pulls downward
        self.speed_y += gravity
        # move
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.alive:
            # animate
            self.index += 1
            if self.index >= len(self.frames):
                self.index = 0
            self.image = self.frames[self.index]
        else:
            self.image = self.image_dead
        # stop at the top/bottom
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed_y = 0
        if self.rect.bottom > HEIGHT-50:
            self.rect.bottom = HEIGHT-50
            self.speed_y = 0

    def move(self):
        # player hit SPACEBAR
        if not self.alive:
            return
        self.speed_y -= FLAP_SPEED
        self.flap_snd.play()

class Pipe(pygame.sprite.Sprite):
    # pipe segment class
    speed_x = -PIPE_SPEED
    width = 36
    def __init__(self, loc, y):
        # loc = upper or lower
        # y = where to place it
        pygame.sprite.Sprite.__init__(self)
        sprite_sheet = SpriteSheet(path.join(img_dir, "pipes.png"))
        if loc == 'u':
            self.image = sprite_sheet.get_image(2, 8, 52, 320)
        else:
            self.image = sprite_sheet.get_image(58, 8, 52, 320)
        self.image.set_colorkey(BLACK)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        # start offscreen to the right
        self.rect.x = WIDTH + 50
        if loc == 'u':
            self.rect.bottom = y
        else:
            self.rect.top = y
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
    # create a new pair of pipes (upper and lower)
    y = random.randrange(30, HEIGHT-50-GAP)
    pipe_u = Pipe('u', y)
    pipe_l = Pipe('l', y + GAP)
    return pipe_u, pipe_l

def draw_background():
    # draw the background (tiled)
    background_rect.bottom = HEIGHT + 20
    background_rect.left = 0
    screen.blit(background, background_rect)
    if background_rect.width < WIDTH:
        background_rect.left = background_rect.width
        screen.blit(background, background_rect)

def draw_ground():
    # draw the ground tiles, moving at the same speed as pipes
    for image in ground_list:
        image.x -= PIPE_SPEED
        if image.right <= 0:
            # if the image has completely moved off the screen, move it to the right
            image.left = 2 * ground.get_width() + image.right
        screen.blit(ground, image)

def draw_text(text, size, x, y):
    # utility function to draw text at a given location
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def show_go_image():
    go_rect.midtop = (WIDTH/2, HEIGHT/2)
    screen.blit(go_image, go_rect)

def show_ready_image():
    ready_rect.midtop = (WIDTH/2, HEIGHT*2/3)
    screen.blit(ready_image, ready_rect)

def load_score_images():
    sprite_sheet = SpriteSheet(path.join(img_dir, 'numbers.png'))
    score_images = []
    image = sprite_sheet.get_image(114, 45, 24, 36)
    score_images.append(image)
    image = sprite_sheet.get_image(2, 4, 24, 36)
    score_images.append(image)
    image = sprite_sheet.get_image(30, 4, 24, 36)
    score_images.append(image)
    image = sprite_sheet.get_image(58, 4, 24, 36)
    score_images.append(image)
    image = sprite_sheet.get_image(86, 4, 24, 36)
    score_images.append(image)
    image = sprite_sheet.get_image(114, 4, 24, 36)
    score_images.append(image)
    image = sprite_sheet.get_image(2, 45, 24, 36)
    score_images.append(image)
    image = sprite_sheet.get_image(30, 45, 24, 36)
    score_images.append(image)
    image = sprite_sheet.get_image(58, 45, 24, 36)
    score_images.append(image)
    image = sprite_sheet.get_image(86, 45, 24, 36)
    score_images.append(image)
    return score_images

def show_score(score):
    # show the score using the score images
    # draw_text(str(int(score)), 22, WIDTH/2, 10)
    digits = [int(c) for c in str(score)]
    for i, digit in enumerate(digits):
        img = score_images[digit]
        img_rect = img.get_rect()
        img_rect.y = 5
        img_rect.x = i * img_rect.width + 5
        screen.blit(img, img_rect)

# initialize pygame
pygame.init()
# initialize sound
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flap")
try:
    pygame.mixer.music.load(path.join(snd_dir, "Choro_bavario_loop.ogg"))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)
except:
    print("Can't load music.")
# background
background = pygame.image.load(path.join(img_dir, "background.png")).convert()
background_rect = background.get_rect()
background_rect.bottom = HEIGHT
background_rect.left = 0
# load some other images we need
go_image = pygame.image.load(path.join(img_dir, "gameover.png")).convert()
go_image.set_colorkey(BLACK)
go_rect = go_image.get_rect()
ready_image = pygame.image.load(path.join(img_dir, "getready.png")).convert()
ready_image.set_colorkey(BLACK)
ready_rect = ready_image.get_rect()
score_images = load_score_images()
# load the ground tile images
ground_list = []
ground = pygame.image.load(path.join(img_dir, "ground.png")).convert()
# three tiles (increase for v. large screen sizes)
for i in range(3):
    image_rect = ground.get_rect()
    image_rect.y = HEIGHT-50
    image_rect.x = i * ground.get_width()
    ground_list.append(image_rect)

while True:
    clock = pygame.time.Clock()
    # timer to generate new pipes
    pygame.time.set_timer(pygame.USEREVENT+1, int(FREQ*1000))
    # groups to hold sprites (all sprites & a group of just the pipes)
    active_sprite_list = pygame.sprite.Group()
    pipe_sprite_list = pygame.sprite.Group()
    # create the player object
    player = Bird()
    active_sprite_list.add(player)
    gravity = 0
    score = 0
    running = True
    clicked = False
    while running:
        clock.tick(FPS)
        if clicked:
            gravity = GRAVITY
        # check for events
        for event in pygame.event.get():
            # this one checks for the window being closed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # # every FREQ seconds, make a new pipe
            elif event.type == pygame.USEREVENT+1:
                upper, lower = new_pipe()
                active_sprite_list.add(upper)
                pipe_sprite_list.add(upper)
                active_sprite_list.add(lower)
                pipe_sprite_list.add(lower)
                if not clicked:
                    clicked = True
            # now check for keypresses
            elif event.type == pygame.KEYDOWN:
                clicked = True
                # this one quits if the player presses Esc
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    player.move()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                player.move()

        ##### Game logic goes here  #########
        # filter out old pipes
        for pipe in pipe_sprite_list:
            if pipe.offscreen():
                active_sprite_list.remove(pipe)
                pipe_sprite_list.remove(pipe)
            elif pipe.rect.right < player.rect.x and not pipe.passed:
                # if the pipe is past the player and hasn't yet been marked
                score += 0.5
                pipe.passed = True
        # check for collisions
        hit_list = pygame.sprite.spritecollide(player, pipe_sprite_list, False,
                                               pygame.sprite.collide_mask)
        if len(hit_list) > 0:
            # too bad! stop flapping and move to the left
            player.alive = False
            player.speed_x = -3
        if player.rect.left <= 0:
            # game ends when the bird goes offscreen
            running = False

        ##### Draw/update screen #########
        draw_background()
        active_sprite_list.update()
        active_sprite_list.draw(screen)
        draw_ground()
        if not player.alive:
            show_go_image()
        if not clicked:
            show_ready_image()
        show_score(int(score))
        # after drawing, flip the display
        pygame.display.flip()
