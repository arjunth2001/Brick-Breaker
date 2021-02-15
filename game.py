from input import Get, input_to
from datetime import datetime
from ball import Ball
from chainbrick import chain_brick
import numpy as np
from unbreakable import Unbreakable
from brick import Brick
from paddle import Paddle
from powerup import Power_up
import os
import time


class Game:
    '''This is the Class of the New Game\n\n
    Functions:\n
    user_input: Takes user input\n
    move_all : Moves all objects\n
    '''
    getch = Get()
    power_up_type = [np.array([["E", "E"], ["E", "E"]]),
                     np.array([["S", "S"], ["S", "S"]]),
                     np.array([["G", "G"], ["G", "G"]]),
                     np.array([["X", "X"], ["X", "X"]]),
                     np.array([[">", ">"], [">", ">"]])]

    def print_meta(self):
        print(f"Lives Left:%d  Score:%d  Time Spend:%d" %
              (self.lives, self.score, self.time_elapsed()))

    def reset(self):
        self.win = False
        self.pause_time = 0
        self.lives = 3
        self.balls = []
        self.paddle = Paddle(65, 29, 8, 0)
        self.bricks = []
        self.put_bricks()
        self.powerups = []
        self.balls.append(Ball(69, 28, -1, -1))
        self.screen.reset_screen()
        self.update_screen()
        self.screen.print_game_screen()
        self.print_meta()

    def put_bricks(self):
        brick_pos = [2, 10, 18, 26, 34, 42, 50, 58, 66,
                     74, 82,   90, 98, 106, 114, 122, 130, 138]
        self.bricks.clear()
        for y in range(3, 15, 3):
            for x in brick_pos:
                if ((y == 3 or y == 12) and x == 74):
                    self.bricks.append(chain_brick(
                        x, y, np.random.choice([1, 2, 3, 4, 5])))
                elif ((y == 6 or y == 9) and (x >= 58 and x <= 82)):
                    self.bricks.append(chain_brick(
                        x, y, np.random.choice([1, 2, 3, 4, 5])))
                else:
                    p = np.random.uniform(0, 1)
                    if(p <= 1/4):
                        self.bricks.append(Unbreakable(x, y))
                    else:
                        self.bricks.append(
                            Brick(x, y, np.random.choice([1, 2, 3, 4, 5])))

    def main_screen(self):
        os.system("clear")
        while True:
            print('\033[0;0H')
            print(
                "This will be main screen. Press x to play. Press i for instructions.q to quit")
            c = input_to(self.getch)
            if(c == "q"):
                quit()
            if(c == 'x'):
                break

            if(c == "i"):
                self.instructions()
                os.system("clear")

    def instructions(self):
        os.system("clear")
        while True:
            print('\033[0;0H')
            print(
                "This will be instructions screen. Press b to go back.")
            c = input_to(self.getch)
            if(c == 'b'):
                break

    def pause_screen(self):
        os.system("clear")
        start_time = datetime.now()
        while True:
            print('\033[0;0H')
            print(
                "This will be pause screen. Press b to go back.")
            c = input_to(self.getch)
            if(c == 'b'):
                end_time = datetime.now()
                time_delta = end_time-start_time
                total_seconds = time_delta.total_seconds()
                self.pause_time += round(total_seconds)//60
                break

    def time_elapsed(self):
        time_delta = datetime.now()-self.start_time
        total_seconds = time_delta.total_seconds()
        minutes = round(total_seconds)//60
        return minutes-self.pause_time

    def __init__(self, screen):
        self.start_time = datetime.now()
        self.score = 0
        self.lives = 3
        self.win = False
        self.pause_time = 0
        self.balls = []
        self.paddle = Paddle(65, 29, 8, 0)
        self.bricks = []
        self.powerups = []
        self.balls.append(Ball(69, 28, -1, -1))
        self.screen = screen
        self.screen.print_game_screen()
        self.print_meta()

    def user_input(self):
        c = input_to(self.getch)
        if(c == "a"):
            self.paddle.move(self.paddle.get_x()-self.paddle.get_xv())
        if(c == "s"):
            self.paddle.move(self.paddle.get_x()+self.paddle.get_xv())
        if(c == "r"):
            for ball in self.balls:
                if not ball.should_move():
                    ball.flip_move()
        if(c == "p"):
            self.pause_screen()
        if(c == "q"):
            quit()

    def move_all(self):
        for powerup in self.powerups:
            powerup.move()
        for powerup in self.powerups:
            col = powerup.did_collide(self.paddle)
            if(col[0]):
                self.execute_powerup(col[1])

    def execute_powerup(self, type):
        if np.array_equal(np.array([["E", "E"], ["E", "E"]]), type):
            self.paddle.make_enlarged()
        if np.array_equal(np.array([["S", "S"], ["S", "S"]]), type):
            self.paddle.make_shrink()
        if np.array_equal(np.array([["X", "X"], ["X", "X"]]), type):
            new_balls = []
            for ball in self.balls:
                new_ball = Ball(ball.x, ball.y, np.random.choice(
                    [1, -1]), np.random.choice([1, -1]))
                new_balls.append(new_ball)
            self.balls.extend(new_balls)
        if np.array_equal(np.array([[">", ">"], [">", ">"]]), type):
            for ball in self.balls:
                ball.setxv(ball.get_xv()*2)
                ball.setyv(ball.get_yv()*2)
        if np.array_equal(np.array([["G", "G"], ["G", "G"]]), type):
            self.paddle.set_grab()

    def collissions(self):
        for ball in self.balls:
            if ball.is_active() and ball.should_move():
                points = ball.trajectory()
                for p in points:
                    ball.move(p[0], p[1])
                    a = self.paddle.did_collide(ball)
                    if a != 0:
                        ball.set_xv(ball.get_xv()+a)
                        ball.set_yv(ball.get_yv()*-1)
                        if self.paddle.get_grab():
                            ball.flip_move()
                        break

                    for brick in self.bricks:
                        if brick.is_active() and brick.did_collide(ball):
                            if isinstance(brick, chain_brick):
                                curr = brick.hit(self.bricks)
                                if(curr == 0):
                                    self.powerups.append(
                                        Power_up(brick.get_x(), brick.get_y(), self.power_up_type[np.random.choice([0, 1, 2, 3, 4])]))
                            else:
                                curr = brick.hit()
                                if(curr == 0):
                                    self.powerups.append(
                                        Power_up(brick.get_x(), brick.get_y(), self.power_up_type[np.random.choice([0, 1, 2, 3, 4])]))
                            if not isinstance(brick, Unbreakable):
                                self.score += 1
                            break

    def update_screen(self):
        self.screen.add_to_game_screen(self.paddle)
        for powerup in self.powerups:
            if(powerup.is_active()):
                self.screen.add_to_game_screen(powerup)
        for brick in self.bricks:
            if(brick.is_active()):
                self.screen.add_to_game_screen(brick)
        for ball in self.balls:
            if(ball.is_active()):
                self.screen.add_to_game_screen(ball)

    def lost(self):
        os.system("clear")
        while True:
            print('\033[0;0H')
            print(
                "You Lost. Press c to continue.")
            c = input_to(self.getch)
            if(c == 'c'):
                break

    def win(self):
        os.system("clear")
        self.win = False
        while True:
            print('\033[0;0H')
            print(
                "You Won. Press c to continue.")
            c = input_to(self.getch)
            if(c == 'c'):
                break

    def new_game(self):
        while True:
            c = input_to(self.getch)
            if(c == "q"):
                quit()
            self.main_screen()
            os.system("clear")
            self.put_bricks()
            while self.lives > 0:
                self.user_input()
                self.move_all()
                self.screen.reset_screen()
                self.update_screen()
                self.screen.print_game_screen()
                self.print_meta()
                self.collissions()
                self.screen.reset_screen()
                self.update_screen()
                self.screen.print_game_screen()
                self.print_meta()
                for ball in self.balls:
                    if ball.is_active():
                        break
                else:
                    self.lives -= 1
                    self.reset()
                for brick in self.bricks:
                    if not isinstance(brick, Unbreakable):
                        if brick.is_active():
                            break
                else:
                    self.win = True
            if self.lives == 0 and not self.win:
                self.lost()
            else:
                self.win()
