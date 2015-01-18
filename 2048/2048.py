# 2048 - Yet another 2048 clone
# by KidsCanCode 2014
# For educational purposes only

# TODO:
# Animate moving tiles

import pygame
import sys
import random

# define some colors (R, G, B)
BLACK = (0, 0, 0)
BGCOLOR = BLACK

# constants for game options
FPS = 15
TILESIZE = 100
MARGIN = 5
BORDER = 8
WIDTH = TILESIZE * 4 + MARGIN * 3 + BORDER * 2
HEIGHT = WIDTH
# increasingly deeper shades of red, based on tile value
COLORS = {0: "0x000000",
          2: "0xFFFFFF",
          4: "0xFFEEEE",
          8: "0xFFDDDD",
          16: "0xFFCCCC",
          32: "0xFFBBBB",
          64: "0xFFAAAA",
          128: "0xFF9999",
          256: "0xFF8888",
          512: "0xFF7777",
          1024: "0xFF6666",
          2048: "0xFF5555",
          4096: "0xFF4444",
          8192: "0xFF3333",
          16384: "0xFF2222",
          32768: "0xFF1111",
          65536: "0xFF0000"}

class Tile(pygame.sprite.Sprite):
    def __init__(self, value=0):
        # create the tile sprite, default value is 0
        pygame.sprite.Sprite.__init__(self)
        self.value = value
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(pygame.Color(COLORS[self.value]))
        self.rect = self.image.get_rect()

    def update(self):
        # make sure we have the right color in case the value has increased
        self.image.fill(pygame.Color(COLORS[self.value]))
        # draw the value of the tile centered on it
        text_surface = FONT.render(str(self.value), True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (50, 40)
        self.image.blit(text_surface, text_rect)


class Board:
    # board object - holds all the tiles
    # new board has 2 random spots filled
    def __init__(self):
        self.sprite_list = pygame.sprite.Group()
        # list comprehension, creates a 4x4 grid as a list of lists
        # each of the items in the list is a tile object
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        for row in range(4):
            for col in range(4):
                self.board[row][col] = Tile()
                self.sprite_list.add(self.board[row][col])
        # self.can_move = True
        self.add_tile()
        self.add_tile()

    def draw(self):
        # draw the board, pause one tick between each tile movement
        # TODO: replace this with better animation
        clock.tick(FPS)
        for i, row in enumerate(self.board):
            for j, tile in enumerate(row):
                tile.rect.x = BORDER + j * TILESIZE + j * MARGIN
                tile.rect.y = BORDER + i * TILESIZE + i * MARGIN
        self.sprite_list.update()
        self.sprite_list.draw(screen)
        pygame.display.flip()

    def add_tile(self):
        # add a random new tile to am empty spot on the board
        # new tiles always have a value of 2
        if not self.full():
            while True:
                row = random.randrange(4)
                col = random.randrange(4)
                if self.board[row][col].value == 0:
                    self.board[row][col].value = 2
                    break

    def full(self):
        # test to see if board is full
        empty_spaces = 0
        for row in self.board:
            for tile in row:
                if tile.value == 0:
                    empty_spaces += 1
        if empty_spaces == 0:
            return True
        else:
            return False

    def move_left(self):
        # move the board to the left
        done = False
        while not done:
            moved = False
            for i, row in enumerate(self.board):
                for j, tile in enumerate(row):
                    # we ignore the tiles in the leftmost column, they can't move
                    # and we ignore 0 value tiles
                    if j > 0 and tile.value > 0:
                        if self.board[i][j-1].value == 0:
                            # it can move to the left, so shift it
                            self.board[i][j-1].value = tile.value
                            tile.value = 0
                            moved = True
                        elif self.board[i][j-1].value == tile.value:
                            # the tile to the left is equal, so add them!
                            self.board[i][j-1].value *= 2
                            tile.value = 0
                            moved = True
            self.draw()
            if not moved:
                done = True

    def move_right(self):
        # move the board right
        done = False
        while not done:
            moved = False
            # count from the right going left
            for i, row in enumerate(self.board):
                for j in range(3, -1, -1):
                    # ignore the tiles in the rightmost column
                    if j < 3 and self.board[i][j].value > 0:
                        if self.board[i][j+1].value == 0:
                            # it can move to the right, so shift it
                            self.board[i][j+1].value = self.board[i][j].value
                            self.board[i][j].value = 0
                            moved = True
                        elif self.board[i][j+1].value == self.board[i][j].value:
                            # the tile to the right is equal, so add them!
                            self.board[i][j+1].value *= 2
                            self.board[i][j].value = 0
                            moved = True
            self.draw()
            if not moved:
                done = True

    def move_up(self):
        # move the board upward
        done = False
        while not done:
            moved = False
            for i, row in enumerate(self.board):
                for j, tile in enumerate(row):
                    # we ignore the tiles in the top row, they can't move
                    # and we ignore 0 value tiles
                    if i > 0 and tile.value > 0:
                        if self.board[i-1][j].value == 0:
                            # it can move up, so shift it
                            self.board[i-1][j].value = tile.value
                            tile.value = 0
                            moved = True
                        elif self.board[i-1][j].value == tile.value:
                            # the tile above is equal, so add them!
                            self.board[i-1][j].value *= 2
                            tile.value = 0
                            moved = True
            self.draw()
            if not moved:
                done = True

    def move_down(self):
        # move the board down
        done = False
        while not done:
            moved = False
            # count from the bottom going up
            for i in range(3, -1, -1):
                for j in range(4):
                    # ignore the tiles in the bottom row
                    if i < 3 and self.board[i][j].value > 0:
                        if self.board[i+1][j].value == 0:
                            # it can move down, so shift it
                            self.board[i+1][j].value = self.board[i][j].value
                            self.board[i][j].value = 0
                            moved = True
                        elif self.board[i+1][j].value == self.board[i][j].value:
                            # the tile to the right is equal, so add them!
                            self.board[i+1][j].value *= 2
                            self.board[i][j].value = 0
                            moved = True
            self.draw()
            if not moved:
                done = True

# initialize pygame
pygame.init()
FONT_NAME = pygame.font.match_font('arial', True)
FONT = pygame.font.Font(FONT_NAME, 24)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
clock = pygame.time.Clock()

board = Board()

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
            if event.key == pygame.K_UP:
                board.move_up()
                board.add_tile()
            if event.key == pygame.K_DOWN:
                board.move_down()
                board.add_tile()
            if event.key == pygame.K_LEFT:
                board.move_left()
                board.add_tile()
            if event.key == pygame.K_RIGHT:
                board.move_right()
                board.add_tile()

    ##### Game logic goes here  #########

    ##### Draw/update screen #########
    screen.fill(BGCOLOR)
    board.draw()
