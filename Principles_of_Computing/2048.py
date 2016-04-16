"""
Clone of 2048 game.
"""

import poc_2048_gui
import random as r

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    result = list(line)
    head = 0
    i = 1
    while (i < len(result)):
        if (result[i] != 0):
            if (result[head] == result[i]):
                result[head] += result[i]
                result[i] = 0
                head += 1
            elif (result[head] == 0):
                result[head] = result[i]
                result[i] = 0
            else:
                tmp = result[i]
                result[i] = 0
                result[head + 1] = tmp
                head += 1
        i += 1
    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.height = grid_height
        self.width = grid_width
        self.init_tiles = {}
        self.init_tiles[UP] = []
        self.init_tiles[DOWN] = []
        self.init_tiles[LEFT] = []
        self.init_tiles[RIGHT] = []
        for i in range(grid_width):
            self.init_tiles[UP].append((0, i))
            self.init_tiles[DOWN].append((grid_height - 1, i))
        for i in range(grid_height):
            self.init_tiles[LEFT].append((i, 0))
            self.init_tiles[RIGHT].append((i, grid_width - 1))
        self.reset()

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.grid[row][col]
        
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.width
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.grid = []
        i = 0
        while (i < self.get_grid_height()):
            j = 0
            tmprow = []
            while (j < self.get_grid_width()):
                tmprow.append(0)
                j += 1
            self.grid.append(tmprow)
            i += 1
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self.get_grid_height()) + "*" + str(self.get_grid_width()) + " game."
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        has_move = False
        if ((direction == UP) or (direction == DOWN)):
            limit = self.get_grid_height()
        else:
            limit = self.get_grid_width()
        for i in self.init_tiles[direction]:
            temp = []
            for j in range(limit):
                temp.append(self.get_tile(i[0] + j * OFFSETS[direction][0], i[1] + j * OFFSETS[direction][1]))
            merged = merge(temp)
            if (temp != merged):
                has_move = True
                for j in range(limit):
                    self.set_tile(i[0] + j * OFFSETS[direction][0], i[1] + j * OFFSETS[direction][1], merged[j])
        if (has_move):
            self.new_tile()
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        empty_tile_pos = []
        for i in range(self.get_grid_height()):
            for j in range(self.get_grid_width()):
                if (self.get_tile(i, j) == 0):
                    empty_tile_pos.append([i, j])
        if (len(empty_tile_pos) == 0):
            self.reset()
        else:
            new_pos = r.choice(empty_tile_pos)
            two_or_four = r.randrange(0, 100)
            if (two_or_four <= 9):
                self.set_tile(new_pos[0], new_pos[1], 4)
            else:
                self.set_tile(new_pos[0], new_pos[1], 2)
 
    
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))