#game/board_3D.py
""" Handles 3D rendering of objects, keep tracks of boardstate, places moves based on cords given"""

# ------------------------ #
#         Imports          #
# ------------------------ #

from ursina import *
from PIL import Image
import numpy as np
from typing import Dict, Union, Any, Tuple
import numpy.typing as npt
import inspect
import os


# ------------------------ #
#          README          #
# ------------------------ #

# Here is a list of available methods to talk to:
# update_from_array -> mirrors array to board
# place_block -> places a single block on board
# get_board_state -> NOTE not added yet currently directly grabs self.board_state


# ------------------------ #
#         Settings         #
# ------------------------ #
trace_back = False # Used for showing where each method is being called from (And every instance of call)



# ------------------------ #
#           Code           #
# ------------------------ #

class GameBoard:
    def __init__(self, size=5, max_height=5):

        # Board Creation
        self.size = size
        self.max_height = max_height
        self.board_state = np.zeros((max_height, size, size), dtype=int) #Indexing: board_state[y, x, z]
        self.column_heights = np.zeros((size, size), dtype=int)

        # Turn Handling
        self.turn_white = True
        self.turn_phase = 1
        self.turn_number = 0

        # Texture (For floor)
        self.tex_light = self._create_solid_texture((180, 140, 100))
        self.tex_dark = self._create_solid_texture((150, 110, 70))

        # Builds board floor (duh)
        self._build_floor()

    # ------------------------ #
    #          Utils           #
    # ------------------------ #

    def _create_solid_texture(self, rgb_tuple):
        """ Creates texture, used for RGB coloring on blocks """

        img = Image.new('RGBA', (1, 1), color=(*rgb_tuple, 255))
        return Texture(img)


    def _build_floor(self):
        """ Builds floor of board """
        
        for x in range(self.size):
            for z in range(self.size):
                tex = self.tex_light if (x + z) % 2 == 0 else self.tex_dark
                e = Entity(
                    parent=scene, position=(x, -0.5, z), model='cube', 
                    texture=tex, color=color.white, scale=(0.9, 0.1, 0.9),
                    collider='box', unlit=True
                )
                e.on_click = Func(self.place_block, x, z)

    def _create_bordered_block(self, x: int, y: int, z: int, color_val: color):
        """ 
        Creates blocks for placement <br>
        Uses edge data to create the edges.


        :arg x, y, z: Where to place the block
        :arg color_val: The color you want the block to be (usually black or white) Example: color.white

        """

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


    def _debug(self) -> Tuple[str, str, str]:
        """ 
        Runs debugging based on settings. This should be called once at top of each code 
        
        :return: funct_name, file_name, file_line of method calling this
        """
        funct_name, file_name, file_line = self._trace_back()


        return funct_name, file_name, file_line

    @staticmethod
    def _trace_back():
        """Runs debugging based on settings. Called from the target code."""
        # stack()[2] is the caller of the helper (_debug)
        # stack()[3] is the caller of the caller (one layer higher)
        caller_of_caller = inspect.stack()[2]
        target_caller = inspect.stack()[3]
        
        funct_name = caller_of_caller.function
        file_name = os.path.basename(caller_of_caller.filename)
        file_line = caller_of_caller.lineno
        
        caller_funct_name = target_caller.function
        caller_file_name = os.path.basename(target_caller.filename)
        caller_file_line = target_caller.lineno
        
        if trace_back: print(f"{file_name}/{funct_name}() called by {caller_funct_name}() in {caller_file_name} at line {caller_file_line}")
        return file_name, funct_name, file_line


    # ------------------------ #
    #           Logic          #
    # ------------------------ #

    def update_from_array(self, new_board_state: np.array):
        """
        Takes a (5, 5, 5) numpy array and updates the 3D scene 
        and the internal board state to match it. (this overwrites the current board state)

        :arg new_board_state: Board has 3 axis, uses 3d array from numpy. Stored as list of 5x5 boards 5 times. <br>
        Each 5x5 board corresponds to a layer. layer 0 = [0 (this is the layer), 0, 0] 

        """

        file_name, funct_name, file_line = self._debug()

        try:
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

        except Exception as e:
            print(f"[Error] File:{file_name}, Function:{funct_name}, Line:{file_line}, Error:{e}")

    def place_block(self, x, z) -> Dict[str, Union[bool, npt.NDArray[np.int8]]]:
        """ 
        Places a block based on x and y cordinate <br>
        Will try to place a block ontop of another block if space is occupied. (Up to max of _ hight usually 5) <br>
        Also handles Cycling of turns after placing move

        :arg x: X cordinate
        :arg y: Y cordinate

        :return: Returns dict with success and board state as an numpy array (5x5x5), <br> 
        Returns False on success if fail or if move invalid exmaple: {'success':True, 'data':self.board_state, 'error':''}

        """

        file_name, funct_name, file_line = self._debug()

        try: 
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

                self.turn_number = self.turn_number + 1
                print(f"Turn number is: {self.turn_number}")

                # 5. Debug output
                print(f"Layer {h} state:\n{self.board_state[h]}")
                
                # 6. Return the full board state
                return {'success':True, 'data':self.board_state, 'error':''}
            else:
                print("Column full!")
                return {'success':False, 'data':self.board_state, 'error':''}
            
        except Exception as e:
            print(f"[Error] File:{file_name}, Function:{funct_name}, Line:{file_line}, Error:{e}")
            return {'success':False, 'data':self.board_state, 'error':e}
        
    def get_board_state(self):
        """ Returns boardstate as 3d np array """
        return self.board_state




