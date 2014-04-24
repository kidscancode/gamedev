# Snake
# by KidsCanCode 2014
# A Pygame snake clone
import pygame
import sys
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

FPS = 15
# WIDTH & HEIGHT need to be multiples of 20
WIDTH = 640
HEIGHT = 480
CELLSIZE = 20
CELLWIDTH = WIDTH / CELLSIZE
CELLHEIGHT = HEIGHT / CELLSIZE

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake")
snake_eat_snd = pygame.mixer.Sound("snd/eat.wav")
snake_eat_snd.set_volume(0.2)
snake_hit_snd = pygame.mixer.Sound("snd/hit.wav")
snake_hit_snd.set_volume(0.2)

def run_game():
    startx = random.randrange(5, CELLWIDTH-5)
    starty = random.randrange(5, CELLHEIGHT-5)
    snake_coords = [Coord(startx, starty),
                    Coord(startx-1, starty),
                    Coord(startx-2, starty)]
    direction = 'r'
    apple = get_random_location()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_LEFT and direction != 'r':
                    direction = 'l'
                elif event.key == pygame.K_RIGHT and direction != 'l':
                    direction = 'r'
                elif event.key == pygame.K_UP and direction != 'd':
                    direction = 'u'
                elif event.key == pygame.K_DOWN and direction != 'u':
                    direction = 'd'

        # check if the snake has eaten an apple
        if snake_coords[0].x == apple.x and snake_coords[0].y == apple.y:
            # add a new apple and don't remove hthe snake's tail
            snake_eat_snd.play()
            apple = get_random_location()
        else:
            del snake_coords[-1]

        # move the snake by adding a new segment in the direction
        if direction == 'u':
            new_head = Coord(snake_coords[0].x, snake_coords[0].y-1)
        elif direction == 'd':
            new_head = Coord(snake_coords[0].x, snake_coords[0].y+1)
        elif direction == 'l':
            new_head = Coord(snake_coords[0].x-1, snake_coords[0].y)
        elif direction == 'r':
            new_head = Coord(snake_coords[0].x+1, snake_coords[0].y)
        # insert the new coord at the front of the coord list
        snake_coords.insert(0, new_head)

        # check if snake hit an edge = death
        if snake_coords[0].x == -1:
            return
        if snake_coords[0].x == CELLWIDTH:
            return
        if snake_coords[0].y == -1:
            return
        if snake_coords[0].y == CELLHEIGHT:
            return

        # check if snake hit itself = death
        for snake_body in snake_coords[1:]:
            if snake_body.x == snake_coords[0].x and snake_body.y == snake_coords[0].y:
                return

        # Update screen
        screen.fill(BGCOLOR)
        draw_grid()
        draw_snake(snake_coords)
        draw_apple(apple)
        draw_score(len(snake_coords) - 3)
        pygame.display.flip()
        clock.tick(FPS)

def draw_grid():
    for x in range(0, WIDTH, CELLSIZE):
        pygame.draw.line(screen, DARKGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELLSIZE):
        pygame.draw.line(screen, DARKGRAY, (0, y), (WIDTH, y))

def get_random_location():
    return Coord(random.randrange(0, CELLWIDTH-1),
                 random.randrange(0, CELLHEIGHT-1))

def draw_apple(loc):
    x = loc.x * CELLSIZE
    y = loc.y * CELLSIZE
    apple_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(screen, RED, apple_rect)

def draw_snake(coords):
    for coord in coords:
        x = coord.x * CELLSIZE
        y = coord.y * CELLSIZE
        segment_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(screen, DARKGREEN, segment_rect)
        inside_rect = pygame.Rect(x+4, y+4, CELLSIZE-8, CELLSIZE-8)
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

def show_go_screen():
    # display the Game Over screen
    screen.fill(BGCOLOR)
    draw_text("GAME OVER", 58, WIDTH/2, HEIGHT/4)
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
    run_game()
    snake_hit_snd.play()
    show_go_screen()
