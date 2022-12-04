import os
from os import system

from board import Board, BoardTile
from draw import *

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

def reveal(mine_board: Board, tile_pos: list[int]): #Get adjacent zeros
    distance_board = []
    completion_board = []
    
    for yy in range(10):
        distance_board.append([])
        completion_board.append([])
        for xx in range(10):
            distance_board[yy].append(9999)
            completion_board[yy].append(False)
    distance_board[ tile_pos[1] ][ tile_pos[0] ] = 0
    completion_board[ tile_pos[1] ][ tile_pos[0] ] = True
    mine_board.reveal_tile(tile_pos)
    offset = [ [0,1], [1,0], [-1,0], [0,-1], [-1,-1], [1,-1], [-1,1], [1,1] ]
    z = True
    while z == True:
        for i in range(8):
            x_scan = tile_pos[0]+offset[i][0]
            y_scan = tile_pos[1]+offset[i][1]
            scan_pos = [x_scan, y_scan]
            if y_scan >= 0 and y_scan <= 9 and x_scan >= 0 and x_scan <= 9:
                # the scan is not out of the bounds of the board
                if completion_board[y_scan][x_scan] == False:
                    # the tile has not been scanned alerady
                    if mine_board.get(scan_pos).is_flagged == False:
                        # the scanned tile is not flagged 
                        if mine_board.get([x_scan, y_scan]).val == BoardTile.Val.ZERO:
                            # the scan picked up a tile with 0 adjacent bombs
                            distance_board[y_scan][x_scan] = distance_board[tile_pos[1]][tile_pos[0]] + 1
                            mine_board.reveal_tile(scan_pos)
                        if int(mine_board.get([x_scan, y_scan]).val) > 0:
                            # if the scan picks up a number
                            # reaveal the scanned number  on the drawn board
                            mine_board.reveal_tile(scan_pos)
                        completion_board[y_scan][x_scan] = True
        #once scanning is complete, the tile is marked as distance 9999
        distance_board[ tile_pos[1] ][ tile_pos[0] ] = 9999
        tile_pos = get_min(distance_board)
        if tile_pos == []:
            z = False


def reveal_bombs(board: Board):
    for xx in range(board.width):
        for yy in range(board.height):
            pos = [xx, yy]
            if board.get(pos).val == BoardTile.Val.BOMB:
                board.reveal_tile(pos)


play = True

go_ahead = False

x_input = 0
y_input = 1
command_input = 2
confirm_input = 4
end_game_input = 5
mine_input = 6

input_state = command_input

### start ###
while play == True:
    flags = mine_amount
    board = Board(10, 10, mine_amount)
    message = "Flags left: " + str(flags)

    while True:
        # draw
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
            if board.get(pos).is_flagged == False:
                go_ahead = False
                if tile.val == BoardTile.Val.BOMB:
                    reveal_bombs(board)
                    message = 'Game Over :('
                    input_state = end_game_input
                        
                elif tile.val == BoardTile.Val.ZERO:
                    reveal(board, pos)
                    
                else:
                    board.reveal_tile(pos)
            else:
                input_state = confirm_input
                go_ahead = False
                
        if com == 'f' or com == 'flag':
            if board.get(pos).is_revealed == False:
                board.flag_tile(pos)
                flags -= 1
            else:
                board.unflag_tile(pos)
                flags += 1
        if flags == 0:
            win_condition = mine_amount
            for yy in range(10):
                for xx in range(10):
                    if board.get([xx, yy]).is_flagged:
                        if board.get([xx, yy]).val == BoardTile.Val.BOMB:
                            win_condition -= 1
            if win_condition == 0:
                message = 'You Won :)'
                input_state = end_game_input
