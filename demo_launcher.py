# GameMenu.py
# Utility classes to display a menu on the screen
# TODO: Background image
# TODO: Button/text images
# TODO: Select cursor / highlight
# TODO: Sounds
# TODO: Animations?
# TODO: Convert to use ptext.py
import pygame
import sys
from subprocess import Popen, call
from os import path

class MenuItem(pygame.font.Font):
    def __init__(self, text, font, font_size=30, color=(255, 255, 255), padding=0):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.label = self.render(self.text, True, self.color)
        self.rect = self.label.get_rect()
        self.rect.inflate_ip(0, padding)
        self.width = self.rect.width
        self.height = self.rect.height
        self.size = (self.width, self.height)
        self.posx = 0
        self.posy = 0
        self.pos = (0, 0)

    def set_pos(self, x, y):
        self.pos = (x, y)
        self.posx = x
        self.posy = y

    def set_color(self, col):
        self.color = col
        self.label = self.render(self.text, True, self.color)

    def is_selected_mouse(self):
        posx, posy = pygame.mouse.get_pos()
        if (posx >= self.posx and posx <= self.posx + self.width) and \
           (posy >= self.posy and posy <= self.posy + self.height):
            return True
        return False

class GameMenu:
    def __init__(self, game, title, items, bg_color=(0, 0, 0), bg_image=None,
                 font=None, font_size=30, color=(255, 255, 255), hcolor=(255, 0, 0),
                 padding=40):
        self.game = game
        self.bg_image = bg_image
        self.title = title
        self.width = self.game.screen.get_width()
        self.height = self.game.screen.get_height()
        self.bg_color = bg_color
        self.color = color
        self.hcolor = hcolor
        self.items = []
        self.cur_item = None
        self.mouse_visible = True
        self.padding = padding
        for index, item in enumerate(items):
            menu_item = MenuItem(item, font, font_size, color, self.padding)
            total_height = len(items) * menu_item.height
            posx = (self.width / 2) - (menu_item.width / 2)
            posy = (self.height / 2) - (total_height / 2) + ((index * 2) + index * menu_item.height) + 50
            menu_item.set_pos(posx, posy)
            self.items.append(menu_item)

    def set_mouse_hover(self, item):
        # highlight the mouse hover item
        if item.is_selected_mouse():
            item.set_color(self.hcolor)
            self.cur_item = self.items.index(item)
            # item.set_italic(True)
        else:
            item.set_color(self.color)
            # item.set_italic(False)

    def set_keyb_selection(self, key):
        # highlight menu item by key selection
        for item in self.items:
            # item.set_italic(False)
            item.set_color(self.color)

        if self.cur_item is None:
            self.cur_item = 0
        else:
            if key == pygame.K_RETURN:
                self.go()
            elif key == pygame.K_UP:
                self.cur_item -= 1
            elif key == pygame.K_DOWN:
                self.cur_item += 1
            self.cur_item = self.cur_item % len(self.items)

        # self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_color(self.hcolor)

    def go(self):
        # execute the selected item's action
        d = path.dirname(__file__)
        if self.cur_item is None:
            return
        if self.items[self.cur_item].text == "Quit":
            pygame.quit()
            sys.exit()
        elif self.items[self.cur_item].text == "Shmup":
            fname = path.join(d, 'tutorials/shmup/shmup-14.py')
            call(['python3', fname])
        elif self.items[self.cur_item].text == "Snake":
            fname = path.join(d, 'snake/snake_oo.py')
            call(['python3', fname])
        elif self.items[self.cur_item].text == "Jump":
            fname = path.join(d, 'tutorials/platform/working/main.py')
            call(['python3', fname])
        elif self.items[self.cur_item].text == "Flappy":
            fname = path.join(d, 'flap/flap.py')
            call(['python3', fname])
        elif self.items[self.cur_item].text == "Snake Duel":
            fname = path.join(d, 'snake_duel/snake_duel.py')
            call(['python3', fname])
        elif self.items[self.cur_item].text == "Bricks":
            fname = path.join(d, 'brick/brick.py')
            call(['python3', fname])
        elif self.items[self.cur_item].text == "Tetris":
            fname = path.join(d, 'tetris/tetris2.py')
            call(['python3', fname])

    def run(self):
        self.running = True
        while self.running:
            self.game.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN]:
                        self.mouse_visible = False
                        self.set_keyb_selection(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.is_selected_mouse():
                            self.go()
            # return mouse visibility if mouse moves
            if pygame.mouse.get_rel() != (0, 0):
                self.mouse_visible = True
                self.cur_item = None

            pygame.mouse.set_visible(self.mouse_visible)
            self.game.screen.fill((0, 0, 0))
            if self.bg_image:
                self.game.screen.blit(self.bg_image, (0, 0))

            if type(self.title) is str:
                self.game.draw_text(self.title, 40, self.game.screen.get_width() / 2, 40)

            if self.bg_image:
                self.game.screen.blit(self.bg_image, self.bg_rect)
            for item in self.items:
                if self.mouse_visible:
                    self.set_mouse_hover(item)
                self.game.screen.blit(item.label, item.pos)
            pygame.display.flip()


# for testing
if __name__ == "__main__":
    class Game:
        def __init__(self):
            pygame.init()
            self.screen = pygame.display.set_mode((480, 700))
            self.clock = pygame.time.Clock()

        def draw_text(self, text, size, x, y, center=True):
            # utility function to draw text at a given location
            # TODO: move font matching to beginning of file (don't repeat)
            font_name = pygame.font.match_font('arial')
            font = pygame.font.Font(font_name, size)
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            if center:
                text_rect.midtop = (x, y)
            else:
                text_rect.topleft = (x, y)
            return self.screen.blit(text_surface, text_rect)

    g = Game()
    font = pygame.font.match_font("Ubuntu Mono")
    # standard list of options and customized labels
    game_list = ["Shmup", "Snake", "Snake Duel", "Jump", "Flappy",
                 "Bricks", "Tetris"]
    menu = GameMenu(g, "Pygame Launcher", game_list, font=font, font_size=32)
    menu.run()
    print("starting game")
