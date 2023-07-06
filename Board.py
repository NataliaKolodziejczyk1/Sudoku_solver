import numpy as np
class Wrong_Board(Exception):
    pass
class Board:
    def __init__(self):
        print("Give numbers without any spaces. If number is not given, print 0")
        self.board = np.zeros((9,9),dtype=int)
        for i in range(9):
            x = list(input("Row nr " + str(i+1) + " "))
            self.board[i,:] = x
        self.check_if_correct()
    def check_if_correct(self):
        temp = np.array(self.board)
        try:
            for x in range(9):
                print(str(x))
                row = temp[x,:]
                row = row[row != 0]
                print(row)
                if len(np.unique(row)) != len(row):
                    raise Wrong_Board()
                col = temp[:,x]
                col = col[col != 0]
                print(col)
                if len(np.unique(col)) != len(col):
                    raise Wrong_Board()
                square = temp[x//3*3:x//3*3+3,x%3*3:x%3*3+3].flatten()
                square = square[square != 0]
                print(square)
                if len(np.unique(square)) != len(square):
                    raise Wrong_Board()
        except Wrong_Board:
            print("Your Sudoku is not correct!")

    def print_board(self):
        print('╒'+('='*7+'╤')*2+'='*7+'╕')
        for i in range(9):
            print(f'│ {self.board[i,0]} {self.board[i,1]} {self.board[i,2]} │ {self.board[i,3]} {self.board[i,4]} {self.board[i,5]} │ {self.board[i,6]} {self.board[i,7]} {self.board[i,8]} │')
            if i == 2 or i == 5:
                print('├'+('─'*7+'┼')*2+'─'*7+'┤')
        print('╘' + ('=' * 7 + '╧') * 2 + '=' * 7 + '╛')






