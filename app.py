from ursina import *
from game.board import GameBoard
# Import Agent specifically from the engine file
from game.rules import Rules
from game.test_engine import dumb_Agent

app = Ursina()
Sky(color=color.light_gray)
game = GameBoard()
EditorCamera()

# Initialize the agent using the imported class
my_ai = dumb_Agent(name="First_Available")

rules = Rules()
game_over = False

def update():
    global game_over

    if game_over:
        return

    winner = rules.get_winner(game.board_state)
    if winner:
        print(f"Player {winner} wins!")
        game_over = True
        return

    if rules.is_board_full(game.column_heights):
        print("It's a draw!")
        game_over = True
        return

    if game.turn_phase == 2:
        move = my_ai.get_move(game.board_state)
        if move:
            game.place_block(move['x'], move['z'])
        else:
            game.turn_phase = 1

app.run()