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

def draw_ortho_grid():
    # draw the orthographic grid
    for x in range(0, 550, 50):
        start = vec(x, 0)
        end = vec(x, 500)
        pygame.draw.line(screen, (128, 128, 128),
                         (start.x+ORTHO_OFFSETX, start.y+ORTHO_OFFSETY),
                         (end.x+ORTHO_OFFSETX, end.y+ORTHO_OFFSETY))
    for y in range(0, 550, 50):
        start = vec(0, y)
        end = vec(500, y)
        pygame.draw.line(screen, (128, 128, 128),
                         (start.x+ORTHO_OFFSETX, start.y+ORTHO_OFFSETY),
                         (end.x+ORTHO_OFFSETX, end.y+ORTHO_OFFSETY))

def draw_iso_grid():
    # draw the isometric grid
    for x in range(0, 550, 50):
        start = iso_to_screen(vec(x, 0))
        end = iso_to_screen(vec(x, 500))
        pygame.draw.line(screen, (128, 128, 128), (start.x, start.y), (end.x, end.y))
    for y in range(0, 550, 50):
        start = iso_to_screen(vec(0, y))
        end = iso_to_screen(vec(500, y))
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
# Flag for iso/ortho mode - start in Ortho
iso_mode = False
while True:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_SPACE:
                # toggle between iso & ortho mode
                iso_mode = not iso_mode
            elif event.key == pygame.K_LEFT:
                pos.x -= 50
            elif event.key == pygame.K_RIGHT:
                pos.x += 50
            elif event.key == pygame.K_UP:
                pos.y -= 50
            elif event.key == pygame.K_DOWN:
                pos.y += 50
            # don't allow movement off the grid
            if pos.x < 0:
                pos.x = 0
            if pos.y < 0:
                pos.y = 0
            if pos.x > 500:
                pos.x = 500
            if pos.y > 500:
                pos.y = 500

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
