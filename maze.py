from microbit import *

BRIGHTNESS_PLAYER = 9
BRIGHTNESS_WALL = 6
BRIGHTNESS_INDICATOR = 2


class Tile:
    def __init__(self):
        self.up = False
        self.right = False
        self.down = False
        self.left = False

    def render(self):
        image = Image(3, 3)
        for x in range(3):
            for y in range(3):
                image.set_pixel(x, y, BRIGHTNESS_WALL)
        if self.up or self.right or self.down or self.left:
            image.set_pixel(1, 1, 0)
        if self.up:
            image.set_pixel(1, 0, 0)
        if self.right:
            image.set_pixel(2, 1, 0)
        if self.down:
            image.set_pixel(1, 2, 0)
        if self.left:
            image.set_pixel(0, 1, 0)
        return image


class Maze:
    def __init__(self, width, height):
        self.cells = []
        self.width = width
        self.height = height
        self.time = 0
        for x in range(width):
            for y in range(height):
                self.cells.append(Tile())
        self.open_paths([(0, 0), (0, 1), (0, 2), (1, 2),
                         (2, 2), (2, 1), (2, 0), (1, 0), (1, 1)])

    def open_paths(self, list):
        # Given a list [a, b, c, d], open the paths between the following:
        # a <-> b, b <-> c, c <-> d
        for i in range(len(list) - 1):
            self.open_path(list[i], list[i + 1])

    def open_path(self, a, b):
        if a[0] > b[0]:
            # a is right of b
            # open a's left side
            self.cells[a[0] + a[1] * 3].left = True
            # open b's right side
            self.cells[b[0] + b[1] * 3].right = True
        elif a[0] < b[0]:
            # a is left of b
            # open a's right side
            self.cells[a[0] + a[1] * 3].right = True
            # open b's left side
            self.cells[b[0] + b[1] * 3].left = True
        elif a[1] > b[1]:
            # a is down of b
            # open a's upside
            self.cells[a[0] + a[1] * 3].up = True
            # open b's downside
            self.cells[b[0] + b[1] * 3].down = True
        elif a[1] < b[1]:
            # a is up of b
            # open a's downside
            self.cells[a[0] + a[1] * 3].down = True
            # open b's upside
            self.cells[b[0] + b[1] * 3].up = True

    def render(self, x_offs, y_offs):
        # Create a "screen buffer"
        image = Image(5, 5)

        # Draw the walls of the maze
        for x in range(3):
            for y in range(3):
                # Calculate the tile positions (apply offsets)
                tile_x = x + x_offs
                tile_y = y + y_offs
                # Check if the tile is out of bounds
                x_out_of_index = tile_x < 0 or tile_x >= self.width
                y_out_of_index = tile_y < 0 or tile_y >= self.height
                if x_out_of_index or y_out_of_index:
                    # Out of bounds, set the tile to the default tile
                    tile = Tile()
                else:
                    # Get the tile (since we're in bounds)
                    tile = self.cells[tile_x + tile_y * self.width]
                # Render the tile
                tile_image = tile.render()

                # Copy the tile to the "screen buffer"
                for tx in range(3):
                    for ty in range(3):
                        # Calculate the "screen buffer" position
                        x_ = x * 2 + tx - 1
                        y_ = y * 2 + ty - 1
                        # Check "screen buffer" bounds
                        if x_ < 0 or y_ < 0 or x_ >= 5 or y_ >= 5:
                            continue
                        # Copy the pixel
                        pixel = tile_image.get_pixel(tx, ty)
                        # Paste the pixel
                        image.set_pixel(x_, y_, pixel)

        # Show the player in the middle of the screen
        image.set_pixel(2, 2, BRIGHTNESS_PLAYER)
        # Show the directional indicator (and blink it)
        if self.time % 2 == 0:
            image.set_pixel(2, 4, BRIGHTNESS_INDICATOR)
        # Update the timer
        self.time += 1

        # Return the rendered "view"
        return image


def main():
    maze = Maze(3, 3)
    while True:
        display.show(maze.render(-1, -1))
        sleep(300)


main()
