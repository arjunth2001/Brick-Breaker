import numpy as np
from Game_Object import Game_object
from colorama import Fore, Back, Style
from config import SCREEN_HEIGHT, SCREEN_WIDTH


class Brick(Game_object):
    '''Class of the brick- Inherits from Game_Object'''
    strength_color = [Back.WHITE + Fore.RED + Style.BRIGHT, Back.GREEN + Fore.WHITE,
                      Back.YELLOW + Fore.WHITE, Back.CYAN + Fore.WHITE, Back.BLUE + Fore.WHITE, Back.RED + Fore.WHITE, Back.WHITE+Fore.RED]

    def __init__(self, x, y, strength):

        brick = np.array([
            ["|", "X", "X", "X", "X", "X", "X", "|"],
        ])
        color = np.full((1, 8), self.strength_color[strength])
        super().__init__(x, y, 8, 1, 0, 0, brick, color)
        self.strength = strength

    def hit(self):
        '''hit the brick and reduce strength'''
        self.strength -= 1
        self.set_color(np.full((1, 8), self.strength_color[self.strength]))
        if self.strength == 0:
            self.set_inactive()
        return self.strength

    def did_collide(self, obj):
        '''checks collission with ball- also changes the velocity of ball
        polymorphism- Overrides Game_Object did_collide with extra functionality'''
        collided = super().did_collide(obj)
        if collided:
            if obj.x < self.x + self.xlength and obj.x >= self.x:
                obj.yv *= -1
            if obj.x < self.x+2:
                obj.xv -= 3
                return collided
            if obj.x < self.x + 4:
                obj.xv -= 2
                return collided
            if obj.x < self.x + 6:
                obj.xv += 2
                return collided
            else:
                obj.xv += 3
                return collided
        return collided
