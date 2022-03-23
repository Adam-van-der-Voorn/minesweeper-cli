import os
import random
import time
import math
import string
import sys
from os import system

system("title "+'Minesweeper')


cols = 30 + 19
lines = 16
mine_amount = 15
os.system('mode con: cols='+str(cols)+' lines='+str(lines))
#random.seed(1287923816)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def get_min(array):  #get pos of min value from grid                      
    min_val = 9999 
    min_val_pos = []
    for yy in range (10):
        for xx in range(10):
            if array[yy][xx] < min_val:
                min_val_pos = [xx, yy]
                min_val = array[yy][xx]
    return min_val_pos

def find(mine_board, drawn_board, current_tile_pos): #Get adjacent zeros
    distance_board = []
    completion_board = []
    
    for yy in range(10):
        distance_board.append([])
        completion_board.append([])
        for xx in range(10):
            distance_board[yy].append(9999)
            completion_board[yy].append(False)
    distance_board[ current_tile_pos[1] ][ current_tile_pos[0] ] = 0
    completion_board[ current_tile_pos[1] ][ current_tile_pos[0] ] = True
    drawn_board[ current_tile_pos[1] ][ current_tile_pos[0] ] = '.'
    offset = [ [0,1], [1,0], [-1,0], [0,-1], [-1,-1], [1,-1], [-1,1], [1,1] ]
    z = True
    while z == True:
        for i in range(8):
            x_scan = current_tile_pos[0]+offset[i][0]
            y_scan = current_tile_pos[1]+offset[i][1]
            if y_scan >= 0 and y_scan <= 9 and x_scan >= 0 and x_scan <= 9: # if the scan is not out of the bounds of the board
                if completion_board[y_scan][x_scan] == False: # if the tile has not been scanned alerady
                    if drawn_board[y_scan][x_scan] != _cyan_h+'F'+_col_end: # check that the scanned tile is not flagged 
                        if mine_board[y_scan][x_scan] == 0: # if the scan picks up a tile with 0 adjacent bombs
                            distance_board[y_scan][x_scan] = distance_board[current_tile_pos[1]][current_tile_pos[0]] + 1 #scanned location on the distace board = current location + 1
                            drawn_board[y_scan][x_scan] = '.' #scanned location marked as empty on the board
                        if mine_board[y_scan][x_scan] > 0: # if the scan picks up a number
                            drawn_board[y_scan][x_scan] = num_colors[mine_board[y_scan][x_scan]-1] + str(mine_board[y_scan][x_scan]) + _col_end # reaveal the scanned number  on the drawn board
                        completion_board[y_scan][x_scan] = True # mark as completed
        distance_board[ current_tile_pos[1] ][ current_tile_pos[0] ] = 9999 #once scanning is complete, the tile is marked as distance 9999
        current_tile_pos = get_min(distance_board)
        if current_tile_pos == []:
            z = False
    return drawn_board


def win():
    pass
### game over ###
def game_over(message, cols, lines):
        cls()
        offset = math.floor((cols-10)/2)
        for i in range(offset):
            print(' ', end = '')
        print('Game  Over')
        print('')
        print(message)
        print('')
        input('Enter to play again')
    
play = True

go_ahead = False



x_input = 0
y_input = 1
com_input = 2
confirm_input = 4
end_game_input = 5
mine_input = 6

_yellow = '\033[1;33m'
_cyan = '\033[1;36m'
_green = '\033[1;32m'
_blue = '\033[1;34m'
_red = '\033[1;31m'
_magenta = '\033[1;35m'
_black = '\033[1;30m'
_red_h = '\033[1;41m'
_cyan_h = '\033[1;46m'
_col_end = '\033[0;0m'
num_colors = [_yellow, _cyan, _green, _blue, _red, _magenta, _black]

input_state = com_input
                       
##for yy in range(10): # show mine board at start
##    for xx in range(10):
##        if mine_board[yy][xx] == -1:
##            mine_board[yy][xx] = 'B'
##        if xx < 9:
##            print(mine_board[yy][xx], end = ' ')
##        else:
##            print(mine_board[yy][xx]


### start ###
while play == True:
    flags = mine_amount
    mine_board = []
    drawn_board = []
    for yy in range(10):
        drawn_board.append([])
        mine_board.append([])
        for xx in range(10):
            drawn_board[yy].append('#')
            mine_board[yy].append(0)
            
    for i in range(mine_amount):
        xx = random.randint(0,9)
        yy = random.randint(0,9)
        while mine_board[yy][xx] == -1:
            xx = random.randint(0,9)
            yy = random.randint(0,9)
        mine_board[yy][xx] = -1
    for yy in range(10):
        for xx in range(10):
            if mine_board[yy][xx] == -1: # if tile is a bomb, skip it
                continue
            for axis_y in range(3):
                for axis_x in range(3):
                    if axis_x-1 == 0 and axis_y-1 == 0: # if you are scanning your own tile, skip it
                        continue
                    y_scan = yy+axis_y-1
                    x_scan = xx+axis_x-1
                    if y_scan >= 0 and y_scan <= 9 and x_scan >= 0 and x_scan <= 9:
                        if mine_board[y_scan][x_scan] == -1:
                            mine_board[yy][xx] += 1
                        
    while True:
        cls()
        if input_state != end_game_input:
            message = "Flags left: " + str(flags) #14 chars
