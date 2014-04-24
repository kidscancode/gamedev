# Template for new Pygame project
# KidsCanCode 2014
import pygame
import sys
import random

# define some colors (R, G, B)
BLACK = (0, 0, 0)
GRAY = (155, 155, 155)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (119, 22, 245)
ORANGE = (255, 159, 0)
BGCOLOR = GRAY

# basic constants for your game options
FPS = 15
COLS = 8
ROWS = 8
MARGIN = 2
BORDER = 5
PAD = 50  # extra space on the bottom of the board for text
CELLWIDTH = 50
CELLHEIGHT = 50
WIDTH = CELLWIDTH * COLS + 2 * BORDER + MARGIN * (COLS - 1)
HEIGHT = CELLHEIGHT * ROWS + 2 * BORDER + MARGIN * (ROWS - 1) + PAD
SHAPES = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE]

class Board:
    # rectanglar board
    def __init__(self):
        self.columns = COLS
        self.rows = ROWS
        self.blank = pygame.Surface((CELLWIDTH, CELLHEIGHT))
        self.blank.fill(GRAY)
        self.selectbox = pygame.Surface((CELLWIDTH, CELLHEIGHT))
        self.selectbox.fill(BLACK)
        self.selectbox.set_colorkey(BLACK)
        self.select_rect = self.selectbox.get_rect()
        pygame.draw.rect(self.selectbox, WHITE, self.select_rect, 3)
        self.board = [[self.blank for _ in range(ROWS)] for _ in range(COLS)]
        self.matches = []
        self.refill = []
        self.score = 0
        self.shapes = []
        self.selected = None
        self.animating = False
        for shape in SHAPES:
            img = pygame.Surface((CELLWIDTH, CELLHEIGHT))
            img.fill(shape)
            self.shapes.append(img)

    def shuffle(self):
        # new board
        for row in range(ROWS):
            for col in range(COLS):
                self.board[row][col] = random.choice(self.shapes)

    def draw(self):
        # draw the board
        for i, row in enumerate(self.board):
            for j, shape in enumerate(row):
                screen.blit(shape,
                            (BORDER + CELLWIDTH * j + MARGIN * j,
                             BORDER + CELLHEIGHT * i + MARGIN * i))
                if self.selected == (i, j):
                    screen.blit(self.selectbox,
                                (BORDER + CELLWIDTH * j + MARGIN * j,
                                 BORDER + CELLHEIGHT * i + MARGIN * i))

    def find_matches(self):
        # find all 3 (or more) in a rows, return a list of cells
        match_list = []
        # first check the columns
        for col in range(COLS):
            length = 1
            for row in range(1, ROWS):
                match = self.board[row][col] == self.board[row-1][col]
                if match:
                    length += 1
                if not match or row == ROWS - 1:
                    if row == ROWS - 1:
                        row += 1
                    if length >= 3:
                        match_cells = []
                        for clear_row in range(row-length, row):
                            match_cells.append((clear_row, col))
                        match_list.append(match_cells)
                    length = 1
        # now check the rows
        for row in range(ROWS):
            length = 1
            for col in range(1, COLS):
                match = self.board[row][col] == self.board[row][col-1]
                if match:
                    length += 1
                if not match or col == COLS - 1:
                    if col == COLS - 1:
                        col += 1
                    if length >= 3:
                        match_cells = []
                        for clear_col in range(col-length, col):
                            match_cells.append((row, clear_col))
                        match_list.append(match_cells)
                    length = 1

        return match_list

    def clear_matches(self, matches):
        for match in matches:
            for cell in match:
                row, col = cell
                self.board[row][col] = self.blank
            self.animating = True
            match_score = len(match) * 10
            self.animate_score(match_score, match[0])
            self.animating = False
            self.score += match_score
            self.draw()

    def animate_score(self, score, loc):
        score_text = str(score)
        y = BORDER + loc[0] * (CELLWIDTH + MARGIN)
        x = BORDER + loc[1] * (CELLHEIGHT + MARGIN)
        for i in range(10):
            draw_text(score_text, 24, x, y, BLACK)
            pygame.display.update()
            clock.tick(FPS)

    def fill_blanks(self):
        for col in range(COLS):
            for row in range(ROWS):
                if self.board[row][col] == self.blank:
                    test = 0
                    length = 0
                    # how long is the clear space?
                    while row + test < ROWS and self.board[row+test][col] == self.blank:
                        length += 1
                        test += 1
                    for blank_row in range(row, ROWS):
                        try:
                            self.board[blank_row][col] = self.board[blank_row+length][col]
                        except:
                            self.board[blank_row][col] = random.choice(self.shapes)

    def clicked(self, pos):
        # convert the pos to a grid location
        click_col = pos[0] // (CELLWIDTH + MARGIN)
        click_row = pos[1] // (CELLHEIGHT + MARGIN)
        # if we click outside the board, select nothing
        if click_col >= COLS or click_row >= ROWS:
            self.selected = None
        else:
            if not self.selected:
                self.selected = (click_row, click_col)
            elif self.selected[0] == click_row and self.selected[1] == click_col:
                self.selected = None
            elif not self.animating:
                if self.adjacent(self.selected, (click_row, click_col)):
                    self.swap(self.selected, (click_row, click_col))
                    self.selected = None

    def adjacent(self, loc1, loc2):
        if (loc1[0] == loc2[0] and abs(loc1[1]-loc2[1]) == 1) or (loc1[1] == loc2[1] and abs(loc1[0]-loc2[0]) == 1):
            return True
        return False

    def swap(self, loc1, loc2):
        self.board[loc1[0]][loc1[1]], self.board[loc2[0]][loc2[1]] = self.board[loc2[0]][loc2[1]], self.board[loc1[0]][loc1[1]]

def draw_text(text, size, x, y, color=WHITE):
    # utility function to draw text on screen
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

# initialize pygame
pygame.init()
# initialize sound - remove if you're not using sound
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

board = Board()
board.shuffle()

running = True
while running:
    clock.tick(FPS)
    # check for all your events
    for event in pygame.event.get():
        # this one checks for the window being closed
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # now check for keypresses
        elif event.type == pygame.KEYDOWN:
            # this one quits if the player presses Esc
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # add any other key events here
            # if event.key == pygame.K_SPACE:
            #     board.fill_blanks()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            board.clicked(event.pos)

    ##### Game logic goes here  #########
    m = board.find_matches()
    board.clear_matches(m)
    board.fill_blanks()
    ##### Draw/update screen #########
    screen.fill(BGCOLOR)
    board.draw()
    score_text = 'Score: %s' % board.score
    draw_text(score_text, 18, BORDER, HEIGHT-30)
    # after drawing, flip the display
    pygame.display.flip()
