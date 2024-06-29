import random
import heapq
import time
from colorama import init, Fore

init(autoreset=True)


# Main class that starts and initializes the game
class MinesweeperGame:
    def __init__(self, rows=10, columns=10, num_of_mines=40):
        self.rows = rows
        self.columns = columns
        self.num_of_mines = num_of_mines
        self.board = [[0 for _ in range(columns)] for _ in range(rows)]
        self.revealed = [[False for _ in range(columns)] for _ in range(rows)]
        self.mine_positions = set()
        self.flags = [[False for _ in range(columns)] for _ in range(rows)]
        self.generate_mines()
        self.count_adjacent_mines()

    # Calculates the adjacent mines for each cell on the board
    # Puts the number on the cell
    def count_adjacent_mines(self):
        for r, c in self.mine_positions:
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.columns and self.board[nr][nc] != 'M':
                        self.board[nr][nc] += 1

    # For User mode
    def reveal_cell(self, rows, columns):
        if self.board[rows][columns] == 'M':
            return False
        self._reveal_recursive(rows, columns)
        return True

    # Helper function for reveal_cell
    # Reveals cells until mines are encountered.
    def _reveal_recursive(self, rows, columns):
        if not (0 <= rows < self.rows and 0 <= columns < self.columns) or self.revealed[rows][columns]:
            return
        self.revealed[rows][columns] = True
        if self.board[rows][columns] == 0:
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    if dr != 0 or dc != 0:
                        self._reveal_recursive(rows + dr, columns + dc)

    # Toggles a flag on/off (user mode only)
    def place_flag(self, rows, columns):
        self.flags[rows][columns] = not self.flags[rows][columns]

    # Returns true if all non-mine cells are revealed
    # otherwise it's false
    def is_victory(self):
        for r in range(self.rows):
            for c in range(self.columns):
                if self.board[r][c] != 'M' and not self.revealed[r][c]:
                    return False
        return True

    # Prints the entire board (user mode only)
    def print_board(self):  # Prints the back-end, true board
        color_map = {
            'M': Fore.RED + "⛔️" + Fore.RESET,  # red color and emoji for the mine
            0: Fore.RESET + "⬛️" + Fore.RESET,  # color and emoji for empty mine
            'F': Fore.YELLOW + "🏁" + Fore.RESET,  # color and emoji for flag
            '#': Fore.BLUE + "🔵" + Fore.RESET,  # unrevealed cell
        }

        for r in range(self.rows):
            for c in range(self.columns):
                if self.revealed[r][c]:
                    cell_value = self.board[r][c]
                    print(color_map.get(cell_value, Fore.GREEN + str(cell_value) + Fore.RESET), end="  ")
                elif self.flags[r][c]:
                    print(color_map['F'], end=" ")
                else:
                    print(color_map['#'], end=" ")
            print()

    # Places mines randomly on the board depending on the board size and number of mines inputted.
    # Updates the self.mine_positions attribute of the minesweeper class
    def generate_mines(self):
        while len(self.mine_positions) < self.num_of_mines:
            rows = random.randint(0, self.rows - 1)
            columns = random.randint(0, self.columns - 1)
            if (rows, columns) not in self.mine_positions and (rows, columns) != (0, 0):
                self.mine_positions.add((rows, columns))
                self.board[rows][columns] = 'M'


# Class to hold AI and User statistics
class Statistics:
    def __init__(self):
        self.ai_wins = 0
        self.ai_losses = 0
        self.user_wins = 0
        self.user_losses = 0

    def record_win_user(self):
        self.user_wins += 1

    def record_loss_user(self):
        self.user_losses += 1

    def record_win_ai(self):
        self.ai_wins += 1

    def record_loss_ai(self):
        self.ai_losses += 1


