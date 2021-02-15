import numpy as np
from brick import Brick
from colorama import Fore, Back, Style
from config import SCREEN_HEIGHT, SCREEN_WIDTH


class chain_brick(Brick):
    def __init__(self, x, y, strength):
        super().__init__(x, y, strength)
        self.array = np.array([[":", "-", "-", "-", "-", "-", "-", ":"],
                               ["|", ">", ">", ">", ">", ">", ">", "|"],
                               [":", "-", "-", "-", "-", "-", "-", ":"]])

    def get_array(self):
        return self.array

    def hit(self, bricks):
        curr_strength = super().hit()
        if curr_strength == 0:
            for brick in bricks:
                if(isinstance(brick, chain_brick) and (brick.x == self.x or brick.y == self.y)):
                    brick.set_inactive()
        return curr_strength
