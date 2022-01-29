"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui
import random

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        
        tiles = range(self._height * self._width)
        random.shuffle(tiles)   
        self._grid = []
        tile_idx = 0


        for row in range(self._height):
            self._grid.append([])
            for col in range(self._width):
                self._grid[row].append(tiles[tile_idx])
                tile_idx += 1        

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def next_tile(self, row, col, width):
        """
        Given the position of a tile, returns position of next tile
        if one moves through grid from left to right and up to down
        """
        row += (col + 1) // width
        col = (col + 1) % width
        return (row, col)
    
    def position_tile(self, current_row, current_col, target_row, target_col):
        """
        Place certain tile at target position
        Tile must be above target position
        Returns a move string
        """
        
        move_string = ""
        
        if current_row != target_row - 1 or current_col != target_col:
            
            move_string += "u" * (target_row - current_row)
                            
            if current_col < target_col:
                move_string += "l" * (target_col - current_col - 1)
                if current_row == 0:
                    while current_col < target_col - 1:
                        move_string += "ldrru"
                        current_col += 1
                else:
                    while current_col < target_col - 1:
                        move_string += "lurrd"
                        current_col += 1
                move_string +=  "ldr"

            elif current_col > target_col:
                move_string += "r" * (current_col - target_col - 1)
                if current_row == 0:
                    while current_col > target_col:
                        move_string += "rdllu"
                        current_col -= 1
                else:
                    while current_col > target_col:
                        move_string += "rulld"
                        current_col -= 1
                move_string += "dr"
                
            else:
                move_string += "d"

            while current_row < target_row - 1:
                move_string += "ulddr"
                current_row += 1                

        return move_string

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self._grid[target_row][target_col] != 0:
            return False
        
        next_tile_row, next_tile_col = self.next_tile(target_row, target_col, self._width)[0], self.next_tile(target_row, target_col, self._width)[1] 

        while next_tile_col < self._width and next_tile_row < self._height:
            if self.current_position(next_tile_row, next_tile_col) != (next_tile_row, next_tile_col):
                return False
            next_tile_row, next_tile_col = self.next_tile(next_tile_row, next_tile_col, self._width)[0], self.next_tile(next_tile_row, next_tile_col, self._width)[1] 

        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        
        assert self.lower_row_invariant(target_row, target_col), "lower row invariant does not hold" + str(target_row) + str(target_col)
        
        move_string = ""
        current_row, current_col = self.current_position(target_row, target_col)
        
        if current_row != target_row:
            move_string += self.position_tile(current_row, current_col, target_row, target_col)     
            move_string += "uld"    
        else:
            move_string += "l" * (target_col - current_col)
            current_col += 1
            while current_col < target_col:
                move_string += "urrdl"
                current_col += 1 
                
        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row, target_col - 1), "incorrect string returned"
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        move_string = "ur"
        current_row, current_col = self.current_position(target_row, 0)
        assert self.lower_row_invariant(target_row, 0), "lower row invariant does not hold"
                
        if (current_row, current_col) == (target_row - 1, 0):
            move_string += "r" * (self._width - 2)
            
        else:
            
            if current_row == target_row - 1 and current_col == 1:
                move_string += "l"
                
            elif current_row < target_row - 1:
                move_string += self.position_tile(current_row, current_col, target_row - 1, 1)
                move_string += "uld"
                
            elif current_row == target_row - 1 and current_col > 1:
                move_string += "r" * (current_col - 2)
                while current_col > 1:
                    move_string += "rulld"
                    current_col -= 1
            
            move_string += "ruldrdlurdluurddlu"
            move_string += "r" * (self._width - 1)
            
        self.update_puzzle(move_string)
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[0][target_col] != 0:
            return False
        
        for row in range(2, self._height):
            for col in range(self._width):
                if self.current_position(row, col) != (row, col):
                    return False
        
        # check for row 0
        for col in range(target_col + 1, self._width):
            if self.current_position(0, col) != (0, col):
                    return False
                
        # check for row 1
        for col in range(target_col, self._width):
            if self.current_position(1, col) != (1, col):
                    return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[1][target_col] != 0:
            return False
        
        for row in range(2, self._height):
            for col in range(self._width):
                if self.current_position(row, col) != (row, col):
                    return False
                
        # check for row 0
        for col in range(target_col + 1, self._width):
            if self.current_position(0, col) != (0, col):
                    return False
                
        # check for row 1
        for col in range(target_col + 1, self._width):
            if self.current_position(1, col) != (1, col):
                    return False
        return True
        
    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        move_string = "ld"
        current_row, current_col = self.current_position(0, target_col)
        
        assert self.row0_invariant(target_col), "row 0 invariant does not hold"
                
        if (current_row, current_col) == (0, target_col - 1):
            self.update_puzzle(move_string)
            return move_string
        
        else:
            if current_row == 1 and current_col == target_col - 1:
                move_string += "uld"
                
            if current_row != 1:
                move_string += self.position_tile(current_row, current_col, 1, target_col - 1)     
                move_string += "uld" 
                
            else:
                move_string += "l" * (target_col - 1 - current_col)
                current_col += 1
                while current_col < target_col - 1:
                    move_string += "urrdl"
                    current_col += 1
                    
        move_string += "urdlurrdluldrruld"
        self.update_puzzle(move_string)
        assert self.row1_invariant(target_col - 1), "incorrect string returned"
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col), "row 1 invariant does not hold"
        
        move_string = ""
        current_row, current_col = self.current_position(1, target_col)
        
        if current_row != 1:
            move_string += self.position_tile(current_row, current_col, 1, target_col)     
            move_string += "u"    
        else:
            move_string += "l" * (target_col - current_col)
            current_col += 1
            while current_col < target_col:
                move_string += "urrdl"
                current_col += 1
            move_string += "ur"
                
        self.update_puzzle(move_string)
                 
        assert self.row0_invariant(target_col), "incorrect string returned"
        
        return move_string
    ###########################################################
    # Phase 3 methods

    def solved(self):
        """
        Check whether the upper left 2x2 part of the puzzle
        has been solved
        """
        for row in range(2):
            for col in range(2):
                
                if self.current_position(row, col) != (row, col):
                    return False
        return True
                
    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        move_string = "lu"
        new_puzzle = self.clone()
        new_puzzle.update_puzzle(move_string)
        
                    
        while not new_puzzle.solved():
            move_string += "rdlu"
            new_puzzle.update_puzzle("rdlu")
            
        self.update_puzzle(move_string)
            
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ""
        
        move_string += "d" * (self._height - self.current_position(0, 0)[0] - 1)
        move_string += "r" * (self._width - self.current_position(0, 0)[1] - 1)
        
        self.update_puzzle(move_string)
        
        for row in range(self._height - 1, 1, -1):
            for col in range(self._width - 1, -1, -1):
                if col != 0:
                    move_string += self.solve_interior_tile(row, col)
                    
                else:
                    move_string += self.solve_col0_tile(row)
                    
        for col in range(self._width - 1, 1, -1):
            for row in range(1, -1, -1):
                if row == 0:
                    move_string += self.solve_row0_tile(col)
                    
                else:
                    move_string += self.solve_row1_tile(col)
                    
        move_string += self.solve_2x2()      
            
        return move_string

# Start interactive simulation
puzzle = Puzzle(4, 4)
poc_fifteen_gui.FifteenGUI(puzzle)
