import numpy as np
from Game_Object import Game_object
from colorama import Fore, Back, Style
from config import SCREEN_HEIGHT, SCREEN_WIDTH


class Brick(Game_object):
    strength_color = [Back.WHITE + Fore.RED + Style.BRIGHT, Back.GREEN + Fore.WHITE,
                      Back.YELLOW + Fore.WHITE, Back.CYAN + Fore.WHITE, Back.BLUE + Fore.WHITE, Back.RED + Fore.WHITE]

    def __init__(self, x, y, strength):

        brick = np.array([[":", "-", "-", "-", "-", "-", "-", ":"],
                          ["|", "X", "X", "X", "X", "X", "X", "|"],
                          [":", "-", "-", "-", "-", "-", "-", ":"]])
        color = np.full((3, 8), self.strength_color[strength])
        super().__init__(x, y, 8, 3, 0, 0, brick, color)
        self.strength = strength

    def hit(self):
        self.strength -= 1
        self.set_color(np.full((3, 8), self.strength_color[self.strength]))
        if self.strength == 0:
            self.set_inactive()
        return self.strength

    def did_collide(self, obj):
        collided = super().did_collide(obj)
        if collided:
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
