import numpy as np
from Game_Object import Game_object
from colorama import Fore, Back, Style
from config import SCREEN_HEIGHT, SCREEN_WIDTH


class Power_up(Game_object):
    def __init__(self, x, y, body):
        color = np.full((2, 2), Fore.RED+Back.GREEN+Style.BRIGHT)
        super().__init__(x, y, 2, 2, 0, 1, body, color)

    def move(self, x=-0.5, y=-0.5):
        super().move(x, y)
        if(self.y > SCREEN_HEIGHT-3):
            self.set_inactive()

    def did_collide(self, obj):
        collide = super().did_collide(obj)
        if(collide):
            return (True, self.get_array())
        else:
            return(False, None)
