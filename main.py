import pygame
import os
import tkinter as tk
import tkinter.messagebox
import pyautogui

root = tk.Tk()
root.overrideredirect(1)
root.withdraw()

WIDTH = 600
HEIGHT = 600
FPS = 60
LINE_COLOR = pygame.Color('#B33030')
BGCOLOR = pygame.Color('#EEEEEE')
SCREEN = pygame.display.set_mode((WIDTH+400, HEIGHT))
pygame.display.set_caption("TicTacToe")
pygame.font.init()
FONT = pygame.font.SysFont('lucidasans', 30)

PICTURE = pygame.image.load(os.path.join('resources', 'tic.png'))
PICTURE = pygame.transform.scale(PICTURE, (WIDTH, HEIGHT))
X = pygame.image.load(os.path.join('resources', 'x.png'))
O = pygame.image.load(os.path.join('resources', 'o.png'))
TURN = 'X'
XO_SURFACE_ON_THE_RIGHT = pygame.image.load(os.path.join('resources', 'x.png'))

XO_LIST = []

def show_start_screen():
    SCREEN.fill(BGCOLOR)
    SCREEN.blit(PICTURE, (0, 0))
    pygame.display.flip()
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting=False

def draw_board():
    SCREEN.fill(BGCOLOR)

    #HORIZONTAL LINES
    pygame.draw.line(SCREEN, LINE_COLOR, (0, HEIGHT / 3), (WIDTH, HEIGHT / 3), 7)
    pygame.draw.line(SCREEN, LINE_COLOR, (0, (HEIGHT / 3)*2), (WIDTH, (HEIGHT / 3)*2), 7)

    #VERTICAL LINES
    pygame.draw.line(SCREEN, LINE_COLOR, (WIDTH / 3, 0), (WIDTH / 3, HEIGHT), 7)
    pygame.draw.line(SCREEN, LINE_COLOR, ((WIDTH / 3)*2, 0), ((WIDTH / 3)*2, HEIGHT), 7)

    #TEXT ON THE RIGHT
    SCREEN.blit(XO_SURFACE_ON_THE_RIGHT, (WIDTH*1.2, HEIGHT/3))

def turn_and_xo_placement(xcor, ycor, square):
    global XO_SURFACE_ON_THE_RIGHT, TURN
    if TURN == 'X':
        SCREEN.blit(X, (xcor, ycor))
        XO_LIST[square] = 'X'
        TURN = 'O'
        XO_SURFACE_ON_THE_RIGHT.fill(BGCOLOR)
        SCREEN.blit(XO_SURFACE_ON_THE_RIGHT, (WIDTH*1.2, HEIGHT/3))
        XO_SURFACE_ON_THE_RIGHT = pygame.image.load(os.path.join('resources', 'o.png'))
        SCREEN.blit(XO_SURFACE_ON_THE_RIGHT, (WIDTH*1.2, HEIGHT/3))
    else:
        SCREEN.blit(O, (xcor, ycor))
        XO_LIST[square] = 'O'
        TURN = 'X'
        XO_SURFACE_ON_THE_RIGHT.fill(BGCOLOR)
        SCREEN.blit(XO_SURFACE_ON_THE_RIGHT, (WIDTH*1.2, HEIGHT/3))
        XO_SURFACE_ON_THE_RIGHT = pygame.image.load(os.path.join('resources', 'x.png'))
        SCREEN.blit(XO_SURFACE_ON_THE_RIGHT, (WIDTH*1.2, HEIGHT/3))

def draw_line_after_win(number):
    if number == 0:
        pygame.draw.line(SCREEN, LINE_COLOR, (0, ((HEIGHT / 3) / 2)), (WIDTH, (HEIGHT / 3) / 2), 7)
    elif number == 3:
        pygame.draw.line(SCREEN, LINE_COLOR, (0, ((HEIGHT / 3) / 2)*3), (WIDTH, ((HEIGHT / 3) / 2)*3), 7)
    elif number == 6:
        pygame.draw.line(SCREEN, LINE_COLOR, (0, ((HEIGHT / 3) / 2)*5), (WIDTH, ((HEIGHT / 3) / 2)*5), 7)
    elif number == 10:
        pygame.draw.line(SCREEN, LINE_COLOR, (((WIDTH / 3) / 2), 0), ((WIDTH / 3) / 2, HEIGHT), 7)
    elif number == 11:
        pygame.draw.line(SCREEN, LINE_COLOR, (((WIDTH / 3) / 2)*3, 0), (((WIDTH / 3) / 2)*3, HEIGHT), 7)
    elif number == 12:
        pygame.draw.line(SCREEN, LINE_COLOR, (((WIDTH / 3) / 2)*5, 0), (((WIDTH / 3) / 2)*5, HEIGHT), 7)

def display_popup(win_draw):
    pygame.display.update()
    if win_draw:
        win = tkinter.messagebox.showinfo(message="You've won! Press OK to restart the game")
        if win:
            pyautogui.click()
    else:
        draw = tkinter.messagebox.showinfo(message="It's a draw! Press OK to restart the game")
        if draw:
            pyautogui.click()

