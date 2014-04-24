import pygame
import sys
import random
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Player(pygame.sprite.Sprite):
    speed = 12
    width = 36
    height = 54

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed_x = 0
        self.speed_y = 0
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # start in the middle of the screen
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT / 2

    def update(self):
        # move sprite
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # check for walls
        if self.rect.left < 0:
            self.rect.left = 0
            self.speed_x = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.speed_x = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed_y = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed_y = 0

    def go(self, dir):
        if dir == 'L':
            self.dir = 'l'
            self.speed_x = -self.speed
        elif dir == 'R':
            self.dir = 'r'
            self.speed_x = self.speed
        elif dir == 'U':
            self.dir = 'u'
            self.speed_y = -self.speed
        elif dir == 'D':
            self.dir = 'd'
            self.speed_y = self.speed

    def stop(self, dir):
        if dir in ('L', 'R'):
            self.speed_x = 0
        if dir in ('U', 'D'):
            self.speed_y = 0

class Mob(pygame.sprite.Sprite):
    width = 48
    height = 72

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = random.randrange(6, 10)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        # start off the screen - pick an edge
        edge = random.choice(['t', 'b', 'l', 'r'])
        if edge == 'l':
            self.dir = random.randrange(-80, 80)
            self.rect.right = 0
            self.rect.y = random.randrange(HEIGHT)
        elif edge == 'r':
            self.dir = random.randrange(100, 260)
            self.rect.left = WIDTH
            self.rect.y = random.randrange(HEIGHT)
        elif edge == 't':
            self.dir = random.randrange(190, 350)
            self.rect.bottom = 0
            self.rect.x = random.randrange(WIDTH)
        elif edge == 'b':
            self.dir = random.randrange(10, 170)
            self.rect.top = HEIGHT
            self.rect.x = random.randrange(WIDTH)

    def update(self):
        # move sprite
        self.rect.x += self.speed * math.cos(math.radians(self.dir))
        self.rect.y += self.speed * math.sin(math.radians(self.dir))

    def offscreen(self):
        # kill mob when it runs offscreen
        if self.rect.x < -self.rect.width * 2 or self.rect.x > WIDTH + self.rect.width * 2:
            return True
        elif self.rect.y < -self.rect.height * 2 or self.rect.y > HEIGHT + self.rect.height * 2:
            return True
        else:
            return False

def show_score(score):
    text = 'Score: %s' % score
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, 18)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (40, 10)
    screen.blit(text_surface, text_rect)

WIDTH = 405
HEIGHT = 540
FPS = 30
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge!")
clock = pygame.time.Clock()
# create a timer to track seconds for score
pygame.time.set_timer(pygame.USEREVENT+1, 1000)
running = True
while True:
    active_sprite_list = pygame.sprite.Group()
    mob_sprite_list = pygame.sprite.Group()
    # create the player object
    score = 0
    player = Player()
    active_sprite_list.add(player)
    # create some mobs
    mobs = []
    for i in range(12):
        mob = Mob()
        mobs.append(mob)
        active_sprite_list.add(mob)
        mob_sprite_list.add(mob)
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # increment the score at every timer event (1 sec)
            elif event.type == pygame.USEREVENT+1:
                score += 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            # other keypresses here
                if event.key == pygame.K_LEFT:
                    player.go('L')
                if event.key == pygame.K_RIGHT:
                    player.go('R')
                if event.key == pygame.K_UP:
                    player.go('U')
                if event.key == pygame.K_DOWN:
                    player.go('D')
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.speed_x < 0:
                    player.stop('L')
                if event.key == pygame.K_RIGHT and player.speed_x > 0:
                    player.stop('R')
                if event.key == pygame.K_UP and player.speed_y < 0:
                    player.stop('U')
                if event.key == pygame.K_DOWN and player.speed_y > 0:
                    player.stop('D')
        # filter mobs and create new ones
        for mob in mobs:
            if mob.offscreen():
                mobs.remove(mob)
                active_sprite_list.remove(mob)
                newmob = Mob()
                mobs.append(newmob)
                active_sprite_list.add(newmob)
                mob_sprite_list.add(newmob)
        # check for hits
        hits_list = pygame.sprite.spritecollide(player, mob_sprite_list, False)
        if len(hits_list) > 0:
            running = False
        # update screen
        screen.fill(BLACK)
        active_sprite_list.update()
        active_sprite_list.draw(screen)
        show_score(score)
        pygame.display.flip()
    running = True
