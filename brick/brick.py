import pygame as pg
import random as rand
from brick_settings import *
from brick_sprites import *
from os import path

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.running = True
        
    def load_data(self):
        self.dir = path.dirname(__file__)
        self.spritesheet = Spritesheet(path.join(self.dir, 'puzzleAssets_sheet.png'))
        sound_folder = path.join(path.dirname(__file__), 'brick_sounds')
        self.wall_sound = pg.mixer.Sound(path.join(sound_folder, 'wall.wav'))
        self.start_sound = pg.mixer.Sound(path.join(sound_folder, 'start.wav'))
        self.paddle_sound = pg.mixer.Sound(path.join(sound_folder, 'paddle.wav'))
        self.lose_sound = pg.mixer.Sound(path.join(sound_folder, 'lose.wav'))
        self.brick_sounds = []
        for i in range(3):
            file = 'brick{}.wav'.format(i)
            self.brick_sounds.append(pg.mixer.Sound(path.join(sound_folder, file)))
        
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.balls = pg.sprite.Group()
        self.bricks = pg.sprite.Group()
        self.start_sound.play()
        self.playing = True
        self.score = 0
        self.shake = False
        self.paddle = Paddle(self.spritesheet.get_image(0, 100, 104, 24))
        self.all_sprites.add(self.paddle)
        self.ball = Ball(self, self.spritesheet.get_image(23, 480, 22, 22))
        self.all_sprites.add(self.ball)
        self.balls.add(self.ball)
        self.spawn_bricks()
        self.start_anim()
        self.game_loop()
    
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
        
    def start_anim(self):
        anim_group = self.bricks.copy()
        for sprite in anim_group:
            sprite.target = sprite.rect.y
            sprite.rect.y -= HEIGHT
            sprite.start = rand.randrange(500)
        t = pg.time.get_ticks()
        while len(anim_group) > 0:
            self.clock.tick(FPS)
            self.events()
            for sprite in anim_group:
                if pg.time.get_ticks() - t > sprite.start:
                    sprite.rect.y += (sprite.target - sprite.rect.y) * 0.1
                    if sprite.target - sprite.rect.y < 10:
                        sprite.rect.y += 1
                    if sprite.rect.y == sprite.target:
                        anim_group.remove(sprite)
            self.screen.fill(BGCOLOR)
            self.all_sprites.draw(self.screen)
            pg.display.flip()
            
    def screen_shake(self, amount):
        if not self.shake:
            self.shake_x = rand.randrange(-amount, amount)
            self.shake_y = rand.randrange(-amount, amount)
            for sprite in self.all_sprites:
                sprite.rect.x += self.shake_x
                sprite.rect.y += self.shake_y
            self.shake = True
            self.shake_time = pg.time.get_ticks()
            
    def spawn_bricks(self):
        img_list = [self.spritesheet.get_image(0, 183, 64, 32),
                    self.spritesheet.get_image(0, 447, 64, 32),
                    self.spritesheet.get_image(0, 414, 64, 32),
                    self.spritesheet.get_image(65, 183, 64, 32),
                    self.spritesheet.get_image(0, 249, 64, 32)]
        for y in range(10):
            for x in range(25):
                brick = Brick(16 + x * (BRICK_WIDTH + BRICK_SPACING),
                              60 + y * (BRICK_HEIGHT + BRICK_SPACING),
                              img_list[y//2])
                self.all_sprites.add(brick)
                self.bricks.add(brick)
                
    def game_loop(self):
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                self.playing = False
        
    def update(self):
        self.all_sprites.update()
        # end shaking
        if self.shake and pg.time.get_ticks() - self.shake_time > 50:
            for sprite in self.all_sprites:
                sprite.rect.x -= self.shake_x
                sprite.rect.y -= self.shake_y
            self.shake = False
        # bounce balls off paddle
        hit_ball = pg.sprite.spritecollide(self.paddle, self.balls, False)
        for ball in hit_ball:
            self.screen_shake(8)
            self.paddle_sound.play()
            ball.vel.y *= -1
            ball.rect.bottom = self.paddle.rect.top
            dist = ball.rect.centerx - self.paddle.rect.centerx
            ball.vel.x = BALL_SPEED * dist * (1 / 50)
            ball.vel = ball.vel.normalize() * BALL_SPEED
        # ball hits bricks
        for ball in self.balls:
            brick_hits = pg.sprite.spritecollide(ball, self.bricks, False)
            for brick in brick_hits:
                if not brick.hit:
                    brick.hit = True
                    rand.choice(self.brick_sounds).play()
                    self.bricks.remove(brick)
                    self.score += 1
            if brick_hits:
                self.screen_shake(10)
                ball.vel.y *= -1
            if ball.rect.bottom > HEIGHT:
                ball.kill()
        # next level
        if len(self.bricks) == 0:
            self.spawn_bricks()
            for ball in self.balls:
                ball.kill()
            ball = Ball(self)
            self.all_sprites.add(ball)
            self.balls.add(ball)
        # game over
        if len(self.balls) == 0:
            self.playing = False
                    
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH*3/4, 20)
        pg.display.flip()
        
    def game_over_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text("BRICK SMASHER!", 64, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Press a key to play", 18, WHITE, WIDTH/2, HEIGHT * 3/4)
        pg.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
        
    def start_screen(self):
        pass
        
g = Game()
g.game_over_screen()
while g.running:
    g.new()
    g.game_over_screen()

pg.quit()