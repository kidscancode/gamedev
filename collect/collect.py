# Collect the Blocks
# by KidsCanCode 2015
# Run around and collect the blocks
# For educational purposes only

# TODO
# time bonus
# powerups
# more mob features (different types, etc)
# Level designs (walls, gravity (black holes?))

import pygame
import sys
import random

# define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

WIDTH = 800
HEIGHT = 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collect the Blocks")
clock = pygame.time.Clock()


def draw_text(text, size, x, y):
    # utility function to draw text on screen
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    # player sprite
    # realistic movement using equations of motion (pos, vel, accel)
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pygame.math.Vector2(WIDTH/2, HEIGHT/2)
        self.vel = pygame.math.Vector2(0, 0)
        self.accel = pygame.math.Vector2(0, 0)
        self.image = pygame.Surface((24, 24))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

    def update(self):
        self.accel = pygame.math.Vector2(0, 0)
        # keep accelerating as long as that dir key is down
        keystate = pygame.key.get_pressed()
        a = 1.5
        if FPS == 60:
            a = 0.7
        if keystate[pygame.K_LEFT]:
            self.accel.x = -a
        if keystate[pygame.K_RIGHT]:
            self.accel.x = a
        if keystate[pygame.K_UP]:
            self.accel.y = -a
        if keystate[pygame.K_DOWN]:
            self.accel.y = a
        # fix diagonals so they are same speed as orthoganal directions
        if self.accel.x != 0 and self.accel.y != 0:
            self.accel *= 0.7071

        # friction (based on vel)
        self.accel += self.vel * -0.12
        # grav example (not going to use in this game, but fun to see)
        # self.accel.y += .7

        # equations of motion
        # for simplicity, using t=1 (change per timestep)
        # p' = 0.5 at**2 + vt + p
        # v' = at + v
        self.pos += self.accel * 0.5 + self.vel
        self.vel += self.accel

        # move the sprite
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)
        # don't move offscreen
        if self.rect.left < 0:
            self.pos.x = 0
            self.vel.x = 0
        if self.rect.right > WIDTH:
            self.pos.x = WIDTH - self.rect.width
            self.vel.x = 0
        if self.rect.top < 0:
            self.pos.y = 0
            self.vel.y = 0
        if self.rect.bottom > HEIGHT:
            self.pos.y = HEIGHT - self.rect.height
            self.vel.y = 0


class Box(pygame.sprite.Sprite):
    # simple static box
    # TODO: moving boxes?
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((24, 24))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Mob(pygame.sprite.Sprite):
    # bad guy!
    # will chase the player
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((24, 24))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.accel = pygame.math.Vector2(0, 0)
        # varied speeds (actually acceleration, but determines max speed)
        # TODO: different types of enemy based on speed?
        self.speed = random.choice([0.1, 0.2, 0.3, 0.4])
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

    def update(self):
        # friction (based on vel)
        self.accel += self.vel * -0.09

        # equations of motion - see Player class
        self.pos += self.accel * 0.5 + self.vel
        self.vel += self.accel

        # move the sprite
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)
        # don't move offscreen
        if self.rect.left < 0:
            self.pos.x = 0
            self.vel.x = 0
        if self.rect.right > WIDTH:
            self.pos.x = WIDTH - self.rect.width
            self.vel.x = 0
        if self.rect.top < 0:
            self.pos.y = 0
            self.vel.y = 0
        if self.rect.bottom > HEIGHT:
            self.pos.y = HEIGHT - self.rect.height
            self.vel.y = 0


all_sprites = pygame.sprite.Group()
boxes = pygame.sprite.Group()
mobs = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(10):
    box = Box(random.randrange(5, WIDTH-29),
              random.randrange(5, HEIGHT-29))
    boxes.add(box)
    all_sprites.add(box)
score = 0
level = 1

running = True
while running:
    clock.tick(FPS)
    # handle all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # collide w/boxes and remove them
    hit_list = pygame.sprite.spritecollide(player, boxes, True)
    score += len(hit_list)

    # level up, create new boxes and mobs
    if len(boxes) == 0:
        level += 1
        for i in range((level+1)*5):
            box = Box(random.randrange(5, WIDTH-29),
                      random.randrange(5, HEIGHT-29))
            boxes.add(box)
            all_sprites.add(box)
        mobs.empty()
        # put the player back in the middle
        player.vel = vec2(0, 0)
        player.pos = vec2(WIDTH/2, HEIGHT/2)
        # create some mobs - start in the corners
        for i in range(level // 2):
            mob = Mob(random.choice([5, WIDTH-29]),
                      random.choice([5, WIDTH-29]))
            mobs.add(mob)

    # accelerate mobs towards player
    for mob in mobs:
        mob.accel = vec2(player.pos.x - mob.pos.x,
                         player.pos.y - mob.pos.y)
        mob.accel = mob.accel * (mob.speed / mob.accel.mag())
        # touch a mob and die!
        if pygame.sprite.collide_rect(mob, player):
            running = False

    screen.fill(BLACK)
    # uncommment to show FPS (useful for troubleshooting)
    fps_txt = "{:.2f}".format(clock.get_fps())
    draw_text(str(fps_txt), 18, WIDTH-50, 10)
    all_sprites.update()
    mobs.update()
    all_sprites.draw(screen)
    mobs.draw(screen)
    score_txt = "Score: {:0}".format(score)
    draw_text(score_txt, 18, 10, 10)
    lvl_txt = "Level: {:0}".format(level)
    draw_text(lvl_txt, 18, 10, 30)
    pygame.display.flip()
