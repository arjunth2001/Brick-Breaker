import numpy as np
from brick import Brick
from colorama import Fore, Back, Style
from config import SCREEN_HEIGHT, SCREEN_WIDTH


class Unbreakable(Brick):
    def __init__(self, x, y):
        super().__init__(x, y, 0)

    def hit(self):
        return 0