# AI class
# Initialize the AI mode as a reference to the minesweeper game class
class MinesweeperAI:
    def __init__(self, game, stats):
        self.game = game
        self.stats = stats
        self.frontier = []
        self.explored = set()
        self.ai_moves_made = 0  # Counter for AI moves
        self.initialize_frontier()

    # Priority Queue for cells to be explored.
    # Starts at 0,0
    def initialize_frontier(self):
        heapq.heappush(self.frontier, (self.heuristic(0, 0), 0, 0))

    # Returns a heuristic value (i.e. the Number of adjacent mines)
    # If it's an M, returns infinity.
    def heuristic(self, rows, columns):
        return self.game.board[rows][columns] if self.game.board[rows][columns] != 'M' else float('inf')

    # Manages the AI move sequence
    # Pops a cell from the frontier and reveals that cell
    # If the cell is a mine the game ends, and it expands the frontier by adding valid neighboring cells
    def make_move(self):
        ai_color_map = {
            'M': Fore.RED + "⛔️" + Fore.RESET,
            0: Fore.RESET + "⚪️" + Fore.RESET,
            'F': Fore.YELLOW + "🏁" + Fore.RESET,
            '#': Fore.BLUE + "🔵" + Fore.RESET
        }
        while self.frontier:
            _, rows, columns = heapq.heappop(self.frontier)
            if (rows, columns) in self.explored:
                continue

            self.explored.add((rows, columns))
            self.ai_moves_made += 1
            emoji_state = ai_color_map.get(self.game.board[rows][columns], str(self.game.board[rows][columns]))
            print(f"Ai is going to reveal{emoji_state} cell at ({rows + 1},{columns + 1}).")

            if not self.game.reveal_cell(rows, columns):
                print(f"Ai hit a mine at ({rows + 1}, {columns + 1})!\n")
                return False  # When a mine is hit

            # The AI picked a cell and let the viewer know what it was
            print(f"Ai revealed cell at ({rows + 1}, {columns + 1}).\n")
            self.expand_frontier(rows, columns)

            # Controls the delay for searching (printing out next step)
            # time.sleep(2) # Delay is set to 2 seconds
            return True
        return False

    # Adds valid neighboring cells to the frontier
    # if they have not been revealed or explored
    def expand_frontier(self, rows, columns):
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = rows + dr, columns + dc
                if 0 <= nr < self.game.rows and 0 <= nc < self.game.columns and (nr, nc) not in self.explored and not \
                        self.game.revealed[nr][nc]:
                    heapq.heappush(self.frontier, (self.heuristic(nr, nc), nr, nc))


def main():
    stats = Statistics()
    print("\nWelcome to Sweep Savvy Solver\n")
    while True:
        try:
            print()
            print(f"User Wins: {stats.user_wins}, User Losses: {stats.user_losses}\n")
            print(f"AI Wins: {stats.ai_wins}, AI Losses: {stats.ai_losses}\n")
            print("1. User mode")
            print("2. AI mode")
            print("3. Quit")

            choice = input("Enter your choice: ")

            if choice == '1':
                user_mode(stats)
            elif choice == '2':
                ai_mode(stats)
            elif choice == '3':
                print("Quitting the game. Goodbye!")
                break
            else:
                print("Please select a valid option.")
        except KeyboardInterrupt:
            print("\nProgram interrupted . Quitting...")
            break


def user_mode(stats):
    game = MinesweeperGame()
    while True:
        game.print_board()

        while True:
            flag = input("Would you like to place or remove a flag? (y/n): ").lower()
            if flag in ['y', 'n']:
                break  # now its valid , exit the loop
            print("Invalid input. Please enter 'y' or 'n'.")  # add error message

        if flag == 'y':

            while True:
                try:
                    row = int(input(f"Enter cell row to place /remove flag (1 to {game.rows}): ")) - 1
                    column = int(input(f"Enter cell column to place /remove flag (1 to {game.columns}): ")) - 1
                    if 0 <= row < game.rows and 0 <= column < game.columns:
                        game.place_flag(row, column)
                        break  #
                    else:
                        print(
                            f"Invalid input. Please enter a row between 1 and {game.rows} and and a column between 1 "
                            f"and {game.columns}.")
                except ValueError:
                    print("Invalid input. Please enter numeric values ")
        else:
            while True:
                try:

                    row = int(input(f"Enter cell row to reveal (1 to {game.rows}): ")) - 1
                    column = int(input(f"Enter cell column to reveal (1 to {game.columns}): ")) - 1
                    if 0 <= row < game.rows and 0 <= column < game.columns:
                        if not game.reveal_cell(row, column):
                            print(f"Game over. You hit a mine at ({row + 1}, {column + 1})!")
                            stats.record_loss_user()
                            return
                        if game.is_victory():
                            game.print_board()
                            print("Congratulations! You won!\n")
                            stats.record_win_user()
                            return
                        break
                    else:
                        print(
                            f"Invalid input. Please enter a row between 1 and {game.rows} and a column between 1 and {game.columns}.")
                except ValueError:
                    print("Invalid input. Please enter numeric values")


def ai_mode(stats):
    game = MinesweeperGame()
    ai = MinesweeperAI(game, stats)
    while True:
        game.print_board()
        print("AI is playing...")
        if not ai.make_move():
            game.print_board()
            print(f"AI hit a mine. Game over. Moves made: {ai.ai_moves_made}")
            ai.stats.record_loss_ai()
            break
        if game.is_victory():
            game.print_board()
            print(f"AI won the game. Moves made: {ai.ai_moves_made}")
            ai.stats.record_win_ai()
            break
        print("AI finished playing.")


if __name__ == "__main__":
    main()
