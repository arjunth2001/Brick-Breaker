import numpy as np
from Game_Object import Game_object
from colorama import Fore, Back, Style


class Ball (Game_object):
    def __init__(self, x, y, xv, yv):
        ball = np.array([["O"]])
        color = np.array([[Fore.WHITE+Back.BLACK+Style.BRIGHT]])
        super().__init__(x, y, 1, 1, xv, yv, ball, color)
        self.bool_move = False

    def should_move(self):
        return self.bool_move

    def flip_move(self):
        self.bool_move = not(self.bool_move)
