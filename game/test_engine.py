# game/test_engine.py
import numpy as np

class Agent:
    def __init__(self, name):
        self.name = name

    def get_move(self, board_state):
        # Always focuses on Layer 0
        layer_0 = board_state[0]
        for x in range(5):
            for z in range(5):
                if layer_0[x, z] == 0:
                    return {'x': x, 'z': z}
        return None