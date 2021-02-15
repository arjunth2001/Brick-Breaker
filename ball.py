import numpy as np
from Game_Object import Game_object
from colorama import Fore, Back, Style
from config import SCREEN_HEIGHT, SCREEN_WIDTH


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

    def trajectory(self):
        x1 = self.x
        x2 = self.x+self.xv
        y1 = self.y
        y2 = self.y + self.yv
        trajectory_return = []
        if x2 == x1:
            step = 0
            if y2 > y1:
                step = 1
            else:
                step = -1
            for y in range(y1+step, y2+step, step):
                trajectory_return.append((x1, y))
            return trajectory_return
        if y2 == y1:
            step = 0
            if x2 > x1:
                step = 1
            else:
                step = -1
            for x in range(x1+step, x2+step, step):
                trajectory_return.append((x, y1))
            return trajectory_return
        step = 0
        if x2 > x1:
            step = 1
        else:
            step = -1
        for x in range(x1+step, x2+step, step):

            y = ((y2-y1)/(x2-x1))*(x-x1)+y1
            if(abs(y-round(y)) < 0.4):
                y = round(y)
                trajectory_return.append((x, y))
        return trajectory_return

    def move(self, x=-0.5, y=-0.5):
        super().move(x, y)
        if(self.x <= 1 or self.x > SCREEN_WIDTH-2):
            self.x = 1 if self.x <= 1 else SCREEN_WIDTH-2
            self.xv *= -1
        if(self.y <= 1 or self.y > SCREEN_HEIGHT-2):
            self.y = 1 if self.y <= 1 else SCREEN_HEIGHT-2
            self.yv *= -1
        if(self.y >= SCREEN_HEIGHT-2):
            self.set_inactive()
