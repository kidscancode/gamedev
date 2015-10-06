# Collect the Blocks
# by KidsCanCode 2015
# Run around and collect the blocks
# For educational purposes only

# TODO: time bonus
# TODO: powerups
# TODO: more mob features (different types, etc)
# TODO: Level designs (walls, gravity (black holes?))

import pygame
import sys
import os
import random

# define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BGCOLOR = BLACK

WIDTH = 800
HEIGHT = 640
FPS = 60
TITLE = "Collect the Stuff!"


class Player(pygame.sprite.Sprite):
    # player sprite
    # realistic movement using equations of motion (pos, vel, accel)
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pygame.math.Vector2(WIDTH/2, HEIGHT/2)
        self.vel = pygame.math.Vector2(0, 0)
        self.accel = pygame.math.Vector2(0, 0)
        self.image = pygame.Surface((24, 24))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

    def update(self):
        self.accel = pygame.math.Vector2(0, 0)
        # keep accelerating as long as that dir key is down
        keystate = pygame.key.get_pressed()
        a = 1.5
        if FPS == 60:
            a = 0.7
        if keystate[pygame.K_LEFT]:
            self.accel.x = -a
        if keystate[pygame.K_RIGHT]:
            self.accel.x = a
        if keystate[pygame.K_UP]:
            self.accel.y = -a
        if keystate[pygame.K_DOWN]:
            self.accel.y = a
        # fix diagonals so they are same speed as orthoganal directions
        if self.accel.x != 0 and self.accel.y != 0:
            self.accel *= 0.7071

        # friction (based on vel)
        self.accel += self.vel * -0.12
        # grav example (not going to use in this game, but fun to see)
        # self.accel.y += .7

        # equations of motion
        # for simplicity, using t=1 (change per timestep)
        # p' = 0.5 at**2 + vt + p
        # v' = at + v
        self.vel += self.accel
        self.pos += self.accel * 0.5 + self.vel

        # move the sprite
        self.rect.x = int(self.pos.x)
        self.check_collisions('x')
        self.rect.y = int(self.pos.y)
        self.check_collisions('y')

    def check_collisions(self, dir):
        if dir == 'x':
            hit_list = pygame.sprite.spritecollide(self, g.walls, False)
            if hit_list:
                if self.vel.x > 0:
                    self.vel.x = 0
                    self.pos.x = hit_list[0].rect.left - self.rect.width
                    self.rect.right = hit_list[0].rect.left
                elif self.vel.x < 0:
                    self.vel.x = 0
                    self.pos.x = hit_list[0].rect.right
                    self.rect.left = hit_list[0].rect.right
        elif dir == 'y':
            hit_list = pygame.sprite.spritecollide(self, g.walls, False)
            if hit_list:
                if self.vel.y > 0:
                    self.vel.y = 0
                    self.pos.y = hit_list[0].rect.top - self.rect.height
                    self.rect.bottom = hit_list[0].rect.top
                elif self.vel.y < 0:
                    self.vel.y = 0
                    self.pos.y = hit_list[0].rect.bottom
                    self.rect.top = hit_list[0].rect.bottom
                self.speed_y = 0


class Box(pygame.sprite.Sprite):
    # simple static box
    # TODO: moving boxes?
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((24, 24))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Mob(pygame.sprite.Sprite):
    # bad guy!
    # will chase the player
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((24, 24))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.accel = pygame.math.Vector2(0, 0)
        # varied speeds (actually acceleration, but determines max speed)
        # TODO: different types of enemy based on speed?
        self.speed = random.choice([0.1, 0.2, 0.3, 0.4])
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

    def update(self):
        # friction (based on vel)
        self.accel += self.vel * -0.09

        # equations of motion - see Player class
        self.pos += self.accel * 0.5 + self.vel
        self.vel += self.accel

        # move the sprite
        self.rect.x = int(self.pos.x)
        self.check_collisions('x')
        self.rect.y = int(self.pos.y)
        self.check_collisions('y')

    def check_collisions(self, dir):
        if dir == 'x':
            hit_list = pygame.sprite.spritecollide(self, g.walls, False)
            if hit_list:
                if self.vel.x > 0:
                    self.vel.x = 0
                    self.pos.x = hit_list[0].rect.left - self.rect.width
                    self.rect.right = hit_list[0].rect.left
                elif self.vel.x < 0:
                    self.vel.x = 0
                    self.pos.x = hit_list[0].rect.right
                    self.rect.left = hit_list[0].rect.right
        elif dir == 'y':
            hit_list = pygame.sprite.spritecollide(self, g.walls, False)
            if hit_list:
                if self.vel.y > 0:
                    self.vel.y = 0
                    self.pos.y = hit_list[0].rect.top - self.rect.height
                    self.rect.bottom = hit_list[0].rect.top
                elif self.vel.y < 0:
                    self.vel.y = 0
                    self.pos.y = hit_list[0].rect.bottom
                    self.rect.top = hit_list[0].rect.bottom


