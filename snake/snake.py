# Snake
# by KidsCanCode 2014, 2017
# A Pygame snake clone
# For educational purposes only
# Modified from http://inventwithpython.com/
import pygame
import sys
from os import path
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

FPS = 15
# WIDTH & HEIGHT need to be multiples of CELLSIZE
WIDTH = 800
HEIGHT = 600
CELLSIZE = 25
CELLWIDTH = WIDTH / CELLSIZE
CELLHEIGHT = HEIGHT / CELLSIZE

# initialize pygame and create the screen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake")
# load some sound effects
snd_dir = path.join(path.dirname(__file__), 'snd')
snake_eat_snd = pygame.mixer.Sound(path.join(snd_dir, "eat.wav"))
snake_eat_snd.set_volume(0.2)
snake_hit_snd = pygame.mixer.Sound(path.join(snd_dir, "hit.wav"))
snake_hit_snd.set_volume(0.2)

def run_game():
    # this function runs the game
    # pick a starting spot for the snake's head (not too close to the wall)
    startx = random.randrange(5, CELLWIDTH - 5)
    starty = random.randrange(5, CELLHEIGHT - 5)
    # this list will hold the coordinates of the snake's body
    snake = [(startx, starty), (startx - 1, starty), (startx - 2, starty)]
    direction = 'r'
    apple = get_random_location()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_LEFT and direction != 'r':
                    direction = 'l'
                elif event.key == pygame.K_RIGHT and direction != 'l':
                    direction = 'r'
                elif event.key == pygame.K_UP and direction != 'd':
                    direction = 'u'
                elif event.key == pygame.K_DOWN and direction != 'u':
                    direction = 'd'

        # check if the snake has eaten an apple
        if snake[0] == apple:
            # add a new apple and don't remove hthe snake's tail
            snake_eat_snd.play()
            apple = get_random_location()
        else:
            del snake[-1]

        # move the snake by adding a new segment in the direction
        x, y = snake[0]
        if direction == 'u':
            y -= 1
        elif direction == 'd':
            y += 1
        elif direction == 'l':
            x -= 1
        elif direction == 'r':
            x += 1
        # insert the new coord at the front of the coord list
        snake.insert(0, (x, y))

        # check if snake hit an edge = death
        x, y = snake[0]
        if x in [-1, CELLWIDTH] or y in [-1, CELLHEIGHT]:
            return

        # check if snake hit itself = death
        if snake[0] in snake[1:]:
            return

        # Update screen
        screen.fill(BGCOLOR)
        draw_grid()
        draw_snake(snake)
        draw_apple(apple)
        draw_score(len(snake) - 3)
        pygame.display.flip()
        clock.tick(FPS)

def draw_grid():
    for x in range(0, WIDTH, CELLSIZE):
        pygame.draw.line(screen, DARKGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELLSIZE):
        pygame.draw.line(screen, DARKGRAY, (0, y), (WIDTH, y))

def get_random_location():
    # pick a random Coord on the grid
    return (random.randrange(0, CELLWIDTH - 1),
            random.randrange(0, CELLHEIGHT - 1))

def draw_apple(loc):
    x, y = loc
    x *= CELLSIZE
    y *= CELLSIZE
    apple_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(screen, RED, apple_rect)

def draw_snake(segments):
    for segment in segments:
        x, y = segment
        x *= CELLSIZE
        y *= CELLSIZE
        segment_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(screen, DARKGREEN, segment_rect)
        inside_rect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(screen, GREEN, inside_rect)

def draw_text(text, size, x, y):
    # utility function to draw text on screen
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def draw_score(score):
    # text = 'Score: %s' % score
    draw_text(str(score), 28, WIDTH / 2, 10)

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
    draw_text("SNAKE", 64, WIDTH / 2, HEIGHT / 4)
    draw_text("Move with the arrow keys", 24, WIDTH / 2, HEIGHT / 2)
    draw_text("Press a key to begin", 24, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.update()
    # wait for a keypress to start
    wait_for_key()
    while True:
        if wait_for_key():
            pygame.event.get()
            return

def show_go_screen():
    # display the Game Over screen
    screen.fill(BGCOLOR)
    draw_text("GAME OVER", 58, WIDTH / 2, HEIGHT / 4)
    draw_text("Press a key to begin", 24, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.update()
    # pause for a moment and then wait for key
    pygame.time.wait(500)
    wait_for_key()
    while True:
        if wait_for_key():
            pygame.event.get()
            return

# Main game loop
show_start_screen()
while True:
    run_game()
    snake_hit_snd.play()
    show_go_screen()
