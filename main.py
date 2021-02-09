from screen import Game_Screen
from ball import Ball
import time
import os

ball = Ball(72, 15, 2, 3)
screen = Game_Screen()
os.system("clear")
print('\033[0;0H')
screen.add_to_game_screen(ball)
screen.print_game_screen()
while True:
    time.sleep(0.1)
    screen.reset_screen()
    screen.add_to_game_screen(ball)
    screen.print_game_screen()
    ball.move()
