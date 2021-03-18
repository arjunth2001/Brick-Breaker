from input import Get, input_to
from datetime import datetime
from ball import Ball
from chainbrick import chain_brick
from Game_Object import Game_object
import numpy as np
from unbreakable import Unbreakable
from brick import Brick
from rainbow_brick import rainbow_brick
from paddle import Paddle
from powerup import Power_up
from config import TIME_PADDLE_POWER_UP, TIME_PASS_THROUGH, TIME_FAST_BALL, TIME_GRAB, LIVES, MOVE_BRICK, SHOOT_TIME
from header import arjun, brickbreaker, presstoplay, gameover, on_continue, on_won
from colorama import Fore, Back, Style
from bullet import Bullet
import os
import time


class Game:
    '''This is the Class of the New Game\n\n
    Functions:\n
    user_input: Takes user input\n
    move_all : Moves all objects\n
    '''
    my_arjun = Game_object(35, 5, 75, 6, 0, 0, arjun, np.full(
        (6, 75), Fore.RED+Back.BLACK+Style.BRIGHT))
    my_brickbreaker = Game_object(10, 13, 123, 6, 0, 0, brickbreaker, np.full(
        (6, 123), Fore.WHITE+Back.CYAN+Style.BRIGHT))
    my_press = Game_object(50, 28, 49, 1, 0, 0, presstoplay, np.full(
        (1, 49), Fore.WHITE+Style.BRIGHT))
    game_over = Game_object(20, 3, 106, 7, 0, 0, gameover, np.full(
        (7, 106), Fore.RED+Style.BRIGHT))
    my_continue = Game_object(65, 28, 19, 1, 0, 0, on_continue, np.full(
        (1, 19), Fore.WHITE+Style.BRIGHT))
    my_win = Game_object(45, 3, 58, 6, 0, 0, on_won, np.full(
        on_won.shape, Fore.WHITE+Style.BRIGHT))
    getch = Get()
    power_up_type = [
        np.array([["P", "P"], ["P", "P"]]),
        np.array([["E", "E"], ["E", "E"]]),
        np.array([["S", "S"], ["S", "S"]]),
        np.array([["G", "G"], ["G", "G"]]),
        np.array([["X", "X"], ["X", "X"]]),
        np.array([[">", ">"], [">", ">"]]),
        np.array([["!", "!"], ["!", "!"]]), ]
    level = 1
    skip_level = False
    level_start = datetime.now()
    over = False

    def print_meta(self):
        print_string = f"\33[2K Level:%d Lives Left:%d  Score:%d  Time Spend:%d" % (
            self.level, self.lives, self.score, self.time_elapsed())
        if(self.pass_through):
            print_string += f" P left: %d" % (TIME_PASS_THROUGH -
                                              self.get_change_in_secs(self.pass_through))
        if(self.paddle.get_powerup_time()):
            print_string += f" S left: %d" % (TIME_PADDLE_POWER_UP -
                                              self.get_change_in_secs(self.paddle.get_powerup_time()))
        if(self.paddle.get_shoot_time()):
            print_string += f" O left: %d" % (SHOOT_TIME -
                                              self.get_change_in_secs(self.paddle.get_shoot_time()))
        if(self.fast_ball):
            print_string += f" F left: %d" % (TIME_FAST_BALL -
                                              self.get_change_in_secs(self.fast_ball))
        if(self.grab_ball):
            print_string += f" G left: %d" % (TIME_GRAB -
                                              self.get_change_in_secs(self.grab_ball))
        print(print_string)
        print('a- LEFT. d - right. r - release ball. l - skip level. s - shoot bullet . PRESS p to pause. q to quit.')

    def get_change_in_secs(self, value):
        time_delta = datetime.now()-value
        total_seconds = time_delta.total_seconds()
        return int(total_seconds)

    def check_powerup_times(self):
        if(self.paddle.get_powerup_time()):
            if(self.get_change_in_secs(self.paddle.get_powerup_time()) > TIME_PADDLE_POWER_UP):
                self.paddle.times_up()
        if(self.paddle.get_shoot_time()):
            if(self.get_change_in_secs(self.paddle.get_powerup_time()) > SHOOT_TIME):
                self.paddle.times_up_shoot()
        if(self.pass_through):
            if(self.get_change_in_secs(self.pass_through) > TIME_PASS_THROUGH):
                self.pass_through = 0
        if(self.fast_ball):
            if(self.get_change_in_secs(self.fast_ball) > TIME_FAST_BALL):
                self.fast_ball = 0
                for ball in self.balls:
                    new_xv = 0
                    new_yv = 0
                    if(ball.get_xv()):
                        new_xy = ball.get_xv()-2*abs(ball.get_xv())//ball.get_xv()
                    if(ball.get_yv()):
                        new_yv = ball.get_yv()-2*abs(ball.get_yv())//ball.get_yv()
                    ball.set_xv(new_xv)
                    ball.set_yv(new_yv)
        if(self.grab_ball):
            if(self.get_change_in_secs(self.grab_ball) > TIME_GRAB):
                self.grab_ball = 0
                self.paddle.set_grab()

    def reset(self):
        self.start_time = datetime.now()
        self.level_start = datetime.now()
        self.pass_through = 0
        self.fast_ball = 0
        self.grab_ball = 0
        self.score = 0
        self.win = False
        self.pause_time = 0
        self.lives = LIVES
        self.balls = []
        self.paddle = Paddle(65, 29, 8, 0)
        self.bricks = []
        self.powerups = []
        self.bullets = []
        self.balls.append(Ball(69, 28, -1, -1))
        self.screen.reset_screen()
        self.update_screen()
        self.screen.print_game_screen()
        self.check_powerup_times()
        self.print_meta()

    def put_bricks(self):
        if self.level == 1:
            brick_pos = [50, 58, 66,
                         74, 82,   90]
            self.bricks.clear()
            for y in range(3, 10, 1):
                for x in brick_pos:
                    if ((y == 6 or y == 9) and x == 74):
                        self.bricks.append(chain_brick(
                            x, y, np.random.choice([1, 2, 3, 4, 5])))
                    elif ((y == 7 or y == 8) and (x >= 58 and x <= 82)):
                        self.bricks.append(chain_brick(
                            x, y, np.random.choice([1, 2, 3, 4, 5])))
                    else:
                        p = np.random.uniform(0, 1)
                        if(p <= 1/4):
                            self.bricks.append(Unbreakable(x, y))
                        else:
                            self.bricks.append(
                                Brick(x, y, np.random.choice([1, 2, 3, 4, 5])))

        if self.level == 2:
            brick_pos = [26, 34, 42, 50, 58, 66,
                         74, 82,   90, 98, 106, 114]
            self.bricks.clear()
            for y in range(3, 10, 1):
                for x in brick_pos:
                    if ((y == 6 or y == 9) and x == 74):
                        self.bricks.append(chain_brick(
                            x, y, np.random.choice([1, 2, 3, 4, 5])))
                    elif ((y == 7 or y == 8) and (x >= 58 and x <= 82)):
                        self.bricks.append(chain_brick(
                            x, y, np.random.choice([1, 2, 3, 4, 5])))
                    else:
                        p = np.random.uniform(0, 1)
                        if(p <= 1/4):
                            self.bricks.append(Unbreakable(x, y))
                        else:
                            p = np.random.uniform(0, 1)
                            if p <= 1/4:
                                self.bricks.append(
                                    rainbow_brick(x, y, np.random.choice([1, 2, 3, 4, 5])))
                            else:
                                self.bricks.append(
                                    Brick(x, y, np.random.choice([1, 2, 3, 4, 5])))

        if self.level == 3:
            brick_pos = [2, 10, 18, 26, 34, 42, 50, 58, 66,
                         74, 82,   90, 98, 106, 114, 122, 130, 138]
            self.bricks.clear()
            for y in range(3, 10, 1):
                for x in brick_pos:
                    if ((y == 6 or y == 9) and x == 74):
                        self.bricks.append(chain_brick(
                            x, y, np.random.choice([1, 2, 3, 4, 5])))
                    elif ((y == 7 or y == 8) and (x >= 58 and x <= 82)):
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
        self.screen.reset_screen()
        self.screen.add_to_game_screen(self.my_arjun)
        self.screen.add_to_game_screen(self.my_brickbreaker)
        self.screen.add_to_game_screen(self.my_press)
        self.screen.print_game_screen()
        while True:
            self.screen.reset_screen()
            self.screen.add_to_game_screen(self.my_arjun)
            self.screen.add_to_game_screen(self.my_brickbreaker)
            self.screen.add_to_game_screen(self.my_press)
            self.screen.print_game_screen()

            c = input_to(self.getch)
            if(c == "q"):
                os.system("clear")
                quit()
            if(c == 'x'):
                break

            if(c == "i"):
                self.instructions()
                os.system("clear")

    def instructions(self):
        os.system("clear")
        text_string = f"Read README and PDFs for rules and instructions."
        body = np.array([list(text_string)])
        obj = Game_object(50, 20, body[0].size,
                          1, 0, 0, body, np.full(body.shape, Fore.WHITE+Style.BRIGHT))
        self.screen.reset_screen()
        self.screen.add_to_game_screen(obj)
        self.screen.add_to_game_screen(self.my_continue)
        self.screen.print_game_screen()
        while True:
            c = input_to(self.getch)
            if(c == 'c'):
                break

    def pause_screen(self):
        os.system("clear")
        text_string = f"The game is paused."
        body = np.array([list(text_string)])
        obj = Game_object(65, 20, body[0].size,
                          1, 0, 0, body, np.full(body.shape, Fore.WHITE+Style.BRIGHT))
        self.screen.reset_screen()
        self.screen.add_to_game_screen(obj)
        self.screen.add_to_game_screen(self.my_continue)
        self.screen.print_game_screen()
        start_time = datetime.now()
        while True:
            c = input_to(self.getch)
            if(c == 'c'):
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

    def small_reset(self):
        self.pass_through = 0
        self.grab_ball = 0
        self.fast_ball = 0
        self.balls = []
        self.paddle = Paddle(65, 29, 8, 0)
        self.powerups = []
        self.bullets = []
        self.balls.append(Ball(69, 28, -1, -1))
        self.screen.reset_screen()
        self.update_screen()
        self.screen.print_game_screen()
        self.check_powerup_times()
        self.print_meta()

    def __init__(self, screen):
        self.start_time = datetime.now()
        self.pass_through = 0
        self.grab_ball = 0
        self.fast_ball = 0
        self.score = 0
        self.lives = LIVES
        self.win = False
        self.pause_time = 0
        self.balls = []
        self.paddle = Paddle(65, 29, 8, 0)
        self.bricks = []
        self.powerups = []
        self.bullets = []
        self.balls.append(Ball(69, 28, -1, -1))
        self.screen = screen
        self.screen.print_game_screen()
        self.check_powerup_times()
        self.print_meta()

    def user_input(self):
        c = input_to(self.getch, 0.1)
        if(c == "a"):
            self.paddle.move(self.paddle.get_x()-self.paddle.get_xv())
            for ball in self.balls:
                if not ball.should_move():
                    ball.move(ball.get_x()-self.paddle.get_xv(), ball.get_y())
        if(c == "d"):
            self.paddle.move(self.paddle.get_x()+self.paddle.get_xv())
            for ball in self.balls:
                if not ball.should_move():
                    ball.move(ball.get_x()+self.paddle.get_xv(), ball.get_y())
        if(c == "r"):
            for ball in self.balls:
                if not ball.should_move():
                    ball.flip_move()
        if(c == "p"):
            self.pause_screen()
        if(c == "q"):
            os.system("clear")
            quit()
        if(c == "l"):
            self.skip_level = True
        if (c == "r"):
            if(self.paddle.get_shoot_time() and self.paddle.last_shoot >= 4):
                self.paddle.last_shoot = 0
                self.bullets.append(
                    Bullet(self.paddle.get_x()+self.paddle.xlength//2, self.paddle.get_y()))

    def move_all(self):
        self.paddle.last_shoot += 1
        for bullet in self.bullets:
            if(bullet.is_active()):
                for brick in self.bricks:
                    if brick.is_active() and bullet.did_collide(brick):
                        bullet.set_inactive()
                        if isinstance(brick, chain_brick):
                            curr = brick.hit(self.bricks)
                            if(curr == 0):
                                self.powerups.append(
                                    Power_up(brick.get_x(), brick.get_y(), 0, 1, self.power_up_type[np.random.choice([0, 1, 2, 3, 4, 5, 6])]))
                        else:
                            curr = brick.hit()
                            if(curr == 0):
                                self.powerups.append(
                                    Power_up(brick.get_x(), brick.get_y(), 0, 1, self.power_up_type[np.random.choice([0, 1, 2, 3, 4, 5, 6])]))
                        if not isinstance(brick, Unbreakable):
                            self.score += 1

        for powerup in self.powerups:
            if(powerup.is_active()):
                powerup.set_yv(powerup.get_yv()+1)
                points = powerup.trajectory()
                for p in points:
                    flag = False
                    flag = powerup.move(p[0], p[1])
                    col = powerup.did_collide(self.paddle)
                    if(col[0]):
                        self.execute_powerup(col[1])
                        powerup.set_inactive()
                    if flag == True:
                        break
        if self.get_change_in_secs(self.level_start) >= MOVE_BRICK:
            for brick in self.bricks:
                self.over = brick.move()
        for brick in self.bricks:
            if isinstance(brick, rainbow_brick):
                brick.change_strength()

    def execute_powerup(self, type):
        if np.array_equal(np.array([["P", "P"], ["P", "P"]]), type):
            self.pass_through = datetime.now()
        if np.array_equal(np.array([["E", "E"], ["E", "E"]]), type):
            self.paddle.make_enlarged()
        if np.array_equal(np.array([["S", "S"], ["S", "S"]]), type):
            self.paddle.make_shrink()
        if np.array_equal(np.array([["X", "X"], ["X", "X"]]), type):
            new_balls = []
            for ball in self.balls:
                new_ball = Ball(ball.x, ball.y, np.random.choice(
                    [1, -1]), np.random.choice([1, -1]))
                new_ball.flip_move()
                new_balls.append(new_ball)
            self.balls.extend(new_balls)
        if np.array_equal(np.array([[">", ">"], [">", ">"]]), type):
            self.fast_ball = datetime.now()
            for ball in self.balls:
                new_xv = 0
                new_yv = 0
                if(ball.get_xv()):
                    new_xy = ball.get_xv()+2*abs(ball.get_xv())//ball.get_xv()
                if(ball.get_yv()):
                    new_yv = ball.get_yv()+2*abs(ball.get_yv())//ball.get_yv()
                ball.set_xv(new_xv)
                ball.set_yv(new_yv)
        if np.array_equal(np.array([["G", "G"], ["G", "G"]]), type):
            self.paddle.set_grab()
            self.grab_ball = datetime.now()

    def collissions(self):
        for ball in self.balls:
            if ball.is_active() and ball.should_move():

                points = ball.trajectory()
                for p in points:
                    flag = False
                    flag = ball.move(p[0], p[1])
                    a = self.paddle.did_collide(ball)
                    if a != 0:
                        ball.set_xv(ball.get_xv()+a)
                        ball.set_yv(ball.get_yv()*-1)
                        flag = True
                        if self.paddle.get_grab():
                            ball.flip_move()
                        break

                    for brick in self.bricks:
                        if self.pass_through and brick.is_active() and brick.pass_through_collide(ball):
                            brick.set_inactive()
                            self.score += 5
                            flag = True
                        elif brick.is_active() and brick.did_collide(ball):
                            flag = True
                            if isinstance(brick, chain_brick):
                                curr = brick.hit(self.bricks)
                                if(curr == 0):
                                    self.powerups.append(
                                        Power_up(brick.get_x(), brick.get_y(), ball.get_xv(), ball.get_yv(), self.power_up_type[np.random.choice([0, 1, 2, 3, 4, 5, 6])]))
                            else:
                                curr = brick.hit()
                                if(curr == 0):
                                    self.powerups.append(
                                        Power_up(brick.get_x(), brick.get_y(), ball.get_xv(), ball.get_yv(), self.power_up_type[np.random.choice([0, 1, 2, 3, 4, 5, 6])]))
                            if not isinstance(brick, Unbreakable):
                                self.score += 1
                    if(flag):
                        break

    def update_screen(self):
        self.screen.add_to_game_screen(self.paddle)
        for powerup in self.powerups:
            if(powerup.is_active()):
                self.screen.add_to_game_screen(powerup)
        for bullet in self.bullets:
            self.screen.add_to_game_screen(bullet)
        for brick in self.bricks:
            if(brick.is_active()):
                self.screen.add_to_game_screen(brick)
        for ball in self.balls:
            if(ball.is_active()):
                self.screen.add_to_game_screen(ball)

    def lost(self):
        score_string = f"SCORE: %d" % (self.score)
        body = np.array([list(score_string)])
        obj = Game_object(70, 20, body[0].size,
                          1, 0, 0, body, np.full(body.shape, Fore.WHITE+Style.BRIGHT))
        self.reset()
        os.system("clear")
        self.screen.reset_screen()
        self.screen.add_to_game_screen(self.game_over)
        self.screen.add_to_game_screen(obj)
        self.screen.add_to_game_screen(self.my_continue)
        self.screen.print_game_screen()

        while True:
            c = input_to(self.getch)
            if(c == 'c'):
                break

    def winpage(self):
        os.system("clear")
        self.win = False
        score_string = f"SCORE: %d" % (self.score)
        body = np.array([list(score_string)])
        obj = Game_object(70, 20, body[0].size,
                          1, 0, 0, body, np.full(body.shape, Fore.WHITE+Style.BRIGHT))
        self.reset()
        os.system("clear")
        self.screen.reset_screen()
        self.screen.add_to_game_screen(self.my_win)
        self.screen.add_to_game_screen(obj)
        self.screen.add_to_game_screen(self.my_continue)
        self.screen.print_game_screen()
        while True:
            c = input_to(self.getch)
            if(c == 'c'):
                break

    def new_game(self):
        while True:
            self.main_screen()
            self.reset()
            os.system("clear")
            self.put_bricks()
            while self.level <= 3 and self.lives > 0:
                self.user_input()
                self.move_all()
                if self.over == True:
                    break

                self.collissions()
                self.screen.reset_screen()
                self.update_screen()
                self.screen.print_game_screen()
                self.check_powerup_times()
                self.print_meta()
                for ball in self.balls:
                    if ball.is_active():
                        break
                else:
                    self.lives -= 1
                    self.small_reset()
                for brick in self.bricks:
                    if not isinstance(brick, Unbreakable):
                        if brick.is_active():
                            break
                else:

                    if self.level == 3:
                        self.win = True
                        break
                    self.level += 1
                    self.level_start = datetime.now()
                    self.small_reset()
                    self.put_bricks()

                if self.skip_level == True:
                    self.skip_level = False
                    self.level += 1
                    self.level_start = datetime.now()
                    self.small_reset()
                    self.put_bricks()
            if self.win:
                self.winpage()
            elif self.lives == 0 or self.over:
                self.over = False
                self.lost()
