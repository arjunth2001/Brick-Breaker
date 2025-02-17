import numpy as np
from brick import Brick
from colorama import Fore, Back, Style
from config import SCREEN_HEIGHT, SCREEN_WIDTH


class chain_brick(Brick):
    '''The chain brick BONUS - Inherits from Brick Class'''

    def __init__(self, x, y, strength):
        super().__init__(x, y, strength)
        self.array = np.array([
            ["|", ">", ">", ">", ">", ">", ">", "|"],
        ])

    def get_array(self):
        '''get's body of chain_brick
        Polymorphism: Overrides Game_Object get_array'''
        return self.array

    def hit(self, bricks):
        '''hits the brick and reduces its strengh
        Initiates chain reaction over other bricks
        Polymorphism: Function overloading over Brick hit'''
        curr_strength = super().hit()
        if curr_strength == 0:
            for brick in bricks:
                if isinstance(brick, chain_brick):
                    for other_brick in bricks:
                        if (other_brick.x == brick.x or other_brick.x == brick.x-brick.xlength or other_brick.x == brick.x+brick.xlength) and (other_brick.y == brick.y or other_brick.y == brick.y-1 or other_brick.y == brick.y+1):
                            other_brick.set_inactive()
        return curr_strength
