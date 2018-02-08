####################################################################################
# NOTE: This program has very bad variable names and the code is structured in     #
#       questionable ways. This is due to the memory limitations of the micro:bit, #
#       which resulted in some required trickery. Thank you for understanding.     #
####################################################################################

from microbit import display, button_a, button_b, sleep, Image
from gc import collect, mem_free
from random import choice

# Free up RAM if possible #
collect()

###########
# Globals #
###########
DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3


# Main function, this is ran at the bottom of the file #
def main():
    def generate_difficulty_img(diff):
        img = Image(5, 5)
        for i in range(diff + 1):
            for j in range(i + 1):
                img.set_pixel(i, 4 - j, 8)
        return img

    def render():
        nonlocal gpos
        nonlocal gdir
        nonlocal gmove
        cell_x = gpos[0] - 1
        cell_y = gpos[1] - 1
        s = render_cells((cell_x, cell_y), gmove)
        s.set_pixel(2, 2, 8)
        if time % 3 != 0 and gmove == (0, 0):
            x = DIRS[gdir][0] * 2
            y = DIRS[gdir][1] * 2
            s.set_pixel(2 + x, 2 + y, 4)
        gmove = (0, 0)
        return s

    def process_input():
        nonlocal gpos
        nonlocal gdir
        nonlocal gmove
        if button_a.was_pressed():
            gmove = DIRS[gdir]
            gpos[0] += DIRS[gdir][0]
            gpos[1] += DIRS[gdir][1]
            # Re-direct if previous gdir is no longer possible
            possible_dirs = get_passages(gpos[0], gpos[1])
            while gdir not in possible_dirs:
                gdir = (gdir + 1) % 4
        if button_b.was_pressed():
            possible_dirs = get_passages(gpos[0], gpos[1])
            gdir = (gdir + 1) % 4
            while gdir not in possible_dirs:
                gdir = (gdir + 1) % 4

    def is_win():
        nonlocal gpos
        global g_w
        global g_h
        if gpos[0] == g_w - 1 and gpos[1] == g_h - 1:
            return True
        else:
            return False

    current_diff = 0
    while True:
        # Difficulty selector #
        while True:
            display.show(generate_difficulty_img(current_diff))
            if button_b.was_pressed():
                current_diff = (current_diff + 1) % 5
            if button_a.was_pressed():
                break

        # The actual game #
        time = 0
        gdir = DIR_RIGHT
        gpos = [0, 0]
        gmove = (0, 0)
        generate_cells(2 + current_diff)

        while not is_win():
            process_input()
            display.show(render())
            time += 1
            sleep(50)
        display.show(Image.HAPPY)
        sleep(2000)


#############
# Map stuff #
#############
cells = []
g_w = 0
g_h = 0


def generate_cells(size):
    global g_w
    global g_h
    global cells
    g_w = size
    g_h = size
    cells = [False] * size**2 * 2
    for i in range(size**2):
        generate_cell(i % size, int(i / size))


def generate_cell(x, y):
    dirs = []
    if x > 0:
        dirs.append(DIR_LEFT)
    if y > 0:
        dirs.append(DIR_UP)
    if len(dirs) > 0:
        direction = choice(dirs)
        x2 = x + DIRS[direction][0]
        y2 = y + DIRS[direction][1]
        create_passage((x, y), (x2, y2))


def create_passage(fc, tc):
    global g_w
    global cells
    if fc[0] < tc[0]:
        # "From" cell is left from "to", so set its right to open
        cells[fc[0] + fc[1] * 2 * g_w] = True
    if fc[0] > tc[0]:
        # "From" cell is right from "to", so set "to's" right to open
        cells[tc[0] + tc[1] * 2 * g_w] = True
    if fc[1] < tc[1]:
        # "From" cell is up from "to", so set its down to open
        cells[fc[0] + (fc[1] * 2 + 1) * g_w] = True
    if fc[1] > tc[1]:
        # "From" cell is down from "to", so set "to's" down to open
        cells[tc[0] + (tc[1] * 2 + 1) * g_w] = True


def get_cell(x, y, down):
    global cells
    global g_w
    global g_h
    y *= 2
    if down:
        y += 1
    if x < 0 or y < 0 or x >= g_w or y >= g_h * 2:
        return False
    else:
        return cells[x + y * g_w]


def get_passages(x, y):
    dirs = []
    if get_cell(x, y - 1, True):
        dirs.append(DIR_UP)
    if get_cell(x - 1, y, False):
        dirs.append(DIR_LEFT)
    if get_cell(x, y, True):
        dirs.append(DIR_DOWN)
    if get_cell(x, y, False):
        dirs.append(DIR_RIGHT)
    return dirs


def render_cells(coff, poff):
    global g_w
    global g_h
    screen = Image(5, 5)

    def render_cell(x, y, b):
        i = Image(3, 3)
        for i_x in range(3):
            for i_y in range(3):
                i.set_pixel(i_x, i_y, 6)
        dirs = get_passages(x, y)
        if len(dirs) > 0:
            i.set_pixel(1, 1, 9 if b else 0)
        if DIR_UP in dirs:
            i.set_pixel(1, 0, 0)
        if DIR_LEFT in dirs:
            i.set_pixel(0, 1, 0)
        if DIR_DOWN in dirs:
            i.set_pixel(1, 2, 0)
        if DIR_RIGHT in dirs:
            i.set_pixel(2, 1, 0)
        return i

    for cbx in range(3):
        for cby in range(3):
            cx = cbx + coff[0]
            cy = cby + coff[1]
            cimage = render_cell(cx, cy, cx == g_w - 1 and cy == g_h - 1)
            for scx in range(3):
                for scy in range(3):
                    sx = cbx * 2 + scx - 1 + poff[0]
                    sy = cby * 2 + scy - 1 + poff[1]
                    x_oob = sx < 0 or sx >= 5
                    y_oob = sy < 0 or sy >= 5
                    if x_oob or y_oob:
                        continue
                    pixel = cimage.get_pixel(scx, scy)
                    screen.set_pixel(sx, sy, pixel)
    return screen


# Execution #
main()
