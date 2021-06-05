import logging
from car import Car
logging.basicConfig( level=logging.DEBUG )

class GameBoard():

    board_matrix = []
    cars = []
    exit_position = ""
    size = 0

    def __init__(self, stage, exit_position=3):
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
        size = 1

        if orientation == "v":
            while not checked:
                try:
                    if not self.board_matrix[y+size][x] == car:
                        checked = True
                    else:
                        size += 1
                except IndexError:
                    checked = True
        else:
            while not checked:
                try:
                    if not self.board_matrix[y][x+size] == car:
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
                self.board_matrix[car.pos_y+length][car.pos_x] = car.name
            else:
                self.board_matrix[car.pos_y][car.pos_x+length] = car.name
                
        
    def clearMatrix(self):

        for y in range(len(self.board_matrix)):
            for x in range(len(self.board_matrix)):
                self.board_matrix[y][x] = 0

    def moveCar(self, car, move):
        logging.debug("Moving car " + str(car) )
        self.cars[car-1].move(move)
        self.updateMatrix()
                        

#TESTS
if __name__ == '__main__':
    board = GameBoard("1-1")
    board.printBoard()
    board.moveCar(2, "dw")
    board.moveCar(1, "up")
    board.printBoard()
 
