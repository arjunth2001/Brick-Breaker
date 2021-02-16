import numpy as np
from Game_Object import Game_object
from colorama import Fore, Back, Style
from config import SCREEN_WIDTH
from datetime import datetime


class Paddle (Game_object):
    def __init__(self, x, y, xv, yv):
        self.grab = False
        self.powerup_time = 0
        self.type = 1
        self.paddle = [
            np.array(
                [["(", "X", "|", "X", "|", "X", "|", "X", ")"]]),
            np.array(
                [["(", "X", "|", "X", "X", "|", "X", "X", "|", "X", "X", "|", "X", "X", "|",  "X", ")"]]),
            np.array(
                [["(", "X", "|", "X", "|", "X", "|", "X", "|", "X", "|", "X", "|", "X", "|", "X", "|", "X", "|", "X", "|", "X", "|", "X", ")"]]),
        ]
        self.color = [np.full((1, 9), (Fore.BLACK
                                       + Back.WHITE+Style.BRIGHT)), np.full((1, 17), (Fore.BLACK
                                                                                      + Back.WHITE+Style.BRIGHT)), np.full((1, 25), (Fore.BLACK
                                                                                                                                     + Back.WHITE+Style.BRIGHT))]
        super().__init__(x, y, 17, 1, xv, yv, self.paddle[1], self.color[1])

    def make_enlarged(self):
        '''increases size of paddle and sets time for powerup'''
        if self.type == 0:
            self.type = 1
            self.xlength = 17

        elif self.type == 1:
            self.type = 2
            self.xlength = 25
        self.powerup_time = datetime.now()
        if self.x <= 1:
            self.x = 1
        if self.x+self.xlength > SCREEN_WIDTH-1:
            self.x = SCREEN_WIDTH-2-self.xlength

    def get_array(self):
        '''Polymorphism: Overrides get_array of Game_object'''
        return self.paddle[self.type]

    def get_color(self):
        '''Polymorphism: Overrides get_color of Game_object'''
        return self.color[self.type]

    def make_shrink(self):
        '''decreases size of paddle and sets time for powerup'''
        if self.type == 1:
            self.type = 0
            self.xlength = 9
        elif self.type == 2:
            self.type = 1
            self.xlength = 17
        self.powerup_time = datetime.now()
        if self.x <= 1:
            self.x = 1
        if self.x+self.xlength > SCREEN_WIDTH-1:
            self.x = SCREEN_WIDTH-2-self.xlength

    def times_up(self):
        self.type = 1
        self.xlength = 17
        self.powerup_time = 0
        if self.x <= 1:
            self.x = 1
        if self.x+self.xlength > SCREEN_WIDTH-1:
            self.x = SCREEN_WIDTH-2-self.xlength

    def get_powerup_time(self):
        return self.powerup_time

    def did_collide(self, obj):
        '''Polymorphism over game_object did_collide. Calculates Positions'''
        if super().did_collide(obj):
            if(type == 0):
                if(obj.x < self.x+3):
                    return -3
                if(obj.x < self.x+5):
                    return -2
                if(obj.x < self.x+7):
                    return 2
                return 3
            elif type == 1:
                if(obj.x < self.x+3):
                    return -4
                if(obj.x < self.x+6):
                    return -3
                if(obj.x < self.x+9):
                    return -2
                if(obj.x < self.x+12):
                    return 2
                if(obj.x < self.x+15):
                    return 3
                return 4
            else:
                if(obj.x < self.x+3):
                    return -5
                if(obj.x < self.x+6):
                    return -4
                if(obj.x < self.x+9):
                    return -3
                if(obj.x < self.x+12):
                    return -2
                if(obj.x < self.x+15):
                    return 2
                if(obj.x < self.x+18):
                    return 3
                if(obj.x < self.x+21):
                    return 4
                return 5

        else:
            return 0

    def move(self, x=-0.5, y=-0.5):
        super().move(x=x, y=y)
        if self.x <= 1:
            self.x = 1
        if self.x+self.xlength > SCREEN_WIDTH-1:
            self.x = SCREEN_WIDTH-2-self.xlength

    def set_grab(self):
        self.grab = not(self.grab)

    def get_grab(self):
        return self.grab
