# Brick breaker example
# by KidsCanCode 2015
# For educational purposes only
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder>
#     licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>

# TODO: Pause
# TODO: Start menu
# TODO: Game over
# TODO: High score
# TODO: Levels
# IDEAS: ball speed, powerups, brick layouts, brick buildin, screen buildin,
#        ball trail, particles
import pygame
import sys
import random

# define some colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
BGCOLOR = BLACK

# basic constants for your game options
TITLE = "Bricks!"
WIDTH = 800
HEIGHT = 600
FPS = 60

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BRICK_WIDTH = 50
BRICK_HEIGHT = 20
BRICK_SPACING = 5
BRICK_COLORS = [BLUE, GREEN, YELLOW, ORANGE, RED]


class Paddle(pygame.sprite.Sprite):
    def __init__(self, images):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
        # self.image.fill(GREEN)
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.posx = WIDTH / 2 - self.rect.width / 2
        self.velx = 0
        self.accelx = 0
        self.rect.x = self.posx
        self.rect.bottom = HEIGHT - 40

    def update(self):
        self.accelx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.accelx = -2.7
        if keystate[pygame.K_RIGHT]:
            self.accelx = 2.7

        # friction and motion
        self.accelx += self.velx * -0.2
        self.posx += self.accelx * 0.5 + self.velx
        self.velx += self.accelx

        # update position
        self.rect.x = self.posx
        if self.rect.left < 0:
            # self.rect.left = 0
            self.posx = 0
            self.velx = 0
        if self.rect.right > WIDTH:
            # self.rect.right = WIDTH
            self.posx = WIDTH - self.rect.width
            self.velx = 0


