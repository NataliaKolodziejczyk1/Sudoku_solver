from Board import *
import pygame

pygame.font.init()

NUM_FONT = pygame.font.SysFont('comicsans',40)

WIDTH, HEIGHT = 750,560
MARGIN = 10
BOARD_SIZE = 540
BOARD_WIDTH = 5

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
def draw_window(win,sudoku):
    win.fill(WHITE)
    draw_grid(win,sudoku)
    draw_numbers(win,sudoku)
def draw_grid(win,sudoku):
    cube_size = (BOARD_SIZE) // 9
    for row in range(9):
        for col in range(9):
            if sudoku.color[row,col] == 2:
                pygame.draw.rect(win,GREEN,pygame.Rect(MARGIN+col*cube_size, MARGIN+row*cube_size,cube_size ,cube_size ))
            if sudoku.color[row,col] == 3:
                pygame.draw.rect(win,BLUE,pygame.Rect(MARGIN+col*cube_size, MARGIN+row*cube_size,cube_size ,cube_size ))

    pygame.draw.rect(win, BLACK, pygame.Rect(MARGIN, MARGIN, BOARD_SIZE, BOARD_SIZE), BOARD_WIDTH)
    for i in range(8):
        if (i + 1) % 3:
            line_width = 3
        else:
            line_width = 5
        pygame.draw.line(win, BLACK, (MARGIN, (i + 1) * cube_size + MARGIN),
                         (MARGIN + BOARD_SIZE - BOARD_WIDTH, (i + 1) * cube_size + MARGIN), line_width)
        pygame.draw.line(win, BLACK, ((i + 1) * cube_size + MARGIN, MARGIN),
                         ((i + 1) * cube_size + MARGIN, MARGIN + BOARD_SIZE - BOARD_WIDTH), line_width)
def draw_numbers(win,sudoku):
    cube_size = (BOARD_SIZE) // 9
    for row in range(9):
        for col in range(9):
            num = sudoku.board[row,col]
            if num != 0:
                num_text = NUM_FONT.render(str(num),1,BLACK)
                win.blit(num_text,(col*cube_size+MARGIN+(cube_size-num_text.get_width())//2,row*cube_size+MARGIN))



def main():

    pygame.font.init()

    win = pygame.display.set_mode((WIDTH,HEIGHT))

    a = Board()
    a.print_possible()
    pygame.display.set_caption("Sudoku solver")

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    a.naked_single(2)

                if event.key == pygame.K_d:
                    a.hidden_single(3)
                    a.naked_single(3)
        draw_window(win,a)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()

a = Board()
a.print_board()

while True:
    print("1. Show possibilities")
    print("2. Naked Single")
    print("3. Hidden Single")
    print("4. Quit\n")
    mode = 4
    if mode == 4:
        break
    if mode == 1:
        a.print_possible()
    if mode == 2:
        a.naked_single(2)
        a.print_board()
    if mode == 3:
        a.naked_single(3)
        a.hidden_single()
        a.naked_single(3)
        a.print_board()