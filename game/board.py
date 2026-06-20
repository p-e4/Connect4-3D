#game/board.py
import numpy as np
"""
Creates a board, memorizes if node filled and which color, and also displays the board
"""
class Board:
    def create_board(self) -> np.ndarray:
        board = np.zeros((5, 5))
        return board

    def is_space_emtpy(self, board: np.ndarray, x: int, y:int) -> bool:
        return board[x][y] == 0

    def place_marker(self, board: np.ndarray, row: int, col: int, player) -> None:
        board[row][col] = player

    def check_winner(self,board: np.ndarray, player) -> bool:
        for i in range(5):
            if all(board[i][j] == player for j in range(3)):
                return True
            if all(board[j][i] == player for j in range(3)):
                return True

            if all(board[i][i] == player for i in range(3)):
                return True
            if all(board[i][4-i] == player for i in range(3)):
                return True
        return False

    def display_board(self, board: np.ndarray) -> None:
        for row in board:
            for space in row:
                if space == 1:
                    print("X", end=" ")
                elif space == 2:
                    print("O", end=" ")
                else:
                    print(".", end=" ")
            print()


game_over = False
turn = 0
game_board = Board()
board = game_board.create_board()

while not game_over:
    player1 = 1
    player2 = 2

    if turn == 0:
        row = int(input("Enter row (0-4): "))
        col = int(input("Enter col (0-4): "))

        if not (0 <= row <= 4 and 0 <= col <= 4):
            print("Invalid row or col")
            continue

        if not game_board.is_space_emtpy(board, row, col):
            print("space is occupied")
            continue

        game_board.place_marker(board, row, col, player1)
        game_board.display_board(board)

        if game_board.check_winner(board, player1):
            game_over = True
    else:
        row = int(input("Enter row (0-4): "))
        col = int(input("Enter col (0-4): "))

        if not (0 <= row <= 4 and 0 <= col <= 4):
            print("Invalid row or col")
            continue

        if not game_board.is_space_emtpy(board, row, col):
            print("space is occupied")
            continue

        game_board.place_marker(board, row, col, player2)
        game_board.display_board(board)

        if game_board.check_winner(board, player2):
            game_over = True
    turn += 1
    turn = turn % 2