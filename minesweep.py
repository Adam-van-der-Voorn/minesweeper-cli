# TODO
# smilies like the o.g


from readchar import readkey, key
from draw import *
from game import Game


def move_terminal_cursor_up(lines: int) -> str:
    return "\033[" + str(lines) + "A"

def input_int(prompt: str, len_limit: int) -> int | None:
    print(prompt, end="", flush=True)
    max_line_len = len(prompt) + len_limit
    clear_line = "\r" + (" " * max_line_len) + "\r"

    result = ""
    while True:
        inp = readkey()

        if inp == key.ENTER and len(result) > 0:
            print(clear_line, end="", flush=True)
            return int(result)

        if inp == "q" or (inp == key.BACKSPACE and len(result) == 0):
            print(clear_line, end="", flush=True)
            return None

        if inp == key.BACKSPACE and len(result) > 0:
            print("\b ", end="\033[1D", flush=True) 
            result = result[:-1]

        if len(result) < len_limit:
            try: 
                # check cast to int
                int(inp)
                print(inp, end="", flush=True) 
                result += inp
            except:
                pass


mine_amount = 15
board_width = 10
board_height = 10
draw_height = board_height + 1


# set cursor position
print("\n" * draw_height, end='')

### start ###
while True:

    game = Game(board_width, board_height, mine_amount)

    while True:
        # draw
        board_string = board_to_string(game.board, game.cursor_pos)
        sidebar = sidebar_string(game.message, 18)
        ui = concat_str_block(board_string, sidebar, 2)
        print(move_terminal_cursor_up(draw_height) + ui, end='')

        # input
        try:    
            input_char = readkey()
            if game.cursor_pos != None:
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
            if input_char.lower() == "x":
                break
            if input_char.lower() == "m":
                new_mine_amount = input_int("Set mine amount (next round): ", 2)
                if new_mine_amount != None:
                    mine_amount = new_mine_amount
            if input_char.lower() == "q":
                exit()
        except KeyboardInterrupt:
            exit()