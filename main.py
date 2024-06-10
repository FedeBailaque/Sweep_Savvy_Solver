import random


class MinesweeperBoard:
    def __init__(self, row, columns, num_of_mines):
        self.row = row
        self.columns = columns
        self.num_of_mines = num_of_mines
        self.board = []
        self.mine_positions = set()
        self.initialize_board()

    def initialize_board(self):
        # This creates an empty board
        for _ in range(self.row):
            self.board.append(['-'] * self.columns)

        # Places mines and marks them with an 'M'
        mines_placed = 0
        while mines_placed < self.num_of_mines:
            row = random.randint(0, self.row - 1)
            col = random.randint(0, self.columns - 1)
            if (row, col) not in self.mine_positions:
                self.mine_positions.add((row, col))
                self.board[row][col] = 'M'
                mines_placed += 1

        # Uses the function count_adjacent_mines to calculate how many adjacent mines the current square has
        for row in range(self.row):
            for col in range(self.columns):
                if self.board[row][col] != 'M':
                    self.board[row][col] = str(self.count_adjacent_mines(row, col))

    def count_adjacent_mines(self, row, col):
        directions = [
            (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
        ]
        count = 0
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.row and 0 <= c < self.columns:
                if self.board[r][c] == 'M':
                    count += 1
        return count

    def print_board(self):
        for row in self.board:
            print(' '.join(row))


# We execute the program. We can select the number of rows, columns, and mines
if __name__ == "__main__":
    rows = 5
    cols = 5
    num_mines = 5
    board = MinesweeperBoard(rows, cols, num_mines)
    board.print_board()
