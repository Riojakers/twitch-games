import pygame as pg

from rusthour.game_board import GameBoard

pg.init()


class CarElement:
    def __init__(self, car, board):
        self.car = car

        self.sprite = pg.image.load("images/" + str(self.car.name) + ".png")
        self.board = board

        if self.car.orientation == 'v':
            self.sprite = pg.transform.scale(self.sprite, (
            int(board.w), int(board.w * self.car.size + board.space * (self.car.size - 1))))

        if self.car.orientation == 'h':
            self.sprite = pg.transform.rotate(self.sprite, -90)
            self.sprite = pg.transform.scale(self.sprite, (
            int(board.w * self.car.size + board.space * (self.car.size - 1)), int(board.w)))

    def draw(self, board):
        x = (self.car.pos_x * board.w) + (board.space * (self.car.pos_x + 1))
        y = (self.car.pos_y * board.w) + (board.space * (self.car.pos_y + 1))

        board.screen.blit(self.sprite, pg.Rect(x, y, board.w, board.w))


class Board:
    size = 900
    space = 20

    def __init__(self, board):
        self.board = board
        self.sprite_board = pg.image.load("images/board.png")
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((self.size, self.size))
        self.screen_rect = self.screen.get_rect()

        self.w = (self.size / self.board.size) - (self.space + (self.space / self.board.size))

        self.cars = [CarElement(car, self) for car in self.board.cars]

    def draw(self):
        done = False
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
            self.draw_board()
            self.draw_elements()

            self.clock.tick(10)
            pg.display.flip()
            pg.display.update()

    def draw_board(self):
        self.screen.blit(self.sprite_board, pg.Rect(0, 0, self.size, self.size))

    def draw_elements(self):
        for car in self.cars:
            car.draw(self)