class Ball(pygame.sprite.Sprite):
    def __init__(self, images):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 9
        self.pos = pygame.math.Vector2(WIDTH/2, HEIGHT/2)
        self.vel = pygame.math.Vector2(random.randrange(-2, 2), -1)
        self.vel = self.vel.normalize() * self.speed
        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)
        # self.image = images[0]
        self.oldimage = self.image
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.hit = False
        self.hit_time = 0
        self.last_update = 0
        self.current_frame = 0

    def update(self):
        if self.hit:
            self.wobble()
        else:
            self.image = self.oldimage
        self.pos += self.vel
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        if self.rect.left < 0:
            self.pos.x = 0
            self.vel.x *= -1
        if self.rect.right > WIDTH:
            self.pos.x = WIDTH - self.rect.width
            self.vel.x *= -1
        if self.rect.top < 0:
            self.vel.y *= -1

    def wobble(self):
        now = pygame.time.get_ticks()
        if now - self.hit_time > 500:
            self.hit = False
            self.current_frame = 0
        if now - self.last_update > 10:
            self.last_update = now
            self.current_frame += 1
            x, y = self.rect.topleft
            self.image = pygame.transform.rotate(self.oldimage,
                                                 self.current_frame*5)
            self.rect = self.image.get_rect()
            self.rect.topleft = x, y


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, col):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([BRICK_WIDTH, BRICK_HEIGHT])
        self.image.fill(col)
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
        self.hit = False
        self.last_update = 0
        self.shrink_count = 0
        self.vely = 0

    def update(self):
        if self.hit:
            # use shrink effect
            self.shrink_away()
            # use fall effect
            self.fall_away()

    def shrink_away(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 30 and self.shrink_count < 10:
            self.last_update = now
            self.shrink_count += 1
            x, y = self.rect.center
            w = int(self.rect.width * 0.9)
            h = int(self.rect.height * 0.9)
            self.image = pygame.transform.smoothscale(self.image, (w, h))
            self.rect = self.image.get_rect()
            self.rect.center = x, y
        if self.shrink_count == 10:
            self.kill()

    def fall_away(self):
        self.vely += 0.5
        self.rect.y += self.vely


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        self.ball_images = []
        for fname in ['img/ballGrey.png', 'img/ballBlue.png']:
            img = pygame.image.load(fname).convert()
            self.ball_images.append(img)
        self.paddle_images = []
        for fname in ['img/paddleBlu.png', 'img/paddleRed.png']:
            img = pygame.image.load(fname).convert()
            self.paddle_images.append(img)
        pygame.mixer.music.load('snd/tgfcoder-FrozenJam-SeamlessLoop.ogg')
        pygame.mixer.music.set_volume(0.5)
        self.paddle_snd = pygame.mixer.Sound('snd/tone1.ogg')
        # self.paddle_snd.set_volume(0.9)
        self.brick_sounds = []
        for fname in ['snd/zap1.ogg', 'snd/zap2.ogg']:
            snd = pygame.mixer.Sound(fname)
            # snd.set_volume(0.9)
            self.brick_sounds.append(snd)

    def new(self):
        # initialize for a new game
        self.running = True
        self.shake = False
        self.level = 1
        self.score = 0
        self.chain = 0
        self.all_sprites = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.paddle = Paddle(self.paddle_images)
        self.all_sprites.add(self.paddle)
        ball = Ball(self.ball_images)
        self.balls.add(ball)
        self.all_sprites.add(ball)
        self.create_bricks()
        pygame.mixer.music.play(loops=-1)

    def create_bricks(self):
        for y in range(5):
            for x in range(14):
                brick = Brick(42+x*(BRICK_WIDTH+BRICK_SPACING),
                              60+y*(BRICK_HEIGHT+BRICK_SPACING),
                              BRICK_COLORS[y])
                self.all_sprites.add(brick)
                self.bricks.add(brick)

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
                if event.key == pygame.K_SPACE:
                    ball = Ball(self.ball_images)
                    self.balls.add(ball)
                    self.all_sprites.add(ball)

    def update(self):
        self.all_sprites.update()
        if self.shake and pygame.time.get_ticks() - self.shake_time > 50:
            for sprite in self.all_sprites:
                sprite.rect.x -= self.shake_x
                sprite.rect.y -= self.shake_y
            self.shake = False
        # bounce paddle
        # TODO: handle side hits
        hit_ball = pygame.sprite.spritecollide(self.paddle, self.balls, False)
        if hit_ball:
            for ball in hit_ball:
                self.paddle_snd.play()
                self.chain = 0
                ball.vel.y *= -1
                self.screen_shake(8)
                ball.pos.y = self.paddle.rect.top - ball.rect.height
                diff = ball.rect.centerx - self.paddle.rect.centerx
                ball.vel.x = ball.speed * diff * (1 / 55)
                ball.vel = ball.vel.normalize() * ball.speed

        # hit bricks
        for ball in self.balls:
            hit_bricks = pygame.sprite.spritecollide(ball, self.bricks, False)
            if hit_bricks:
                ball.vel.y *= -1
                self.screen_shake(6)
            for brick in hit_bricks:
                ball.hit = True
                ball.hit_time = pygame.time.get_ticks()
                brick.hit = True
                self.chain += 1
                self.score += 10 * (self.chain+1)
                brick.hit_time = pygame.time.get_ticks()
                brick.last_update = brick.hit_time
                self.bricks.remove(brick)
                self.brick_sounds[random.randrange(len(self.brick_sounds))].play()
            if ball.rect.bottom >= HEIGHT:
                ball.kill()

        if len(self.balls) == 0:
            self.running = False

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        score_txt = "Score: {:0}".format(self.score)
        self.draw_text(score_txt, 18, 20, 10)
        chain_txt = "Combo: {:0}".format(self.chain)
        self.draw_text(chain_txt, 18, WIDTH/2, 10)
        # uncommment to show FPS (useful for troubleshooting)
        fps_txt = "{:.2f}".format(self.clock.get_fps())
        self.draw_text(str(fps_txt), 18, WIDTH-50, 10)
        pygame.display.flip()

    def draw_text(self, text, size, x, y):
        # utility function to draw text at a given location
        # TODO: move font matching to beginning of file (don't repeat)
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def screen_shake(self, amount):
        if not self.shake:
            self.shake_x = random.randrange(-amount, amount+1)
            self.shake_y = random.randrange(-amount, amount+1)
            for sprite in self.all_sprites:
                sprite.rect.x += self.shake_x
                sprite.rect.y += self.shake_y
            self.shake = True
            self.shake_time = pygame.time.get_ticks()

    def start_screen(self):
        pass

    def go_screen(self):
        pass

g = Game()
while True:
    g.start_screen()
    g.new()
    g.run()
    g.go_screen()
