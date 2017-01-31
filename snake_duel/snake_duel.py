# Snake Duel (aka Tron) (a 2 player snake game)
# by KidsCanCode 2016
import pygame as pg
import sys

GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (40, 40, 40)

# game options
WIDTH = 800
HEIGHT = 600
CELLSIZE = 10
GRIDWIDTH = WIDTH / CELLSIZE
GRIDHEIGHT = HEIGHT / CELLSIZE
FPS = 15
# alias for pygame vector class
vec = pg.math.Vector2

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Snake Duel")
clock = pg.time.Clock()

font_name = pg.font.match_font('arial')
def draw_text(surf, text, size, color, x, y):
    # draw some text on the screen
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_grid():
    # background for the game
    for x in range(0, WIDTH, CELLSIZE):
        pg.draw.line(screen, GREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELLSIZE):
        pg.draw.line(screen, GREY, (0, y), (WIDTH, y))

def wait_for_key():
    # pause and wait for a key to continue - used on the menu screens
    pg.event.get()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYUP:
                waiting = False

def show_start_screen():
    # welcome screen
    screen.fill(BLACK)
    draw_text(screen, "Snake Duel", 64, WHITE, WIDTH / 2, HEIGHT / 4 - 50)
    draw_text(screen, "GREEN: Arrow keys move", 22, GREEN, WIDTH / 2, HEIGHT / 2 - 50)
    draw_text(screen, "RED: WASD keys move", 22, RED, WIDTH / 2, HEIGHT / 2 + 50)
    draw_text(screen, "Press a key to begin", 18, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
    pg.display.flip()
    wait_for_key()

def show_go_screen():
    # Game over screen - show who won
    # screen.fill(BLACK)
    draw_text(screen, "GAME OVER", 64, WHITE, WIDTH / 2, HEIGHT / 4)
    if players[0].alive:
        draw_text(screen, "GREEN Wins!", 64, GREEN, WIDTH / 2, HEIGHT / 2)
    else:
        draw_text(screen, "RED Wins!", 64, RED, WIDTH / 2, HEIGHT / 2)
    pg.display.flip()
    pg.time.wait(2000)
    draw_text(screen, "Press a key to play again", 18, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
    pg.display.flip()
    wait_for_key()

class Snake:
    def __init__(self, num):
        self.keys = {'up': 0, 'down': 0, 'left': 0, 'right': 0}
        self.num = num
        self.alive = True
        # depending on which player, set different values
        if self.num == 0:
            self.body = [vec(GRIDWIDTH - 5, GRIDHEIGHT - 5)]
            self.dir = 'u'
            self.color = GREEN
            self.keys['up'] = pg.K_UP
            self.keys['down'] = pg.K_DOWN
            self.keys['left'] = pg.K_LEFT
            self.keys['right'] = pg.K_RIGHT
        elif self.num == 1:
            self.body = [vec(5, 5)]
            self.dir = 'd'
            self.color = RED
            self.keys['up'] = pg.K_w
            self.keys['down'] = pg.K_s
            self.keys['left'] = pg.K_a
            self.keys['right'] = pg.K_d

    def control(self, key):
        # change direction, but not 180 degrees
        if key == self.keys['up'] and self.dir != 'd':
            self.dir = 'u'
        if key == self.keys['down'] and self.dir != 'u':
            self.dir = 'd'
        if key == self.keys['left'] and self.dir != 'r':
            self.dir = 'l'
        if key == self.keys['right'] and self.dir != 'l':
            self.dir = 'r'

    def move(self):
        # advance one square in the snake's direction
        if self.dir == 'u':
            new_head = vec(self.body[0].x, self.body[0].y - 1)
        if self.dir == 'd':
            new_head = vec(self.body[0].x, self.body[0].y + 1)
        if self.dir == 'l':
            new_head = vec(self.body[0].x - 1, self.body[0].y)
        if self.dir == 'r':
            new_head = vec(self.body[0].x + 1, self.body[0].y)
        # snake dies if it hits the wall
        if new_head.x in [-1, GRIDWIDTH] or new_head.y in [-1, GRIDHEIGHT]:
            self.alive = False
        else:
            self.body.insert(0, new_head)

    def draw(self):
        for segment in self.body:
            x = segment.x * CELLSIZE
            y = segment.y * CELLSIZE
            segment_rect = pg.Rect(x, y, CELLSIZE, CELLSIZE)
            pg.draw.rect(screen, self.color, segment_rect)

players = []
for i in range(2):
    players.append(Snake(i))

show_start_screen()
game_over = False
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        # respawn players after restart
        players = []
        for i in range(2):
            players.append(Snake(i))

    clock.tick(FPS)
    # Game loop - events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            for player in players:
                if event.key in player.keys.values():
                    player.control(event.key)

    # Game loop - updates
    # move the snakes
    for player in players:
        player.move()
        # collide with self?
        if player.body[0] in player.body[1:]:
            player.alive = False

    # collide with other snake?
    if players[0].body[0] in players[1].body:
        players[0].alive = False
    elif players[1].body[0] in players[0].body:
        players[1].alive = False

    # is either snake dead?
    for player in players:
        if not player.alive:
            game_over = True

    # Game loop - draw
    screen.fill(BLACK)
    draw_grid()
    for player in players:
        player.draw()
    pg.display.flip()

pg.quit()
