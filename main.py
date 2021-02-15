from screen import Game_Screen
from game import Game
import time
import os
screen = Game_Screen()
game = Game(screen)
os.system("clear")
print('\033[0;0H')
game.new_game()
