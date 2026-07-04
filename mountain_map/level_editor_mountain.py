import pygame
import pygame_widgets
from pygame_widgets.button import Button
import csv

pygame.init()

level_info = {
    0: {"name": "mountain", "folder": "mountain_map"},
    1: {"name": "desert",   "folder": "desert_map"},
    2: {"name": "jungle",   "folder": "jungle_map"},
    3: {"name": "snow",     "folder": "snow_map"}
}

# Game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = (SCREEN_WIDTH * 0.8)
LOWER_MARGIN = 100
SIDE_MARGIN = 300
#variable screen made to store the game window dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption("Level Editor")

SAVE_DIR = r"c:/pyhton_nea\Adventure_shooting_assets/img/mountain_map"
FILE_NAME = "level0.csv"
FULL_PATH = f"{SAVE_DIR}/{FILE_NAME}"


# Define game variables
ROWS = 20
MAX_COLS = 25
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 19
level = 0 
current_tile = 0
scroll = 0
scroll_speed = 0
cloud_scroll = 0



# Store tiles in a list
import os # Add this at the very top of your script



save_img = pygame.image.load(r"c:\pyhton_nea\Adventure_shooting_assets\img\icons\save_btn.png")
load_img = pygame.image.load(r"c:\pyhton_nea\Adventure_shooting_assets\img\icons\load_btn.png")

GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

# Define font
font = pygame.font.SysFont("comic sans", 30)

# Create empty tile list 

# Create a grid of -1(no tile) to represent an empty level
world_data = []
for r in range(ROWS):
    row = [-1] * MAX_COLS
    world_data.append(row)

# fills the grid with the csv data
try:
    with open("level0.csv", newline="") as file:
        reader = csv.reader(file)

        for r_idx, csv_row in enumerate(reader):
            for c_idx, item in enumerate(csv_row):
                if r_idx < ROWS and c_idx < MAX_COLS:
                    # Clean the data and turn it into an integer
                    if item.strip():
                        world_data[r_idx][c_idx] = int(item)
    print("Level loaded successfully!")
except Exception as e:
    # If the file is blank or missing, it just stays as the -1 grid we made above
    print(f"Starting with a fresh blank level. (Reason: {e})")


# Function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Create function for drawing background
def draw_bg():
    global cloud_scroll
    # draw Scrolling Sky
    if sky_img:
        screen.blit(sky_img, (cloud_scroll, 0))
        screen.blit(sky_img, (cloud_scroll + SCREEN_WIDTH, 0))

    for index, img in enumerate(bg_images):
            if index == 0:
                # MOUNTAIN: Lift it way up so the peaks are visible
                # Increase -150 to lift it even higher
                y_pos = SCREEN_HEIGHT - img.get_height() - 100 
            else:
                # PINES: Keep them lower on the horizon
                y_pos = SCREEN_HEIGHT - img.get_height() - 20
                
            screen.blit(img, (0 - (scroll * 0.5), y_pos))

    # Update the Sky movement
    cloud_scroll -= 0.3  # Slow drift speed
    if abs(cloud_scroll) >= SCREEN_WIDTH:
        cloud_scroll = 0
    
# Draw grid
def draw_grid():
    # Vertical lines shift with scroll
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    for r in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, r * TILE_SIZE), (SCREEN_WIDTH, r * TILE_SIZE))

def save_level():
    info = level_info.get(level)
    folder = info["folder"]
    name = info["name"]
    full_path = rf"c:\pyhton_nea\Adventure_shooting_assets\img\{folder}\{name}_level{level}.csv"
    
    with open(full_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for row in world_data:
            writer.writerow(row)
    print(f"Saved: {full_path}")

def load_level():
    global world_data
    info = level_info.get(level)
    folder = info["folder"]
    name = info["name"]
    full_path = rf"c:\pyhton_nea\Adventure_shooting_assets\img\{folder}\{name}_level{level}.csv"
    
    try:
        with open(full_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    if x < len(world_data) and y < len(world_data[0]):
                        world_data[x][y] = int(tile)
        print(f"Loaded: {full_path}")
    except FileNotFoundError:
        print(f"Error: {full_path} not found. Draw something and save first!")


def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                # This is the Safety 
                # It checks if the number 'tile' is actually inside the img_list
                if tile < len(img_list):
                    screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))
                else:
                    # If it finds a bad number, it prints it so you know which one is broken
                    print(f"Error: Tile {tile} doesn't exist! Fixing it to -1.")
                    world_data[y][x] = -1

def set_current_tile(tile_index):
    global current_tile
    current_tile = tile_index

def reset_world():
    for row in range(ROWS):
        for col in range(MAX_COLS):
            world_data[row][col] = -1
    for tile in range(0, MAX_COLS):
        world_data[ROWS - 1][tile] = 0

