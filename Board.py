import numpy as np
from functools import reduce
import random
import pygame
import time

WIDTH, HEIGHT = 750,560
MARGIN = 10
BOARD_SIZE = 540
BOARD_WIDTH = 5

WHITE = (255,255,255)
BLACK = (0,0,0)
BACKGROUND_COLOR = (255,254,229)
LIGHT_GREEN = (204,255,153)
DARK_GREEN = (102,204,0)
LIGHT_BLUE = (153,255,255)
DARK_BLUE = (0,204,204)
BLUE = (0,0,255)

class Wrong_Board(Exception):
    pass
class Board:
    def __init__(self):
        #print("Give numbers without any spaces. If number is not given, print 0")
        #self.board = np.zeros((9,9),dtype=int)
        #for i in range(9):
        #    x = list(input("Row nr " + str(i+1) + " "))
        #    self.board[i,:] = x

        self.board = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0]])
        self.board = np.array([[4, 0, 0, 0, 0, 0, 0, 3, 8],
                               [0, 0, 2, 0, 0, 4, 1, 0, 0],
                               [0, 0, 5, 3, 0, 0, 2, 4, 0],
                               [0, 7, 0, 6, 0, 9, 0, 0, 4],
                               [0, 2, 0, 0, 0, 0, 0, 7, 0],
                               [6, 0, 0, 7, 0, 3, 0, 9, 0],
                               [0, 5, 7, 0, 0, 8, 3, 0, 0],
                               [0, 0, 3, 9, 0, 0, 4, 0, 0],
                               [2, 4, 0, 0, 0, 0, 0, 0, 9]])
        self.check_if_correct()
        self.possible = np.array(self.board)
        self.simple_elimination()
        self.color = [1 if x > 0 else 0 for x in self.board.flatten()]
        self.color = np.array(self.color).reshape((9, 9))
        self.strategy = 0

    def update_Board(self,level):
        if level == 1:
            num = random.randint(0,len(level_easy_sudoku)-1)
            self.board = np.array(level_easy_sudoku[num])
            self.possible = np.array(self.board)
            self.simple_elimination()
            self.color = [1 if x > 0 else 0 for x in self.board.flatten()]
            self.color = np.array(self.color).reshape((9, 9))
            self.strategy = 0
        if level == 2:
            num = random.randint(0, len(level_gentle_sudoku) - 1)
            self.board = np.array(level_gentle_sudoku[num])
            self.possible = np.array(self.board)
            self.simple_elimination()
            self.color = [1 if x > 0 else 0 for x in self.board.flatten()]
            self.color = np.array(self.color).reshape((9, 9))
            self.strategy = 0
        if level == 3:
            num = random.randint(0, len(level_moderate_sudoku) - 1)
            self.board = np.array(level_moderate_sudoku[num])
            self.possible = np.array(self.board)
            self.simple_elimination()
            self.color = [1 if x > 0 else 0 for x in self.board.flatten()]
            self.color = np.array(self.color).reshape((9, 9))
            self.strategy = 0

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
    def draw_colors(self,win):
        cube_size = (BOARD_SIZE) // 9
        for row in range(9):
            for col in range(9):
                if self.color[row, col] == 2:
                    pygame.draw.rect(win, LIGHT_GREEN,
                                     pygame.Rect(MARGIN + col * cube_size, MARGIN + row * cube_size, cube_size,
                                                 cube_size))
                if self.color[row, col] == 3:
                    pygame.draw.rect(win, LIGHT_BLUE,
                                     pygame.Rect(MARGIN + col * cube_size, MARGIN + row * cube_size, cube_size,
                                                 cube_size))
        pygame.display.update()
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
        cell = list(set(list(range(1,10))).difference(cell))
        cell.sort()
        cell = int(reduce(lambda a, b: str(a) + str(b), cell))
        return cell

    def is_solved(self):
        if self.board[np.unravel_index(np.argmin(self.board),self.board.shape)]:
            return True
        else:
            return False

    def naked_single(self):
        flag = 1
        while flag:
            flag = 0
            log = np.logical_and(self.possible<10,self.possible!=self.board)
            idxs = list(zip(*np.where(log==True)))
            for i in idxs:
                self.board[i] = self.possible[i]
                self.color[i] = self.strategy
                self.update_possible(*i)
                flag = 1


    def update_possible(self,row,col):
        square, square_idx = self.square_and_index(row,col)
        number = set(str(self.possible[row,col]))
        for x in range(9):
            if x!=square_idx:
                new_val = list(set(str(square[x])).difference(number))
                new_val.sort()
                new_val = int(reduce(lambda a, b: str(a) + str(b), new_val))
                square[x] = new_val
                self.possible[row//3*3:row//3*3+3,col//3*3:col//3*3+3] = square.reshape((3,3))
            if x!=row:
                new_val = list(set(str(self.possible[x,col])).difference(number))
                new_val.sort()
                new_val = int(reduce(lambda a, b: str(a) + str(b), new_val))
                self.possible[x, col] = new_val
            if x!=col:
                new_val = list(set(str(self.possible[row, x])).difference(number))
                new_val.sort()
                new_val = int(reduce(lambda a, b: str(a) + str(b), new_val))
                self.possible[row, x] = new_val
    def hidden_single(self):
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
                        self.color[row,col] = self.strategy
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
    def naked_pair(self):
        flag = 1
        while flag:
            flag = 0
            for i in range(81):
                row = i // 9
                col = i % 9
                square, square_idx = self.square_and_index(row,col)
                num = self.possible[row,col]
                if num > 9 and num < 100:
                    for x in range(9):
                        if x != col:
                            if num == self.possible[row,x]:
                                self.remove_from_row(row,num)
                                break
                        if x != row:
                            if num == self.possible[x,col]:
                                self.remove_from_col(col,num)
                                break
                        if x != square_idx:
                            if num == square[x]:
                                new_square = self.remove_from_square(square,num)
                                self.possible[row//3*3:row//3*3+3,col//3*3:col//3*3+3] = new_square.reshape((3,3))



    def remove_from_row(self,row,num):
        for i in range(9):
            if self.possible[row,i] != num:
                temp = list(set(str(self.possible[row,i])).difference(set(str(num))))
                temp.sort()
                temp = int(reduce(lambda a, b: str(a) + str(b), temp))
                self.possible[row, i] = temp

    def remove_from_col(self,col,num):
        for i in range(9):
            if self.possible[i,col] != num:
                temp = list(set(str(self.possible[i,col])).difference(set(str(num))))
                temp.sort()
                temp = int(reduce(lambda a, b: str(a) + str(b), temp))
                self.possible[i,col] = temp
    def remove_from_square(self,square,num):
        for i in range(9):
            if square[i] != num:
                temp = list(set(str(square[i])).difference(set(str(num))))
                temp.sort()
                temp = int(reduce(lambda a, b: str(a) + str(b), temp))
                square[i] = temp
        return square
    def square_and_index(self,row,col):
        square = self.possible[row // 3 * 3:row // 3 * 3 + 3, col // 3 * 3:col // 3 * 3 + 3].flatten()
        idx = np.argwhere(square == self.possible[row, col])[0]
        return square, idx
level_easy_sudoku = [
                     np.array([[0,0,0,1,0,5,0,0,0],
                               [1,4,0,0,0,0,6,7,0],
                               [0,8,0,0,0,2,4,0,0],
                               [0,6,3,0,7,0,0,1,0],
                               [9,0,0,0,0,0,0,0,3],
                               [0,1,0,0,9,0,5,2,0],
                               [0,0,7,2,0,0,0,8,0],
                               [0,2,6,0,0,0,0,3,5],
                               [0,0,0,4,0,9,0,0,0]])
                     ]
level_gentle_sudoku = [np.array([[0,0,0,0,0,4,0,2,8],
                                 [4,0,6,0,0,0,0,0,5],
                                 [1,0,0,0,3,0,6,0,0],
                                 [0,0,0,3,0,1,0,0,0],
                                 [0,8,7,0,0,0,1,4,0],
                                 [0,0,0,7,0,9,0,0,0],
                                 [0,0,2,0,1,0,0,0,3],
                                 [9,0,0,0,0,0,5,0,7],
                                 [6,7,0,4,0,0,0,0,0]]),
                       np.array([[2, 0, 0, 0, 7, 0, 0, 3, 8],
                                 [0, 0, 0, 0, 0, 6, 0, 7, 0],
                                 [3, 0, 0, 0, 4, 0, 6, 0, 0],
                                 [0, 0, 8, 0, 2, 0, 7, 0, 0],
                                 [1, 0, 0, 0, 0, 0, 0, 0, 6],
                                 [0, 0, 7, 0, 3, 0, 4, 0, 0],
                                 [0, 0, 4, 0, 8, 0, 0, 0, 9],
                                 [8, 6, 0, 4, 0, 0, 0, 0, 0],
                                 [9, 1, 0, 0, 6, 0, 0, 0, 2]]),
                       ]
level_moderate_sudoku = [np.array([[7,2,0,0,9,6,0,0,3],
                      [0,0,0,2,0,5,0,0,0],
                      [0,8,0,0,0,4,0,2,0],
                      [0,0,0,0,0,0,0,6,0],
                      [1,0,6,5,0,3,8,0,7],
                      [0,4,0,0,0,0,0,0,0],
                      [0,3,0,8,0,0,0,9,0],
                      [0,0,0,7,0,2,0,0,0],
                      [2,0,0,4,3,0,0,1,8]])]