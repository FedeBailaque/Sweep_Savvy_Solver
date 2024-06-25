import random
import heapq


# import time

# I changed the name from MinesweeperBoard to MinesweeperGame because it will makes more sense
# and it goes in accordance with its function
class MinesweeperGame:
    def __init__(self, rows=10, columns=10, num_of_mines=45):
        self.rows = rows
        self.columns = columns
        self.num_of_mines = num_of_mines
        self.board = [[0 for _ in range(columns)] for _ in range(rows)]
        # self.board = []
        # self.visible_board = []
        self.revealed = [[False for _ in range(columns)] for _ in range(rows)]
        self.mine_positions = set()
        # self.flags = set()
        self.flags = [[False for _ in range(columns)] for _ in range(rows)]
        # self.initialize_board()
        self.generate_mines()
        self.count_adjacent_mines()
        # self.game_end = False

    # def initialize_board(self):
    #     # This creates an empty board
    #     for _ in range(self.rows):
    #         self.board.append(['-'] * self.columns)
    #
    #     # Places mines and marks them with an 'M'
    #     mines_placed = 0
    #     while mines_placed < self.num_of_mines:
    #         rows = random.randint(0, self.rows - 1)
    #         cols = random.randint(0, self.columns - 1)
    #         if (rows, cols) not in self.mine_positions:
    #             self.mine_positions.add((rows, cols))
    #             self.board[rows][cols] = 'M'
    #             mines_placed += 1
    #
    #     # Uses the function count_adjacent_mines to calculate how many adjacent mines the current square has
    #     for rows in range(self.rows):
    #         for cols in range(self.columns):
    #             if self.board[rows][cols] != 'M':
    #                 self.board[rows][cols] = str(self.count_adjacent_mines(rows, cols))
    #
    #     # This creates the visible board
    #     for _ in range(self.rows):
    #         self.visible_board.append(['#'] * self.columns)

    def count_adjacent_mines(self):
        for r, c in self.mine_positions:
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.columns and self.board[nr][nc] != 'M':
                        self.board[nr][nc] += 1
        # directions = [
        #     (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
        # ]
        # count = 0
        # for dr, dc in directions:
        #     r = rows + dr
        #     c = cols + dc
        #     if 0 <= r < self.rows and 0 <= c < self.columns:
        #         if self.board[r][c] == 'M':
        #             count += 1
        # return count

    def reveal_cell(self, rows, columns):
        if self.board[rows][columns] == 'M':
            # self.game_end = True
            return False
            # self.visible_board[rows][cols] = 'M'
        self._reveal_recursive(rows, columns)
        return True
        # print("\nYou've hit a mine!")
        # else:
        #     self.visible_board[rows][columns] = str(self.board[rows][columns])
        #     # Remove flags when revealing board
        #     self.flags.discard((rows, columns))
        #     # This is optional and only if we reach improvements stage,
        # # but we need to add some recursive function to do the reveal
        # # of everything around that is 0 (Skipped for now)
        # self.check_game_end()

    def _reveal_recursive(self, rows, columns):
        if not (0 <= rows < self.rows and 0 <= columns < self.columns) or self.revealed[rows][columns]:
            return
        self.revealed[rows][columns] = True
        if self.board[rows][columns] == 0:
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    if dr != 0 or dc != 0:
                        self._reveal_recursive(rows + dr, columns + dc)

    def place_flag(self, rows, columns):
        self.flags[rows][columns] = not self.flags[rows][columns]

    def is_victory(self):
        for r in range(self.rows):
            for c in range(self.columns):
                if self.board[r][c] != 'M' and not self.revealed[r][c]:
                    return False
        return True

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
        for r in range(self.rows):
            for c in range(self.columns):
                if self.revealed[r][c]:
                    print(self.board[r][c], end=" ")
                elif self.flags[r][c]:
                    print("F", end=" ")
                else:
                    print("#", end=" ")
            print()
        # # Determine the width needed for the largest number
        # col_width = len(str(max(self.rows, self.columns)))
        #
        # # Print column numbers with formatting
        # header = " " * (col_width + 1) + " ".join(str(i + 1).rjust(col_width) for i in range(self.columns))
        # print(header)
        #
        # # Print rows with row numbers with formating
        # for idx, row in enumerate(self.board):
        #     print(str(idx + 1).rjust(col_width) + " " + ' '.join(cell.rjust(col_width) for cell in row))

    def generate_mines(self):
        while len(self.mine_positions) < self.num_of_mines:
            rows = random.randint(0, self.rows - 1)
            columns = random.randint(0, self.columns - 1)
            if (rows, columns) not in self.mine_positions:
                self.mine_positions.add((rows, columns))
                self.board[rows][columns] = 'M'


