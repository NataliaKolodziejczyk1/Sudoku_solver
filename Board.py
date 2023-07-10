import numpy as np
from functools import reduce
class Wrong_Board(Exception):
    pass
class Board:
    def __init__(self):
        #print("Give numbers without any spaces. If number is not given, print 0")
        #self.board = np.zeros((9,9),dtype=int)
        #for i in range(9):
        #    x = list(input("Row nr " + str(i+1) + " "))
        #    self.board[i,:] = x

        self.board = np.array([[2, 0, 0, 0, 7, 0, 0, 3, 8],
                               [0, 0, 0, 0, 0, 6, 0, 7, 0],
                               [3, 0, 0, 0, 4, 0, 6, 0, 0],
                               [0, 0, 8, 0, 2, 0, 7, 0, 0],
                               [1, 0, 0, 0, 0, 0, 0, 0, 6],
                               [0, 0, 7, 0, 3, 0, 4, 0, 0],
                               [0, 0, 4, 0, 8, 0, 0, 0, 9],
                               [8, 6, 0, 4, 0, 0, 0, 0, 0],
                               [9, 1, 0, 0, 6, 0, 0, 0, 2]])
        self.check_if_correct()
        self.possible = np.array(self.board)
        self.simple_elimination()
        self.color = [1 if x > 0 else 0 for x in self.board.flatten()]
        self.color = np.array(self.color).reshape((9, 9))
        self.strategy = 1


    def check_if_correct(self):
        temp = np.array(self.board)
        try:
            for x in range(9):
                row = temp[x,:]
                row = row[row != 0]
                if len(np.unique(row)) != len(row):
                    raise Wrong_Board()
                col = temp[:,x]
                col = col[col != 0]
                if len(np.unique(col)) != len(col):
                    raise Wrong_Board()
                square = temp[x//3*3:x//3*3+3,x%3*3:x%3*3+3].flatten()
                square = square[square != 0]
                if len(np.unique(square)) != len(square):
                    raise Wrong_Board()
        except Wrong_Board:
            print("Your Sudoku is not correct!")

    def print_board(self):
        print('╒'+('='*7+'╤')*2+'='*7+'╕')
        for i in range(9):
            print(f'│ {self.board[i,0]} {self.board[i,1]} {self.board[i,2]} │ {self.board[i,3]} {self.board[i,4]} '
                  f'{self.board[i,5]} │ {self.board[i,6]} {self.board[i,7]} {self.board[i,8]} │')
            if i == 2 or i == 5:
                print('├'+('─'*7+'┼')*2+'─'*7+'┤')
        print('╘' + ('=' * 7 + '╧') * 2 + '=' * 7 + '╛')

    def print_possible(self):
        print('╒' + ('=' * 31 + '╤') * 2 + '=' * 31 + '╕')
        for i in range(9):
            print(f'│ {self.possible[i,0]:<9} {self.possible[i,1]:<9} {self.possible[i,2]:<9} │ {self.possible[i,3]:<9} '
                  f'{self.possible[i,4]:<9} {self.possible[i,5]:<9} │ {self.possible[i,6]:<9} {self.possible[i,7]:<9} '
                  f'{self.possible[i,8]:<9} │')
            if i == 2 or i == 5:
                print('├'+('─'*31+'┼')*2+'─'*31+'┤')
        print('╘' + ('=' * 31 + '╧') * 2 + '=' * 31 + '╛')
    def simple_elimination(self):
        for i in range(81):
            row = i//9
            col = i%9
            if self.board[row,col] == 0:
                self.possible[row,col] = self.simple_elimination_cell(row, col)

    def simple_elimination_cell(self,row,col):
        cell = set()
        square, _ = self.square_and_index(row,col)
        for i in range(9):
            cell.add(self.board[row,i])
            cell.add(self.board[i,col])
            cell.add(square[i])
        cell = set(list(range(1,10))).difference(cell)
        cell = int(reduce(lambda a, b: str(a) + str(b), cell))
        return cell

    def is_solved(self):
        if self.board[np.unravel_index(np.argmin(self.board),self.board.shape)]:
            return True
        else:
            return False

    def naked_single(self,strategy):
        flag = 1
        while flag:
            flag = 0
            log = np.logical_and(self.possible<10,self.possible!=self.board)
            idxs = list(zip(*np.where(log==True)))
            for i in idxs:
                self.board[i] = self.possible[i]
                self.color[i] = strategy
                self.update_possible(*i)
                flag = 1


    def update_possible(self,row,col):
        square, square_idx = self.square_and_index(row,col)
        number = set(str(self.possible[row,col]))
        for x in range(9):
            if x!=square_idx:
                new_val = set(str(square[x])).difference(number)
                new_val = int(reduce(lambda a, b: str(a) + str(b), new_val))
                square[x] = new_val
                self.possible[row//3*3:row//3*3+3,col//3*3:col//3*3+3] = square.reshape((3,3))
            if x!=row:
                new_val = set(str(self.possible[x,col])).difference(number)
                new_val = int(reduce(lambda a, b: str(a) + str(b), new_val))
                self.possible[x, col] = new_val
            if x!=col:
                new_val = set(str(self.possible[row, x])).difference(number)
                new_val = int(reduce(lambda a, b: str(a) + str(b), new_val))
                self.possible[row, x] = new_val
    def hidden_single(self,strategy):
        flag = 1
        while flag:
            flag = 0
            for i in range(81):
                row = i//9
                col = i%9
                if self.possible[row,col] > 9:
                    num =  self.is_hidden_single(row,col)
                    if num != 0:
                        self.possible[row, col] = num
                        self.board[row,col] = num
                        self.color[row,col] = strategy
                        self.update_possible(row,col)
                        flag = 1


    def is_hidden_single(self, row, col):
        nums = [int(x) for x in str(self.possible[row,col])]
        for num in nums:
            for i in range(9):
                if i != col:
                    if num in [int(x) for x in str(self.possible[row,i])]:
                        break
            else:
                return num
            for i in range(9):
                if i != row:
                    if num in [int(x) for x in str(self.possible[i, col])]:
                        break
            else:
                return num
            square, square_idx = self.square_and_index(row,col)
            for i in range(9):
                if i != square_idx:
                    if num in [int(x) for x in str(square[i])]:
                        break
            else:
                return num
        return 0

    def square_and_index(self,row,col):
        square = self.possible[row // 3 * 3:row // 3 * 3 + 3, col // 3 * 3:col // 3 * 3 + 3].flatten()
        idx = np.argwhere(square == self.possible[row, col])[0]
        return square, idx

