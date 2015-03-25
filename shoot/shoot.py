# Shoot!
# by KidsCanCode 2014
# A generic space shooter
# For educational purposes only
# Art & sounds from http://opengameart.org
# Meteors - http://opengameart.org/content/asteroids
# Rocket - http://opengameart.org/content/rocket
# Lasers = Modified from http://opengameart.org/content/lasers-and-beams

# TODO: timer on powerups
# TODO: powerup variety (spray, beam, etc)
# TODO: auto-fire (as long as key is down)
# TODO: enemies, enemy health, enemy pushback
# TODO: moving starfield
import pygame
import sys
import random

# define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BGCOLOR = BLACK

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

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # start with a random speed
        self.speed = random.randrange(3, 12)
        # load the images for the animation frames
        # 10 % will be big meteors
        chance = random.randrange(10)
        self.frames = []
        for i in range(16):
            if chance == 9:
                image = pygame.image.load("img/b400{:02}.png".format(i))
            else:
                image = pygame.image.load("img/b100{:02}.gif".format(i))
            image = image.convert()
            image.set_colorkey([0, 0, 0])
            self.frames.append(image)
        # set starting image to a random one
        self.image = random.choice(self.frames)
        self.rect = self.image.get_rect()
        # start off the top of the screen
        self.rect.y = random.randrange(-50, -30)
        self.rect.x = random.randrange(WIDTH)

    def update(self):
        # move the sprite
        self.rect.y += self.speed
        frame = (self.rect.y // 20) % len(self.frames)
        self.image = self.frames[frame]
        if self.rect.y > HEIGHT + 10:
            self.rect.y = random.randrange(-50, -30)
            self.rect.x = random.randrange(WIDTH)


class Player(pygame.sprite.Sprite):
    speed = 12
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed_x = 0
        self.level = 0
        self.score = 0
        self.shot_sounds = []
        snd = pygame.mixer.Sound("snd/laser4.wav")
        self.shot_sounds.append(snd)
        snd = pygame.mixer.Sound("snd/laser5.wav")
        snd.set_volume(0.5)
        self.shot_sounds.append(snd)
        snd = pygame.mixer.Sound("snd/laser8.wav")
        snd.set_volume(0.2)
        self.shot_sounds.append(snd)
        self.hit_snd = pygame.mixer.Sound("snd/explode.wav")
        self.explode_snd = pygame.mixer.Sound("snd/die.wav")
        self.powerup_snd = pygame.mixer.Sound("snd/powerup.wav")
        self.powerup_snd.set_volume(1.0)
        self.image = pygame.image.load("img/red_rocket.gif").convert()
        self.image.set_colorkey([0, 0, 0])
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.bottom = HEIGHT - 10

    def update(self):
        # move the sprite
        self.rect.x += self.speed_x
        # check for edges
        if self.rect.left < 0:
            self.rect.left = 0
            self.speed_x = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.speed_x = 0

    def go(self, dir):
        if dir == 'L':
            self.speed_x = -self.speed
        elif dir == 'R':
            self.speed_x = self.speed

    def stop(self):
        self.speed_x = 0

    def shoot(self):
        bullet = Bullet(self.rect.midtop, self.rect.y, self.level)
        active_sprite_list.add(bullet)
        bullet_sprite_list.add(bullet)
        self.shot_sounds[self.level].play()

class Bullet(pygame.sprite.Sprite):
    speed = -15
    def __init__(self, x, y, level):
        pygame.sprite.Sprite.__init__(self)
        self.speed *= (level + 1)
        self.frames = []
        image = pygame.image.load("img/shot1.png").convert()
        image.set_colorkey([0, 0, 0])
        self.frames.append(image)
        image = pygame.image.load("img/shot2.png").convert()
        image.set_colorkey([0, 0, 0])
        self.frames.append(image)
        image = pygame.image.load("img/shot3.png").convert()
        image.set_colorkey([0, 0, 0])
        self.frames.append(image)
        self.image = self.frames[level]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.midtop = x
        self.rect.y = y

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Powerup(pygame.sprite.Sprite):
    speed = random.randrange(5, 9)
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        sprite_sheet = SpriteSheet("img/powerup-sheet.png")
        image = sprite_sheet.get_image(5, 0, 22, 32)
        image.set_colorkey([0, 0, 0])
        self.frames.append(image)
        image = sprite_sheet.get_image(37, 0, 21, 32)
        image.set_colorkey([0, 0, 0])
        self.frames.append(image)
        image = sprite_sheet.get_image(69, 0, 21, 32)
        image.set_colorkey([0, 0, 0])
        self.frames.append(image)
        image = sprite_sheet.get_image(102, 0, 21, 32)
        image.set_colorkey([0, 0, 0])
        self.frames.append(image)
        image = sprite_sheet.get_image(134, 0, 20, 32)
        image.set_colorkey([0, 0, 0])
        self.frames.append(image)
        image = sprite_sheet.get_image(165, 0, 21, 32)
        image.set_colorkey([0, 0, 0])
        self.frames.append(image)
        image = sprite_sheet.get_image(198, 0, 21, 32)
        image.set_colorkey([0, 0, 0])
        self.frames.append(image)
        image = sprite_sheet.get_image(230, 0, 21, 32)
        image.set_colorkey([0, 0, 0])
        self.frames.append(image)
        self.image = self.frames[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(-50, -30)
        self.rect.x = random.randrange(WIDTH)

    def update(self):
        self.rect.y += self.speed
        frame = (self.rect.y // 30) % len(self.frames)
        self.image = self.frames[frame]
        if self.rect.top > HEIGHT:
            self.kill()


def draw_text(text, size, x, y):
    # utility function to draw text on screen
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def show_start_screen():
    # Display the starting screen
    screen.blit(background, background_rect)
    draw_text("Shoot!", 72, WIDTH/2, HEIGHT/4)
    draw_text("Move with the arrow keys", 24, WIDTH/2, HEIGHT/2)
    draw_text("Shoot the meteors", 24, WIDTH/2, HEIGHT*5/8)
    draw_text("Press a key to begin", 24, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    # wait for a keypress to start
    wait_for_key()
    while True:
        if wait_for_key():
            pygame.event.get()
            return

def show_go_screen(score):
    # display the Game Over screen
    screen.blit(background, background_rect)
    draw_text("GAME OVER", 58, WIDTH/2, HEIGHT/4)
    text = "Score: %s" % score
    draw_text(text, 24, WIDTH/2, HEIGHT/2)
    draw_text("Press a key to begin", 24, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    # pause for a moment and then wait for key
    pygame.time.wait(500)
    wait_for_key()
    while True:
        if wait_for_key():
            pygame.event.get()
            return

def wait_for_key():
    # utility function to pause waiting for a keypress
    # still allow Esc to exit
    # Actually, we look for KEYUP event, not KEYPRESS
    if len(pygame.event.get(pygame.QUIT)) > 0:
        pygame.quit()
        sys.exit()
    keyup_events = pygame.event.get(pygame.KEYUP)
    if len(keyup_events) == 0:
        return None
    if keyup_events[0].key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
    return keyup_events[0].key

# basic constants for your game options
WIDTH = 360
HEIGHT = 480
FPS = 30

# initialize pygame
pygame.init()
# initialize sound - remove if you're not using sound
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot!")
# background
background = pygame.image.load("img/starfield.png").convert()
background_rect = background.get_rect()
clock = pygame.time.Clock()

running = True

show_start_screen()
while True:
    active_sprite_list = pygame.sprite.Group()
    meteor_sprite_list = pygame.sprite.Group()
    bullet_sprite_list = pygame.sprite.Group()
    player = Player()
    active_sprite_list.add(player)
    powerup = None
    for i in range(10):
        meteor = Meteor()
        active_sprite_list.add(meteor)
        meteor_sprite_list.add(meteor)
    # play the game!
    while running:
        clock.tick(FPS)
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
                if event.key == pygame.K_LEFT:
                    player.go('L')
                if event.key == pygame.K_RIGHT:
                    player.go('R')
                if event.key == pygame.K_SPACE:
                    player.shoot()
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    player.stop()
                # add any other key events here

        ##### Game logic goes here  #########
        # rare chance of a powerup appearing
        if random.random() > 0.98 and powerup is None and player.level < 2:
            powerup = Powerup()
            active_sprite_list.add(powerup)
        # check for collisions
        # first, ship with meteors
        hit = pygame.sprite.spritecollideany(player, meteor_sprite_list,
                                             pygame.sprite.collide_mask)
        if hit:
            # you die
            player.explode_snd.play()
            pygame.time.wait(500)
            running = False
        # next, check bullets with meteors
        hits = pygame.sprite.groupcollide(meteor_sprite_list, bullet_sprite_list,
                                          True, True, pygame.sprite.collide_mask)
        # for each meteor destroyed, spawn a new one
        for hit in hits:
            player.hit_snd.play()
            player.score += 10
            newmeteor = Meteor()
            active_sprite_list.add(newmeteor)
            meteor_sprite_list.add(newmeteor)
        # check for powerup
        if powerup is not None:
            hit = pygame.sprite.collide_mask(player, powerup)
            if hit:
                active_sprite_list.remove(powerup)
                powerup = None
                player.powerup_snd.play()
                player.level += 1
                if player.level == 3:
                    player.level = 2

        ##### Draw/update screen ########
        # screen.fill(BGCOLOR)
        screen.blit(background, background_rect)
        active_sprite_list.update()
        active_sprite_list.draw(screen)
        text = 'Score: %s' % player.score
        draw_text(text, 18, 45, 10)
        # after drawing, flip the display
        fps_txt = "{:.2f}".format(clock.get_fps())
        draw_text(str(fps_txt), 18, WIDTH-50, 10)
        pygame.display.flip()

    show_go_screen(player.score)
    running = True
