from microbit import *

BRIGHTNESS_PLAYER = 9
BRIGHTNESS_WALL = 6
BRIGHTNESS_INDICATOR = 3
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3


class Player:
    def __init__(self, maze):
        self.x = 0
        self.y = 0
        self.direction = DIR_DOWN
        self.update_possible_directions(maze)

    def change_direction(self):
        self.direction = (self.direction + 1) % 4
        while self.direction not in self.possible_directions:
            self.direction = (self.direction + 1) % 4

    def move(self, maze):
        self.x += DIRECTIONS[self.direction][0]
        self.y += DIRECTIONS[self.direction][1]
        self.update_possible_directions(maze)

    def update_possible_directions(self, maze):
        tile = maze.cells[self.x + self.y * maze.width]
        self.possible_directions = tile.get_directions()
        if self.direction not in self.possible_directions:
            self.direction = self.possible_directions[0]


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

    def get_directions(self):
        directions = []
        if self.up:
            directions += DIR_UP
        if self.right:
            directions += DIR_RIGHT
        if self.down:
            directions += DIR_DOWN
        if self.left:
            directions += DIR_LEFT
        return directions


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
        for i in range(len(list) - 1):
            self.open_path(list[i], list[i + 1])

    def open_path(self, a, b):
        if a[0] > b[0]:
            # a is right of b, open a's left side
            self.cells[a[0] + a[1] * 3].left = True
            # open b's right side
            self.cells[b[0] + b[1] * 3].right = True
        elif a[0] < b[0]:
            # a is left of b, open a's right side
            self.cells[a[0] + a[1] * 3].right = True
            # open b's left side
            self.cells[b[0] + b[1] * 3].left = True
        elif a[1] > b[1]:
            # a is down of b, open a's upside
            self.cells[a[0] + a[1] * 3].up = True
            # open b's downside
            self.cells[b[0] + b[1] * 3].down = True
        elif a[1] < b[1]:
            # a is up of b, open a's downside
            self.cells[a[0] + a[1] * 3].down = True
            # open b's upside
            self.cells[b[0] + b[1] * 3].up = True

    def render(self, offset, indicator_dir):
        # Create a "screen buffer"
        image = Image(5, 5)

        # Draw the walls of the maze
        for x in range(3):
            for y in range(3):
                tile_x = x + offset[0]
                tile_y = y + offset[1]
                # Check if the tile is out of bounds
                x_oob = tile_x < 0 or tile_x >= self.width
                y_oob = tile_y < 0 or tile_y >= self.height
                if x_oob or y_oob:
                    tile = Tile()
                else:
                    tile = self.cells[tile_x + tile_y * self.width]
                tile_image = tile.render()

                # Copy the tile to the "screen buffer"
                for tx in range(3):
                    for ty in range(3):
                        x_ = x * 2 + tx - 1
                        y_ = y * 2 + ty - 1
                        if x_ < 0 or y_ < 0 or x_ >= 5 or y_ >= 5:
                            continue
                        pixel = tile_image.get_pixel(tx, ty)
                        image.set_pixel(x_, y_, pixel)

        # Show the player in the middle of the screen
        image.set_pixel(2, 2, BRIGHTNESS_PLAYER)
        # Show the directional indicator (and blink it)
        if self.time % 2 == 0:
            indicator_x = 2 + 2 * DIRECTIONS[indicator_dir][0]
            indicator_y = 2 + 2 * DIRECTIONS[indicator_dir][1]
            image.set_pixel(indicator_x, indicator_y, BRIGHTNESS_INDICATOR)

        self.time += 1

        return image


def main():
    maze = Maze(3, 3)
    player = Player(maze)
    while True:
        if button_a.was_pressed():
            player.move(maze)
        if button_b.was_pressed():
            player.change_direction()
        display.show(maze.render((-1, -1), player.dir))
        sleep(300)


main()
