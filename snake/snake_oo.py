# Snake
# by KidsCanCode 2014
# A Pygame snake clone
import pygame
import sys
import random
from os import path

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARKRED = (155, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

FPS = 15
# WIDTH & HEIGHT need to be multiples of CELLSIZE
WIDTH = 640
HEIGHT = 480
CELLSIZE = 20
CELLWIDTH = WIDTH / CELLSIZE
CELLHEIGHT = HEIGHT / CELLSIZE

class Coord:
    # a utility object to hold X/Y coordinates
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Apple:
    # apple object for the snake to eat
    def __init__(self):
        self.loc = Coord(random.randrange(0, CELLWIDTH-1),
                         random.randrange(0, CELLHEIGHT-1))

    def draw(self):
        x = self.loc.x * CELLSIZE
        y = self.loc.y * CELLSIZE
        apple_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(screen, RED, apple_rect)

class Snake:
    # snake object - made up of a list of coordinates
    def __init__(self):
        # load the sound effects
        snd_dir = path.join(path.dirname(__file__), 'snd')
        self.eat_snd = pygame.mixer.Sound(path.join(snd_dir, "eat.wav"))
        self.eat_snd.set_volume(0.2)
        self.hit_snd = pygame.mixer.Sound(path.join(snd_dir, "hit.wav"))
        self.hit_snd.set_volume(0.2)
        # pick a random spot for the snake to start (not too close to the wall)
        x = random.randrange(5, CELLWIDTH-5)
        y = random.randrange(5, CELLHEIGHT-5)
        # this list will hold the coordinates of the snake's body
        self.coords = []
        # the snake starts with 3 segments to the left of the head
        for i in range(3):
            self.coords.append(Coord(x-i, y))
        # start moving right
        self.dir = 'r'

    def draw(self):
        # draw the snake on the screen
        for coord in self.coords:
            x = coord.x * CELLSIZE
            y = coord.y * CELLSIZE
            # each segment is two squares (dark/light)
            segment_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            pygame.draw.rect(screen, DARKGREEN, segment_rect)
            inside_rect = pygame.Rect(x+4, y+4, CELLSIZE-8, CELLSIZE-8)
            pygame.draw.rect(screen, GREEN, inside_rect)

    def move(self):
        # move the snake by adding a new segment in the direction
        if self.dir == 'u':
            new_head = Coord(self.coords[0].x, self.coords[0].y-1)
        elif self.dir == 'd':
            new_head = Coord(self.coords[0].x, self.coords[0].y+1)
        elif self.dir == 'l':
            new_head = Coord(self.coords[0].x-1, self.coords[0].y)
        elif self.dir == 'r':
            new_head = Coord(self.coords[0].x+1, self.coords[0].y)
        # insert the new coord at the front of the coord list
        self.coords.insert(0, new_head)

    def eat(self, apple):
        # check if the snake has eaten an apple
        if self.coords[0].x == apple.loc.x and self.coords[0].y == apple.loc.y:
            self.eat_snd.play()
            return True
        return False

    def hit(self):
        # check if snake hit an edge
        if self.coords[0].x == -1:
            return True
        if self.coords[0].x == CELLWIDTH:
            return True
        if self.coords[0].y == -1:
            return True
        if self.coords[0].y == CELLHEIGHT:
            return True

        # check if snake hit itself
        for snake_body in self.coords[1:]:
            if snake_body.x == self.coords[0].x and snake_body.y == self.coords[0].y:
                return True
        return False

# initialize pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake")

def run_game():
    # this function runs the game
    snake = Snake()
    apple = Apple()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # don't move in the opposite direction
                elif event.key == pygame.K_LEFT and snake.dir != 'r':
                    snake.dir = 'l'
                elif event.key == pygame.K_RIGHT and snake.dir != 'l':
                    snake.dir = 'r'
                elif event.key == pygame.K_UP and snake.dir != 'd':
                    snake.dir = 'u'
                elif event.key == pygame.K_DOWN and snake.dir != 'u':
                    snake.dir = 'd'

        if snake.eat(apple):
            # make a new apple
            apple = Apple()
        else:
            # remove the last segment from the snake (it stayed the same size)
            del snake.coords[-1]

        snake.move()
        if snake.hit():
            # dead - play the hit sound and return the score
            snake.hit_snd.play()
            return len(snake.coords) - 3

        # Update screen
        screen.fill(BGCOLOR)
        draw_grid()
        draw_score(len(snake.coords) - 3)
        snake.draw()
        apple.draw()
        pygame.display.flip()
        clock.tick(FPS)

def draw_grid():
    # draw the grid of lines on the screen
    for x in range(0, WIDTH, CELLSIZE):
        pygame.draw.line(screen, DARKGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELLSIZE):
        pygame.draw.line(screen, DARKGRAY, (0, y), (WIDTH, y))

def draw_text(text, size, x, y):
    # utility function to draw text on screen
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def draw_score(score):
    text = 'Score: %s' % score
    draw_text(text, 18, WIDTH-70, 10)

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

def show_start_screen():
    # Display the starting screen
    screen.fill(BGCOLOR)
    draw_text("SNAKE", 64, WIDTH/2, HEIGHT/4)
    draw_text("Move with the arrow keys", 24, WIDTH/2, HEIGHT/2)
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
    screen.fill(BGCOLOR)
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

show_start_screen()
while True:
    score = run_game()
    show_go_screen(score)
