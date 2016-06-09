# quick demo to help explain masks and pixel perfect collisions
import pygame as pg
import random

WIDTH = 480
HEIGHT = 480
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# initialize pg and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game")
clock = pg.time.Clock()

def draw_text(text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)
        
class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('playerShip1_orange.png').convert()
        self.image = pg.transform.scale(self.image, (200, 76*2))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        
all_sprites = pg.sprite.Group()
p1 = Player()
all_sprites.add(p1)
p2 = Player()
all_sprites.add(p2)
p2.rect.x -= 125
p2.rect.y -= 125

def draw_mask(sprite):
    # fill the sprite's mask
    for x in range(sprite.rect.width):
        for y in range(sprite.rect.height):
            if sprite.mask.get_at((x, y)):
                pg.draw.circle(sprite.image, MAGENTA, (x, y), 1)
                
def draw_outline(sprite):
    # outline the sprite's mask
    o = sprite.mask.outline()
    for px in o:
        pg.draw.circle(sprite.image, MAGENTA, px, 2)

# Game loop
running = True
pg.key.set_repeat(200, 50)
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                p2.rect.x -= 1
            if event.key == pg.K_RIGHT:
                p2.rect.x += 1
            if event.key == pg.K_UP:
                p2.rect.y -= 1
            if event.key == pg.K_DOWN:
                p2.rect.y += 1

    # Update
    all_sprites.update()
    h = pg.sprite.collide_mask(p1, p2)
    draw_outline(p2)
    draw_outline(p1)
    # h = p1.mask.overlap_area(p2.mask, (p1.rect.x-p2.rect.x, p1.rect.y-p2.rect.y))
    # pg.display.set_caption(str(h))
    
    screen.fill((40, 40, 40))
    screen.blit(p1.image, p1.rect)
    pg.draw.rect(screen, WHITE, p1.rect, 1)
    screen.blit(p2.image, p2.rect)
    draw_text("Hit: "+str(h), 18, WHITE, WIDTH/2, 5)
    if h:
        px = (h[0] + p1.rect.x, h[1] + p1.rect.y)
        pg.draw.circle(screen, CYAN, px, 4)
    pg.display.flip()

pg.quit()
