from blessed import Terminal
from PIL import Image

# Constants
IMAGE_WIDTH = 100
IMAGE_HEIGHT = 50

# Filepaths for images
# Text overlays have the same filepath, with "_overlay" appended
# All images are .png files and are saved in a "Resources" directory
# Images have a pixel size of 100x50
MENU_IMAGE_PATH = 'menu'

# Defines the options available on the menu
MENU_TEXTS = ['Box packing', 'Files', 'Game', 'Settings']

# Defines which text-overlay colors correspond to what
OVERLAY_COLORS = {
    (0, 0, 255, 255): MENU_TEXTS
}

def draw_image(terminal: Terminal, path: str) -> None:
    """
    Draws the provided image path to the terminal. Does not include text
    """
    menu_image = Image.open('Resources/' + path + '.png')
    pixels = [[menu_image.getpixel((x, y)) for x in range(IMAGE_WIDTH)] for y in range(IMAGE_HEIGHT)]
    for row in pixels:
        line = ''
        for pixel in row:
            # Double spaces to compensate for rectangular pixels
            line += terminal.on_color_rgb(*pixel) + '  '
        # print() is slow, which makes this method faster than printing each pixel individually
        print(line + terminal.normal)


def get_text(path: str) -> dict:
    """
    Processes a text overlay
    Returns: dictionary of colors (as tuples) and their coordinates
    """
    text_image = Image.open('Resources/' + path + '_overlay.png')
    # Compensates for double-width pixels
    # Nearest-neighbor resizing is used because color clarity is needed
    text_image = text_image.resize((IMAGE_WIDTH * 2, IMAGE_HEIGHT), Image.NEAREST)
    pixels = [[text_image.getpixel((x, y)) for x in range(IMAGE_WIDTH * 2)] for y in range(IMAGE_HEIGHT)]
    out = {}
    for x in range(IMAGE_WIDTH * 2):
        for y in range(IMAGE_HEIGHT):
            pixel = pixels[y][x]
            #If pixel is not white
            if pixel != (255, 255, 255, 255):
                if pixel in out:
                    out[pixel].append((x, y))
                    continue
                out[pixel] = [(x, y)]
    return out
    

def main() -> None:
    terminal = Terminal()
    print(terminal.clear)
    draw_image(terminal, MENU_IMAGE_PATH)
    menu_text = get_text(MENU_IMAGE_PATH)

    current_menu = 0

    for color in menu_text:
        coordinates = menu_text[color]
        text_width = coordinates[-1][0] - coordinates[0][0]
        text = OVERLAY_COLORS[color][current_menu].center(text_width)
        # Will be replaced with background checking later
        print(terminal.move_xy(*coordinates[0]) + terminal.black_on_bright_white(text), end='')
    

if __name__ == '__main__':
    main()