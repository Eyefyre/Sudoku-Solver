import pygame
import random
import numpy as np

WIDTH,HEIGHT = 900,900
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Sudoku Solver")
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
squares = [[0 for i in range(9)] for j in range(9)]
choices = [1,2,3,4,5,6,7,8,9]
pygame.font.init()  
myfont = pygame.font.SysFont('Comic Sans MS', 25)
FPS = 120
GameSpeed = 50
squareHeight,squareWidth = 75,75

def main():
    chosen = 0
    clock = pygame.time.Clock()
    mouse = pygame.mouse.get_pos() 
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                chosen = checkKeyDown(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                checkMouseClick(chosen)
        draw_all(chosen)
    
    pygame.quit()

def draw_all(chosen):
    draw_window()
    draw_board()
    draw_choices(chosen)
    draw_solve_button()
    update_display()

def draw_window():
    WINDOW.fill(WHITE)
    
def draw_board():
    for x in range(9):
        for y in range(9):
            xLoc = (90 + (80 * x))
            yLoc = (90 + (80 * y))
            pygame.draw.rect(WINDOW, BLACK, [yLoc,xLoc, squareHeight,squareWidth], 2)
            valueSurface = myfont.render(str(squares[x][y]), True, (0, 0, 0))
            if(squares[x][y] != 0):
                WINDOW.blit(valueSurface,(xLoc + squareHeight/2.25 ,yLoc + squareWidth/4))

def draw_solve_button():
    xLoc = 450
    yLoc = 10
    pygame.draw.rect(WINDOW, BLACK, [xLoc-75/2,yLoc, 75,45], 2)
    valueSurface = myfont.render("Solve", True, BLACK)
    WINDOW.blit(valueSurface,(xLoc-75/2.5 ,yLoc))

def draw_choices(chosen):
    for x in choices:
        xLoc = 10
        yLoc = (30 + (80 * x))
        he = 45
        wi = 45
        pygame.draw.rect(WINDOW, BLACK, [xLoc,yLoc, he,wi], 2)
        valueSurface = myfont.render(str(x), True, BLACK)
        if(chosen == x):
            valueSurface = myfont.render(str(x), True, RED)
        WINDOW.blit(valueSurface,(xLoc + he/3 ,yLoc + wi/8))

def checkMouseClick(chosen):
    mouse = pygame.mouse.get_pos()
    solveButtonLocX = 450
    solveButtonLocY = 10
    if solveButtonLocX-75/2 <= mouse[0] <= (solveButtonLocX + 75/2) and solveButtonLocY <= mouse[1] <= (solveButtonLocY + 45): 
        solve(chosen)
    for x in range(9):
        for y in range(9):
            xLoc = (90 + (80 * x))
            yLoc = (90 + (80 * y))
            if xLoc <= mouse[0] <= (xLoc + squareWidth) and yLoc <= mouse[1] <= (yLoc + squareHeight): 
                squares[x][y] = chosen

def checkKeyDown(event):
    if event.key == pygame.K_1:
        return 1
    if event.key == pygame.K_2:
        return 2
    if event.key == pygame.K_3:
        return 3
    if event.key == pygame.K_4:
        return 4
    if event.key == pygame.K_5:
        return 5
    if event.key == pygame.K_6:
        return 6
    if event.key == pygame.K_7:
        return 7
    if event.key == pygame.K_8:
        return 8
    if event.key == pygame.K_9:
        return 9
    return 0

def update_display():
    pygame.display.update()

def printGrid():
    for i in range(9):
        for j in range(9):
            print(squares[j][i],end = " ")
        print()
    print()

def solve(chosen):
    for x in range(GameSpeed):
        draw_all(chosen)
    find = find_empty_square()
    if not find:
        return True
    else:
        x, y = find

    for i in range(1,10):
        if valid(i, (x, y)):
            squares[x][y] = i
            if solve(chosen):
                return True
            squares[x][y] = 0

    return False


def valid(v, pos):
    for i in range(9):
        if squares[pos[0]][i] == v and pos[1] != i:
            return False

    for i in range(9):
        if squares[i][pos[1]] == v and pos[0] != i:
            return False

    box_x = (pos[1] // 3) * 3
    box_y = (pos[0] // 3) * 3

    for i in range(box_y, box_y + 3):
        for j in range(box_x, box_x + 3):
            if squares[i][j] == v and (i,j) != pos:
                return False

    return True

def find_empty_square():
    for i in range(9):
        for j in range(9):
            if squares[i][j] == 0:
                return (i, j)

    return None


if __name__ == "__main__":
    main()