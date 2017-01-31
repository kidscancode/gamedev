import pygame as pg
from settings import *
from tools import *

class Snake:
    def __init__(self, game, loc, length, images):
        self.game = game
        self.segments = []
        for i in range(length):
            self.segments.append(Coord(loc.x - i, loc.y))
        self.images = images
        self.dir = 'r'
        self.last_move = 0

    @property
    def head(self):
        return self.segments[0]

    def draw(self, surf, camera):
        for segment in self.segments[1:]:
            segment.draw(surf, camera, self.images[1])
        # draw the head, rotate in dir
        img = pg.transform.rotate(self.images[0], ROTATIONS[self.dir])
        self.head.draw(surf, camera, img)
        # draw the tails, rotate in dir
        # img = pg.transform.rotate(self.images[2], ROTATIONS[self.dir])
        # self.segments[-1].draw(surf, camera, img)

    def hit_self(self):
        if self.head in self.segments[1:]:
            return True
        return False

    def hit_walls(self):
        if self.head.x in [-1, GRIDWIDTH] or self.head.y in [-1, GRIDHEIGHT]:
            return True
        if self.head in self.game.tilemap.walls:
            return True
        return False

    def move(self):
        now = pg.time.get_ticks()
        if now - self.last_move > SNAKE_SPEED:
            self.last_move = now
            new_head = Coord(self.head.x + DIRECTIONS[self.dir][0],
                             self.head.y + DIRECTIONS[self.dir][1])
            self.segments.insert(0, new_head)
            if self.head == self.game.apple:
                self.game.apple = self.game.tilemap.get_random_tile(1)
            else:
                del self.segments[-1]
