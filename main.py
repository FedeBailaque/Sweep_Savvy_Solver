import random


class MinesweeperBoard:
    def __init__(self, rows, columns, num_of_mines):
        self.rows = rows
        self.columns = columns
        self.num_of_mines = num_of_mines
        self.board = []
        self.visible_board = []
        self.mine_positions = set()
        self.initialize_board()
        self.game_end = False

    def initialize_board(self):
        # This creates an empty board
        for _ in range(self.rows):
            self.board.append(['-'] * self.columns)

        # Places mines and marks them with an 'M'
        mines_placed = 0
        while mines_placed < self.num_of_mines:
            rows = random.randint(0, self.rows - 1)
            col = random.randint(0, self.columns - 1)
            if (rows, col) not in self.mine_positions:
                self.mine_positions.add((rows, col))
                self.board[rows][col] = 'M'
                mines_placed += 1

        # Uses the function count_adjacent_mines to calculate how many adjacent mines the current square has
        for rows in range(self.rows):
            for col in range(self.columns):
                if self.board[rows][col] != 'M':
                    self.board[rows][col] = str(self.count_adjacent_mines(rows, col))

        # This creates the visible board
        for _ in range(self.rows):
            self.visible_board.append(['#'] * self.columns)

    def count_adjacent_mines(self, rows, col):
        directions = [
            (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
        ]
        count = 0
        for dr, dc in directions:
            r = rows + dr
            c = col + dc
            if 0 <= r < self.rows and 0 <= c < self.columns:
                if self.board[r][c] == 'M':
                    count += 1
        return count

    def reveal_cell(self, row, col):
        if self.board[row][col] == 'M':
            self.game_end = True
            self.visible_board[row][col] = 'M'
            print("\nYou've hit a mine!")
        else:
            self.visible_board[row][col] = str(self.board[row][col])
        # This is optional and only if we reach improvements stage, but we need to add some recursive function to do the reveal of everything around that is 0. 
        # Skipped for now
        self.check_game_end()

    def flag_cell(self, rows, columns):
        # Implement flag logic. Skipped for now, see notes from June 10.
        pass

    def print_board(self): # Prints the back-end, true board
        for rows in self.board:
            print(' '.join(rows))

    def print_visible_board(self): # Prints the board currently visible to the player
        for rows in self.visible_board:
                print(' '.join(str(cell) for cell in rows))


    def play(self):
        print("\n")
        print("Welcome to Sweep Savvy Solver - Player Edition.")
        print("Good luck!\n")

        while (self.game_end == False):
            self.print_visible_board()
            print("\n")
            print("Choose which cell to reveal next")
            try:
                row = int(input("Enter cell row: "))
                col = int(input("Enter cell col: "))
                row = row-1
                col = col-1
                if 0 <= row < self.rows and 0 <= col < self.columns:
                    self.reveal_cell(row, col)
                else:
                    print("Invalid input, please enter numbers within the board limit.")
            except ValueError:
                print("Invalid input, please enter integers.")

        print("Game over.\n")
        self.print_board()

    def check_game_end(self):
        for row in range(self.rows):
            for col in range(self.columns):
                if self.visible_board[row][col] == '#' and self.board[row][col] != 'M':
                    return
        self.game_end = True
        print("\nCongratulations! You've found all the mines!\n")


# We execute the program. We can select the number of rows, columns, and mines
if __name__ == "__main__":
    rows = 5
    cols = 5
    num_mines = 5
    board = MinesweeperBoard(rows, cols, num_mines)

    #board.print_board()

    board.play()
