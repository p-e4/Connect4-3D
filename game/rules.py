# game/rules.py
import numpy as np

"""
Rules for 3D Connect Four on a 5x5x5 board.
Designed to work with GameBoard's board_state[y, x, z] convention.
4 in a row wins in any direction.
"""
DEFAULT_SIZE   = 5  # Board dimensions (5x5x5)
DEFAULT_TARGET = 4  # How many in a row to win


class Rules:
    def __init__(self, size: int = DEFAULT_SIZE, target: int = DEFAULT_TARGET):
        self.size = size
        self.target = target

    # ------------------------ #
    #     Helper functions     #
    # ------------------------ #

    def is_board_full(self, column_heights: np.ndarray) -> bool:
        return np.all(column_heights >= self.size)

    # ------------------------ #
    #       Checks winner      #
    # ------------------------ #

    def check_winner(self, board_state: np.ndarray, player: int) -> bool:
        """Checks if the given player has 4 in a row anywhere on the board."""
        b = board_state
        p = player
        n = self.size
        t = self.target

        def check_line(cells):
            for i in range(len(cells) - t + 1):
                if all(cells[i + k] == p for k in range(t)):
                    return True
            return False

        lines = []

        for i in range(n):
            for j in range(n):
                lines.append([b[i, k, j] for k in range(n)])  # along x, fixed y and z
                lines.append([b[i, j, k] for k in range(n)])  # along z, fixed y and x
                lines.append([b[k, i, j] for k in range(n)])  # vertical pillars

            # Diagonals within each layer
            lines.append([b[i, k, k] for k in range(n)])
            lines.append([b[i, k, n-1-k] for k in range(n)])

            # Diagonals across layers, fixed x
            lines.append([b[k, i, k] for k in range(n)])
            lines.append([b[k, i, n-1-k] for k in range(n)])

            # Diagonals across layers, fixed z
            lines.append([b[k, k, i] for k in range(n)])
            lines.append([b[k, n-1-k, i] for k in range(n)])

        # 4 true 3D space diagonals
        lines.append([b[k, k, k] for k in range(n)])
        lines.append([b[k, k, n-1-k] for k in range(n)])
        lines.append([b[k, n-1-k, k] for k in range(n)])
        lines.append([b[k, n-1-k, n-1-k] for k in range(n)])

        return any(check_line(line) for line in lines)

    def get_winner(self, board_state: np.ndarray) -> int:
        """Returns 1 if player 1 won, 2 if player 2 won, 0 if no winner yet."""
        if self.check_winner(board_state, 1):
            return 1
        if self.check_winner(board_state, 2):
            return 2
        return 0

    # ------------------------ #
    #        Game Status       #
    # ------------------------ #

    def get_game_status(self, board_state: np.ndarray, column_heights: np.ndarray, last_player: int) -> str:
        """
        Returns:
          'win'     — last_player just won
          'draw'    — board is full, no winner
          'ongoing' — game continues
        """
        if self.check_winner(board_state, last_player):
            return 'win'
        if self.is_board_full(column_heights):
            return 'draw'
        return 'ongoing'