class MinesweeperAI:
    def __init__(self, game):
        self.game = game
        self.frontier = []
        self.explored = set()
        self.initialize_frontier()

    def initialize_frontier(self):
        heapq.heappush(self.frontier, (self.heuristic(0,0), 0, 0))

    def heuristic(self, rows, columns):
        return self.game.board[rows][columns] if self.game.board[rows][columns] != 'M' else float('inf')

    ## We need to add the function for the AI to flag a mine
    def make_move(self):
        while self.frontier:
            _, rows, columns = heapq.heappop(self.frontier)
            if (rows, columns) in self.explored:
                continue
            self.explored.add((rows, columns))
            if not self.game.reveal_cell(rows,columns):
                print(f"Ai hit a mine at ({rows + 1}, {columns + 1})!")
                return False
            print(f"Ai revealed cell at ({rows + 1}, {columns + 1}).")
            self.expand_frontier(rows,columns)
            return True
        return False

    # def print_visible_board(self):  # Prints the board currently visible to the player
    #     # Determine the width needed for the largest number
    #     col_width = len(str(max(self.rows, self.columns)))
    #
    #     # Print column numbers with formating
    #     header = " " * (col_width + 1) + " ".join(str(i + 1).rjust(col_width) for i in range(self.columns))
    #     print(header)
    #
    #     # Print rows with row numbers with formating
    #     for idx, row in enumerate(self.visible_board):
    #         print(str(idx + 1).rjust(col_width) + " " + ' '.join(str(cell).rjust(col_width) for cell in row))

    def expand_frontier(self, rows, columns):
        for dr in range(-1,2):
            for dc in range(-1,2):
                nr, nc = rows + dr, columns + dc
                if 0 <= nr < self.game.rows and 0 <= nc < self.game.columns and (nr, nc) not in self.explored and not self.game.revealed[nr][nc]:
                    heapq.heappush(self.frontier, (self.heuristic(nr, nc), nr, nc))





    # def play(self):
    #     print("Good luck!\n")
    #
    #     while not self.game_end:
    #         self.print_visible_board()
    #         print("\n")
    #         print("Choose which cell to reveal next or place a flag.")
    #         try:
    #             print("\n")
    #             action = input("Would you like to place or remove a flag? (y/n): ").lower()
    #             if action == 'y':
    #                 rows = int(input("Enter cell row to place flag: "))
    #                 cols = int(input("Enter cell col to place flag: "))
    #                 rows -= 1
    #                 cols -= 1
    #                 if 0 <= rows < self.rows and 0 <= cols < self.columns:
    #                     self.flag_cell(rows, cols)
    #                 else:
    #                     print("Invalid input, please enter numbers within the board limit.")
    #             else:
    #                 rows = int(input("Enter cell row to reveal: "))
    #                 cols = int(input("Enter cell col to reveal: "))
    #                 rows -= 1
    #                 cols -= 1
    #                 if 0 <= rows < self.rows and 0 <= cols < self.columns:
    #                     self.reveal_cell(rows, cols)
    #                 else:
    #                     print("Invalid input, please enter numbers within the board limit.")
    #         except ValueError:
    #             print("Invalid input, please enter integers.")
    #
    #     print("Game over.\n")
    #     self.print_board()
    #
    # def check_game_end(self):
    #     # Check if all non-mine cells are revealed
    #     for rows in range(self.rows):
    #         for cols in range(self.columns):
    #             if self.visible_board[rows][cols] == '#' and self.board[rows][cols] != 'M':
    #                 return

        # Check if all mines are flagged correctly
        # Flag position have to match mine locations
        # if self.flags == self.mine_positions:
        #     print("\nCongratulations! You've found all the mines and placed the flags correctly!\n")
        # else:
        #     self.game_end = True
        #     # The user literally has to put like all Fs in the board for this to work
        #     print("\nYou have placed some flags incorrectly. Better luck next time!\n")
        # self.game_end = True