# Create buttons
save_btn = Button(screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, 150, 40, 
                  image=save_img, onRelease=save_level)

load_btn = Button(screen, SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, 150, 40, 
                  image=load_img, onRelease=load_level)

# Make a button list
button_list = []
button_col = 0
button_row = 0

img_list = []
bg_images = []
sky_img = None

for i in range(len(img_list)):
    tile_button = Button(
        screen, 
        SCREEN_WIDTH + (75 * button_col) + 50, 
        (75 * button_row) + 50, 
        40, 
        40, 
        image=img_list[i],
        onRelease=lambda x=i: set_current_tile(x)
    )
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

# defines the function to load the tile images based on the current level
def load_tile_images(level_index):
    global img_list, bg_images, sky_img
    
    info = level_info.get(level_index)
    folder = info["folder"]
    folder_path = rf"c:\pyhton_nea\Adventure_shooting_assets\img\{folder}"
    
    # Load Tiles
    img_list = []
    for x in range(TILE_TYPES):
        tile_path = os.path.join(folder_path, f"{x}.png")
        img = pygame.image.load(tile_path).convert_alpha()
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        img_list.append(img)
    
    # Load Sky
    sky_img = pygame.image.load(os.path.join(folder_path, "sky.png")).convert_alpha()
    sky_img = pygame.transform.scale(sky_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load Dynamic BG Layers
# dynamic background layers

    bg_images = []
    i = 0
    while os.path.exists(os.path.join(folder_path, f"bg{i}.png")):
        img = pygame.image.load(os.path.join(folder_path, f"bg{i}.png")).convert_alpha()
        
        w = img.get_width()
        h = img.get_height()
        ratio = SCREEN_WIDTH / w
        
        # If it's the first layer (Mountain), make it huge!
        if i == 0:
            scale_factor = 2.0  # Double the height
        else:
            scale_factor = 1.2  # Keep pines smaller
            
        new_height = int(h * ratio * scale_factor)
        img = pygame.transform.scale(img, (SCREEN_WIDTH, new_height))
        bg_images.append(img)
        i += 1

    # Update sidebar buttons if they exist
    if 'button_list' in globals():
        for i, btn in enumerate(button_list):
            btn.image = img_list[i]

# create buttons

button_list = []
button_col = 0
button_row = 0
for i in range(TILE_TYPES):
    tile_button = Button(
        screen, 
        SCREEN_WIDTH + (75 * button_col) + 50, 
        (75 * button_row) + 50, 
        40, 
        40, 
        image=pygame.Surface((40, 40)), # Placeholder until load_tile_images runs
        onRelease=lambda x=i: set_current_tile(x)
    )
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

#initial load
load_tile_images(level)

run = True
while run:
    event_list = pygame.event.get()

    # Draw the world first
    draw_bg()
    draw_grid()
    draw_world()

    #  Draw Panels
    pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT, SCREEN_WIDTH + SIDE_MARGIN, LOWER_MARGIN))
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))


# Draw the TEXT
    info = level_info.get(level, {"name": "unknown", "folder": "unknown"})
    current_map_name = info["name"].upper()
    
    draw_text(f"LEVEL: {level} - {current_map_name}", font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text(f"Press UP/DOWN to switch maps", font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

    #  Highlight selected button
    selected_button = button_list[current_tile]
    pygame.draw.rect(screen, RED, (selected_button.getX(), selected_button.getY(), 
                                   selected_button.getWidth(), selected_button.getHeight()), 3)

    #Mouse position and logic
    pos = pygame.mouse.get_pos()
    x = (pos[0]) // TILE_SIZE
    y = (pos[1]) // TILE_SIZE

    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        # Add scroll to pos[0] so we select the correct column in world_data
        x = (pos[0] + scroll) // TILE_SIZE 
        y = (pos[1]) // TILE_SIZE

        if pygame.mouse.get_pressed()[0] == 1:
            world_data[int(y)][int(x)] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[int(y)][int(x)] = -1
        if scroll_speed < 0 and scroll > 0:
            scroll += scroll_speed
        if scroll_speed > 0 and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
            scroll += scroll_speed

    for event in event_list:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if level < 3:
                    level += 1
                    load_tile_images(level)
                    load_level() 
            if event.key == pygame.K_DOWN:
                if level > 0:
                    level -= 1
                    load_tile_images(level)
                    load_level()             
            if event.key == pygame.K_LEFT:
                scroll_speed = -5
            if event.key == pygame.K_RIGHT:
                scroll_speed = 5                
            if event.key == pygame.K_c: # Added 'C' to manually clear world
                reset_world()
            if event.key == pygame.K_s:
                save_level()
                ("print world saved")
            if event.key == pygame.K_l:
                load_level()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                scroll_speed = 0




    pygame_widgets.update(event_list)
    pygame.display.update()

pygame.quit()