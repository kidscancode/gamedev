# Gamedev In-depth
# Pathfinding - part 1
# KidsCanCode 2016
import pygame as pg
vec = pg.math.Vector2

TILESIZE = 32
GRIDWIDTH = 25
GRIDHEIGHT = 20
WIDTH = TILESIZE * GRIDWIDTH
HEIGHT = TILESIZE * GRIDHEIGHT
# WIDTH = 1200
# HEIGHT = 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)
MEDGRAY = (60, 60, 60)
LIGHTGRAY = (140, 140, 140)

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (0, y), (WIDTH, y))

class Wall(pg.sprite.Sprite):
    def __init__(self, x=0, y=0, w=TILESIZE, h=TILESIZE):
        self.groups = all_sprites, walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.image = pg.Surface((w, h))
        self.image.fill(LIGHTGRAY)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILESIZE, y * TILESIZE)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

all_sprites = pg.sprite.Group()
walls = pg.sprite.Group()
#p = Player()

running = True
while running:
    clock.tick(FPS)
    now = pg.time.get_ticks()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_SPACE:
                pass  # execute pathfind
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mpos = pg.mouse.get_pos()
                deleted = False
                for wall in walls:
                    if wall.rect.collidepoint(mpos):
                        wall.kill()
                        deleted = True
                if not deleted:
                    Wall(x=mpos[0] // TILESIZE, y=mpos[1] // TILESIZE)

    all_sprites.update()
    # mouse pos for highlight and pathfind
    mpos = pg.mouse.get_pos()
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGRAY)
    draw_grid()
    all_sprites.draw(screen)
    pg.draw.rect(screen, MEDGRAY, pg.Rect(mpos[0] // TILESIZE * TILESIZE, mpos[1] // TILESIZE * TILESIZE, TILESIZE, TILESIZE))
    pg.display.flip()