class Wall(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()

    def new(self):
        # initialize for a new game
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.boxes = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.level = 1
        self.score = 0
        self.create_walls()
        self.create_enemies()
        self.create_boxes()

    def load_data(self):
        # load image and sound data
        game_dir = os.path.dirname(__file__)
        img_dir = os.path.join(game_dir, "img")
        wall_images = ["brick_blue32.png",
                       "brick_green32.png",
                       "brick_red32.png"]
        self.wall_images = []
        for img in wall_images:
            filename = os.path.join(img_dir, img)
            self.wall_images.append(pygame.image.load(filename).convert())

        # load level data from txt file
        self.level_data = [[]]
        with open(os.path.join(game_dir, "levels.txt"), 'rt') as f:
            lines = f.read().splitlines()
        for line in lines:
            if line[0] == ":":
                level = int(line[1])
                self.level_data.append([])
            else:
                self.level_data[level].append(line)

    def create_walls(self):
        # load level based on self.level
        # empty any old walls before creating new ones
        if self.level == len(self.level_data):
            self.running = False
        else:
            for wall in self.walls:
                self.all_sprites.remove(wall)
            self.walls.empty()
            img = random.choice(self.wall_images)
            for row, tiles in enumerate(self.level_data[self.level]):
                for col, tile in enumerate(tiles):
                    if tile == '1':
                        wall = Wall(img, col*16, row*32)
                        self.all_sprites.add(wall)
                        self.walls.add(wall)

    def create_enemies(self):
        # create number/type of enemies based on self.level
        self.enemies.empty()
        for i in range(self.level // 2):
            enemy = Mob(random.choice([35, WIDTH-60]),
                        random.choice([35, HEIGHT-60]))
            self.enemies.add(enemy)

    def create_boxes(self):
        # create number/type of boxes based on self.level
        self.boxes.empty()
        for i in range(self.level * 5):
            box = Box(random.randrange(35, WIDTH-59),
                      random.randrange(35, HEIGHT-59))
            # keep trying locs until we find an open one
            while pygame.sprite.spritecollide(box, self.walls, False):
                box.rect.topleft = (random.randrange(35, WIDTH-59),
                                    random.randrange(35, HEIGHT-59))
            self.boxes.add(box)
            self.all_sprites.add(box)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()  # check for events
            self.update()  # update the game state
            self.draw()    # draw the next frame

    def quit(self):
        pygame.quit()
        sys.exit()

    def events(self):
        # handle all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

    def update(self):
        # collide player w/boxes and remove them
        hit_list = pygame.sprite.spritecollide(self.player, self.boxes, True)
        self.score += len(hit_list)

        # if we level up
        if len(self.boxes) == 0:
            self.level += 1
            self.create_walls()
            self.create_boxes()
            self.create_enemies()
            self.player.vel = pygame.math.Vector2(0, 0)
            self.player.pos = pygame.math.Vector2(WIDTH/2, HEIGHT/2)

        # move mobs toward player
        for enemy in self.enemies:
            enemy.accel = pygame.math.Vector2(self.player.pos.x - enemy.pos.x,
                               self.player.pos.y - enemy.pos.y)
            enemy.accel = enemy.accel * (enemy.speed / enemy.accel.length())
            if pygame.sprite.collide_rect(enemy, self.player):
                self.running = False

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.update()
        self.enemies.update()
        self.all_sprites.draw(self.screen)
        self.enemies.draw(self.screen)
        score_txt = "Score: {:0}".format(self.score)
        self.draw_text(score_txt, 18, 33, 33)
        lvl_txt = "Level: {:0}".format(self.level)
        self.draw_text(lvl_txt, 18, 33, 53)
        # uncommment to show FPS (useful for troubleshooting)
        fps_txt = "{:.2f}".format(self.clock.get_fps())
        self.draw_text(str(fps_txt), 18, WIDTH-50, 10)
        pygame.display.flip()

    def draw_text(self, text, size, x, y):
        # utility function to draw text on screen
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def go_screen(self):
        pass

    def start_screen(self):
        pass


g = Game()
while True:
    g.start_screen()
    g.new()
    g.run()
    g.go_screen()
