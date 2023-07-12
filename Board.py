import numpy as np
from functools import reduce
import random
from itertools import combinations


class Wrong_Board(Exception):
    pass
# there is our class to solve sudoku
class Board:
    def __init__(self):
        # we start with empty board, 0 is considered to be empty cell
        # we can choose a sudoku to start with and enter the numbers here
        self.board = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0]])
        # we check if this sudoku is correct, if not exception is thrown
        self.check_if_correct()
        # we fill other numpy array with possible candidates for a cell
        self.possible = np.array(self.board)
        self.simple_elimination()
        # color array is needed for further coloring
        self.color = [1 if x > 0 else 0 for x in self.board.flatten()]
        self.color = np.array(self.color).reshape((9, 9))
        # strategy will determine which color we pick for coloring
        self.strategy = 0
        self.solved = self.is_solved()

    # when difficulty button is clicked, one of sudoku boards is randomly selected from list,
    # and we need to update this object
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
            num = random.randint(0, len(level_moderate_sudoku) - 1)
            self.board = np.array(level_moderate_sudoku[num])
            self.possible = np.array(self.board)
            self.simple_elimination()
            self.color = [1 if x > 0 else 0 for x in self.board.flatten()]
            self.color = np.array(self.color).reshape((9, 9))
            self.strategy = 0
        if level == 3:
            num = random.randint(0, len(level_tough_sudoku) - 1)
            self.board = np.array(level_tough_sudoku[num])
            self.possible = np.array(self.board)
            self.simple_elimination()
            self.color = [1 if x > 0 else 0 for x in self.board.flatten()]
            self.color = np.array(self.color).reshape((9, 9))
            self.strategy = 0
    # method that checks whether our sudoku is entered correctly
    # we check if there is uniqe numbers in every row, column and square
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
    # text version of solution
    def print_board(self):
        print('╒'+('='*7+'╤')*2+'='*7+'╕')
        for i in range(9):
            print(f'│ {self.board[i,0]} {self.board[i,1]} {self.board[i,2]} │ {self.board[i,3]} {self.board[i,4]} '
                  f'{self.board[i,5]} │ {self.board[i,6]} {self.board[i,7]} {self.board[i,8]} │')
            if i == 2 or i == 5:
                print('├'+('─'*7+'┼')*2+'─'*7+'┤')
        print('╘' + ('=' * 7 + '╧') * 2 + '=' * 7 + '╛')
    # text version of candidates for every cell
    def print_possible(self):
        print('╒' + ('=' * 31 + '╤') * 2 + '=' * 31 + '╕')
        for i in range(9):
            print(f'│ {self.possible[i,0]:<9} {self.possible[i,1]:<9} {self.possible[i,2]:<9} │ {self.possible[i,3]:<9} '
                  f'{self.possible[i,4]:<9} {self.possible[i,5]:<9} │ {self.possible[i,6]:<9} {self.possible[i,7]:<9} '
                  f'{self.possible[i,8]:<9} │')
            if i == 2 or i == 5:
                print('├'+('─'*31+'┼')*2+'─'*31+'┤')
        print('╘' + ('=' * 31 + '╧') * 2 + '=' * 31 + '╛')

    # first part of solution
    # we basically fill every empty cell with candidates for that position - to do this we eliminate numbers
    # that are already present in considered unit (row,column or square)
    def simple_elimination(self):
        for i in range(81):
            row = i//9
            col = i%9
            if self.board[row,col] == 0: # if it is not 0 at this point, it is one of starting numbers
                self.possible[row,col] = self.simple_elimination_cell(row, col)

    def simple_elimination_cell(self,row,col):
        # we add to set cell every number that is in the same row, column or square that cell [row,col]
        cell = set()
        square, _ = self.square_and_index(row,col)
        for i in range(9):
            cell.add(self.board[row,i])
            cell.add(self.board[i,col])
            cell.add(square[i])
        # we eliminate found numbers
        cell = list(set(list(range(1,10))).difference(cell))
        # sorting list helps keeping right order
        cell.sort()
        cell = int(reduce(lambda a, b: str(a) + str(b), cell))
        return cell
    # possible board works like this - if there is number 1678 in a cell that means, that
    # 1, 6, 7 or 8 are possible candidates for that cell

    # if minimal number on board is 0, sudoku is not solved yet
    def is_solved(self):
        # we search for minimum
        if self.board[np.unravel_index(np.argmin(self.board),self.board.shape)]:
            return True
        else:
            return False
    # first strategy
    # after simple elimination, we might have removed some numbers and leave a cell with only one candidate -
    # that means that this is solution for this cell (no other number can possibly fill this cell)
    def naked_single(self):
        # we do this as long as we make any changes (after one loop there may appear another naked single)
        flag = 1
        while flag:
            flag = 0
            # we search for cells that has only one candidate, so this is numbers between 1-9
            # and it is not solved yet (so we haven't transferred it on board)
            log = np.logical_and(self.possible<10,self.possible!=self.board)
            # list of indexes we found
            idxs = list(zip(*np.where(log==True)))
            for i in idxs:
                # we put this numbers on board (where we keep solution)
                self.board[i] = self.possible[i]
                # put color
                self.color[i] = self.strategy
                # possible board must be updated
                self.update_possible(*i)
                flag = 1

    # this function accepts two arguments - position of new solved cell
    # we iterate through row, column and square where this cell is, and update candidates in other cells here
    def update_possible(self,row,col):
        # here we get square where cell is located
        square, square_idx = self.square_and_index(row,col)
        # set allow us to make mathematical set operations - this is really useful
        # .difference() let us remove number from other set
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
    # second strategy
    # sometimes there are more than one candidate in a cell, but among these candidates is a number that must
    # be here because it can't be anywhere else in this unit - its hidden single
    def hidden_single(self):
        flag = 1
        while flag:
            flag = 0
            for i in range(81):
                row = i//9
                col = i%9
                # after finding naked single we only consider cells with more than 1 candidate
                if self.possible[row,col] > 9:
                    # check if there is a hidden single
                    num =  self.is_hidden_single(row,col)
                    if num != 0:
                        # if yes, we update possible array and put solution on board
                        self.possible[row, col] = num
                        self.board[row,col] = num
                        self.color[row,col] = self.strategy
                        self.update_possible(row,col)
                        flag = 1

    # return 0 if there is no hidden single in cell, or return number that is hidden single in this cell
    def is_hidden_single(self, row, col):
        # list of candidates in that cell
        nums = [int(x) for x in str(self.possible[row,col])]
        # we check every candidate - if it is present anywhere else in a unit
        for num in nums:
            # rows
            for i in range(9):
                if i != col:
                    # if we find this number else it is not hidden single in this row
                    if num in [int(x) for x in str(self.possible[row,i])]:
                        break
            else:
                return num
            #cols
            for i in range(9):
                if i != row:
                    if num in [int(x) for x in str(self.possible[i, col])]:
                        break
            else:
                return num
            #squares
            square, square_idx = self.square_and_index(row,col)
            for i in range(9):
                if i != square_idx:
                    if num in [int(x) for x in str(square[i])]:
                        break
            else:
                return num
        return 0
    # this is third strategy
    # "Naked Pair" refers to a situation, where in two cells in the same unit there are the same pair of candidates
    # It means that this numbers can't be anywhere else in this unit
    # In fact this does not solve anything, but can create a naked or hidden single somewhere
    def naked_pair(self):
        flag = 1
        while flag:
            flag = 0
            # we search possible for numbers between 11-99 (two candidates)
            for i in range(81):
                row = i // 9
                col = i % 9
                square, square_idx = self.square_and_index(row,col)
                num = self.possible[row,col]
                if num > 10 and num < 100:
                    # for each found number we check if there is the same looking cell
                    for x in range(9):
                        if x != col:
                            # if yes, we found our naked pair
                            if num == self.possible[row,x]:
                                # we need to remove this pair from other cells in this row
                                flag += self.remove_from_row(row,num)
                        # do the same for column and square
                        if x != row:
                            if num == self.possible[x,col]:
                                flag += self.remove_from_col(col,num)

                        if x != square_idx:
                            if num == square[x]:
                                # new_square is square after removing naked pair from other cells here
                                new_square = self.remove_from_square(square,num)
                                # if it is different than before, we change possible
                                if (new_square.reshape((3,3)) !=  self.possible[row//3*3:row//3*3+3,col//3*3:col//3*3+3]).any():
                                    self.possible[row//3*3:row//3*3+3,col//3*3:col//3*3+3] = new_square.reshape((3,3))
                                    flag = 1

    # Naked triple is similar to naked pair, but it is three cells in one unit that contain in total only three
    # different candidates. Then we are able to remove this triple from other cells in a unit
    def naked_triple(self):
        flag = 1
        while flag:
            flag = 0
            for i in range(9):
                #rows
                for col1 in range(9):
                    num1 = self.possible[i,col1]
                    # we search for numbers between 11 and 999
                    if num1 > 10 and num1 < 1000:
                        for col2 in range(col1+1,9):
                            num2 = self.possible[i,col2]
                            if num2 > 10 and num2 < 1000:
                                # we try to pair two numbers and check if there is no more than 3 candidates in total
                                cur_set = set(str(num1)).union(set(str(num2)))
                                if len(cur_set) < 4:
                                    for col3 in range(col2+1,9):
                                        # if we found a pair, we try to add third number to them
                                        num3 = self.possible[i,col3]
                                        if num3 > 10 and num3 < 1000:
                                            cur_set_2 = cur_set.union(set(str(num3)))
                                            # check if there is exactly 3 possible numbers
                                            if len(cur_set_2) == 3:
                                                #We found our naked tripple at positions [i,col1],[i,col2],[i,col3]
                                                total_num = list(cur_set_2)
                                                total_num.sort()
                                                total_num = int(reduce(lambda a, b: str(a) + str(b), total_num))
                                                # total_num has now format of cells in possible
                                                flag += self.remove_from_row(i,total_num)
                #cols
                for row1 in range(9):
                    num1 = self.possible[row1,i]
                    if num1 > 9 and num1 < 1000:
                        for row2 in range(row1 + 1, 9):
                            num2 = self.possible[row2,i]
                            if num2 > 9 and num2 < 1000:
                                cur_set = set(str(num1)).union(set(str(num2)))
                                if len(cur_set) < 4:
                                    for row3 in range(row2+1, 9):
                                        num3 = self.possible[row3,i]
                                        if num3 > 9 and num3 < 1000:
                                            cur_set_2 = cur_set.union(set(str(num3)))
                                            if len(cur_set_2) == 3:
                                                # We found our naked triple at positions [row1,i],[row2,i],[row3,i]
                                                total_num = list(cur_set_2)
                                                total_num.sort()
                                                total_num = int(reduce(lambda a, b: str(a) + str(b), total_num))
                                                flag += self.remove_from_col(i, total_num)
                #squares
                square = self.possible[i//3*3:i//3*3+3,i%3*3:i%3*3+3].flatten()
                for sq_idx1 in range(9):
                    num1 = square[sq_idx1]
                    if num1 > 9 and num1 < 1000:
                        for sq_idx2 in range(sq_idx1+1,9):
                            num2 = square[sq_idx2]
                            if num2 > 9 and num2 < 1000:
                                cur_set = set(str(num1)).union(set(str(num2)))
                                if len(cur_set) < 4:
                                    for sq_idx3 in range(sq_idx2+1,9):
                                        num3 = square[sq_idx3]
                                        if num3 > 9 and num3 < 1000:
                                            cur_set_2 = cur_set.union(set(str(num3)))
                                            if len(cur_set_2) == 3:
                                                # We found our naked tripple at positions [sq_idx1],[sq_idx2],[sq_idx3] in square i
                                                total_num = list(cur_set_2)
                                                total_num.sort()
                                                total_num = int(reduce(lambda a, b: str(a) + str(b), total_num))
                                                new_square = self.remove_from_square(square,total_num)
                                                if (new_square.reshape((3,3)) != self.possible[i//3*3:i//3*3+3,i%3*3:i%3*3+3]).any():
                                                    self.possible[i//3*3:i//3*3+3,i%3*3:i%3*3+3] = new_square.reshape((3,3))
                                                    flag = 1

    # After introduction of naked single, naked pair and naked triple here are the boss - naked quad
    # it is not that common, but sometimes it is needed to open up the board
    # We now search for 4 cells with exactly 4 candidates in total
    # I used the same algorithm as for Naked Triple, but extended it by one number and made some required changes
    def naked_quad(self):
        flag = 1
        while flag:
            flag = 0
            for i in range(9):
                #rows
                for col1 in range(9):
                    num1 = self.possible[i,col1]
                    # we now search for no more than 4 candidates or less
                    if num1 > 9 and num1 < 10000:
                        for col2 in range(col1+1,9):
                            num2 = self.possible[i,col2]
                            if num2 > 9 and num2 < 10000:
                                cur_set = set(str(num1)).union(set(str(num2)))
                                if len(cur_set) < 5:
                                    for col3 in range(col2+1,9):
                                        num3 = self.possible[i,col3]
                                        if num3 > 9 and num3 < 10000:
                                            cur_set_2 = cur_set.union(set(str(num3)))
                                            if len(cur_set_2) < 5:
                                                for col4 in range(col3 + 1, 9):
                                                    num4 = self.possible[i, col4]
                                                    if num4 > 9 and num4 < 10000:
                                                        cur_set_3 = cur_set_2.union(set(str(num4)))
                                                        if len(cur_set_3) < 5:
                                                            #We found our naked quad at positions [i,col1],[i,col2],[i,col3],[i,col4]
                                                            total_num = list(cur_set_3)
                                                            total_num.sort()
                                                            total_num = int(reduce(lambda a, b: str(a) + str(b), total_num))
                                                            flag += self.remove_from_row(i,total_num)
                #cols
                for row1 in range(9):
                    num1 = self.possible[row1,i]
                    if num1 > 9 and num1 < 10000:
                        for row2 in range(row1 + 1, 9):
                            num2 = self.possible[row2,i]
                            if num2 > 9 and num2 < 10000:
                                cur_set = set(str(num1)).union(set(str(num2)))
                                if len(cur_set) < 5:
                                    for row3 in range(row2+1, 9):
                                        num3 = self.possible[row3,i]
                                        if num3 > 9 and num3 < 10000:
                                            cur_set_2 = cur_set.union(set(str(num3)))
                                            if len(cur_set_2) < 5:
                                                for row4 in range(row3+1,9):
                                                    num4 = self.possible[row4,i]
                                                    if num4 > 9 and num3 < 10000:
                                                        cur_set_3 = cur_set_2.union(set(str(num4)))
                                                        if len(cur_set_3) < 5:
                                                            # We found our naked quad at positions [row1,i],[row2,i],[row3,i],[row4,i]
                                                            total_num = list(cur_set_3)
                                                            total_num.sort()
                                                            total_num = int(reduce(lambda a, b: str(a) + str(b), total_num))
                                                            flag += self.remove_from_col(i, total_num)
                #squares
                square = self.possible[i//3*3:i//3*3+3,i%3*3:i%3*3+3].flatten()
                for sq_idx1 in range(9):
                    num1 = square[sq_idx1]
                    if num1 > 9 and num1 < 10000:
                        for sq_idx2 in range(sq_idx1+1,9):
                            num2 = square[sq_idx2]
                            if num2 > 9 and num2 < 10000:
                                cur_set = set(str(num1)).union(set(str(num2)))
                                if len(cur_set) < 5:
                                    for sq_idx3 in range(sq_idx2+1,9):
                                        num3 = square[sq_idx3]
                                        if num3 > 9 and num3 < 10000:
                                            cur_set_2 = cur_set.union(set(str(num3)))
                                            if len(cur_set_2) < 5:
                                                for sq_idx4 in range(sq_idx3 + 1, 9):
                                                    num4 = square[sq_idx4]
                                                    if num4 > 9 and num3 < 10000:
                                                        cur_set_3 = cur_set_2.union(set(str(num4)))
                                                        if len(cur_set_3) < 5:
                                                            # We found our naked quad at positions [sq_idx1],[sq_idx2],[sq_idx3],[sq_idx4] in square i
                                                            total_num = list(cur_set_3)
                                                            total_num.sort()
                                                            total_num = int(reduce(lambda a, b: str(a) + str(b), total_num))
                                                            new_square = self.remove_from_square(square,total_num)
                                                            if (new_square.reshape((3,3)) != self.possible[i//3*3:i//3*3+3,i%3*3:i%3*3+3]).any():
                                                                self.possible[i//3*3:i//3*3+3,i%3*3:i%3*3+3] = new_square.reshape((3,3))
                                                                flag = 1

    # We pass here row of found naked pair, triple or quad and numbers, this function removes this numbers from
    # other cells in the same row. If no change were made it returns 0, if changes were made returns 1
    def remove_from_row(self,row,num):
        change = 0
        # iteration through row
        for i in range(9):
            # temp is a list of numbers after removal of candidates passed to a function
            temp = list(set(str(self.possible[row, i])).difference(set(str(num))))
            # if temp is empty, it means it is cell present in naked group we found previously
            if temp:
                temp.sort()
                temp = int(reduce(lambda a, b: str(a) + str(b), temp))
                # if temp is equal to self.possible[row, i], it means nothing was removed - no change made
                if temp != self.possible[row, i]:
                    change = 1
                    self.possible[row, i] = temp
        return change

    # We pass here column of found naked pair, triple or quad and numbers, this function removes this numbers from
    # other cells in the same column. If no change were made it returns 0, if changes were made returns 1
    def remove_from_col(self,col,num):
        change = 0
        for i in range(9):
            # temp is a list of numbers after removal of candidates passed to a function
            temp = list(set(str(self.possible[i, col])).difference(set(str(num))))
            # if temp is empty, it means it is cell present in naked group we found previously
            if temp:
                temp.sort()
                temp = int(reduce(lambda a, b: str(a) + str(b), temp))
                # if temp is equal to self.possible[row, i], it means nothing was removed - no change made
                if temp != self.possible[i,col]:
                    change = 1
                    self.possible[i,col] = temp
        return change
    # We pass here a numpy array of square and numbers of found naked pair, triple or quad, this function removes
    # this numbers from other cells in the same square. It returns updated square
    def remove_from_square(self,square,num):
        for i in range(9):
            temp = list(set(str(square[i])).difference(set(str(num))))
            if temp:
                temp.sort()
                temp = int(reduce(lambda a, b: str(a) + str(b), temp))
                square[i] = temp
        return square
    # Hidden Pair is fifth strategy, in fact before naked quads.
    # Now the pair of numbers is "hidden" among other candidates, and we need to find them
    # It is situation, when a pair of numbers can be only in two cells in a unit. It means that in one cell must be one
    # of them and in second must be other one, so we can remove other candidates than this pair from this cells
    def hidden_pair(self):
        flag = 1
        while flag:
            flag = 0
            # we check every row, column and square
            for i in range(9):
                #rows
                # in this dictionary we count instances of every possible pair
                pairs_in_row = {}
                # in this dictionary we count instances of every single number
                nums_in_row = {}
                for col in range(9):
                    num = self.possible[i,col]
                    if num > 9:
                        num_list = [ int(x) for x in str(num) ]
                        for n in num_list:
                            nums_in_row[n] = nums_in_row.get(n,0) + 1
                        # it creates a list of pairs as tuples
                        pairs = list(combinations(num_list, 2))
                        # we convert this to a list of numbers
                        pairs = [10*int(x[0]) + int(x[1]) for x in pairs]
                        for pair in pairs:
                            # keep track of every instance of pair
                            pairs_in_row[pair] = pairs_in_row.get(pair,0) + 1
                # check if there is a pair with 2 instances
                for key,value in pairs_in_row.items():
                    if value == 2:
                        n1 = key//10
                        n2 = key%10
                        # then we must check if this two numbers are only present in this two cells
                        if nums_in_row[n1] == 2 and nums_in_row[n2] == 2:
                            # if there is such pair, we can leave in a cell containing this pair only this pair
                            flag += self.remove_from_row_hidden(i,key)
                #cols
                # in this dictionary we count instances of every possible pair
                pairs_in_col = {}
                # in this dictionary we count instances of every single number
                nums_in_col = {}
                for row in range(9):
                    num = self.possible[row,i]
                    if num > 9:
                        num_list = [int(x) for x in str(num)]
                        for n in num_list:
                            nums_in_col[n] = nums_in_col.get(n,0) + 1
                        # it creates a list of pairs as tuples
                        pairs = list(combinations(num_list, 2))
                        # we convert this to a list of numbers
                        pairs = [10 * int(x[0]) + int(x[1]) for x in pairs]
                        for pair in pairs:
                            # keep track of every instance of pair
                            pairs_in_col[pair] = pairs_in_col.get(pair, 0) + 1
                # check if there is a pair with 2 instances
                for key, value in pairs_in_col.items():
                    if value == 2:
                        n1 = key // 10
                        n2 = key % 10
                        # then we must check if this two numbers are only present in this two cells
                        if nums_in_col[n1] == 2 and nums_in_col[n2] == 2:
                            # if there is such pair, we can leave in a cell containing this pair only this pair
                            flag += self.remove_from_col_hidden(i, key)
                #square
                # in this dictionary we count instances of every possible pair
                pairs_in_square = {}
                # in this dictionary we count instances of every single number
                nums_in_square = {}
                square = self.possible[i // 3 * 3:i // 3 * 3 + 3, i % 3 * 3:i % 3 * 3 + 3].flatten()
                for sq_idx in range(9):
                    num = square[sq_idx]
                    if num > 9:
                        num_list = [int(x) for x in str(num)]
                        for n in num_list:
                            nums_in_square[n] = nums_in_square.get(n,0) + 1
                        # it creates a list of pairs as tuples
                        pairs = list(combinations(num_list, 2))
                        # we convert this to a list of numbers
                        pairs = [10 * int(x[0]) + int(x[1]) for x in pairs]
                        for pair in pairs:
                            # keep track of every instance of pair
                            pairs_in_square[pair] = pairs_in_square.get(pair, 0) + 1
                # check if there is a pair with 2 instances
                for key, value in pairs_in_square.items():
                    if value == 2:
                        n1 = key // 10
                        n2 = key % 10
                        # then we must check if this two numbers are only present in this two cells
                        if nums_in_square[n1] == 2 and nums_in_square[n2] == 2:
                            new_square = self.remove_from_square_hidden(square, key)
                            # if there is a difference, we want to update possible board
                            if (new_square.reshape((3,3)) != self.possible[i//3*3:i//3*3+3,i%3*3:i%3*3+3]).any():
                                self.possible[i//3*3:i//3*3+3,i%3*3:i%3*3+3] = new_square.reshape((3,3))
                                flag = 1


    # function that remove from cell in a row containing nums every other possible candidate
    def remove_from_row_hidden(self,row,nums):
        change = 0
        for i in range(9):
            temp = set(str(self.possible[row, i])).difference(set(str(nums)))
            #check if cell contains this pair
            if temp != set(str(self.possible[row,i])) and temp:
                change = 1
                # we leave only this pair here
                self.possible[row, i] = nums
        return change

    # function that remove from cell in a col containing nums every other possible candidate
    def remove_from_col_hidden(self, col, nums):
        change = 0
        for i in range(9):
            temp = set(str(self.possible[i,col])).difference(set(str(nums)))
            # check if cell contains this pair
            if temp != set(str(self.possible[i,col])) and temp:
                change = 1
                # we leave only this pair here
                self.possible[i,col] = nums
        return change
    # it returns a new updated square
    def remove_from_square_hidden(self,square,nums):
        for i in range(9):
            temp = set(str(square[i])).difference(set(str(nums)))
            # check if cell contains this pair
            if set(str(square[i])) != temp and temp:
                square[i] = nums
        return square

    # this function accepts position of a cell and return whole square where this cell is located and index of
    # this cell in returned square
    def square_and_index(self,row,col):
        square = self.possible[row // 3 * 3:row // 3 * 3 + 3, col // 3 * 3:col // 3 * 3 + 3].flatten()
        idx = np.argwhere(square == self.possible[row, col])[0]
        return square, idx
# lists of sudoku
level_easy_sudoku = [
                     np.array([[0, 0, 0, 1, 0, 5, 0, 0, 0],
                               [1, 4, 0, 0, 0, 0, 6, 7, 0],
                               [0, 8, 0, 0, 0, 2, 4, 0, 0],
                               [0, 6, 3, 0, 7, 0, 0, 1, 0],
                               [9, 0, 0, 0, 0, 0, 0, 0, 3],
                               [0, 1, 0, 0, 9, 0, 5, 2, 0],
                               [0, 0, 7, 2, 0, 0, 0, 8, 0],
                               [0, 2, 6, 0, 0, 0, 0, 3, 5],
                               [0, 0, 0, 4, 0, 9, 0, 0, 0]]),
                     np.array([[0, 0, 4, 0, 5, 0, 0, 0, 0],
                               [9, 0, 0, 7, 3, 4, 6, 0, 0],
                               [0, 0, 3, 0, 2, 1, 0, 4, 9],
                               [0, 3, 5, 0, 9, 0, 4, 8, 0],
                               [0, 9, 0, 0, 0, 0, 0, 3, 0],
                               [0, 7, 6, 0, 1, 0, 9, 2, 0],
                               [3, 1, 0, 9, 7, 0, 2, 0, 0],
                               [0, 0, 9, 1, 8, 2, 0, 0, 3],
                               [0, 0, 0, 0, 6, 0, 1, 0, 0]]),
                     np.array([[8, 0, 1, 3, 4, 0, 0, 2, 0],
                               [0, 5, 0, 6, 0, 0, 8, 0, 3],
                               [0, 0, 0, 0, 9, 5, 1, 0, 0],
                               [6, 0, 0, 0, 5, 9, 0, 0, 4],
                               [0, 0, 3, 0, 0, 0, 7, 5, 0],
                               [0, 0, 5, 2, 3, 0, 6, 8, 0],
                               [0, 0, 9, 5, 0, 8, 4, 0, 6],
                               [5, 7, 0, 1, 0, 0, 2, 0, 8],
                               [3, 0, 6, 0, 0, 0, 0, 0, 0]])
                     ]
level_moderate_sudoku = [np.array([[0, 0, 0, 0, 0, 4, 0, 2, 8],
                                 [4, 0, 6, 0, 0, 0, 0, 0, 5],
                                 [1, 0, 0, 0, 3, 0, 6, 0, 0],
                                 [0, 0, 0, 3, 0, 1, 0, 0, 0],
                                 [0, 8, 7, 0, 0, 0, 1, 4, 0],
                                 [0, 0, 0, 7, 0, 9, 0, 0, 0],
                                 [0, 0, 2, 0, 1, 0, 0, 0, 3],
                                 [9, 0, 0, 0, 0, 0, 5, 0, 7],
                                 [6, 7, 0, 4, 0, 0, 0, 0, 0]]),
                       np.array([[2, 0, 0, 0, 7, 0, 0, 3, 8],
                                 [0, 0, 0, 0, 0, 6, 0, 7, 0],
                                 [3, 0, 0, 0, 4, 0, 6, 0, 0],
                                 [0, 0, 8, 0, 2, 0, 7, 0, 0],
                                 [1, 0, 0, 0, 0, 0, 0, 0, 6],
                                 [0, 0, 7, 0, 3, 0, 4, 0, 0],
                                 [0, 0, 4, 0, 8, 0, 0, 0, 9],
                                 [8, 6, 0, 4, 0, 0, 0, 0, 0],
                                 [9, 1, 0, 0, 6, 0, 0, 0, 2]]),
                       np.array([[4, 0, 0, 0, 0, 0, 0, 3, 8],
                                 [0, 0, 2, 0, 0, 4, 1, 0, 0],
                                 [0, 0, 5, 3, 0, 0, 2, 4, 0],
                                 [0, 7, 0, 6, 0, 9, 0, 0, 4],
                                 [0, 2, 0, 0, 0, 0, 0, 7, 0],
                                 [6, 0, 0, 7, 0, 3, 0, 9, 0],
                                 [0, 5, 7, 0, 0, 8, 3, 0, 0],
                                 [0, 0, 3, 9, 0, 0, 4, 0, 0],
                                 [2, 4, 0, 0, 0, 0, 0, 0, 9]]),
                       np.array([[2, 6, 0, 0, 0, 0, 0, 8, 4],
                                 [4, 0, 0, 0, 0, 8, 7, 0, 0],
                                 [0, 0, 0, 0, 5, 2, 0, 0, 1],
                                 [0, 0, 6, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 8, 6, 0, 1, 4, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 6, 0, 0],
                                 [8, 0, 0, 9, 3, 0, 0, 0, 0],
                                 [0, 0, 5, 1, 0, 0, 0, 0, 3],
                                 [3, 2, 0, 0, 0, 0, 0, 4, 5]])
                       ]
level_tough_sudoku = [np.array([[7, 2, 0, 0, 9, 6, 0, 0, 3],
                                   [0, 0, 0, 2, 0, 5, 0, 0, 0],
                                   [0, 8, 0, 0, 0, 4, 0, 2, 0],
                                   [0, 0, 0, 0, 0, 0, 0, 6, 0],
                                   [1, 0, 6, 5, 0, 3, 8, 0, 7],
                                   [0, 4, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 3, 0, 8, 0, 0, 0, 9, 0],
                                   [0, 0, 0, 7, 0, 2, 0, 0, 0],
                                   [2, 0, 0, 4, 3, 0, 0, 1, 8]]),
                         np.array([[0, 0, 0, 0, 3, 0, 0, 8, 6],
                                   [0, 0, 0, 0, 2, 0, 0, 0, 0],
                                   [0, 0, 0, 0, 0, 8, 5, 0, 0],
                                   [3, 7, 1, 0, 0, 0, 0, 9, 4],
                                   [9, 0, 0, 0, 0, 0, 0, 0, 5],
                                   [4, 0, 0, 0, 0, 7, 6, 0, 0],
                                   [2, 0, 0, 7, 0, 0, 8, 0, 0],
                                   [0, 3, 0, 0, 0, 5, 0, 0, 0],
                                   [7, 0, 0, 0, 0, 4, 0, 3, 0]]),
                         np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [9, 0, 4, 6, 0, 7, 0, 0, 0],
                                   [0, 7, 6, 8, 0, 4, 1, 0, 0],
                                   [3, 0, 9, 7, 0, 1, 0, 8, 0],
                                   [0, 0, 8, 0, 0, 0, 3, 0, 0],
                                   [0, 5, 0, 3, 0, 8, 7, 0, 2],
                                   [0, 0, 7, 5, 0, 2, 6, 1, 0],
                                   [0, 0, 0, 4, 0, 3, 2, 0, 8],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
                         np.array([[0, 0, 5, 6, 0, 0, 7, 0, 8],
                                   [0, 7, 0, 0, 0, 0, 0, 0, 4],
                                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                   [0, 3, 0, 0, 8, 0, 6, 5, 0],
                                   [2, 0, 0, 0, 9, 0, 0, 0, 3],
                                   [0, 5, 8, 0, 1, 0, 0, 7, 0],
                                   [0, 9, 0, 0, 0, 0, 0, 0, 0],
                                   [1, 0, 0, 0, 0, 0, 0, 3, 0],
                                   [4, 0, 6, 0, 0, 1, 2, 0, 0]]),
                         np.array([[2, 0, 0, 0, 1, 0, 0, 0, 0],
                                   [6, 0, 0, 8, 0, 0, 0, 0, 9],
                                   [3, 0, 0, 6, 0, 7, 0, 5, 4],
                                   [0, 0, 0, 0, 5, 6, 0, 0, 0],
                                   [0, 4, 0, 0, 8, 0, 0, 6, 0],
                                   [0, 0, 0, 4, 7, 0, 0, 0, 0],
                                   [7, 3, 0, 1, 0, 4, 0, 0, 5],
                                   [9, 0, 0, 0, 0, 5, 0, 0, 1],
                                   [0, 0, 0, 0, 2, 0, 0, 0, 7]])


                         ]