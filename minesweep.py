import os
import random
import re
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
    mine_board.reveal_tile(current_tile_pos)
    offset = [ [0,1], [1,0], [-1,0], [0,-1], [-1,-1], [1,-1], [-1,1], [1,1] ]
    z = True
    while z == True:
        for i in range(8):
            x_scan = current_tile_pos[0]+offset[i][0]
            y_scan = current_tile_pos[1]+offset[i][1]
            scan_pos = [x_scan, y_scan]
            if y_scan >= 0 and y_scan <= 9 and x_scan >= 0 and x_scan <= 9:
                # the scan is not out of the bounds of the board
                if completion_board[y_scan][x_scan] == False:
                    # the tile has not been scanned alerady
                    if mine_board.get(scan_pos).is_flagged == False:
                        # the scanned tile is not flagged 
                        if mine_board.get([x_scan, y_scan]).val == BoardTile.Val.ZERO:
                            # the scan picked up a tile with 0 adjacent bombs
                            distance_board[y_scan][x_scan] = distance_board[current_tile_pos[1]][current_tile_pos[0]] + 1
                            mine_board.reveal_tile(scan_pos)
                            drawn_board[y_scan][x_scan] = '.'
                        if int(mine_board.get([x_scan, y_scan]).val) > 0:
                            # if the scan picks up a number
                            # reaveal the scanned number  on the drawn board
                            mine_board.reveal_tile(scan_pos)
                            drawn_board[y_scan][x_scan] = num_colors[int(mine_board.get([x_scan, y_scan]).val)-1] + str(int(mine_board.get([x_scan, y_scan]).val)) + _col_end
                        completion_board[y_scan][x_scan] = True
        #once scanning is complete, the tile is marked as distance 9999
        distance_board[ current_tile_pos[1] ][ current_tile_pos[0] ] = 9999
        current_tile_pos = get_min(distance_board)
        if current_tile_pos == []:
            z = False
    return drawn_board


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
        if tile.is_revealed and tile.val == BoardTile.Val.BOMB:
            token = token_map.get(tile.val)
            if (token == None):
                token = _red_h + "ERR" + _col_end
            return token

        if tile.is_flagged == True:
            return _cyan_h + "F" + _col_end

        if tile.is_revealed == False:
            return "#"

        token = token_map.get(tile.val)
        if (token == None):
            token = _red_h + "ERR" + _col_end
        return token

    string = ""
    for yy in range(board.height):
        for xx in range(board.width):
            tile = board.get([xx, yy])
            string += get_token(tile) + " "
        string.strip()
        string += "\n"
    return string

def str_with_len(string: str, intended_length: int):
    if string == None:
        string = ""
    
    true_length = len_no_color(string)
    if true_length > intended_length:
        overflow = true_length - intended_length
        string = string[:-overflow]
        true_length = len_no_color(string)

    right_padding = " " * (intended_length - true_length)
    return string + right_padding

def sidebar_string(message: str, width: int) -> str:
    BUFFER_SIZE_HORI = 4
    width = max(BUFFER_SIZE_HORI, width)
    TEXT_MAX_WIDTH = width - BUFFER_SIZE_HORI

    FRAME_HORI = "+-" + ("-" * TEXT_MAX_WIDTH) + "-+\n"
    str = FRAME_HORI
    str += "| " + str_with_len(message, TEXT_MAX_WIDTH) + " |\n"
    str += FRAME_HORI
    str += "| " + str_with_len("Commands:", TEXT_MAX_WIDTH) + " |\n"
    str += "| " + str_with_len("R: Reveal tile", TEXT_MAX_WIDTH) + " |\n"
    str += "| " + str_with_len("F: Flag tile", TEXT_MAX_WIDTH) + " |\n"
    str += "| " + str_with_len("G: Grid reset", TEXT_MAX_WIDTH) + " |\n"
    str += "| " + str_with_len("N: Mine amount", TEXT_MAX_WIDTH) + " |\n"
    str += "| " + str_with_len("Q: Quit game", TEXT_MAX_WIDTH) + " |\n"
    str += FRAME_HORI
    return str

def len_no_color(string: str) -> int:
    str_no_color = re.sub(r"\x1b.*?m(?P<colored_text>.*?)\x1b\[0;0m", r"\g<colored_text>", string, flags=re.IGNORECASE)
    return len(str_no_color)


def concat_str_block(s_left: str, s_right: str, offset: int) -> str:
    left_lines = s_left.split("\n")
    right_lines = s_right.split("\n")

    left_line_lengths = [len_no_color(i) for i in left_lines]
    longest_left_line: int = max(left_line_lengths)

    concat_str = ""
    for i in range(max(len(right_lines), len(left_lines))):
        if i < len(left_lines):
            concat_str += str_with_len(left_lines[i], longest_left_line)
        else:
            concat_str += " " * longest_left_line

        if i < len(right_lines):
            concat_str += " " * offset
            concat_str += right_lines[i]

        concat_str += "\n"
    return concat_str

def reveal_bombs(board: Board):
    for xx in range(board.width):
        for yy in range(board.height):
            pos = [xx, yy]
            if board.get(pos).val == BoardTile.Val.BOMB:
                board.reveal_tile(pos)


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
        if input_state != end_game_input:
            message = "Flags left: " + str(flags) #14 chars

        cls()
        board_string = board_to_string(board)
        sidebar = sidebar_string(message, 18)
        ui = concat_str_block(board_string, sidebar, 2)
        print(ui)
        

        # input
        if input_state == command_input:
            com = input('command: ')
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
            amount = input('Amount of mines: ')
            mine_amount = int(amount)
            input_state = command_input
            continue
            
        elif input_state == x_input:
            x = input('x: ')
            input_state = y_input
            continue
        
        elif input_state == y_input:
            y = input('y: ')
            input_state = command_input


        elif input_state == confirm_input:
            confirm = input('Flag selected. Reveal anyway? y/n: ')
            confirm = confirm.lower()
            input_state = command_input
            if confirm == 'y' or confirm == 'yes':
                go_ahead = True
                flags += 1
            else:
                continue
        elif input_state == end_game_input:
            input()
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
                    reveal_bombs(board)
                    message = 'Game Over :('
                    input_state = end_game_input
                        
                elif tile.val == BoardTile.Val.ZERO:
                    drawn_board = find(board, drawn_board, pos)
                    
                else:
                    drawn_board[ int(pos[1]) ][ int(pos[0]) ] = num_colors[int(tile.val)-1]+str(int(tile.val))+_col_end
                    board.reveal_tile(pos)
            else:
                input_state = confirm_input
                go_ahead = False
                
        if com == 'f' or com == 'flag':
            if drawn_board[ pos[1] ][ pos[0] ] == '#':
                drawn_board[ pos[1] ][ pos[0] ] = _cyan_h+'F'+_col_end
                board.flag_tile(pos)
                flags -= 1
            else:
                drawn_board[ pos[1] ][ pos[0] ] = '#'
                board.unflag_tile(pos)
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