def who_wins():
    for x in range(3):
        # Checking rows
        for number in range(0, 7, 3):
            if XO_LIST[number] == XO_LIST[number+1] == XO_LIST[number+2] and XO_LIST[number] != '':
                draw_line_after_win(number)
                display_popup(win_draw=True)
                initialize_the_game()
        # Checking columns
        for number in range(0, 3):
            if XO_LIST[number] == XO_LIST[number+3] == XO_LIST[number+6] and XO_LIST[number] != '':
                draw_line_after_win(number+10)
                display_popup(win_draw=True)
                initialize_the_game()
    #Checking diagonals
    if XO_LIST[0] == XO_LIST[4] == XO_LIST[8] and XO_LIST[0] != '':
        pygame.draw.line(SCREEN, LINE_COLOR, (0, 0), (WIDTH, HEIGHT), 7)
        display_popup(win_draw=True)
        initialize_the_game()
    if XO_LIST[2] == XO_LIST[4] == XO_LIST[6] and XO_LIST[2] != '':
        pygame.draw.line(SCREEN, LINE_COLOR, (WIDTH, 0), (0, HEIGHT), 7)
        display_popup(win_draw=True)
        initialize_the_game()
    if all(XO_LIST):
        display_popup(win_draw=False)
        initialize_the_game()


def location_on_the_board():
    global XO_SURFACE_ON_THE_RIGHT
    # 1 SQUARE ON THE BOARD
    if pygame.mouse.get_pos()[0] < (WIDTH / 3) and pygame.mouse.get_pos()[1] < (HEIGHT / 3) and XO_LIST[0] == '':
        turn_and_xo_placement(xcor=0, ycor=0, square=0)

    # 2 SQUARE ON THE BOARD
    if pygame.mouse.get_pos()[0] > (WIDTH / 3) and pygame.mouse.get_pos()[0] < ((WIDTH / 3) * 2) \
        and pygame.mouse.get_pos()[1] <= (HEIGHT / 3) and XO_LIST[1] == '':
        turn_and_xo_placement(xcor=200, ycor=0, square=1)

    # 3 SQUARE ON THE BOARD
    if pygame.mouse.get_pos()[0] > ((WIDTH / 3) * 2) and pygame.mouse.get_pos()[0] < ((WIDTH / 3) * 3) \
        and pygame.mouse.get_pos()[1] < (HEIGHT / 3) and XO_LIST[2] == '':
        turn_and_xo_placement(xcor=400, ycor=0, square=2)

    # 4 SQUARE ON THE BOARD
    if pygame.mouse.get_pos()[0] < (WIDTH / 3) and pygame.mouse.get_pos()[1] > (HEIGHT / 3) and \
        pygame.mouse.get_pos()[1] < ((HEIGHT / 3) * 2) and XO_LIST[3] == '':
        turn_and_xo_placement(xcor=0, ycor=200, square=3)

    # 5 SQUARE ON THE BOARD
    if pygame.mouse.get_pos()[0] > (WIDTH / 3) and pygame.mouse.get_pos()[0] < ((WIDTH / 3) * 2) \
        and pygame.mouse.get_pos()[1] > (HEIGHT / 3) and pygame.mouse.get_pos()[1] < ((HEIGHT / 3) * 2) and XO_LIST[
        4] == '':
        turn_and_xo_placement(xcor=200, ycor=200, square=4)

    # 6 SQUARE ON THE BOARD
    if pygame.mouse.get_pos()[0] > ((WIDTH / 3) * 2) and pygame.mouse.get_pos()[0] < ((WIDTH / 3) * 3) \
        and pygame.mouse.get_pos()[1] > (HEIGHT / 3) and pygame.mouse.get_pos()[1] < ((HEIGHT / 3) * 2) and XO_LIST[
        5] == '':
        turn_and_xo_placement(xcor=400, ycor=200, square=5)

    # 7 SQUARE ON THE BOARD
    if pygame.mouse.get_pos()[0] < (WIDTH / 3) and pygame.mouse.get_pos()[1] > ((HEIGHT / 3) * 2) and \
        pygame.mouse.get_pos()[1] < ((HEIGHT / 3) * 3) and XO_LIST[6] == '':
        turn_and_xo_placement(xcor=0, ycor=400, square=6)

    # 8 SQUARE ON THE BOARD
    if pygame.mouse.get_pos()[0] > (WIDTH / 3) and pygame.mouse.get_pos()[0] < ((WIDTH / 3) * 2) \
        and pygame.mouse.get_pos()[1] > ((HEIGHT / 3) * 2) and pygame.mouse.get_pos()[1] < ((HEIGHT / 3) * 3) and \
        XO_LIST[7] == '':
        turn_and_xo_placement(xcor=200, ycor=400, square=7)

    # 9 SQUARE ON THE BOARD
    if pygame.mouse.get_pos()[0] > ((WIDTH / 3) * 2) and pygame.mouse.get_pos()[0] < ((WIDTH / 3) * 3) \
        and pygame.mouse.get_pos()[1] > ((HEIGHT / 3) * 2) and pygame.mouse.get_pos()[1] < ((HEIGHT / 3) * 3) and \
        XO_LIST[8] == '':
        turn_and_xo_placement(xcor=400, ycor=400, square=8)
    pygame.display.update()

def initialize_the_game():
    global XO_LIST
    XO_LIST = ['', '', '' ,'' ,'' ,'' ,'', '' ,'']
    pygame.display.update()
    draw_board()

    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.system(exit())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
                location_on_the_board()
                print(XO_LIST)
                who_wins()
        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(FPS)


initialize_the_game()

