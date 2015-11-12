from pygame.locals import *
import pygame

pygame.init()
size = width, height = 500, 700
screen = pygame.display.set_mode(size)
# consider naming your group something more friendly
plr_g = pygame.sprite.Group()

blue = (0, 206, 209)

class Player(pygame.sprite.Sprite):
    # assuming s_x and s_y are supposed to be size. What about using width/height?
    def __init__(self, w, h):
        pygame.sprite.Sprite.__init__(self, plr_g)
        # what are these for?
        # self.s_x = 300
        # self.s_y = 300
        self.image = pygame.Surface([w, h])
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        # this isn't necessary, since you're adding to the group in the __super__ call
        # plr_g.add(self)
        # set your location via the rect:
        self.rect.center = (250, 350)


player = Player(50, 50)
while True:
    for event in pygame.event.get():
        # don't put multiple statements on a single line
        if event.type == pygame.QUIT:
            sys.exit()

    plr_g.update()

    screen.fill((50, 50, 50))
    plr_g.draw(screen)
    pygame.display.flip()
