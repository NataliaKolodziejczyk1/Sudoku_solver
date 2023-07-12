from Board import *
import pygame

#initialize pygame font library
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
LIGHT_BLUE = (153,153,255)
DARK_BLUE = (0,0,204)
LIGHT_MAGENTA = (255,153,255)
DARK_MAGENTA = (204,0,204)
LIGHT_VIOLET = (204,153,255)
DARK_VIOLET = (102,0,204)
LIGHT_SPRINGGREEN = (153,255,204)
DARK_SPRINGGREEN = (0,204,102)
LIGHT_YELLOW = (255,255,153)
DARK_YELLOW = (204,204,0)

#definition of button class
class Button:
    def __init__(self,win,x,y,text,font,font_size,text_col,button_col,width,height,border_col):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.font_size = font_size
        self.text_col = text_col
        self.button_col = button_col
        self.win = win
        self.width = width
        self.height = height
        self.border_col = border_col
    def draw(self):
        button_font = pygame.font.SysFont(self.font,self.font_size)
        button_text = button_font.render(self.text,1,self.text_col)
        self.button_rect = pygame.Rect(self.x, self.y,self.width,self.height)
        pygame.draw.rect(self.win,self.button_col,self.button_rect,0,10)
        pygame.draw.rect(self.win, self.border_col, self.button_rect, 2, 10)
        self.win.blit(button_text,(self.x+(self.width-button_text.get_width())//2,self.y+(self.height-button_text.get_height())//2))



def draw_window(win,sudoku):
    win.fill(BACKGROUND_COLOR)
    draw_grid(win,sudoku)
    draw_numbers(win,sudoku)
    text_font = pygame.font.SysFont('Arial', 30)
    text = text_font.render("Strategies:", 1, BLACK)
    win.blit(text, (2 * MARGIN + BOARD_SIZE + 30, MARGIN+12))
    text_font = pygame.font.SysFont('Arial', 24)
    text = text_font.render("Select difficulty:", 1, BLACK)
    win.blit(text, (2 * MARGIN + BOARD_SIZE + 26, MARGIN + 340))
def draw_grid(win,sudoku):
    cube_size = (BOARD_SIZE) // 9
    #fill board with colors corresponding to strategy
    for row in range(9):
        for col in range(9):
            if sudoku.color[row,col] == 2:
                pygame.draw.rect(win,LIGHT_YELLOW,pygame.Rect(MARGIN+col*cube_size, MARGIN+row*cube_size,cube_size ,cube_size ))
            if sudoku.color[row,col] == 3:
                pygame.draw.rect(win,LIGHT_GREEN,pygame.Rect(MARGIN+col*cube_size, MARGIN+row*cube_size,cube_size ,cube_size ))
            if sudoku.color[row,col] == 4:
                pygame.draw.rect(win,LIGHT_CYAN,pygame.Rect(MARGIN+col*cube_size, MARGIN+row*cube_size,cube_size ,cube_size ))
            if sudoku.color[row,col] == 5:
                pygame.draw.rect(win,LIGHT_BLUE,pygame.Rect(MARGIN+col*cube_size, MARGIN+row*cube_size,cube_size ,cube_size ))
            if sudoku.color[row,col] == 6:
                pygame.draw.rect(win, LIGHT_VIOLET,
                                 pygame.Rect(MARGIN + col * cube_size, MARGIN + row * cube_size, cube_size, cube_size))
            if sudoku.color[row,col] == 7:
                pygame.draw.rect(win, LIGHT_MAGENTA,
                                 pygame.Rect(MARGIN + col * cube_size, MARGIN + row * cube_size, cube_size, cube_size))
    #draw sudoku grid
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


def solve_strategy(strategy,sudoku):
    if strategy >= 2 and not sudoku.is_solved():
        sudoku.strategy = 2
        sudoku.naked_single()
    if strategy >= 3 and not sudoku.is_solved():
        sudoku.strategy = 3
        sudoku.hidden_single()
        sudoku.naked_single()
    if strategy >= 4 and not sudoku.is_solved():
        sudoku.strategy = 4
        sudoku.naked_pair()
        sudoku.hidden_single()
        sudoku.naked_single()
    if strategy >= 5 and not sudoku.is_solved():
        sudoku.strategy = 5
        sudoku.naked_triple()
        sudoku.naked_pair()
        sudoku.hidden_single()
        sudoku.naked_single()
    if strategy >= 6 and not sudoku.is_solved():
        sudoku.strategy = 6
        sudoku.hidden_pair()
        sudoku.naked_triple()
        sudoku.naked_pair()
        sudoku.hidden_single()
        sudoku.naked_single()
    if strategy >= 7 and not sudoku.is_solved():
        sudoku.strategy = 7
        sudoku.naked_quad()
        sudoku.hidden_pair()
        sudoku.naked_triple()
        sudoku.naked_pair()
        sudoku.hidden_single()
        sudoku.naked_single()


def main():

    # main surface where we draw everything
    win = pygame.display.set_mode((WIDTH,HEIGHT))

    #create our board
    sudoku = Board()

    #creating all needed buttons
    naked_single_button = Button(win,2*MARGIN+BOARD_SIZE+20,MARGIN+60,'Naked Single','Arial',20,
                                 DARK_YELLOW,LIGHT_YELLOW,140,30,DARK_YELLOW)
    hidden_single_button = Button(win,2*MARGIN+BOARD_SIZE+20,MARGIN+100,'Hidden Single','Arial',20,
                                  DARK_GREEN,LIGHT_GREEN,140,30,DARK_GREEN)
    naked_pair_button = Button(win,2*MARGIN+BOARD_SIZE+20,MARGIN+140,'Naked Pair','Arial',20,
                               DARK_CYAN,LIGHT_CYAN,140,30,DARK_CYAN)
    naked_triple_button = Button(win,2*MARGIN+BOARD_SIZE+20,MARGIN+180,'Naked Triple','Arial',20,
                                 DARK_BLUE,LIGHT_BLUE,140,30,DARK_BLUE)
    hidden_pair_button = Button(win,2*MARGIN+BOARD_SIZE+20,MARGIN+220,'Hidden Pair','Arial',20,
                                 DARK_VIOLET,LIGHT_VIOLET,140,30,DARK_VIOLET)
    naked_quad_button = Button(win,2*MARGIN+BOARD_SIZE+20,MARGIN+260,'Naked Quad','Arial',20,
                               DARK_MAGENTA,LIGHT_MAGENTA,140,30,DARK_MAGENTA)
    easy_button = Button(win,2*MARGIN+BOARD_SIZE+20,MARGIN+380,'Easy','Arial',20,
                               BLACK,WHITE,140,30,BLACK)
    gentle_button = Button(win,2*MARGIN+BOARD_SIZE+20,MARGIN+420,'Moderate','Arial',20,
                         BLACK,WHITE,140,30,BLACK)
    moderate_button = Button(win,2*MARGIN+BOARD_SIZE+20,MARGIN+460,'Tough','Arial',20,
                         BLACK,WHITE,140,30,BLACK)
    #title of window
    pygame.display.set_caption("Sudoku solver")

    run = True

    #main loop
    while run:
        # we get list of events that happend
        for event in pygame.event.get():
            # QUIT event is when we press X on the window
            if event.type == pygame.QUIT:
                run = False
            # When something on keyboard was clicked
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # we may print text version of board filled with candidates
                    sudoku.print_possible()
            # handle of button click
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if naked_single_button.button_rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0]:
                        solve_strategy(2,sudoku)
                if hidden_single_button.button_rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0]:
                        solve_strategy(3,sudoku)
                if naked_pair_button.button_rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0]:
                        solve_strategy(4,sudoku)
                if naked_triple_button.button_rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0]:
                        solve_strategy(5,sudoku)
                if hidden_pair_button.button_rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0]:
                        solve_strategy(6, sudoku)
                if naked_quad_button.button_rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0]:
                        solve_strategy(7,sudoku)
                if easy_button.button_rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0]:
                        sudoku.update_Board(1)
                if gentle_button.button_rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0]:
                        sudoku.update_Board(2)
                if moderate_button.button_rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0]:
                        sudoku.update_Board(3)
        # redraw window if any changes happend
        draw_window(win,sudoku)
        # button draw
        naked_single_button.draw()
        hidden_single_button.draw()
        naked_pair_button.draw()
        naked_triple_button.draw()
        hidden_pair_button.draw()
        naked_quad_button.draw()
        easy_button.draw()
        gentle_button.draw()
        moderate_button.draw()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
