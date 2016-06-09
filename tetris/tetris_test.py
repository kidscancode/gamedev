import pygame as pg
import random
from tetris_shapes import *

# game settings
WIDTH = 500
HEIGHT = 600
FPS = 60
BLOCKSIZE = 20
BOARDWIDTH = 12
BOARDHEIGHT = 25
SIDEMARGIN = int((WIDTH - BOARDWIDTH * BLOCKSIZE) / 2)
TOPMARGIN = HEIGHT - (BOARDHEIGHT * BLOCKSIZE) - 10

# colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 128, 0)
CYAN = (0, 255, 255)
GREY = (50, 50, 50)
BGCOLOR = BLACK
COLORS = [BLACK, GREEN, BLUE, RED, YELLOW, PURPLE, ORANGE, CYAN]

SHAPES = {'S': S_SHAPE,
          'Z': Z_SHAPE,
          'O': O_SHAPE,
          'I': I_SHAPE,
          'J': J_SHAPE,
          'L': L_SHAPE,
          'T': T_SHAPE}
          
font_name = pg.font.match_font('arial bold')
def draw_text(surf, text, size, color, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.x = x
    text_rect.y = y
    surf.blit(text_surface, text_rect)
            
class Piece:
    def __init__(self):
        self.shape = random.choice(list(SHAPES.keys()))
        self.rotation = random.randrange(len(SHAPES[self.shape]))
        self.x = int(BOARDWIDTH / 2) - int(5 / 2)
        self.y = -1
        self.color = random.randrange(1, len(COLORS))
    
    def rotate(self, dir):
        if dir == 'r':
            self.rotation = (self.rotation + 1) % len(SHAPES[self.shape])
        else:
            self.rotation = (self.rotation - 1) % len(SHAPES[self.shape])
            
    def draw(self, dx=0, dy=0):
        for y, row in enumerate(SHAPES[self.shape][self.rotation]):
            y += self.y + dy
            if y >= 0 and y < BOARDHEIGHT:
                for x, block in enumerate(row):
                    if int(block):
                        x += self.x + dx
                        px = SIDEMARGIN + BLOCKSIZE * x
                        py = TOPMARGIN + BLOCKSIZE * y
                        rect = pg.Rect(px, py, BLOCKSIZE, BLOCKSIZE)
                        pg.draw.rect(screen, COLORS[self.color], rect)
                        pg.draw.rect(screen, BLACK, rect, 1)
        
class Board:
    def __init__(self):
        self.board = []
        for i in range(BOARDHEIGHT):
            self.board.append([0] * BOARDWIDTH)
        self.piece = Piece()
        self.next = Piece()
        self.score = 0
        self.level = 1
        self.drop_speed = 500
                        
    def draw_board(self):
        # draw board outline
        rect = pg.Rect(SIDEMARGIN, TOPMARGIN, BOARDWIDTH * BLOCKSIZE, BOARDHEIGHT * BLOCKSIZE)
        pg.draw.rect(screen, GREY, rect, 5)
        # show score
        draw_text(screen, 'Level: '+str(self.level), 32, WHITE, 
                  BOARDWIDTH * BLOCKSIZE + SIDEMARGIN + 10, 100)
        draw_text(screen, 'Lines: '+str(self.score), 32, WHITE, 
                  BOARDWIDTH * BLOCKSIZE + SIDEMARGIN + 10, 130)
        # show next
        draw_text(screen, 'Next:', 28, WHITE, BOARDWIDTH * BLOCKSIZE + SIDEMARGIN + 10, 200)
        box_size = BLOCKSIZE * 5
        box_rect = pg.Rect(0, 0, box_size, box_size)
        box_rect.center = (BOARDWIDTH * BLOCKSIZE + SIDEMARGIN * 1.5, 300)
        pg.draw.rect(screen, GREY, box_rect, 5)
        self.next.draw(dx=9, dy=9)
        # draw board spaces
        for y, row in enumerate(self.board):
            for x, block in enumerate(row):
                if int(block):
                    px = SIDEMARGIN + BLOCKSIZE * x
                    py = TOPMARGIN + BLOCKSIZE * y
                    rect = pg.Rect(px, py, BLOCKSIZE, BLOCKSIZE)
                    pg.draw.rect(screen, COLORS[int(block)], rect)
                    pg.draw.rect(screen, BLACK, rect, 1)
                    
    
    def collide_with_board(self, dx, dy):
        # check if piece collides with board when moved dx, dy
        for y, row in enumerate(SHAPES[self.piece.shape][self.piece.rotation]):
            for x, block in enumerate(row):
                if int(block):
                    if x + self.piece.x + dx < 0:
                        return True
                    elif x + self.piece.x + dx >= BOARDWIDTH:
                        return True
                    elif y + self.piece.y + dy >= BOARDHEIGHT:
                        return True
                    elif int(self.board[y+self.piece.y+dy][x+self.piece.x+dx]):
                        return True
        return False
                    
        
    def drop_piece(self):
        if not self.collide_with_board(dx=0, dy=1):
            self.move_piece(dx=0, dy=1)
        else:
            self.absorb_piece()
            self.delete_lines()
    
    def full_drop_piece(self):
        while not self.collide_with_board(dx=0, dy=1):
            self.drop_piece()
        self.drop_piece()
        
    def game_over(self):
        if sum(self.board[0]) > 0 or sum(self.board[1]) > 0:
            return True
        return False
        
    def can_move(self, dx, dy):
        if self.collide_with_board(dx=dx, dy=dy):
            return False
        return True
        
    def move_piece(self, dx=0, dy=0):
        if self.can_move(dx, dy):
            self.piece.x += dx
            self.piece.y += dy
        
    def absorb_piece(self):
        for y, row in enumerate(SHAPES[self.piece.shape][self.piece.rotation]):
            for x, block in enumerate(row):
                if int(block):
                    self.board[y + self.piece.y][x + self.piece.x] = self.piece.color
        self.piece = self.next
        self.next = Piece()
        
    def try_rotate(self):
        self.piece.rotate('r')
        collide = self.collide_with_board(dx=0, dy=0)
        if collide:
            self.piece.rotate('l')
        
    def delete_lines(self):
        remove = [y for y, row in enumerate(self.board) if all(row)]
        for y in remove:
            for line in reversed(range(1, y+1)):
                self.board[line] = list(self.board[line-1])
            self.score += 1
            if self.score % 10 == 0:
                self.level += 1
                self.drop_speed -= 50
                pg.time.set_timer(DROP_EVENT, self.drop_speed)
                    
            
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Tetris")
clock = pg.time.Clock()
pg.mixer.music.load('Tetris.ogg')

board = Board()
DROP_EVENT = pg.USEREVENT
pg.time.set_timer(DROP_EVENT, board.drop_speed)

# Game Loop
pg.mixer.music.play(loops=-1)
running = True
while running:
    # Events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == DROP_EVENT:
            board.drop_piece()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                board.move_piece(dx=1)
            if event.key == pg.K_LEFT:
                board.move_piece(dx=-1)
            if event.key == pg.K_UP:
                board.try_rotate()
            if event.key == pg.K_DOWN:
                board.drop_piece()
            if event.key == pg.K_SPACE:
                board.full_drop_piece()

    # Updates
    if board.game_over():
        running = False
    # Draw
    screen.fill(BGCOLOR)
    board.draw_board()
    board.piece.draw()
    pg.display.flip()
    
pg.quit()