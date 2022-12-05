import re
from board import Board, BoardTile

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

def board_to_string(board: Board, cursor_pos: list[int]) -> str:
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
            if [xx, yy] == cursor_pos:
                string += "0 "
            else:
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