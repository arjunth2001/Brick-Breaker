import numpy as np
from Game_Object import Game_object
from colorama import Fore, Back, Style
from config import SCREEN_WIDTH
from datetime import datetime


class UFO (Game_object):
    def __init__(self, x, y, xv, yv):
        self.last_shoot = 0
        self.health = 10
        self.paddle = [
            np.array(
                [["<", "U", "W", "U", "|", "U", "W", "U", "|", "U", "W", "U", ">"]]),
        ]
        self.color = [np.full((1, 13), (Fore.BLACK
                                        + Back.GREEN + Style.BRIGHT))]
        super().__init__(x, y, 13, 1, xv, yv, self.paddle[0], self.color[0])

    def move(self, x=-0.5, y=-0.5):
        super().move(x=x, y=y)
        if self.x <= 1:
            self.x = 1
        if self.x+self.xlength > SCREEN_WIDTH-1:
            self.x = SCREEN_WIDTH-2-self.xlength

    def hit(self):
        self.health -= 1

    def did_collide(self, obj):
        '''Polymorphism over game_object did_collide. Calculates Positions'''

        if super().did_collide(obj):
            if(obj.x < self.x+4):
                return -3
            if(obj.x < self.x+6):
                return -2
            if(obj.x < self.x+9):
                return 2
            return 3
        return 0
