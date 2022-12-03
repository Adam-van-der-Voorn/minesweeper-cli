import os
import random
import math
from os import system

from board import Board, BoardTile

system("title "+'Minesweeper')


cols = 30 + 19
lines = 16
mine_amount = 15

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

def find(mine_board: Board, drawn_board, current_tile_pos): #Get adjacent zeros
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
            if y_scan >= 0 and y_scan <= 9 and x_scan >= 0 and x_scan <= 9:
                # the scan is not out of the bounds of the board
                if completion_board[y_scan][x_scan] == False:
                    # the tile has not been scanned alerady
                    if drawn_board[y_scan][x_scan] != _cyan_h+'F'+_col_end:
                        # the scanned tile is not flagged 
                        if mine_board.get([x_scan, y_scan]).val == BoardTile.Val.ZERO:
                            # the scan picked up a tile with 0 adjacent bombs
                            distance_board[y_scan][x_scan] = distance_board[current_tile_pos[1]][current_tile_pos[0]] + 1
                            drawn_board[y_scan][x_scan] = '.'
                        if int(mine_board.get([x_scan, y_scan]).val) > 0:
                            # if the scan picks up a number
                            # reaveal the scanned number  on the drawn board
                            drawn_board[y_scan][x_scan] = num_colors[int(mine_board.get([x_scan, y_scan]).val)-1] + str(int(mine_board.get([x_scan, y_scan]).val)) + _col_end
                        completion_board[y_scan][x_scan] = True
        #once scanning is complete, the tile is marked as distance 9999
        distance_board[ current_tile_pos[1] ][ current_tile_pos[0] ] = 9999
        current_tile_pos = get_min(distance_board)
        if current_tile_pos == []:
            z = False
    return drawn_board


### game over ###
def game_over(message, cols):
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
command_input = 2
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

input_state = command_input

def board_to_string(board: Board) -> str:
    token_map = {
        BoardTile.Val.ZERO: ".",
        BoardTile.Val.ONE: _yellow + "1" + _col_end,
        BoardTile.Val.TWO: _cyan + "2" + _col_end,
        BoardTile.Val.THREE: _green + "3" + _col_end,
        BoardTile.Val.FOUR:_blue + "4" + _col_end,
        BoardTile.Val.FIVE: _red + "5" + _col_end,
        BoardTile.Val.SIX: _magenta + "6" + _col_end,
        BoardTile.Val.SEVEN: _magenta + "7" + _col_end,
        BoardTile.Val.EIGHT: _magenta + "8" + _col_end,
        BoardTile.Val.NINE: _magenta + "9" + _col_end,
        BoardTile.Val.BOMB: _red_h + "B" + _col_end,
    }

    def get_token(tile: BoardTile):
        if tile.is_revealed == False:
            return "#"

        token = token_map.get(tile.val)
        if (token == None):
            token = _red_h + "ERR" + _col_end
        return token

    str = ""
    for yy in range(board.height):
        for xx in range(board.width):
            tile = board.get([xx, yy])
            str += get_token(tile) + " "
        str.strip()
        str += "\n"
    return str

def ui_to_string(message: str, width: int) -> str:
    BUFFER_SIZE_HORI = 4
    width = max(BUFFER_SIZE_HORI, width)
    TEXT_MAX_WIDTH = width - BUFFER_SIZE_HORI

    FRAME_HORI = "+-" + ("-" * TEXT_MAX_WIDTH) + "-+\n"

    def frame_with_text(txt):
        txt = txt[:TEXT_MAX_WIDTH]
        right_padding = " " * (TEXT_MAX_WIDTH - len(txt))
        return "| " + txt + right_padding + " |\n"

    str = FRAME_HORI
    str += frame_with_text(message)
    str += FRAME_HORI
    str += frame_with_text("Commands:")
    str += frame_with_text("R: Reveal tile")
    str += frame_with_text("F: Flag tile")       
    str += frame_with_text("G: Grid reset")
    str += frame_with_text("N: Mine amount")
    str += frame_with_text("Q: Quit game")
    str += FRAME_HORI
    return str


### start ###
while play == True:
    flags = mine_amount
    board = Board(10, 10, mine_amount)
    drawn_board = []
    for yy in range(10):
        drawn_board.append([])
        for xx in range(10):
            drawn_board[yy].append('#')
                        
    while True:
        # draw
        cls()
        if input_state != end_game_input:
            message = "Flags left: " + str(flags) #14 chars
        
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

        # input
        if input_state == command_input:
            com = input('   command: ')
            com = com.lower()
            if com == 'g' or com == 'grid reset' or com == 'reset':
                input_state = command_input
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
            input_state = command_input
            continue
            
        elif input_state == x_input:
            x = input('   x: ')
            input_state = y_input
            continue
        
        elif input_state == y_input:
            y = input('   y: ')
            input_state = command_input


        elif input_state == confirm_input:
            confirm = input('   Flag selected. Reveal anyway? y/n: ')
            confirm = confirm.lower()
            input_state = command_input
            if confirm == 'y' or confirm == 'yes':
                go_ahead = True
                flags += 1
            else:
                continue
        elif input_state == end_game_input:
            input('   ')
            input_state = command_input
            break
                
        pos = [-1,-1]
        pos[0] = int(x)
        pos[1] = int(y)
        tile = board.get(pos)
        if com == 'x' or com == 'r' or com == 'reveal':
            if drawn_board[ int(pos[1]) ][ int(pos[0]) ] != _cyan_h+'F'+_col_end or go_ahead == True: #if tile not a flag
                go_ahead = False
                if tile.val == BoardTile.Val.BOMB:
                    for yy in range(10):
                        for xx in range(10):
                            if board.get([xx, yy]).val == BoardTile.Val.BOMB:
                                drawn_board[yy][xx] = _red_h+'B'+_col_end
                    message = 'Game Over :('
                    input_state = end_game_input
                        
                elif tile.val == BoardTile.Val.ZERO:
                    drawn_board = find(board, drawn_board, pos)
                    
                else:
                    drawn_board[ int(pos[1]) ][ int(pos[0]) ] = num_colors[int(tile.val)-1]+str(int(tile.val))+_col_end
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
                        if board.get([xx, yy]).val == BoardTile.Val.BOMB:
                            win_condition -= 1
            if win_condition == 0:
                message = 'You Won :)'
                input_state = end_game_input
