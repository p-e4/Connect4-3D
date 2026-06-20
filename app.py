from ursina import *
from game.tmp_prototype_board import GameBoard
# Import Agent specifically from the engine file
from game.test_engine import Agent 

app = Ursina()
Sky(color=color.light_gray)
game = GameBoard()
EditorCamera()

# Initialize the agent using the imported class
my_ai = Agent(name="StrategyAI") 

def update():
    # PHASE 2: AI Move
    if game.turn_phase == 2:
        # Give the AI a small frame-budget or delay if needed, 
        # but for now, it triggers immediately when phase is 2
        move = my_ai.get_move(game.board_state)
        
        if move:
            # game.place_block returns the state and cycles the turn to 1
            game.place_block(move['x'], move['z'])
            print(f"AI placed block at {move}")
        else:
            print("AI has no moves!")
            game.turn_phase = 1

app.run()