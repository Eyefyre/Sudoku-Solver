import pygame
import random
import numpy as np

WIDTH,HEIGHT = 900,900
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Sudoku Solver")
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (255,240,240)
BEIGE = (249,243,221)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
#squares = [[0 for i in range(9)] for j in range(9)]
squares = []
choices = [1,2,3,4,5,6,7,8,9]
pygame.font.init()  
myfont = pygame.font.SysFont('Comic Sans MS', 35)
myfont2 = pygame.font.SysFont('Comic Sans MS', 45)
FPS = 120
GameSpeed = 5
chosen = 0
squareHeight,squareWidth = 75,75

def createSquares():
    squares = []
    for i in range(9):
        row = []
        for j in range(9):
            row.append([0,False])
        squares.append(row)
    #print(squares)
    return squares


def main():
    global squares
    global chosen
    squares = createSquares()
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
                if event.button == 3:
                    chosen = 0
                elif event.button == 1:
                    checkMouseClick()
        draw_all()
    
    pygame.quit()

def draw_all():
    draw_window()
    draw_board()
    draw_choices()
    draw_solve_button()
    draw_reset_button()
    update_display()

def draw_window():
    WINDOW.fill(BEIGE)
    
def draw_board():
    for x in range(9):
        for y in range(9):
            xLoc = (150 + (80 * x))
            yLoc = (90 + (80 * y))
            if squares[x][y][1]:
                pygame.draw.rect(WINDOW, BLUE, [xLoc,yLoc, squareHeight,squareWidth], 8)
            else: 
                pygame.draw.rect(WINDOW, BLACK, [xLoc,yLoc, squareHeight,squareWidth], 4)
            pygame.draw.rect(WINDOW, WHITE, [xLoc+1,yLoc+1, squareHeight-1,squareWidth-1])
            #print(squares[x][y])
            valueSurface = myfont2.render(str(squares[x][y][0]), True, BLACK)
            if(squares[x][y][0] != 0):
                WINDOW.blit(valueSurface,(xLoc + squareHeight/2.75 ,yLoc + squareWidth/8))

def draw_reset_button():
    xLoc = 550
    yLoc = 25
    pygame.draw.rect(WINDOW, BLACK, [xLoc,yLoc, 315,45], 4)
    pygame.draw.rect(WINDOW, GREY, [xLoc+1,yLoc+1, 315-1,45-1])
    valueSurface = myfont.render("RESET", True, BLACK)
    WINDOW.blit(valueSurface,(xLoc+ xLoc/6 ,yLoc))

def draw_solve_button():
    xLoc = 150
    yLoc = 25
    pygame.draw.rect(WINDOW, BLACK, [xLoc,yLoc, 315,45], 4)
    pygame.draw.rect(WINDOW, GREY, [xLoc+1,yLoc+1, 315-1,45-1])
    valueSurface = myfont.render("SOLVE", True, BLACK)
    WINDOW.blit(valueSurface,(xLoc+ xLoc/2 +20 ,yLoc))

def draw_choices():
    global chosen
    for i, x in enumerate(choices):
        xLoc = 20
        yLoc = (90 + (80 * i))
        he = 75
        wi = 75
        pygame.draw.rect(WINDOW, GREY, [xLoc+1,yLoc+1, he-1,wi-1])
        valueSurface = myfont2.render(str(x), True, BLACK)
        if(chosen == x):
            pygame.draw.rect(WINDOW, GREEN, [xLoc,yLoc, he,wi], 4)
        else:
            pygame.draw.rect(WINDOW, RED, [xLoc,yLoc, he,wi], 4)
        WINDOW.blit(valueSurface,(xLoc + he/2.75 ,yLoc + wi/8))

def resetBoard():
    global squares
    squares = createSquares()

def checkMouseClick():
    global chosen
    mouse = pygame.mouse.get_pos()
    solveButtonLocX = 150
    solveButtonLocY = 25
    resetButtonLocX = 550
    resetButtonLocY = 25
    if solveButtonLocX <= mouse[0] <= (solveButtonLocX + 315) and solveButtonLocY <= mouse[1] <= (solveButtonLocY + 45): 
        solve()
    if resetButtonLocX <= mouse[0] <= (resetButtonLocX + 315) and resetButtonLocY <= mouse[1] <= (resetButtonLocY + 45): 
        resetBoard()
    for x in range(9):
        for y in range(9):
            xLoc = (150 + (80 * x))
            yLoc = (90 + (80 * y))
            if xLoc <= mouse[0] <= (xLoc + squareWidth) and yLoc <= mouse[1] <= (yLoc + squareHeight): 
                squares[x][y][0] = chosen
                if chosen == 0:
                    squares[x][y][1] = False
                else:
                    squares[x][y][1] = True
    for i, x in enumerate(choices):
        xLoc = 20
        yLoc = (90 + (80 * i))
        he = 75
        wi = 75
        if xLoc <= mouse[0] <= (xLoc + squareWidth) and yLoc <= mouse[1] <= (yLoc + squareHeight): 
                chosen = x

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
            print(squares[j][i][0],end = " ")
        print()
    print()

def solve():
    for x in range(GameSpeed):
        draw_all()
    find = find_empty_square()
    if not find:
        return True
    else:
        x, y = find

    for i in range(1,10):
        if valid(i, (x, y)):
            squares[x][y][0] = i
            if solve():
                return True
            squares[x][y][0] = 0

    return False


def valid(v, pos):
    for i in range(9):
        if squares[pos[0]][i][0] == v and pos[1] != i:
            return False

    for i in range(9):
        if squares[i][pos[1]][0] == v and pos[0] != i:
            return False

    box_x = (pos[1] // 3) * 3
    box_y = (pos[0] // 3) * 3

    for i in range(box_y, box_y + 3):
        for j in range(box_x, box_x + 3):
            if squares[i][j][0] == v and (i,j) != pos:
                return False

    return True

def find_empty_square():
    for i in range(9):
        for j in range(9):
            if squares[i][j][0] == 0:
                return (i, j)

    return None


if __name__ == "__main__":
    main()