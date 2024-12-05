import arcade
import random
import PIL

# Constants for the game board dimensions
ROW_COUNT = 22
COLUMN_COUNT = 10

# Constants for the size of each block and the margin between blocks
WIDTH = 30
HEIGHT = 30
MARGIN = 5

# Constants for the screen dimensions and title
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Tetris"

# Define colors for the Tetris blocks
colors = [
    (0,   0,   0, 255),    # Color for empty space
    (255, 0,   0, 255),    # Color for shape 1
    (0,   150, 0, 255),    # Color for shape 2
    (216, 229, 247, 255),  # Color for shape 3
    (216, 238, 223, 255),  # Color for shape 4
    (242, 217, 239, 255),  # Color for shape 5
    (253, 241, 201, 255),  # Color for shape 6
    (254, 220, 219, 255)   # Color for shape 7
]

# Define the shapes of Tetris blocks
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

# Function to create textures for each color
def create_textures():
    new_textures = []
    for color in colors:
        # Create a new image with the specified color
        image = PIL.Image.new('RGBA', (WIDTH, HEIGHT), color)
        new_textures.append(arcade.Texture(str(color), image=image))
    return new_textures

# Create a list of textures for the colors
texture_list = create_textures()

# Function to rotate a Tetris shape counterclockwise
def rotate_counterclockwise(shape):
    return [[shape[y][x] for y in range(len(shape))]
            for x in range(len(shape[0]) - 1, -1, -1)]

# Function to check for collisions between the board and a shape
def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            if cell and board[cy + off_y][cx + off_x]:
                return True
    return False

# Function to remove a completed row from the board
def remove_row(board, row):
    del board[row]
    return [[0 for _ in range(COLUMN_COUNT)]] + board

# Function to join two matrices (the board and the shape)
def join_matrixes(matrix_1, matrix_2, matrix_2_offset):
    offset_x, offset_y = matrix_2_offset
    for cy, row in enumerate(matrix_2):
        for cx, val in enumerate(row):
            matrix_1[cy + offset_y - 1][cx + offset_x] += val
    return matrix_1

# Function to create a new game board filled with 0's
def new_board():
    board = [[0 for _x in range(COLUMN_COUNT)] for _y in range(ROW_COUNT)]
    # Add a bottom border of 1's to prevent shapes from falling off the board
    board += [[1 for _x in range(COLUMN_COUNT)]]
    return board

# Main game class
class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # Set the background color of the game
        arcade.set_background_color(arcade.color.WHITE)

        # Initialize game variables
        self.board = None
        self.frame_count = 0
        self.game_over = False
        self.paused = False
        self.board_sprite_list = None

        self.stone = None
        self.stone_x = 0
        self.stone_y = 0

    def new_stone(self):
        # Initializes a new Tetris stone (block) by randomly selecting a shape
        # Places it in the middle-top of the game board
        self.stone = random.choice(tetris_shapes)
        self.stone_x = int(COLUMN_COUNT / 2 - len(self.stone[0]) / 2)  # Horizontal position
        self.stone_y = 0  # Start at the top of the board

        # Check if the new stone collides immediately (game over condition)
        if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
            self.game_over = True


    def setup(self):
        # Initializes the game state, including the board and UI components
        self.board = new_board()  # Creates a blank Tetris board

        # Create sprites for visualizing the board
        self.board_sprite_list = arcade.SpriteList()
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                sprite = arcade.Sprite()
                for texture in texture_list:  # Add textures for the Tetris blocks
                    sprite.append_texture(texture)
                sprite.set_texture(0)  # Default texture (empty cell)
                sprite.center_x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2  # Sprite position (X)
                sprite.center_y = SCREEN_HEIGHT - (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2  # Sprite position (Y)

                self.board_sprite_list.append(sprite)

        # Load and start background music
        self.background_music = arcade.Sound("background_music.ogg")
        self.background_music.play(loop=True)

        self.new_stone()  # Create the first stone
        self.update_board()  # Sync the board state with visuals


    def drop(self):
        # Handles the downward movement of the current Tetris stone
        if not self.game_over and not self.paused:
            self.stone_y += 1  # Move the stone one row down

            # Check for collisions after moving the stone
            if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
                # Join the stone to the board
                self.board = join_matrixes(self.board, self.stone, (self.stone_x, self.stone_y))

                # Remove completed rows, if any
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:  # Row is full
                            self.board = remove_row(self.board, i)  # Remove row and shift
                            break
                    else:
                        break

                self.update_board()  # Update visuals
                self.new_stone()  # Generate a new stone


    def rotate_stone(self):
        # Rotates the current stone counterclockwise if possible
        if not self.game_over and not self.paused:
            new_stone = rotate_counterclockwise(self.stone)  # Calculate rotated stone

            # Adjust the position if the rotation goes out of bounds
            if self.stone_x + len(new_stone[0]) >= COLUMN_COUNT:
                self.stone_x = COLUMN_COUNT - len(new_stone[0])

            # Apply the rotation if no collision occurs
            if not check_collision(self.board, new_stone, (self.stone_x, self.stone_y)):
                self.stone = new_stone


    def on_update(self, dt):
        # Updates the game state at a regular interval (frame logic)
        self.frame_count += 1
        if self.frame_count % 10 == 0:  # Drop the stone every 10 frames
            self.drop()


    def move(self, delta_x):
        # Moves the stone horizontally (left/right) if possible
        if not self.game_over and not self.paused:
            new_x = self.stone_x + delta_x  # Calculate the new position

            # Ensure the stone stays within bounds
            if new_x < 0:
                new_x = 0
            if new_x > COLUMN_COUNT - len(self.stone[0]):
                new_x = COLUMN_COUNT - len(self.stone[0])

            # Move the stone if no collision occurs
            if not check_collision(self.board, self.stone, (new_x, self.stone_y)):
                self.stone_x = new_x


    def on_key_press(self, key, modifiers):
        # Handles keyboard input for controlling the stone
        if key == arcade.key.LEFT:
            self.move(-1)  # Move left
        elif key == arcade.key.RIGHT:
            self.move(1)  # Move right
        elif key == arcade.key.UP:
            self.rotate_stone()  # Rotate the stone
        elif key == arcade.key.DOWN:
            self.drop()  # Drop the stone


    def draw_grid(self, grid, offset_x, offset_y):
        # Draws a grid representation (used for stones and board)
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                if grid[row][column]:  # Draw non-empty cells
                    color = colors[grid[row][column]]  # Get the block color
                    x = (MARGIN + WIDTH) * (column + offset_x) + MARGIN + WIDTH // 2
                    y = SCREEN_HEIGHT - (MARGIN + HEIGHT) * (row + offset_y) + MARGIN + HEIGHT // 2

                    # Draw the cell as a filled rectangle
                    arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)


    def update_board(self):
        # Syncs the visual sprites with the logical board state
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                v = self.board[row][column]  # Get the value of the cell
                i = row * COLUMN_COUNT + column  # Calculate the index in the sprite list
                self.board_sprite_list[i].set_texture(v)  # Set the sprite texture


    def on_draw(self):
        # Renders the game visuals
        self.clear()  # Clear the screen
        self.board_sprite_list.draw()  # Draw the board sprites
        self.draw_grid(self.stone, self.stone_x, self.stone_y)  # Draw the current stone


def main():
    # Entry point for the game
    my_game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    my_game.setup()  # Set up the game
    arcade.run()  # Start the game loop


if __name__ == "__main__":
    main()