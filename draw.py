from enum import Enum
import re
from board import Board, BoardTile

class Color(Enum):
    GRAY = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36


def colored_text(text: str, color: Color, highlight: bool = False) -> str:
    col_end = '\033[0;0m'
    color_num = color.value
    if (highlight):
        color_num += 10
    return "\033[1;" + str(color_num) + "m" + text + col_end


def board_to_string(board: Board, cursor_pos: list[int]) -> str:
    token_map = {
        BoardTile.Val.ZERO: ".",
        BoardTile.Val.ONE: colored_text("1", Color.YELLOW),
        BoardTile.Val.TWO: colored_text("2", Color.CYAN),
        BoardTile.Val.THREE: colored_text("3", Color.GREEN),
        BoardTile.Val.FOUR:colored_text("4", Color.BLUE),
        BoardTile.Val.FIVE: colored_text("5", Color.RED),
        BoardTile.Val.SIX: colored_text("6", Color.MAGENTA),
        BoardTile.Val.SEVEN: colored_text("7", Color.MAGENTA),
        BoardTile.Val.EIGHT: colored_text("8", Color.MAGENTA),
        BoardTile.Val.NINE: colored_text("9", Color.MAGENTA),
        BoardTile.Val.BOMB: colored_text("B", Color.RED, True),
    }

    def get_token_from_map(val: BoardTile.Val):
        token = token_map[val]
        if (token == None):
            token = colored_text("ERR", Color.RED, True)
        return token

    def get_cursor_token(tile: BoardTile):
        if tile.is_flagged:
            return colored_text("F", Color.RED, True)

        if tile.is_revealed == False:
            return colored_text("#", Color.RED, True)

        if tile.val == BoardTile.Val.ZERO:
            return colored_text(".", Color.RED, True)

        return colored_text(str(tile.val.value), Color.RED, True)

    def get_token(tile: BoardTile):
        if tile.is_revealed and tile.val == BoardTile.Val.BOMB:
            return get_token_from_map(tile.val)

        if tile.is_flagged == True:
            return colored_text("F", Color.MAGENTA, False)

        if tile.is_revealed == False:
            return "#"

        return get_token_from_map(tile.val)

    string = ""
    for yy in range(board.height):
        for xx in range(board.width):
            tile = board.get([xx, yy])
            if [xx, yy] == cursor_pos:
                string += get_cursor_token(tile) + " "
            else:
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