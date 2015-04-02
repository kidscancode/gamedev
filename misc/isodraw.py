# Demonstrate isometric coordinate mapping
# by KidsCanCode 2015
# For educational purposes only
import pygame
# ptext module for pygame text rendering and formatting
import ptext

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ortho vs. Iso Coordinates")
clock = pygame.time.Clock()
# OFFSETS for drawing grid in a reasonable location
ISO_OFFSETX = 400
ISO_OFFSETY = 50
ORTHO_OFFSETX = 50
ORTHO_OFFSETY = 50
GRIDSIZE = 50
# alias for Vector2 class (saves typing)
vec = pygame.math.Vector2

# current grid pos and screen pos
pos = pygame.math.Vector2(0, 0)
scr_pos = pygame.math.Vector2(0, 0)

def iso_to_screen(pt):
    # convert a given grid position to screen coordinates in isometric mode
    screen_x = pt.x - pt.y + ISO_OFFSETX
    screen_y = (pt.x + pt.y) / 2 + ISO_OFFSETY
    return vec(screen_x, screen_y)

def screen_to_iso(pos):
    # convert a screen coordinate to grid position (ex: mouse click)
    grid_x = (pos.x + 2 * pos.y - ISO_OFFSETX - 2 * ISO_OFFSETY) / 2
    grid_y = (2 * pos.y - pos.x + ISO_OFFSETX - 2 * ISO_OFFSETY) / 2
    return vec(grid_x, grid_y)

def draw_ortho_grid():
    # draw the orthographic grid
    for x in range(0, GRIDSIZE*11, GRIDSIZE):
        start = vec(x+ORTHO_OFFSETX, 0+ORTHO_OFFSETY)
        end = vec(x+ORTHO_OFFSETX, GRIDSIZE*10+ORTHO_OFFSETY)
        pygame.draw.line(screen, (128, 128, 128), (start.x, start.y), (end.x, end.y))
    for y in range(0, GRIDSIZE*11, GRIDSIZE):
        start = vec(0+ORTHO_OFFSETX, y+ORTHO_OFFSETY)
        end = vec(GRIDSIZE*10+ORTHO_OFFSETX, y+ORTHO_OFFSETY)
        pygame.draw.line(screen, (128, 128, 128), (start.x, start.y), (end.x, end.y))

def draw_iso_grid():
    # draw the isometric grid
    for x in range(0, GRIDSIZE*11, GRIDSIZE):
        start = iso_to_screen(vec(x, 0))
        end = iso_to_screen(vec(x, GRIDSIZE*10))
        pygame.draw.line(screen, (128, 128, 128), (start.x, start.y), (end.x, end.y))
    for y in range(0, GRIDSIZE*11, GRIDSIZE):
        start = iso_to_screen(vec(0, y))
        end = iso_to_screen(vec(GRIDSIZE*10, y))
        pygame.draw.line(screen, (128, 128, 128), (start.x, start.y), (end.x, end.y))

def draw_point(pos, iso_mode):
    # draw a circle at the current grid pos
    if iso_mode:
        scr_pos = iso_to_screen(pos)
        pygame.draw.circle(screen, (255, 255, 255), (int(scr_pos.x), int(scr_pos.y)), 10)
    else:
        pygame.draw.circle(screen, (255, 255, 255),
                           (int(pos.x)+ORTHO_OFFSETX, int(pos.y)+ORTHO_OFFSETY), 10)

def draw_labels(iso_mode):
    # draw all the text on the screen (axis labels, current location, etc.)
    ptext.draw("Press <space> to change modes", midbottom=(400, 590))
    if iso_mode:
        ptext.draw("X", (610, 120), fontsize=40)
        ptext.draw("Y", (180, 120), fontsize=40)
        # ptext.draw("(0,0)", (390, 15))
        ptext.draw("X OFFSET: "+str(ISO_OFFSETX), bottomright=(790, 550), fontsize=30)
        ptext.draw("Y OFFSET: "+str(ISO_OFFSETY), bottomright=(790, 590), fontsize=30)
        ptext.draw("Grid Pos:", bottomleft=(10, 500), fontsize=30, fontname=None)
        ptext.draw("({:.0f}, {:.0f})".format(pos.x, pos.y),
                   bottomleft=(10, 530), fontsize=40,  fontname=None)
        ptext.draw("Screen Pos:", bottomleft=(10, 560), fontsize=30, fontname=None)
        ptext.draw("({:.0f}, {:.0f})".format(scr_pos.x, scr_pos.y),
                   bottomleft=(10, 590), fontsize=40, fontname=None)
    else:
        ptext.draw("X", midtop=(300, 10), fontsize=40)
        ptext.draw("Y", midleft=(20, 300), fontsize=40)
        ptext.draw("X OFFSET: "+str(ORTHO_OFFSETX), bottomright=(790, 550), fontsize=30)
        ptext.draw("Y OFFSET: "+str(ORTHO_OFFSETY), bottomright=(790, 590), fontsize=30)
        ptext.draw("Grid Pos:", topleft=(560, 50), fontsize=30, fontname=None)
        ptext.draw("({:.0f}, {:.0f})".format(pos.x, pos.y),
                   topleft=(560, 80), fontsize=40, fontname=None)
        ptext.draw("Screen Pos:", topleft=(560, 120), fontsize=30, fontname=None)
        ptext.draw("({:.0f}, {:.0f})".format(scr_pos.x, scr_pos.y),
                   topleft=(560, 150), fontsize=40, fontname=None)

def do_click(pos, iso_mode):
    # testing the screen_to_iso conversion
    if iso_mode:
        pos = vec(pos[0], pos[1])
        grid_pos = screen_to_iso(pos)
        print("Screen: ({}, {})".format(pos.x, pos.y))
        print("Grid: ({}, {})".format(grid_pos.x, grid_pos.y))

# Flag for iso/ortho mode - start in Ortho
iso_mode = False
while True:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            do_click(event.pos, iso_mode)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_SPACE:
                # toggle between iso & ortho mode
                iso_mode = not iso_mode
            elif event.key == pygame.K_LEFT:
                pos.x -= GRIDSIZE
            elif event.key == pygame.K_RIGHT:
                pos.x += GRIDSIZE
            elif event.key == pygame.K_UP:
                pos.y -= GRIDSIZE
            elif event.key == pygame.K_DOWN:
                pos.y += GRIDSIZE
            # don't allow movement off the grid
            if pos.x < 0:
                pos.x = 0
            if pos.y < 0:
                pos.y = 0
            if pos.x > GRIDSIZE*10:
                pos.x = GRIDSIZE*10
            if pos.y > GRIDSIZE*10:
                pos.y = GRIDSIZE*10

    screen.fill((0, 0, 0))
    if iso_mode:
        draw_iso_grid()
        draw_labels(iso_mode)
        draw_point(pos, iso_mode)
        scr_pos = iso_to_screen(pos)
    else:
        draw_ortho_grid()
        draw_labels(iso_mode)
        draw_point(pos, iso_mode)
        scr_pos.x, scr_pos.y = pos.x+ORTHO_OFFSETX, pos.y+ORTHO_OFFSETY

    pygame.display.flip()
