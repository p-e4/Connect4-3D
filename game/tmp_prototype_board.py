from ursina import *
from PIL import Image

app = Ursina()

# --- HELPER: GENERATE SOLID TEXTURES ---
def create_solid_texture(rgb_tuple):
    img = Image.new('RGBA', (1, 1), color=(*rgb_tuple, 255))
    return Texture(img)

# Define our wood colors
wood_light_rgb = (180, 140, 100)
wood_dark_rgb = (150, 110, 70)

# Pre-generate textures
tex_light = create_solid_texture(wood_light_rgb)
tex_dark = create_solid_texture(wood_dark_rgb)

# --- LIGHTER BACKGROUND ---
Sky(color=color.light_gray)

# Grid configuration
GRID_SIZE = 5
MAX_HEIGHT = 5
column_heights = {(x, z): 0 for x in range(GRID_SIZE) for z in range(GRID_SIZE)}
turn_white = True

def create_bordered_block(x, y, z, color_val):
    # Main block: We use the same unlit texture logic here to keep colors consistent
    cube = Entity(model='cube', color=color_val, position=(x, y, z), scale=0.9, unlit=True)
    
    # Define the 12 edges for the border
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
    
    return cube

def place_block(x, z):
    global turn_white
    h = column_heights[(x, z)]
    
    if h < MAX_HEIGHT:
        # Use simple color for the stackable blocks
        color_to_use = color.white if turn_white else color.black
        create_bordered_block(x, h, z, color_to_use)
        
        column_heights[(x, z)] += 1
        turn_white = not turn_white
    else:
        print("Column full!")

# --- ALTERNATING WOOD BASE ---
for x in range(GRID_SIZE):
    for z in range(GRID_SIZE):
        # Choose texture based on grid position
        tex = tex_light if (x + z) % 2 == 0 else tex_dark
        
        e = Entity(
            parent=scene, 
            position=(x, -0.5, z), 
            model='cube', 
            texture=tex,
            color=color.white, # Texture is already colored, tint white
            scale=(0.9, 0.1, 0.9),
            collider='box',
            unlit=True
        )
        e.on_click = Func(place_block, x, z)

EditorCamera()
app.run()