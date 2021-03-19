import numpy as np
from Game_Object import Game_object
from colorama import Fore, Back, Style
from config import SCREEN_HEIGHT, SCREEN_WIDTH


class Bullet (Game_object):
    '''The Class of bullet - Inherits from Game_Object
    '''

    def __init__(self, x, y):
        bullet = np.array([["@"]])
        color = np.array([[Fore.RED+Back.WHITE+Style.BRIGHT]])
        super().__init__(x, y, 1, 1, 0, -1, bullet, color)

    def move(self, x=-0.5, y=-0.5):
        super().move(x, y)
        if(self.x <= 1 or self.x > SCREEN_WIDTH-2):
            self.set_inactive()
        if(self.y <= 1):
            self.set_inactive()
        if(self.y > SCREEN_HEIGHT-2):
            self.set_inactive()
