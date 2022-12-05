from board import Board, BoardTile


def get_min(array):  #get pos of min value from grid                      
    min_val = 9999 
    min_val_pos = []
    for yy in range (10):
        for xx in range(10):
            if array[yy][xx] < min_val:
                min_val_pos = [xx, yy]
                min_val = array[yy][xx]
    return min_val_pos


class Game:
    def __init__(self, mine_amount):
        self.flags = mine_amount
        self.board = Board(10, 10, mine_amount)
        self.message = "Flags left: " + str(self.flags)
        self.cursor_pos = [0,0]


    def set_cursor(self, new_pos: list[int]):
        if self.board.is_in_bounds(new_pos):
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
            if self.flags > 0:
                self.board.flag_tile(pos)
                self.flags -= 1


    def reveal_bombs(self):
        for xx in range(self.board.width):
            for yy in range(self.board.height):
                pos = [xx, yy]
                if self.board.get(pos).val == BoardTile.Val.BOMB:
                    self.board.reveal_tile(pos)


    def reveal(self, tile_pos: list[int]): #Get adjacent zeros
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
        self.board.reveal_tile(tile_pos)
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
                        if self.board.get(scan_pos).is_flagged == False:
                            # the scanned tile is not flagged 
                            if self.board.get([x_scan, y_scan]).val == BoardTile.Val.ZERO:
                                # the scan picked up a tile with 0 adjacent bombs
                                distance_board[y_scan][x_scan] = distance_board[tile_pos[1]][tile_pos[0]] + 1
                                self.board.reveal_tile(scan_pos)
                            if int(self.board.get([x_scan, y_scan]).val) > 0:
                                # if the scan picks up a number
                                # reaveal the scanned number  on the drawn board
                                self.board.reveal_tile(scan_pos)
                            completion_board[y_scan][x_scan] = True
            #once scanning is complete, the tile is marked as distance 9999
            distance_board[ tile_pos[1] ][ tile_pos[0] ] = 9999
            tile_pos = get_min(distance_board)
            if tile_pos == []:
                z = False