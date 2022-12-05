# TODO
# cursor:
## Green # when on unrevealed
## green background F when on flag
## red X when on revealed tile
## make it loop around
# implement bomb amounts
# change flag color to red?
# try to prevent flickering... dont wanna just buffer terminal though. Maybe raw mode??


import os

from readchar import readkey, key

from board import BoardTile
from draw import *
from game import Game


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


mine_amount = 15

### start ###
while True:

    game = Game(mine_amount)

    while True:
        # draw
        cls()
        board_string = board_to_string(game.board, game.cursor_pos)
        sidebar = sidebar_string(game.message, 18)
        ui = concat_str_block(board_string, sidebar, 2)
        print(ui, end='')

        # input
        input_char = readkey()
        if input_char == key.UP:
            game.set_cursor([game.cursor_pos[0], game.cursor_pos[1] - 1])
        if input_char == key.DOWN:
            game.set_cursor([game.cursor_pos[0], game.cursor_pos[1] + 1])
        if input_char == key.LEFT:
            game.set_cursor([game.cursor_pos[0] - 1, game.cursor_pos[1]])
        if input_char == key.RIGHT:
            game.set_cursor([game.cursor_pos[0] + 1, game.cursor_pos[1]])
        if input_char.lower() == "r":
            game.reveal_tile(game.cursor_pos)
        if input_char.lower() == "f":
            game.try_toggle_tile_flag(game.cursor_pos)
            game.message = "Flags left: " + str(game.flags)
        if input_char.lower() == "g":
            break
        if input_char.lower() == "n":
            raise RuntimeError("mine amount not implemented")
        if input_char.lower() == "q":
            exit()
                
        # check for winner
        if game.flags == 0:
            win_condition = mine_amount
            for yy in range(10):
                for xx in range(10):
                    tile = game.board.get([xx, yy])
                    if tile.is_flagged and tile.val == BoardTile.Val.BOMB:
                        win_condition -= 1
            if win_condition == 0:
                game.message = 'You Won :)'