import numpy as np
from Game_Object import Game_object
from colorama import Fore, Back, Style
from config import SCREEN_WIDTH


class Paddle (Game_object):
    def __init__(self, x, y, xv, yv):
        self.grab = False
        self.type = 0
        self.paddle = [np.array(
            [["(", "X", "|", "X", "X", "|", "X", ")"]]),
            np.array(
                [["(", "X", "|", "X", "|", "X", "|", "X", "|", "X", "|", "X", ")"]]),
            np.array(
            [["(", "X", "|", "X", ")"]]), ]
        self.color = [np.full((1, 8), (Fore.BLACK
                                       + Back.WHITE+Style.BRIGHT)), np.full((1, 13), (Fore.BLACK
                                                                                      + Back.WHITE+Style.BRIGHT)), np.full((1, 5), (Fore.BLACK
                                                                                                                                    + Back.WHITE+Style.BRIGHT))]
        super().__init__(x, y, 8, 1, xv, yv, self.paddle[0], self.color[0])

    def make_enlarged(self):
        self.type = 1
        self.xlength = 13

    def get_array(self):
        return self.paddle[self.type]

    def get_color(self):
        return self.color[self.type]

    def make_shrink(self):
        self.type = 2
        self.xlength = 5

    def did_collide(self, obj):
        if super().did_collide(obj):
            if(type == 0):
                if(obj.x < self.x+2):
                    return -3
                if(obj.x < self.x+5):
                    return -2
                if(obj.x < self.x+7):
                    return 2
                return 3
            elif type == 1:
                if(obj.x < self.x+2):
                    return -4
                if(obj.x < self.x+4):
                    return -3
                if(obj.x < self.x+6):
                    return -2
                if(obj.x < self.x+8):
                    return 2
                if(obj.x+self.x+10):
                    return 3
                return 4
            else:
                if(obj.x < self.x+2):
                    return -2
                else:
                    return 2
        else:
            return 0

    def move(self, x=-0.5, y=-0.5):
        super().move(x=x, y=y)
        if self.x <= 1:
            self.x = 1
        if self.x+self.xlength > SCREEN_WIDTH-1:
            self.x = SCREEN_WIDTH-2-self.xlength

    def set_grab(self):
        self.grab = True

    def get_grab(self):
        return self.grab
