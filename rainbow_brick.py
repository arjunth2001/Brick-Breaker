import numpy as np
from brick import Brick
from colorama import Fore, Back, Style
from config import SCREEN_HEIGHT, SCREEN_WIDTH


class rainbow_brick(Brick):
    '''The rainbow brick - Inherits from Brick Class'''

    def __init__(self, x, y, strength):
        super().__init__(x, y, strength)
        self.change = True
        self.strength_color = [Back.WHITE + Fore.RED + Style.BRIGHT, Back.GREEN + Fore.WHITE,
                               Back.YELLOW + Fore.WHITE, Back.CYAN + Fore.WHITE, Back.BLUE + Fore.WHITE, Back.RED + Fore.WHITE, Back.WHITE+Fore.RED]
        self.array = np.array([
            ["|", "R", "R", "R", "R", "R", "R", "|"],
        ])

    def get_array(self):
        '''get's body of rainbow_brick
        Polymorphism: Overrides Game_Object get_array'''
        return self.array

    def did_collide(self, obj):
        collided = super().did_collide(obj)
        if collided == True:
            self.change = False
        return collided

    def change_strength(self):
        if self.change == True:
            self.strength = np.random.choice([1, 2, 3, 4, 5])

    def get_color(self):
        return self.strength_color[self.strength]
