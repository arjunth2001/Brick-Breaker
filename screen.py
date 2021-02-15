import numpy as np
from config import SCREEN_HEIGHT, SCREEN_WIDTH
from colorama import Fore, Back, Style


class Game_Screen:
    '''A Class for the numpy grid that gets printed to the screen on each iteration of game loop'''
    __color = np.full((SCREEN_HEIGHT, SCREEN_WIDTH),
                      Fore.WHITE+Back.BLACK+Style.BRIGHT)
    __array = np.full((SCREEN_HEIGHT, SCREEN_WIDTH), " ")
    __array[::, 0] = "|"
    __array[::, -1] = "|"
    __array[0, ::] = "-"
    __array[-1, ::] = "-"

    def add_to_game_screen(self, obj):
        '''adds the game object passed as argument to the grid along with it's color'''
        self.__color[obj.y:obj.y+obj.ylength,
                     obj.x:obj.x+obj.xlength] = obj.get_color()
        self.__array[obj.y:obj.y+obj.ylength,
                     obj.x:obj.x + obj.xlength] = obj.get_array()

    def print_game_screen(self):
        '''prints the current state of the game screen'''
        print('\033[0;0H')
        for i in range(SCREEN_HEIGHT):
            for j in range(SCREEN_WIDTH):
                print(self.__color[i][j]+self.__array[i][j], end="")
            print()

    def reset_screen(self):
        '''Function to reset the game screen'''
        self.__color = np.full((SCREEN_HEIGHT, SCREEN_WIDTH),
                               Fore.WHITE+Back.BLACK+Style.BRIGHT)
        self.__array = np.full((SCREEN_HEIGHT, SCREEN_WIDTH), " ")
        self.__array[::, 0] = "|"
        self.__array[::, -1] = "|"
        self.__array[0, ::] = "-"
        self.__array[-1, ::] = "-"
