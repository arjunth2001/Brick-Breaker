import numpy as np
from Game_Object import Game_object
from colorama import Fore, Back, Style
from config import SCREEN_HEIGHT, SCREEN_WIDTH


class Bomb (Game_object):
    '''The Class of Bomb - Inherits from Game_Object
    '''

    def __init__(self, x, y):
        bomb = np.array([["#"]])
        color = np.array([[Fore.WHITE+Back.RED+Style.BRIGHT]])
        super().__init__(x, y, 1, 1, 0, 1, bomb, color)

    def move(self, x=-0.5, y=-0.5):
        super().move(x, y)
        if(self.x <= 1 or self.x > SCREEN_WIDTH-2):
            self.set_inactive()
        if(self.y <= 1):
            self.set_inactive()
        if(self.y > SCREEN_HEIGHT-2):
            self.set_inactive()
