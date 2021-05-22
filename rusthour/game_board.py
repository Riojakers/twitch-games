import logging
from car import Car
logging.basicConfig( level=logging.DEBUG )

class GameBoard():

    board_matrix = []
    cars = []
    exit_position = ""
    size = 0

    def __init__(self, stage, exit_position=4):
        self.createBoard(stage)
        self.exit_position = exit_position
        self.parseCarsPositions()
        logging.debug(len(self.cars))
        logging.debug("Cars instanciated: " + str([ car.__dict__ for car in self.cars]))

    def get(self):
        return self.board_matrix

    def createBoard(self, stage):
        file_board = open("rusthour/boards/" + stage)
        
        for line in file_board.readlines():
            self.board_matrix.append([int(value) for value in line.rstrip().split(" ")])

        self.size = len(self.board_matrix)


    def isntanceCars(self):
        pass
       
    def parseCarsPositions(self):
        lastCar = False
        
        car = 1

        while not lastCar:
            eccounter = False
            for y in range(self.size):
                for x in range(self.size):
                    logging.debug("Car :" + str(car) + " Col: "+ str(x) + " Row: " + str(y))
                    logging.debug("Valor: " + str( self.board_matrix[y][x]) )
                    car_size = 0
                    car_orientation = ""
                    actual_value = self.board_matrix[y][x]

                    """ Search the begin of the car """
                    if car == actual_value and not eccounter:
                        eccounter = True
                        """Check the orientation """
                        if car == self.board_matrix[y+1][x]:
                            car_orientation = "v"
                            car_size = self.countCarSize(x,y,car_orientation,car)
                            self.cars.append(Car(car, x, y, car_orientation, car_size, self))
                        else:
                            car_orientation = "h"
                            car_size = self.countCarSize(x,y,car_orientation,car)
                            self.cars.append(Car(car, x, y, car_orientation, car_size, self))

            if not eccounter:
                lastCar = True
            car += 1

    def countCarSize(self,x,y,orientation,car):
        checked = False
        sum = 1

        if orientation == "v":
            while not checked:
                try:
                    if not self.board_matrix[y+sum][x] == car:
                        checked = True
                    sum += 1
                except IndexError:
                    checked = True
        else:
            while not checked:
                try:
                    if not self.board_matrix[y][x+sum] == car:
                        checked = True
                    sum += 1
                except IndexError:
                    checked = True
                  
        return sum

    def printBoard(self):
        for x in self.board_matrix:
            print(x)

    def updateCarPosition(self, name, pos_x, pos_y, size, orientation):

        """ Clean latest position """
        for row in board_matrix:
            for col in row:
                print("Tablero")

                        

#TESTS
if __name__ == '__main__':
    board = GameBoard("1-1")
    board.printBoard()