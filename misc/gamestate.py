import pygame as pg
import os

class StateManager:
    def __init__(self, screen, state):
        self.screen = screen
        self.state = state

    def change(self, state):
        self.state = state
        print("Changed to state: " + state)

    def update(self):
        self.state.update()

    def draw(self):
        self.state.draw()

class GameState:
    """Generic game state object"""

    def __init__(self, screen):
        self.screen = screen
        self.name = None
        self.label = None
        self.bgcolor = (20, 20, 20)
        pg.display.set_caption(self.label)

    def update(self):
        pass

    def draw(self):
        pass

    def events(self):
        pass

class SplashScreen(GameState):
    """docstring for SplashScreen"""

    def __init__(self, screen):
        GameState.__init__(self, screen)
        self.name = "splash"
        self.label = "Welcome!"

    def draw(self):
        self.screen.fill(self.bgcolor)
        # draw title and splash images here
        pass

    def
