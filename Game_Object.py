from config import SCREEN_HEIGHT, SCREEN_WIDTH


class Game_object:

    ''' The generalisation of a Game Object. Base class for all objects in the game'''

    def __init__(self, x, y, xlength, ylength, xv, yv, __array, __color):
        self.x = x
        self.y = y
        self.xv = xv
        self.yv = yv
        self.__array = __array
        self.__color = __color
        self.xlength = xlength
        self.ylength = ylength
        self.active = True

    def get_array(self):
        return self.__array

    def set_inactive(self):
        self.active = False

    def is_active(self):
        return self.active

    def get_color(self):
        return self.__color

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_color(self, color):
        self.__color[::, ::] = color

    def set_xv(self, xv):
        self.xv = xv

    def set_yv(self, yv):
        self.yv = yv

    def did_collide(self, obj):
        '''returns true if the object collided'''
        if self.y > obj.y + obj.ylength:
            return False
        elif self.y + self.ylength < obj.y:
            return False

        if self.x > obj.x + obj.xlength:
            return False
        elif self.x + self.xlength < obj.x:
            return False
        return True

    def get_x(self):
        return self.x

    def get_xv(self):
        return self.xv

    def get_yv(self):
        return self.yv

    def get_y(self):
        return self.y

    def move(self, x=-0.5, y=-0.5):
        '''moves the game object'''
        self.x = self.x+self.xv if x == -0.5 else x
        self.y = self.y+self.yv if y == -0.5 else y
