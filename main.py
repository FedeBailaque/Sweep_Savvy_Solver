import random


class MinesweeperBoard:
    def __init__(self, rows, columns, num_of_mines):
        self.rows = rows
        self.columns = columns
        self.num_of_mines = num_of_mines
        self.board = []
        self.visible_board = []
        self.mine_positions = set()
        self.flags = set()
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
            cols = random.randint(0, self.columns - 1)
            if (rows, cols) not in self.mine_positions:
                self.mine_positions.add((rows, cols))
                self.board[rows][cols] = 'M'
                mines_placed += 1

        # Uses the function count_adjacent_mines to calculate how many adjacent mines the current square has
        for rows in range(self.rows):
            for cols in range(self.columns):
                if self.board[rows][cols] != 'M':
                    self.board[rows][cols] = str(self.count_adjacent_mines(rows, cols))

        # This creates the visible board
        for _ in range(self.rows):
            self.visible_board.append(['#'] * self.columns)

    def count_adjacent_mines(self, rows, cols):
        directions = [
            (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
        ]
        count = 0
        for dr, dc in directions:
            r = rows + dr
            c = cols + dc
            if 0 <= r < self.rows and 0 <= c < self.columns:
                if self.board[r][c] == 'M':
                    count += 1
        return count

    def reveal_cell(self, rows, cols):
        if self.board[rows][cols] == 'M':
            self.game_end = True
            self.visible_board[rows][cols] = 'M'
            print("\nYou've hit a mine!")
        else:
            self.visible_board[rows][cols] = str(self.board[rows][cols])
            # Remove flags when revealing board 
            self.flags.discard((rows, cols))
            # This is optional and only if we reach improvements stage,
        # but we need to add some recursive function to do the reveal
        # of everything around that is 0 (Skipped for now)
        self.check_game_end()

    def flag_cell(self, rows, cols):
        # user can only place a flag on a spot with a #
        if self.visible_board[rows][cols] == '#':
            self.visible_board[rows][cols] = 'F'
            self.flags.add((rows, cols))

        # if the user would like to remove flag, replace the F with # again
        elif self.visible_board[rows][cols] == 'F':
            self.visible_board[rows][cols] = '#'
            self.flags.discard((rows, cols))
        self.check_game_end()

    def print_board(self):  # Prints the back-end, true board
        # Determine the width needed for the largest number
        col_width = len(str(max(self.rows, self.columns)))

        # Print column numbers with formatting
        header = " " * (col_width + 1) + " ".join(str(i + 1).rjust(col_width) for i in range(self.columns))
        print(header)

        # Print rows with row numbers with formating
        for idx, row in enumerate(self.board):
            print(str(idx + 1).rjust(col_width) + " " + ' '.join(cell.rjust(col_width) for cell in row))

    def print_visible_board(self):  # Prints the board currently visible to the player
        # Determine the width needed for the largest number
        col_width = len(str(max(self.rows, self.columns)))

        # Print column numbers with formating
        header = " " * (col_width + 1) + " ".join(str(i + 1).rjust(col_width) for i in range(self.columns))
        print(header)

        # Print rows with row numbers with formating
        for idx, row in enumerate(self.visible_board):
            print(str(idx + 1).rjust(col_width) + " " + ' '.join(str(cell).rjust(col_width) for cell in row))

    def play(self):
        print("Good luck!\n")

        while not self.game_end:
            self.print_visible_board()
            print("\n")
            print("Choose which cell to reveal next or place a flag.")
            try:
                print("\n")
                action = input("Would you like to place or remove a flag? (y/n): ").lower()
                if action == 'y':
                    rows = int(input("Enter cell row to place flag: "))
                    cols = int(input("Enter cell col to place flag: "))
                    rows -= 1
                    cols -= 1
                    if 0 <= rows < self.rows and 0 <= cols < self.columns:
                        self.flag_cell(rows, cols)
                    else:
                        print("Invalid input, please enter numbers within the board limit.")
                else:
                    rows = int(input("Enter cell row to reveal: "))
                    cols = int(input("Enter cell col to reveal: "))
                    rows -= 1
                    cols -= 1
                    if 0 <= rows < self.rows and 0 <= cols < self.columns:
                        self.reveal_cell(rows, cols)
                    else:
                        print("Invalid input, please enter numbers within the board limit.")
            except ValueError:
                print("Invalid input, please enter integers.")

        print("Game over.\n")
        self.print_board()

    def check_game_end(self):
        # Check if all non-mine cells are revealed
        for rows in range(self.rows):
            for cols in range(self.columns):
                if self.visible_board[rows][cols] == '#' and self.board[rows][cols] != 'M':
                    return

        # Check if all mines are flagged correctly
        # Flag position have to match mine locations
        if self.flags == self.mine_positions:
            print("\nCongratulations! You've found all the mines and placed the flags correctly!\n")
        else:
            self.game_end = True
            # The user literally has to put like all Fs in the board for this to work
            print("\nYou have placed some flags incorrectly. Better luck next time!\n")

        self.game_end = True


# We execute the program. We can select the number of rows, columns, and mines
if __name__ == "__main__":
    rows = 10
    cols = 10
    num_mines = 25

    while True:
        print("\nWelcome to Sweep Savvy Solver - Player Edition.")
        print("1. User mode")
        print("2. AI mode (not implemented yet)")
        print("3. Quit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            board = MinesweeperBoard(rows, cols, num_mines)
            board.play()
        elif choice == '2':
            print("AI mode is not implemented yet.")
            # Placeholder for AI mode implementation
        elif choice == '3':
            print("Quitting the game. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

    # board.print_board()

    # board.print_menu()

    # board.play()
