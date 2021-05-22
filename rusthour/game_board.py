class GameBoard():

    board_matrix = []
    exit_position = ""

    def __init__(self, stage, exit_position=4):
        self.createBoard(stage)
        self.exit_position = exit_position

    def get(self):
        return self.board_matrix

    def createBoard(self, stage):
        file_board = open("rusthour/boards/" + stage)
        
        for line in file_board.readlines():
            self.board_matrix.append(line.rstrip().split(" "))


    def printBoard(self):
        for x in self.board_matrix:
            print(x)

    


#TESTS
board = GameBoard("1-1")
board.printBoard()