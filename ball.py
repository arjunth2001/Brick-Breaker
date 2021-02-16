import numpy as np
from Game_Object import Game_object
from colorama import Fore, Back, Style
from config import SCREEN_HEIGHT, SCREEN_WIDTH


class Ball (Game_object):
    '''The Class of ball - Inherits from Game_Object
            Functions:
                        should_move() - Returns if to move or not:
                        flip_move() - Flips the move state
                        trajectory()- Returns the points on the trajectory of the next move
                        move(x,y)- moves the ball around to x,y. If no x,y directly moves. This is overriding the basic move with extra functionality
                                   (example of polymorphism)
    '''

    def __init__(self, x, y, xv, yv):
        ball = np.array([["O"]])
        color = np.array([[Fore.WHITE+Back.BLACK+Style.BRIGHT]])
        super().__init__(x, y, 1, 1, xv, yv, ball, color)
        self.bool_move = False

    def should_move(self):
        '''Returns if to move or not'''
        return self.bool_move

    def flip_move(self):
        '''Flips the move state'''
        self.bool_move = not(self.bool_move)

    def trajectory(self):
        '''Returns the points on the trajectory of the next move'''
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

            y_ = ((y2-y1)*(x-x1))/(x2-x1)+y1
            y = int(round(y_))
            if y == y_:
                trajectory_return.append((x, y))
        return trajectory_return

    def move(self, x=-0.5, y=-0.5):
        '''moves the ball around to x,y. If no x,y directly moves. This is overriding the basic move with extra functionality
                                   (example of polymorphism)'''
        super().move(x, y)
        flag = False
        if(self.x <= 1 or self.x > SCREEN_WIDTH-2):
            self.x = 1 if self.x <= 1 else SCREEN_WIDTH-2
            self.xv *= -1
            flag = True
        if(self.y <= 1):
            self.y = 1
            self.yv *= -1
            flag = True
        if(self.y > SCREEN_HEIGHT-2):
            self.set_inactive()
            flag = True
        return flag