def main():
    print("\nWelcome to Sweep Savvy Solver")
    while True:
        print("1. User mode")
        print("2. AI mode")
        print("3. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            user_mode()
        elif choice == '2':
            ai_mode()
        elif choice == '3':
            print("Quitting the game. Goodbye!")
            break
        else:
            print("Please select a valid option.")

def user_mode():
    game = MinesweeperGame()
    while True:
        game.print_board()
        flag = input("Would you like to place or remove a flag? (y/n): ").lower()
        if flag == 'y':
            row = int(input("Enter cell row to place/remove flag: ")) - 1
            column = int(input("Enter cell col to place/remove flag: ")) - 1
            game.place_flag(row,column)
        else:
            row = int(input("Enter cell row to reveal: ")) - 1
            column = int(input("Enter cell column to reveal: ")) - 1
            if not game.reveal_cell(row, column):
                print(f"Game over. You hit a mine at ({row + 1}, {column + 1})!")
                break
            if game.is_victory():
                game.print_board()
                print("Congratulations! You won")
                break
#We should show the the revealed board when we lose
def ai_mode():
    game = MinesweeperGame()
    ai = MinesweeperAI(game)
    while True:
        game.print_board()
        print("AI is playing...")
        if not ai.make_move():
            game.print_board()
            print("AI hit a mine. Game over.")
            break
        if game.is_victory():
            game.print_board()
            print("AI won the game.")
            break
        print("AI finished playing.")

#We should show the the revealed board when we lose

if __name__ == "__main__":
    main()


    # def play_ai(self):
    #
    #     print("AI is playing...\n")
    #     # start_row = random.randint(0, self.rows - 1)
    #     # start_col = random.randint(0, self.columns - 1)
    #
    #     start_row = 0
    #     start_col = 0
    #
    #     self.dfs(start_row, start_col)
    #
    #     # AI chooses a row and col to start at.
    #     # DFS will make a decision for what the AI will do next.
    #     #   Create valid checker, to make sure AI picks a valid coord
    #     #   is_valid_cell()
    #
    #     # You run into a mine
    #     # Or you run into a cell that has already been flagged
    #     for rows in range(self.rows):
    #         for cols in range(self.columns):
    #             if not self.game_end:
    #                 self.reveal_cell(rows, cols)
    #             else:
    #                 break
    #         if self.game_end:
    #             break
    #
    #     print("AI has finished playing")
    #     self.print_board()
    #
    # # pass
    # #   def ai_play(self):
    # #       print("AI is playing...\n")
    # #
    # #       # start_row = random.randint(0, self.rows - 1)
    # #       # start_col = random.randint(0, self.columns - 1)
    # #
    # #       start_row = 0
    # #       start_col = 0
    # #
    # #       self.dfs(start_row, start_col)
    # #
    # #       print("Game over\n")
    # #       self.print_board()
    # def dfs(self, rows, columns):
    #     if not self.is_valid_cell(rows, columns):
    #         return

    # def is_valid_cell(self, rows, columns):
    #     return 0 <= rows < self.rows and 0 <= columns < self.columns and self.visible_board[rows][columns] == '#'


# We execute the program. We can select the number of rows, columns, and mines
# if __name__ == "__main__":
#     rows = 10
#     cols = 10
#     num_mines = 20
#
#     while True:
#         print("\nWelcome to Sweep Savvy Solver - Player Edition.")
#         print("1. User mode")
#         print("2. AI mode (not implemented yet)")
#         print("3. Quit")
#
#         choice = input("Enter your choice: ").strip()
#
#         if choice == '1':
#             board = MinesweeperBoard(rows, cols, num_mines)
#             board.play()
#         elif choice == '2':
#             board = MinesweeperBoard(rows, cols, num_mines)
#             print("AI mode is not implemented yet.")
#             # Placeholder for AI mode implementation
#             board.play_ai()
#         elif choice == '3':
#             print("Quitting the game. Goodbye!")
#             break
#         else:
#             print("Invalid choice. Please select a valid option.")

    # board.print_board()

    # board.print_menu()

    # board.play()
