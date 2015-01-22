# Jump!
# by KidsCanCode 2014
# A Doodle Jump style game in Pygame
# For educational purposes only
import pygame
import sys
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
# higher gravity is harder!
WIDTH = 360
HEIGHT = 480
FPS = 30
GRAVITY = 1

class Player(pygame.sprite.Sprite):
    # The player object - a nice red rectangle
    # constants for player properties - size and speed
    width = 24
    height = 36
    speed = 8
    jump_speed = 18

    def __init__(self):
        # player init - create the sprite and set the starting location
        pygame.sprite.Sprite.__init__(self)
        self.speed_x = 0
        self.speed_y = 0
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(RED)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 50

    def update(self):
        # update the player's position
        # add gravity
        self.speed_y += GRAVITY
        # move the sprite
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        #stop at the left and right sides
        if self.rect.left < 0:
            self.rect.left = 0
            self.speed_x = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.speed_x = 0

    def jump(self):
        # need to see if there's a platform under us.  If not, can't jump
        # move down a little bit and see if there's a collision
        self.rect.y += 1
        hit_list = pygame.sprite.spritecollide(self, platform_sprite_list, False)
        self.rect.y -= 1
        if hit_list:
            self.speed_y -= self.jump_speed

    def stop(self, dir):
        # stop moving if that direction's key is released
        if dir == 'l' and self.speed_x < 0:
            self.speed_x = 0
        if dir == 'r' and self.speed_x > 0:
            self.speed_x = 0

    def go(self, dir):
        # move in the direction pressed
        if dir == 'l':
            self.speed_x = -self.speed
        if dir == 'r':
            self.speed_x = self.speed

class Platform(pygame.sprite.Sprite):
    # platform objects - green rectangles
    def __init__(self, x, y, size):
        # platform init - set location and size (width)
        pygame.sprite.Sprite.__init__(self)
        # platform thickness is 20, set lower for thinner platforms
        self.image = pygame.Surface((size, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def offscreen(self):
        # check to see if the platform has moved off the bottom of the screen
        if self.rect.top > HEIGHT + 10:
            return True
        return False

def draw_text(text, size, x, y):
    # utility function to draw text at a given location
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jump!")
clock = pygame.time.Clock()

# create a sprite group to hold all sprites
all_sprite_list = pygame.sprite.Group()
player = Player()
all_sprite_list.add(player)
# create the starting platforms
platform_list = [[0, HEIGHT-20, WIDTH],
                 [25, 350, 50],
                 [125, 250, 65],
                 [225, 150, 50],
                 [100, 50, 50]]
# this sprite group just holds the platforms - they go in the all list too
platform_sprite_list = pygame.sprite.Group()
for loc in platform_list:
    plat = Platform(loc[0], loc[1], loc[2])
    all_sprite_list.add(plat)
    platform_sprite_list.add(plat)
score = 0
running = True
# start the game loop
while running:
    dt = clock.tick(FPS)
    # check for all your events
    for event in pygame.event.get():
        # this one checks for the window being closed
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # now check for keypresses
        elif event.type == pygame.KEYDOWN:
            # this one quits if the player presses Esc
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_LEFT:
                player.go('l')
            if event.key == pygame.K_RIGHT:
                player.go('r')
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.stop('l')
            if event.key == pygame.K_RIGHT:
                player.stop('r')

    ##### Game logic goes here  #########
    # shift all platforms down when player jumps into the top 1/4 of screen
    if player.rect.top <= HEIGHT / 4:
        for sprite in all_sprite_list:
            sprite.rect.y += max(abs(player.speed_y), 8)

    # only collide with the platforms if falling down
    if player.speed_y >= 0:
        hit_list = pygame.sprite.spritecollide(player, platform_sprite_list, False)
        if len(hit_list) > 0:
            player.speed_y = 0
            player.rect.bottom = hit_list[0].rect.top

    # delete platforms that fall off the screen and create new ones to replace
    for plat in platform_sprite_list:
        if plat.offscreen():
            all_sprite_list.remove(plat)
            platform_sprite_list.remove(plat)
            # new platform is created off the top of the screen
            newplat = Platform(random.randrange(-10, WIDTH-30),
                               -20, random.randrange(40, 65))
            all_sprite_list.add(newplat)
            platform_sprite_list.add(newplat)
            score += 10

    # die
    if player.rect.bottom > HEIGHT:
        for plat in platform_sprite_list:
            plat.rect.y -= max(player.speed_y, 10)
            if plat.rect.bottom < -100:
                all_sprite_list.remove(plat)
                platform_sprite_list.remove(plat)
    if len(platform_sprite_list) == 0:
        running = False

    ##### Draw/update screen #########
    screen.fill(BGCOLOR)
    all_sprite_list.update()
    all_sprite_list.draw(screen)
    score_text = 'Score: %s' % int(score)
    draw_text(score_text, 18, 10, 10)
    # after drawing, flip the display
    pygame.display.flip()
