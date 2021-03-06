import logging
from car import Car

logging.basicConfig(level=logging.DEBUG)


class GameBoard():
    board_matrix = []
    cars = []
    exit_position = 0
    size = 0

    def __init__(self, stage, exit_position=3):
        self.createBoard(stage)
        self.exit_position = exit_position
        self.parseCarsPositions()
        logging.debug(len(self.cars))
        logging.debug("Cars instanciated: " + str([car.__dict__ for car in self.cars]))

    def get(self):
        return self.board_matrix

    def createBoard(self, stage):
        file_board = open("boards/" + stage)

        for line in file_board.readlines():
            self.board_matrix.append([int(value) for value in line.rstrip().split(" ")])

        self.size = len(self.board_matrix)

    def getCell(self, x, y):
        if 0 <= x <= (self.size - 1) and 0 <= y <= (self.size - 1):
            return self.board_matrix[y][x]
        return -1

    def isntanceCars(self):
        pass

    def parseCarsPositions(self):

        added = []
        for y in range(self.size):
            for x in range(self.size):
                cell = self.getCell(x, y)
                cell = int(cell)

                """ Check if not zero and not added """
                if cell > 0 and cell not in added:
                    added.append(cell)
                    orientation = "v"
                    size = 2

                    """ Next value of cell """
                    next_cell = int(self.getCell(x + 1, y))

                    if next_cell == cell:
                        orientation = 'h'
                        if int(self.getCell(x + 2, y)) == cell:
                            size = 3
                    else:
                        if int(self.getCell(x, y + 2)) == cell:
                            size = 3

                    self.cars.append(Car(cell, x, y, orientation, size, self))

        """ Sort by name """
        self.cars = sorted(self.cars, key=lambda k: k.name)
  

    def countCarSize(self, x, y, orientation, car):
        checked = False
        size = 1

        if orientation == "v":
            while not checked:
                try:
                    if not self.board_matrix[y + size][x] == car:
                        checked = True
                    else:
                        size += 1
                except IndexError:
                    checked = True
        else:
            while not checked:
                try:
                    if not self.board_matrix[y][x + size] == car:
                        checked = True
                    else:
                        size += 1
                except IndexError:
                    checked = True

        return size

    def printBoard(self):
        for x in self.board_matrix:
            print(x)

    def updateMatrix(self):
        self.clearMatrix()
        for car in self.cars:
            self.updateCarPosition(car)

    def updateCarPosition(self, car):
        for length in range(car.size):
            if car.orientation == "v":
                self.board_matrix[car.pos_y + length][car.pos_x] = car.name
            else:
                self.board_matrix[car.pos_y][car.pos_x + length] = car.name

    def clearMatrix(self):

        for y in range(len(self.board_matrix)):
            for x in range(len(self.board_matrix)):
                self.board_matrix[y][x] = 0

    def moveCar(self, car, move):
        logging.debug("Moving car " + str(car))
        self.cars[car - 1].move(move)
        self.updateMatrix()

    def checkResolvedStage(self):
        if self.board_matrix[self.exit_position][-1] == 1:
            logging.debug("Has ganado")
            return True
        else:
            return False


# TESTS
if __name__ == '__main__':
    board = GameBoard("1-1")
    board.printBoard()
    board.moveCar(1, "rg")
    board.moveCar(1, "rg")
    board.moveCar(2, "up")
    board.moveCar(2, "up")
    board.moveCar(2, "up")
    board.moveCar(1, "rg")
    board.moveCar(1, "rg")
    board.printBoard()
    board.checkResolvedStage()
