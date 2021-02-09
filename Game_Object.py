from config import SCREEN_HEIGHT, SCREEN_WIDTH


class Game_object:

    ''' The generalisation of a Game Object'''

    def __init__(self, x, y, xlength, ylength, xv, yv, __array, __color):
        self.x = x
        self.y = y
        self.xv = xv
        self.yv = yv
        self.__array = __array
        self.__color = __color
        self.xlength = xlength
        self.ylength = ylength

    def get_array(self):
        return self.__array

    def get_color(self):
        return self.__color

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

    def move(self):
        back_x = self.x
        back_y = self.y
        try:
            self.x += self.xv//abs(self.xv)
            self.y += self.yv//abs(self.yv)
            flag = False
            if(self.x < 0 or self.x >= SCREEN_WIDTH):
                self.x = back_x
                self.xv *= -1
                flag = True
            if(self.y < 0 or self.y >= SCREEN_HEIGHT):
                self.y = back_y
                self.yv *= -1
                flag = True
            return flag
        except:
            return False
