import random
from enum import Enum

class BoardTile:
    class Val(Enum):
        BOMB = -1,
        ZERO = 0, 
        ONE = 1, 
        TWO = 2, 
        THREE = 3, 
        FOUR = 4, 
        FIVE = 5, 
        SIX = 6, 
        SEVEN = 7, 
        EIGHT = 8, 
        NINE = 9

        def __new__(cls, value: int):
            member = object.__new__(cls)
            member._value_ = value
            return member

        def __int__(self):
            return self.value

        def inc(self):
            return BoardTile.Val(self.value + 1)

    def __init__(self, val: Val):
        self.val = val
        self.is_revealed = False
        self.is_flagged = False


class Board:
    def __init__(self, width: int, height: int, num_mines: int):
        self.board = []
        self.width = width
        self.height = height

        # init arr
        for yy in range(height):
            self.board.append([])
            for xx in range(width):
                self.board[yy].append(BoardTile(BoardTile.Val.ZERO))
        
        # place the mines
        possibilities = [*range(self.width * self.height)]
        random.shuffle(possibilities)
        for _ in range(num_mines):
            possibility = possibilities.pop()
            pos_x = possibility % self.width
            pos_y = possibility // self.width
            self.reset_tile([pos_x, pos_y], BoardTile.Val.BOMB)

        # set up the numbers on the board
        for yy in range(height):
            for xx in range(width):
                pos = [xx, yy]

                # if tile is a bomb, skip it
                if self.get(pos).val == BoardTile.Val.BOMB: 
                    continue
                
                for adjacent_pos in self.get_adjacent_positions(pos):
                    if self.get(adjacent_pos).val == BoardTile.Val.BOMB:
                        self.reset_tile(pos, self.get(pos).val.inc())


    def get_adjacent_positions(self, pos: list[int]) -> list[list[int]]:
        offsets = [ [0,1], [1,0], [-1,0], [0,-1], [-1,-1], [1,-1], [-1,1], [1,1] ]
        adjacent_positions = []
        for offset in offsets:
            adjacent_pos = [pos[0] + offset[0], pos[1] + offset[1]]
            if self.is_in_bounds(adjacent_pos):
                adjacent_positions.append(adjacent_pos)
        return adjacent_positions


    def is_in_bounds(self, pos: list[int]):
        return pos[0] >= 0 and pos[0] < self.width and pos[1] >= 0 and pos[1] < self.height

    def get(self, pos: list[int]) -> BoardTile:
        return self.board[pos[0]][pos[1]]

    def reset_tile(self, pos: list[int], val: BoardTile.Val):
        self.board[pos[0]][pos[1]] = BoardTile(val)

    def reveal_tile(self, pos: list[int]):
        self.board[pos[0]][pos[1]].is_revealed = True

    def flag_tile(self, pos: list[int]):
        self.board[pos[0]][pos[1]].is_flagged = True

    def unflag_tile(self, pos: list[int]):
        self.board[pos[0]][pos[1]].is_flagged = False



