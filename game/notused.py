# game/board.py
import numpy as np

class Board:
    def create_board(self) -> np.ndarray:
        return np.zeros((5, 5, 5), dtype=int)  # (layer, row, col)

    def is_space_empty(self, board: np.ndarray, row: int, col: int) -> bool:
        return board[0][row][col] == 0  # full if even top layer is occupied

    def drop_piece(self, board: np.ndarray, row: int, col: int, player: int) -> int:
        """Drops piece to lowest empty layer. Returns layer index or -1 if column is full."""
        for layer in range(4, -1, -1):
            if board[layer][row][col] == 0:
                board[layer][row][col] = player
                return layer
        return -1

    def check_winner(self, board: np.ndarray, player: int) -> bool:
        b = board
        p = player
        n = 5
        target = 4

        def check_line(cells):
            for i in range(len(cells) - target + 1):
                if all(cells[i + k] == p for k in range(target)):
                    return True
            return False

        lines = []

        for i in range(n):
            for j in range(n):
                lines.append([b[i][j][k] for k in range(n)])  # rows
                lines.append([b[i][k][j] for k in range(n)])  # cols
                lines.append([b[k][i][j] for k in range(n)])  # vertical pillars

            # Layer diagonals
            lines.append([b[i][k][k] for k in range(n)])
            lines.append([b[i][k][n-1-k] for k in range(n)])

            # Diagonal slices across layers
            lines.append([b[k][i][k] for k in range(n)])
            lines.append([b[k][i][n-1-k] for k in range(n)])
            lines.append([b[k][k][i] for k in range(n)])
            lines.append([b[k][n-1-k][i] for k in range(n)])

        # 4 space diagonals
        lines.append([b[k][k][k] for k in range(n)])
        lines.append([b[k][k][n-1-k] for k in range(n)])
        lines.append([b[k][n-1-k][k] for k in range(n)])
        lines.append([b[k][n-1-k][n-1-k] for k in range(n)])

        return any(check_line(line) for line in lines)

    def is_full(self, board: np.ndarray) -> bool:
        return not np.any(board == 0)

    def display_board(self, board: np.ndarray) -> None:
        symbols = {0: ".", 1: "X", 2: "O"}
        for i, layer in enumerate(board):
            print(f"--- Layer {i} ({"top" if i == 0 else "bottom" if i == 4 else ""}) ---")
            for row in layer:
                print(" ".join(symbols[cell] for cell in row))
            print()


# --- Game loop ---
game_over = False
turn = 0
game_board = Board()
board = game_board.create_board()
game_board.display_board(board)

while not game_over:
    player = 1 if turn == 0 else 2
    symbol = "X" if player == 1 else "O"
    print(f"Player {player} ({symbol})'s turn")

    try:
        row = int(input("Enter row (0-4): "))
        col = int(input("Enter col (0-4): "))
    except ValueError:
        print("Numbers only.\n")
        continue

    if not all(0 <= v <= 4 for v in (row, col)):
        print("Values must be 0-4.\n")
        continue

    if not game_board.is_space_empty(board, row, col):
        print("That column is full.\n")
        continue

    layer = game_board.drop_piece(board, row, col, player)
    game_board.display_board(board)

    if game_board.check_winner(board, player):
        print(f"Player {player} ({symbol}) wins!")
        game_over = True
    elif game_board.is_full(board):
        print("It's a draw!")
        game_over = True
    else:
        turn = 1 - turn