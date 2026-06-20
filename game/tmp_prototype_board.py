from ursina import *
from PIL import Image
import numpy as np

class GameBoard:
    def __init__(self, size=5, max_height=5):
        self.size = size
        self.max_height = max_height
        # Indexing: board_state[y, x, z]
        self.board_state = np.zeros((max_height, size, size), dtype=int)
        self.column_heights = np.zeros((size, size), dtype=int)
        self.turn_white = True
        
        self.turn_phase = 1

        self.tex_light = self._create_solid_texture((180, 140, 100))
        self.tex_dark = self._create_solid_texture((150, 110, 70))
        

        self.turn_number = 0
        self.movelist = [(0, 0), (1, 1), (2, 2)] # Pre-defined moves
        self.is_manual_turn = True # Toggle this to False for AI/Auto turns
        self._build_floor()

    def _create_solid_texture(self, rgb_tuple):
        img = Image.new('RGBA', (1, 1), color=(*rgb_tuple, 255))
        return Texture(img)


    def play_turn(self, x=None, z=None):
        """Processes a turn. If x/z is None, it pulls from movelist."""
        if x is None or z is None:
            if self.movelist:
                x, z = self.movelist.pop(0)
                print(f"Auto-playing from movelist: {x}, {z}")
            else:
                print("Movelist empty! Switching to manual.")
                self.is_manual_turn = True
                return

        # Place the block
        self.place_block(x, z)
        self.turn_number += 1
        # Toggle turn mode for the next turn
        self.is_manual_turn = not self.is_manual_turn

    def update_from_array(self, new_board_state):
        """
        Takes a (5, 5, 5) numpy array and updates the 3D scene 
        and the internal board state to match it.
        """
        # 1. Update internal state
        self.board_state = new_board_state
        
        # 2. Clear existing non-base entities (y > -0.5)
        for e in scene.entities:
            # We check the model to avoid deleting the floor or sky
            if e.position.y > -0.4 and e.model == 'cube':
                destroy(e)
                
        # 3. Rebuild based on new state
        for y in range(new_board_state.shape[0]):
            for x in range(new_board_state.shape[1]):
                for z in range(new_board_state.shape[2]):
                    val = new_board_state[y, x, z]
                    
                    if val != 0: # 1 for White, 2 for Black
                        color_to_use = color.white if val == 1 else color.black
                        self._create_bordered_block(x, y, z, color_to_use)
                        
        # 4. Update column_heights tracker to match the new array
        for x in range(self.size):
            for z in range(self.size):
                # Find the highest index that is not 0
                occupied = np.where(self.board_state[:, x, z] != 0)[0]
                self.column_heights[x, z] = occupied[-1] + 1 if len(occupied) > 0 else 0


    def _build_floor(self):
        for x in range(self.size):
            for z in range(self.size):
                tex = self.tex_light if (x + z) % 2 == 0 else self.tex_dark
                e = Entity(
                    parent=scene, position=(x, -0.5, z), model='cube', 
                    texture=tex, color=color.white, scale=(0.9, 0.1, 0.9),
                    collider='box', unlit=True
                )
                e.on_click = Func(self.place_block, x, z)

    def place_block(self, x, z):
        h = self.column_heights[x, z]
        
        if h < self.max_height:
            # 1. Update state: Layer (h) -> X -> Z
            self.board_state[h, x, z] = 1 if self.turn_white else 2
            
            # 2. Visuals
            color_to_use = color.white if self.turn_white else color.black
            self._create_bordered_block(x, h, z, color_to_use)
            
            # 3. Update internal trackers
            self.column_heights[x, z] += 1
            self.turn_white = not self.turn_white
            
            # 4. Cycle turn phase
            self.turn_phase = 2 if self.turn_phase == 1 else 1
            print(f"Turn phase cycled to: {self.turn_phase}")
            
            # 5. Debug output
            print(f"Layer {h} state:\n{self.board_state[h]}")
            
            # 6. Return the full board state
            return self.board_state
        else:
            print("Column full!")
            # IMPORTANT: Returning None explicitly ensures the loop knows the move failed
            return None

    def _create_bordered_block(self, x, y, z, color_val):
        cube = Entity(model='cube', color=color_val, position=(x, y, z), scale=0.9, unlit=True)
        # ... (edge data remains the same)
        edge_data = [
            (1.05, 0.05, 0.05, 0, -0.5, -0.5), (1.05, 0.05, 0.05, 0, -0.5, 0.5),
            (0.05, 0.05, 1.05, -0.5, -0.5, 0), (0.05, 0.05, 1.05, 0.5, -0.5, 0),
            (1.05, 0.05, 0.05, 0, 0.5, -0.5), (1.05, 0.05, 0.05, 0, 0.5, 0.5),
            (0.05, 0.05, 1.05, -0.5, 0.5, 0), (0.05, 0.05, 1.05, 0.5, 0.5, 0),
            (0.05, 1.05, 0.05, -0.5, 0, -0.5), (0.05, 1.05, 0.05, 0.5, 0, -0.5),
            (0.05, 1.05, 0.05, -0.5, 0, 0.5), (0.05, 1.05, 0.05, 0.5, 0, 0.5)
        ]
        for s_x, s_y, s_z, p_x, p_y, p_z in edge_data:
            Entity(parent=cube, model='cube', color=color.gray, scale=(s_x, s_y, s_z), position=(p_x, p_y, p_z), unlit=True)




