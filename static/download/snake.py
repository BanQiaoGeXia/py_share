# -*- coding: utf-8 -*-
import json
import uuid
from tkinter import *
import threading
import queue
import time
import random
import logging
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%d %b %Y %H:%M:%S',
    filename='snake.log',
    filemode='w+'
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


class GUI(Tk):
    """
    class GUI use to create the gui
    """

    def __init__(self, q, username):
        Tk.__init__(self)
        self.username = username
        self.queue = q
        self.is_game_over = False
        self.canvas = Canvas(self, width=495, height=305, bg='#000000')
        self.canvas.pack()
        self.snake = self.canvas.create_line((0, 0), (0, 0), fill='#FFFF00', width=10)
        self.food = self.canvas.create_rectangle(0, 0, 0, 0, fill='#00FF00', outline='#00FF00')
        self.point_score = self.canvas.create_text(455, 15, fill='white', text='score:0')
        self.queue_handler()

    def restart(self):
        self.destroy()
        main()

    def queue_handler(self):
        try:
            while True:
                task = self.queue.get(block=False)
                if task.get('game_over'):
                    self.game_over(task['score'])
                elif task.get('move'):
                    points = [x for point in task['move'] for x in point]
                    self.canvas.coords(self.snake, *points)
                elif task.get('food'):
                    self.canvas.coords(self.food, *task['food'])
                elif task.get('points_score'):
                    self.canvas.itemconfigure(self.point_score,
                                              text='score:{}'.format(task['points_score']))
                    self.queue.task_done()
        except queue.Empty:
            if not self.is_game_over:
                self.canvas.after(80, self.queue_handler)

    def game_over(self, score):
        self.is_game_over = True
        logging.info("Game Over user is %s, score is %s" % (self.username, score))
        self.canvas.create_text(220, 150, fill='white', text='Game Over!')
        quit_btn = Button(self, text='Quit', command=self.destroy)
        ret_btn = Button(self, text='Resume', command=self.restart)
        self.canvas.create_window(230, 180, anchor=W, window=quit_btn)
        self.canvas.create_window(200, 180, anchor=E, window=ret_btn)
        log_upload(self.username)


class Food(object):
    """
    class Food use to make food
    """

    def __init__(self, q):
        self.queue = q
        self.position = None
        self.exppos = None
        self.make_food()

    def make_food(self):
        x = random.randrange(5, 480, 10)
        y = random.randrange(5, 295, 10)
        self.position = x, y
        logging.info("food location is (%s, %s)" % (x, y))
        self.exppos = x-5, y-5, x+5, y+5
        self.queue.put({'food': self.exppos})


class Snake(threading.Thread):
    """
    class Snake use to create snake and response action
    """

    def __init__(self, gui, q):
        threading.Thread.__init__(self)
        self.gui = gui
        self.queue = q
        self.daemon = True
        self.points_score = 0
        self.snake_points = [(495, 55), (485, 55), (475, 55), (465, 55), (455, 55)]
        self.food = Food(self.queue)
        self.direction = 'Left'
        self.start()

    def run(self):
        if self.gui.is_game_over:
            self._delete()
        while not self.gui.is_game_over:
            self.queue.put({'move': self.snake_points})
            time.sleep(0.08)
            self.move()

    def key_pressed(self, e):
        old_direction = self.direction
        self.direction = e.keysym
        if self.direction != old_direction:
            logging.info("Enter keys %s" % self.direction)

    def move(self):
        new_snake_point = self.calculate_new_coordinates()
        if self.food.position == new_snake_point:
            add_snake_point = self.calculate_new_coordinates()
            self.snake_points.append(add_snake_point)
            self.points_score += 1
            self.queue.put({'points_score': self.points_score})
            self.food.make_food()
        else:
            self.snake_points.pop(0)
            self.check_game_over(new_snake_point)
            self.snake_points.append(new_snake_point)

    def calculate_new_coordinates(self):
        last_x, last_y = self.snake_points[-1]
        new_snake_point = 0, 0
        if self.direction == 'Up':
            new_snake_point = last_x, last_y-10
        elif self.direction == 'Down':
            new_snake_point = last_x, last_y+10
        elif self.direction == 'Left':
            new_snake_point = last_x-10, last_y
        elif self.direction == 'Right':
            new_snake_point = last_x+10, last_y
        return new_snake_point

    def check_game_over(self, snake_point):
        x, y = snake_point[0], snake_point[1]
        if not -5 < x < 505 or not -5 < y < 315 or snake_point in self.snake_points:
            self.queue.put({'game_over': True, 'score': self.points_score})


def log_upload(username):
    f = open("snake.log", "r")
    url = 'http://10.255.6.44:9898/upload/'
    headers = {
        "Content-type": "application/json; charset=utf-8",
    }
    log_list = f.readlines()
    data = {
        "username": str(username),
        "tips": "log_upload",
        "log_list": log_list
    }
    post_data = json.dumps(data)

    resp = requests.post(url, headers=headers, data=post_data)
    content = resp.content
    resp_data = json.loads(content.decode())
    print(resp_data)

    f.close()


def main():
    username = uuid.uuid4()
    logging.info("game start, user is %s" % username)
    q = queue.Queue()
    gui = GUI(q, username)
    gui.title("snake")
    snake = Snake(gui, q)
    gui.bind('<Key-Left>', snake.key_pressed)
    gui.bind('<Key-Right>', snake.key_pressed)
    gui.bind('<Key-Up>', snake.key_pressed)
    gui.bind('<Key-Down>', snake.key_pressed)
    gui.mainloop()

if __name__ == '__main__':
    main()
