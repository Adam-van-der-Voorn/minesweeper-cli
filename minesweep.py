# TODO
# implement bomb amounts
# fix bug where there are not enough bombs 
# proper game over state 
# smilies like the o.g


from readchar import readkey, key

from board import BoardTile
from draw import *
from game import Game


def move_terminal_cursor_up(lines: int) -> str:
    return "\033[" + str(lines) + "A"


mine_amount = 15
print("\n" * 11)
### start ###
while True:

    game = Game(mine_amount)

    while True:
        # draw        
        board_string = board_to_string(game.board, game.cursor_pos)
        sidebar = sidebar_string(game.message, 18)
        ui = concat_str_block(board_string, sidebar, 2)
        print(move_terminal_cursor_up(11) + ui, end='')

        # input
        try:    
            input_char = readkey()
            if input_char == key.UP:
                game.move_cursor([0, -1])
            if input_char == key.DOWN:
                game.move_cursor([0, 1])
            if input_char == key.LEFT:
                game.move_cursor([-1, 0])
            if input_char == key.RIGHT:
                game.move_cursor([1, 0])
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
        except KeyboardInterrupt:
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