from Board import *
import pygame

pygame.font.init()

NUM_FONT = pygame.font.SysFont('Arial',45)


WIDTH, HEIGHT = 750,560
MARGIN = 10
BOARD_SIZE = 540
BOARD_WIDTH = 5

WHITE = (255,255,255)
BLACK = (0,0,0)
BACKGROUND_COLOR = (255,254,229)
LIGHT_GREEN = (204,255,153)
DARK_GREEN = (102,204,0)
LIGHT_CYAN = (153,255,255)
DARK_CYAN = (0,204,204)
LIGHT_PURPLE = (153,153,255)
DARK_PURPLE = (0,0,204)

BLUE = (0,0,255)
class Button:
    def __init__(self,win,x,y,text,font,font_size,text_col,button_col,padding_x,padding_y,border_col):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.font_size = font_size
        self.text_col = text_col
        self.button_col = button_col
        self.win = win
        self.padding_x = padding_x
        self.padding_y = padding_y
        self.border_col = border_col
    def draw(self):
        button_font = pygame.font.SysFont(self.font,self.font_size)
        button_text = button_font.render(self.text,1,self.text_col)
        self.button_rect = pygame.Rect(self.x, self.y,button_text.get_width()+2*self.padding_x,button_text.get_height()+2*self.padding_y)
        pygame.draw.rect(self.win,self.button_col,self.button_rect,0,10)
        pygame.draw.rect(self.win, self.border_col, self.button_rect, 2, 10)
        self.win.blit(button_text,(self.x+self.padding_x,self.y+self.padding_y))



def draw_window(win,sudoku):
    win.fill(BACKGROUND_COLOR)
    draw_grid(win,sudoku)
    draw_numbers(win,sudoku)
    text_font = pygame.font.SysFont('Arial', 30)
    text = text_font.render("Strategies:", 1, BLACK)
    win.blit(text, (2 * MARGIN + BOARD_SIZE + 30, MARGIN+12))
def draw_grid(win,sudoku):
    cube_size = (BOARD_SIZE) // 9
    for row in range(9):
        for col in range(9):
            if sudoku.color[row,col] == 2:
                pygame.draw.rect(win,LIGHT_GREEN,pygame.Rect(MARGIN+col*cube_size, MARGIN+row*cube_size,cube_size ,cube_size ))
            if sudoku.color[row,col] == 3:
                pygame.draw.rect(win,LIGHT_CYAN,pygame.Rect(MARGIN+col*cube_size, MARGIN+row*cube_size,cube_size ,cube_size ))
            if sudoku.color[row,col] == 4:
                pygame.draw.rect(win,LIGHT_PURPLE,pygame.Rect(MARGIN+col*cube_size, MARGIN+row*cube_size,cube_size ,cube_size ))

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
                win.blit(num_text,(col*cube_size+MARGIN+(cube_size-num_text.get_width())//2,
                                   row*cube_size+MARGIN+(cube_size-num_text.get_height())//2))



def main():

    pygame.font.init()

    win = pygame.display.set_mode((WIDTH,HEIGHT))

    a = Board()
    a.print_possible()

    naked_single_button = Button(win,2*MARGIN+BOARD_SIZE+20,MARGIN+60,'Naked Single','Arial',20,DARK_GREEN,LIGHT_GREEN,20,5,DARK_GREEN)
    hidden_single_button = Button(win, 2 * MARGIN + BOARD_SIZE + 20, MARGIN + 100, 'Hidden Single', 'Arial', 20,
                                 DARK_CYAN, LIGHT_CYAN, 20, 5, DARK_CYAN)
    naked_pair_button = Button(win, 2 * MARGIN + BOARD_SIZE + 20, MARGIN + 140, 'Naked Pair', 'Arial', 20,
                                 DARK_PURPLE, LIGHT_PURPLE, 20, 5, DARK_PURPLE)
    pygame.display.set_caption("Sudoku solver")

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    a.update_Board(1)
                if event.key == pygame.K_2:
                    a.update_Board(2)
                if event.key == pygame.K_3:
                    a.update_Board(3)
                if event.key == pygame.K_p:
                    a.print_possible()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if naked_single_button.button_rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0]:
                        a.strategy = 2
                        a.naked_single()
                if hidden_single_button.button_rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0]:
                        a.strategy = 2
                        a.naked_single()
                        a.strategy = 3
                        a.hidden_single()
                        a.naked_single()
                if naked_pair_button.button_rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0]:
                        a.strategy = 2
                        a.naked_single()
                        a.strategy = 3
                        a.hidden_single()
                        a.naked_single()
                        a.strategy = 4
                        a.naked_pair()
                        a.hidden_single()
                        a.naked_single()


        draw_window(win,a)
        naked_single_button.draw()
        hidden_single_button.draw()
        naked_pair_button.draw()
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
