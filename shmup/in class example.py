# opengameart.org
# Kenney

import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS = 30

# Colors - (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHMUP")
clock = pygame.time.Clock()
pew_sound = pygame.mixer.Sound('pewpew.wav')
pygame.mixer.music.load("Casual.ogg")
pygame.mixer.music.set_volume(0.5)
background = pygame.image.load('shmup_files/starfield.png')
background_rect = background.get_rect()
meteor_list = ['shmup_files/meteorBrown_med3.png', 'shmup_files/meteorBrown_med1.png',
               'shmup_files/meteorBrown_small2.png', 'shmup_files/meteorBrown_tiny1.png']

def draw_text(text, size, x, y):
    # generic function to draw some text
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def show_go_screen():
    pygame.mixer.music.stop()
    pygame.event.get()
    draw_text("GAME OVER", 60, WIDTH/2, HEIGHT/4)
    draw_text("Press a key to continue", 24, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    pygame.time.wait(500)
    while not pygame.event.get(pygame.KEYUP):
        if pygame.event.get(pygame.QUIT):
            pygame.quit()
    pygame.event.get()

class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('shmup_files/bolt_gold.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.speedy = random.randrange(3, 8)
        self.rect.x = random.randrange(0, WIDTH-20)
        self.rect.y = -30

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('shmup_files/laserRed16.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -15

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(random.choice(meteor_list)).convert()
        self.image.set_colorkey(BLACK)
        self.image0 = self.image
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.8 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH-self.rect.width)
        self.rect.y = random.randrange(-80, -50)
        self.speedy = random.randrange(3, 12)
        self.rot = 0
        self.last_update = pygame.time.get_ticks()
        self.rot_speed = random.randrange(-8, 8)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image0, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect =  self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.y = random.randrange(-80, -50)
            self.rect.x = random.randrange(WIDTH-self.rect.width)
            self.speedy = random.randrange(3, 12)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('shmup_files/playerShip1_orange.png').convert()
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, (50, 38))
        self.rect = self.image.get_rect()
        self.radius = 22
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx, self.speedy = 0, 0
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        if self.power == 1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            pew_sound.play()
        if self.power == 2:
            bullet1 = Bullet(self.rect.left, self.rect.centery)
            bullet2 = Bullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            bullets.add(bullet1)
            bullets.add(bullet2)
            pew_sound.play()

    def update(self):
        if self.power == 2 and pygame.time.get_ticks() - self.power_time > 5000:
            self.power = 1
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10

        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

while True:
    pygame.mixer.music.play(loops=-1)
    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(10):
        mob = Mob()
        all_sprites.add(mob)
        mobs.add(mob)
    score = 0
    # Game Loop
    running = True
    while running:
        clock.tick(FPS)
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
        # Updates
        all_sprites.update()
        # spawn a powerup (maybe)
        if random.random() > 0.995:
            powerup = Powerup()
            all_sprites.add(powerup)
            powerups.add(powerup)
        # check if player hits powerup
        hits = pygame.sprite.spritecollide(player, powerups, True)
        if hits:
            player.power = 2
            player.power_time = pygame.time.get_ticks()
        # check if mobs hit player
        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        if hits:
            running = False
        #check if bullets hit mobs
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += 1
            newmob = Mob()
            all_sprites.add(newmob)
            mobs.add(newmob)
        # Draw
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        score_text = "Score: " + str(score)
        draw_text(score_text, 18, WIDTH/2, 10)
        pygame.display.flip()

    show_go_screen()
