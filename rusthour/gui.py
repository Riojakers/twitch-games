import pygame as pg

from rusthour.game_board import GameBoard

pg.init()


class CarElement:
    def __init__(self, car, board):
        self.car = car
        self.sprite = pg.image.load("images/orange.png")
        self.board = board

        if self.car.orientation == 'v':
            self.sprite = pg.transform.scale(self.sprite, (int(board.w), int(board.w * 2 + board.space)))

        if self.car.orientation == 'h':
            self.sprite = pg.transform.rotate(self.sprite, 90)
            self.sprite = pg.transform.scale(self.sprite, (int(board.w * 2 + board.space), int(board.w)))

    def draw(self, board):
        x = (self.car.pos_x * board.w) + (board.space * (self.car.pos_x + 1))
        y = (self.car.pos_y * board.w) + (board.space * (self.car.pos_y + 1))

        board.screen.blit(self.sprite, pg.Rect(x, y, board.w, board.w))


class Board:
    size = 900
    space = 20

    def __init__(self):
        self.board = GameBoard("1-1")
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

            self.clock.tick(40)
            pg.display.flip()
            pg.display.update()

    def draw_board(self):
        x = 0
        y = 0
        for row in range(0, self.board.size):
            y = y + self.space
            for col in range(0, self.board.size):
                x = x + self.space
                box = pg.Rect(x, y, self.w, self.w)
                # board_matrix
                pg.draw.rect(self.screen, (255, 255, 255), box)

                x = x + self.w
            y = y + self.w
            x = 0

    def draw_elements(self):
        for car in self.cars:
            car.draw(self)


board = Board()
board.draw()
