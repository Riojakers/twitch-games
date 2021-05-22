import logging

class Car():

    name = 0
    pos_x = 0
    pos_y = 0
    orientation = ""
    size = 0
    board  = []

    def __init__(self, name, pos_x, pos_y, orientation, size, board):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.orientation = orientation
        self.size = size
        self.board = board
        
        
    
    def move(self, direction):
        
        if self.orientation == "v":
            if direction == "up":
                self.move_up()
            elif direction == "dw":
                self.move_down()
            else:
                logging.warning("Cars in a upright position can only be moved up or down")
        elif self.orientation == "h":
            if direction == "rg":
                self.move_right()
            elif direction == "lf":
                self.move_left()
            else:
                logging.warning("Cars in horizontal position can only be moved up or down")
    

    def moveUp(self):
        try:
            if self.board.get()[self.pos_y-1][self.pos_x] == 0:
                    self.board.updateCarPosition(self.name, self.pos_y-1,self.pos_x, self.size, self.orientation)
            else:
                logging.warning("The car have crashed against another car")   
        except IndexError:
            logging.warning("The car have crashed against a wall")


    def moveDown(self):
        try:
            if self.board.get()[self.pos_y+1][self.pos_x] == 0:
                    self.board.updateCarPosition(self.name, self.pos_y+1, self.pos_x, self.size, self.orientation)
            else:
                logging.warning("The car have crashed against another car")   
        except IndexError:
            logging.warning("The car have crashed against a wall")


    def moveRight(self):
        try:
            if self.board.get()[self.pos_y][self.pos_x+1] == 0:
                    self.board.updateCarPosition(self.name, self.pos_y, self.pos_x+1, self.size, self.orientation)
            else:
                logging.warning("The car have crashed against another car")   
        except IndexError:
            logging.warning("The car have crashed against a wall")


    def moveLeft(self):
        try:
            if self.board.get()[self.pos_y][self.pos_x-1] == 0:
                    self.board.updateCarPosition(self.name, [self.pos_y][self.pos_x-1], self.size, self.orientation)
            else:
                logging.warning("The car have crashed against another car")   
        except IndexError:
            logging.warning("The car have crashed against a wall")


