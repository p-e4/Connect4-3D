from ursina import *
from game.tmp_prototype_board import GameBoard
from game.test_engine import Agent  # Assuming your AI is here

app = Ursina()
game = GameBoard()
my_ai = Agent(name="StrategyAI") # Your Agent class

def update():
    # PHASE 1: Player Click
    # We do nothing here, the click event in GameBoard handles it.
    
    # PHASE 2: AI Move
    if game.turn_phase == 2:
        print("AI is thinking...")
        move = my_ai.get_move(game.board_state)
        
        if move:
            game.place_block(move['x'], move['z'])
        else:
            print("AI has no moves!")
            game.turn_phase = 1 # Reset to player if stuck