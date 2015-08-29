import pygame

# define some colors (R, G, B)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 480
HEIGHT = 600
FPS = 60
TITLE = "SHMUP"
BGCOLOR = BLACK

def draw_shield_bar(x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(screen, GREEN, fill_rect)
    pygame.draw.rect(screen, WHITE, outline_rect, 2)

class Player(pygame.sprite.Sprite):
    # player sprite - moves left/right, shoots
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_image, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 22
        # uncomment to test the radius
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100

    def update(self):
        # only move if arrow key is pressed
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5

        # move the sprite
        self.rect.x += self.speedx
        # stop at the edges
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

player_image = pygame.image.load('img/playerShip1_orange.png').convert()
shield_images = []
for i in range(3):
    fname = 'img/shield{:01}.png'.format(i + 1)
    shield_images.append(pygame.image.load(fname).convert())

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

running = True
while running:
    clock.tick(FPS)
    # check for events
    for event in pygame.event.get():
        # this one checks for the window being closed
        if event.type == pygame.QUIT:
            running = False

    ##### Game logic goes here  #########
    all_sprites.update()
    ##### Draw/update screen #########
    screen.fill(BGCOLOR)
    all_sprites.draw(screen)
    draw_shield_bar(5, 5, player.shield)
    pygame.display.flip()
