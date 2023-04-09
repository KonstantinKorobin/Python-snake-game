import pygame as pg
from game_objects import *
from save import *
from highscore import *
import sys

import pygame_menu
from pygame_menu import themes


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Snake Game')
        self.WINDOW_SIZE = 900
        self.TILE_SIZE = 45
        self.screen = pg.display.set_mode((1300, 930))
        self.clock = pg.time.Clock()
        self.new_game()
        self.fruits_eaten = 1
        self.counter = 0
        self.record = 0
        self.playing = True
        self.user_name = ''
        self.input_active = True
        self.best_scores = []
        self.font = pygame.font.SysFont('babelfish', 25)
        self.save_data = Save()
        # self.save_data.add('hs', {})

        self.high_scores = (self.save_data.get('hs'))
        self.table = Records(self)
        self.name = EnterName(self)

        self.results = []

        self.lifes = 3

    def draw_grid(self):
        [pg.draw.line(self.screen, [45] * 3, (x, 0), (x, self.WINDOW_SIZE))
         for x in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]

        [pg.draw.line(self.screen, [45] * 3, (0, y), (self.WINDOW_SIZE, y))
         for y in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]

    def new_game(self):
        self.snake = Snake(self)
        self.food = Apple(self)
        self.grape = Grape(self)
        self.score = Score(self)
        self.brick = Brick(self)
        self.fruits_eaten = 1
        self.counter = 0
        self.lifes = 3

    def update(self):
        self.snake.update()
        pg.display.flip()
        self.clock.tick(60)

    def draw(self):
        self.screen.fill('black')
        self.draw_grid()
        self.food.draw()
        if self.fruits_eaten % 5 == 0:
            self.grape.draw()
        self.snake.draw()
        self.score.draw()
        self.name.draw()
        self.table.draw()
        if self.fruits_eaten % 3 == 0:
            self.brick.draw()

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if self.name.active == False:
                self.snake.control(event)
            self.name.name_input(event)

    def run(self):
        while self.playing:
            self.check_event()
            self.update()
            self.draw()
        self.game_over()



if __name__ == '__main__':
    game = Game()
    game.run()