##        print('black: \033[1;30m'+'F B . # 1 2 3 4 5 6 7 8'+'\033[0;0m')
##        print('red: \033[1;31m'+'F B . # 1 2 3 4 5 6 7 8'+'\033[0;0m')
##        print('green: \033[1;32m'+'F B . # 1 2 3 4 5 6 7 8'+'\033[0;0m')
##        print('yellow: \033[1;33m'+'F B . # 1 2 3 4 5 6 7 8'+'\033[0;0m')
##        print('blue: \033[1;34m'+'F B . # 1 2 3 4 5 6 7 8'+'\033[0;0m')
##        print('magenta: \033[1;35m'+'F B . # 1 2 3 4 5 6 7 8'+'\033[0;0m')
##        print('cyan: \033[1;36m'+'F B . # 1 2 3 4 5 6 7 8'+'\033[0;0m')
##        print('white: \033[1;37m'+'F B . # 1 2 3 4 5 6 7 8'+'\033[0;0m')
##        print('b black: \033[1;40m'+'F B . # 1 2 3 4 5 6 7 8'+'\033[0;0m')
##        print('b red: \033[1;41m'+'F B . # 1 2 3 4 5 6 7 8'+'\033[0;0m')
##        print('b green: \033[1;42m'+'F B . # 1 2 3 4 5 6 7 8'+'\033[0;0m')
##        print('b yellow: \033[1;43m'+'F B . # 1 2 3 4 5 6 7 8'+'\033[0;0m')
##        print('b blue: \033[1;44m'+'F B . # 1 2 3 4 5 6 7 8'+'\033[0;0m')
##        print('b magenta: \033[1;45m'+'F B . # 1 2 3 4 5 6 7 8'+'\033[0;0m')
##        print('b cyan: \033[1;46m'+'F B . # 1 2 3 4 5 6 7 8'+'\033[0;0m')
##        print('b white: \033[1;47m'+'F B . # 1 2 3 4 5 6 7 8'+'\033[0;0m')
        
        print('')
        print('      0 1 2 3 4 5 6 7 8 9   +----------------+')
        print('                            | '+message, end = '')
        for i in range(14 - len(message)):
            print(' ', end = '')
        print(' |') # 14 chars
        for yy in range(10):
                for xx in range(12):
                    if xx == 0:
                        print('   '+ str(yy), end = '  ')
                    
                    elif xx <= 10:
                        print(drawn_board[yy][xx-1], end = ' ')
                    else:
                        if yy == 0:                          
                            print('  +----------------+', end = '')
                        if yy == 2:                          
                            print('  +----------------+', end = '')
                        if yy == 3:
                            print('  | Commands:      |', end = '')
                        if yy == 4:
                            print('  | R: Reveal tile |', end = '')
                        if yy == 5:
                            print('  | F: Flag tile   |', end = '')       
                        if yy == 6:                          
                            print('  | G: Grid reset  |', end = '')
                        if yy == 7:
                            print('  | N: Mine amount |', end = '')
                        if yy == 8:
                            print('  | Q: Quit game   |', end = '')
                        if yy == 9:
                            print('  +----------------+', end = '')
                        print('')                  
        print('')
        if input_state == com_input:
            com = input('   command: ')
            com = com.lower()
            if com == 'g' or com == 'grid reset' or com == 'reset':
                input_state = com_input
                break
            elif com == 'q' or com == 'quit':
                play = False
                break
            elif com == 'n':
                input_state = mine_input
            else:
                input_state = x_input
                
            continue

        elif input_state == mine_input:
            amount = input('   Amount of mines: ')
            mine_amount = int(amount)
            input_state = com_input
            continue
            
        elif input_state == x_input:
            x = input('   x: ')
            input_state = y_input
            continue
        
        elif input_state == y_input:
            y = input('   y: ')
            input_state = com_input


        elif input_state == confirm_input:
            confirm = input('   Flag selected. Reveal anyway? y/n: ')
            confirm = confirm.lower()
            input_state = com_input
            if confirm == 'y' or confirm == 'yes':
                go_ahead = True
                flags += 1
            else:
                continue
        elif input_state == end_game_input:
            input('   ')
            input_state = com_input
            break
                
        pos = [-1,-1]
        pos[0] = int(x)
        pos[1] = int(y)
        tile = mine_board[ int(pos[1]) ][ int(pos[0]) ]
        if com == 'x' or com == 'r' or com == 'reveal':
            if drawn_board[ int(pos[1]) ][ int(pos[0]) ] != _cyan_h+'F'+_col_end or go_ahead == True: #if tile not a flag
                go_ahead = False
                if tile == -1:
                    for yy in range(10):
                        for xx in range(10):
                            if mine_board[yy][xx] == -1:
                                drawn_board[yy][xx] = _red_h+'B'+_col_end
                    message = 'Game Over :('
                    input_state = end_game_input
                        
                elif tile == 0:
                    drawn_board = find(mine_board, drawn_board, pos)
                    
                else:
                    drawn_board[ int(pos[1]) ][ int(pos[0]) ] = num_colors[tile-1]+str(tile)+_col_end
            else:
                input_state = confirm_input
                go_ahead = False
                
        if com == 'f' or com == 'flag':
            if drawn_board[ pos[1] ][ pos[0] ] == '#':
                drawn_board[ pos[1] ][ pos[0] ] = _cyan_h+'F'+_col_end
                flags -= 1
            else:
                drawn_board[ pos[1] ][ pos[0] ] = '#'
                flags += 1
        if flags == 0:
            win_condition = mine_amount
            for yy in range(10):
                for xx in range(10):
                    if drawn_board[yy][xx] == _cyan_h+'F'+_col_end:
                        if mine_board[yy][xx] == -1:
                            win_condition -= 1
            if win_condition == 0:
                message = 'You Won :)'
                input_state = end_game_input
