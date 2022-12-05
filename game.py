from board import Board, BoardTile


class Game:
    def __init__(self, mine_amount):
        self.flags = mine_amount
        self.board = Board(10, 10, mine_amount)
        self.message = "Flags left: " + str(self.flags)
        self.cursor_pos = [0,0]


    def move_cursor(self, offset: list[int]):
        new_pos = [self.cursor_pos[0] + offset[0], self.cursor_pos[1] + offset[1]]

        def loop_val(val: int, limit: int) -> int:
            if val < 0:
                return limit + val
            if val >= limit:
                return val % limit
            return val

        new_pos[0] = loop_val(new_pos[0], self.board.width)
        new_pos[1] = loop_val(new_pos[1], self.board.width)

        self.cursor_pos = new_pos


    def reveal_tile(self, pos: list[int]):
        tile = self.board.get(pos)
        if tile.is_flagged:
            return

        if tile.val == BoardTile.Val.BOMB:
            self.reveal_bombs()
            self.message = 'Game Over :('
            return
            
        self.reveal(pos)


    def try_toggle_tile_flag(self, pos: list[int]):
        if self.board.get(pos).is_flagged:
            self.board.unflag_tile(pos)
            self.flags += 1
        else:
            is_tile_not_revealed = self.board.get(pos).is_revealed == False
            if self.flags > 0 and is_tile_not_revealed:
                self.board.flag_tile(pos)
                self.flags -= 1


    def reveal_bombs(self):
        for xx in range(self.board.width):
            for yy in range(self.board.height):
                pos = [xx, yy]
                if self.board.get(pos).val == BoardTile.Val.BOMB:
                    self.board.reveal_tile(pos)

    def reveal(self, tile_pos: list[int]):
        self.reveal_rec(tile_pos, [])

    def reveal_rec(self, tile_pos: list[int], searched: list[list[int]]):
        searched.append(tile_pos)
        tile = self.board.get(tile_pos)
        self.board.reveal_tile(tile_pos)
        if tile.val != BoardTile.Val.ZERO:
            return
        
        for adjacent_pos in self.board.get_adjacent_positions(tile_pos):
            if adjacent_pos in searched or self.board.get(adjacent_pos).is_flagged:
                continue

            self.reveal_rec(adjacent_pos, searched)