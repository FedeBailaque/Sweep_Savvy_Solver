import random
import heapq

# Main class that starts the initializes the game
class MinesweeperGame:
    def __init__(self, rows=10, columns=10, num_of_mines=45):
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
            # self.game_end = True
            return False
            # self.visible_board[rows][cols] = 'M'
        self._reveal_recursive(rows, columns)
        return True

    # Helper function for reveal_cell 
    # Reveals cells until mines are encounter. 
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

    # Returns true is all Non mine cells are revealed
    # otherwise it's false
    def is_victory(self):
        for r in range(self.rows):
            for c in range(self.columns):
                if self.board[r][c] != 'M' and not self.revealed[r][c]:
                    return False
        return True

    # (User mode only)
    # Allows placement of the character F (represent a flag)
    # User is allowed to removed a flag from a position
    # When a flag is removed, the # symbol is put back
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

    # Prints the entire board (user mode only)
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
 
    # Places mines randomly on the board depending on the board size and number of mines inputed. 
    # Updates the self.mine_positions attribute of the minesweeper class
    def generate_mines(self):
        while len(self.mine_positions) < self.num_of_mines:
            rows = random.randint(0, self.rows - 1)
            columns = random.randint(0, self.columns - 1)
            if (rows, columns) not in self.mine_positions:
                self.mine_positions.add((rows, columns))
                self.board[rows][columns] = 'M'

# AI class 
# Initialize the AI mode as a reference to the minesweeper game class 

class MinesweeperAI:
    def __init__(self, game):
        self.game = game
        self.frontier = []
        self.explored = set()
        self.initialize_frontier()

    # Priority Queue for cells to be explored.
    # Starts at 0,0 
    def initialize_frontier(self):
        heapq.heappush(self.frontier, (self.heuristic(0,0), 0, 0))

    # Returns a heurisitc value (i.e. the Number of adjacent mines)
    # If its an M, returns infinity.
    def heuristic(self, rows, columns):
        return self.game.board[rows][columns] if self.game.board[rows][columns] != 'M' else float('inf')

    # Manages the AI move sequence
    # Pops a cell from the frontier and reveals that cell
    # If the cell is a mine the game ends and it expands the frontier by adding valid neighboring cells
    def make_move(self):
        while self.frontier:
            _, rows, columns = heapq.heappop(self.frontier)
            if (rows, columns) in self.explored:
                continue

            self.explored.add((rows, columns))
            if not self.game.reveal_cell(rows,columns):
                print(f"Ai hit a mine at ({rows + 1}, {columns + 1})!\n")
                return False # When a mine is hit
            
            # The AI picked a cell and let the viewer know what it was
            print(f"Ai revealed cell at ({rows + 1}, {columns + 1}).\n")
            self.expand_frontier(rows,columns)
            return True
        return False 

  

    # Adds valid neighboring cells to the frontier 
    # if they have not been revealed or explored 
    def expand_frontier(self, rows, columns):
        for dr in range(-1,2):
            for dc in range(-1,2):
                nr, nc = rows + dr, columns + dc
                if 0 <= nr < self.game.rows and 0 <= nc < self.game.columns and (nr, nc) not in self.explored and not self.game.revealed[nr][nc]:
                    heapq.heappush(self.frontier, (self.heuristic(nr, nc), nr, nc))

def main():
    print("\nWelcome to Sweep Savvy Solver\n")
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


