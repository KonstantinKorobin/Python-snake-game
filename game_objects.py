import pygame as pg
from random import randrange
import pygame.freetype

vec2 = pg.math.Vector2


class Snake:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE - 1, game.TILE_SIZE - 1])
        self.rect.center = self.get_random_position()
        self.direction = vec2(0, 0)
        self.step_delay = 100
        self.time = 0
        self.length = 1
        self.segments = []
        self.directions = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

    def control(self, event):
        if event.type == pg.KEYDOWN:

            if event.key == pg.K_w and self.directions[pg.K_w]:
                self.direction = vec2(0, -self.size)
                self.directions = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}

            if event.key == pg.K_s and self.directions[pg.K_s]:
                self.direction = vec2(0, self.size)
                self.directions = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

            if event.key == pg.K_a and self.directions[pg.K_a]:
                self.direction = vec2(-self.size, 0)
                self.directions = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}

            if event.key == pg.K_d and self.directions[pg.K_d]:
                self.direction = vec2(self.size, 0)
                self.directions = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}

    def delta_time(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time > self.step_delay:
            self.time = time_now
            return True
        return False

    def get_random_position(self):
        return [randrange(self.size // 2, self.game.WINDOW_SIZE - self.size // 2, self.size)] * 2

    def move(self):
        if self.delta_time():
            self.rect.move_ip(self.direction)
            self.segments.append(self.rect.copy())
            self.segments = self.segments[-self.length:]

    def difficalty_update(self):
        if self.step_delay > 40:
            self.step_delay = (105 - 2 * self.game.fruits_eaten)

    def update(self):
        self.check_selfeating()
        self.check_borders()
        self.check_food()
        self.check_bricks()
        self.check_grapes()
        self.check_lifes()
        self.move()
        self.difficalty_update()

    def draw(self):
        [pg.draw.rect(self.game.screen, 'green', segment) for segment in self.segments]

    def check_food(self):
        if self.rect.center == self.game.food.rect.center:
            self.game.food.rect.center = self.get_random_position()
            self.length += 1
            self.game.counter += 1
            self.game.fruits_eaten += 1

    def check_grapes(self):
        if self.rect.center == self.game.grape.rect.center and self.game.fruits_eaten % 5 == 0:
            self.game.food.rect.center = self.get_random_position()
            self.length += 1
            self.game.counter += 5
            self.game.fruits_eaten += 1

    def check_bricks(self):
        if self.rect.center == self.game.brick.rect.center and self.game.fruits_eaten % 3 == 0:
            self.game.brick.rect.center = self.get_random_position()
            self.game.counter -= 3
            self.game.fruits_eaten += 1
            self.game.lifes -= 1

    def check_borders(self):
        if self.rect.left < 0 or self.rect.right > self.game.WINDOW_SIZE:
            if self.game.counter > self.game.record:
                self.game.record = self.game.counter
            player = Player(self.game.counter, self.game.name.text)
            self.game.results.append(player)
            self.game.new_game()

        if self.rect.top < 0 or self.rect.bottom > self.game.WINDOW_SIZE:
            if self.game.counter > self.game.record:
                self.game.record = self.game.counter
            player = Player(self.game.counter, self.game.name.text)
            self.game.results.append(player)
            self.game.new_game()

    def check_selfeating(self):
        if len(self.segments) != len(set(segment.center for segment in self.segments)):
            if self.game.counter > self.game.record:
                self.game.record = self.game.counter
            player = Player(self.game.counter, self.game.name.text)
            self.game.results.append(player)
            self.game.new_game()

    def check_lifes(self):
        if self.game.lifes == 0:
            player = Player(self.game.counter, self.game.name.text)
            self.game.results.append(player)
            self.game.new_game()


class Apple:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        self.rect.center = self.game.snake.get_random_position()

    def draw(self):
        pg.draw.rect(self.game.screen, 'red', self.rect)


class Grape:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        self.rect.center = self.game.snake.get_random_position()

    def draw(self):
        pg.draw.rect(self.game.screen, 'purple', self.rect)


class Brick:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE - 2, game.TILE_SIZE - 2])
        self.rect.center = self.game.snake.get_random_position()

    def draw(self):
        pg.draw.rect(self.game.screen, 'orange', self.rect)


class Score:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont('babelfish', 25)

    def draw(self):
        txt1 = self.font.render('SCORE: ' + str(self.game.counter) + ' RECORD: ' + str(self.game.record), True,
                                (255, 255, 255))

        self.game.screen.blit(txt1, (1000, 100))

        txt2 = self.font.render('Введите имя', True,
                                (255, 255, 255))

        self.game.screen.blit(txt2, (1040, 470))

        txt3 = self.font.render('Осталось жизней' + ' ' + str(self.game.lifes), True,
                                (255, 255, 255))

        self.game.screen.blit(txt3, (1000, 50))


class EnterName:
    def __init__(self, game):
        self.game = game
        self.font = pg.font.Font(None, 32)
        self.input_box = pg.Rect(1000, 500, 140, 32)
        self.color_inactive = pg.Color('lightskyblue3')
        self.color_active = pg.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.done = False

    def name_input(self, event):
        if event.type == pg.QUIT:
            done = True
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.input_box.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self):

        txt_surface = self.font.render(self.text, True, self.color)
        width = max(200, txt_surface.get_width() + 10)
        self.input_box.w = width
        self.game.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pg.draw.rect(self.game.screen, self.color, self.input_box, 2)


class Records:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont('babelfish', 25)

    def draw(self):
        cnt = 0
        self.game.results.sort(key=lambda x: x.points, reverse=True)
        for player in self.game.results:

            txt = self.font.render(str(cnt + 1) + ' ' + str(player.user_name) + ' ' + str(player.points), True,
                                   (255, 255, 255))

            self.game.screen.blit(txt, (950, 200 + 25 * cnt))
            cnt += 1
            if cnt > 10:
                break


class Player:
    def __init__(self, value, name):
        self.user_name = name
        self.points = value
