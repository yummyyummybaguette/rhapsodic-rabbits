from pathlib import Path
from typing import Union, Tuple, List

from PIL import Image
from blessed import Terminal

# Constants
IMAGE_WIDTH = 100
IMAGE_HEIGHT = 50

# Filepaths for images
# Text overlays have the same filepath, with "_overlay" appended
# All images are .png files and are saved in a "Resources" directory
# Images have a pixel size of 100x50
MENU_BASE_PATH = Path('menu')

# Defines the options available on the menu
MENU_TEXTS = ['Box packing', 'Files', 'Game', 'Settings']

# Defines what function each menu option points to
# TODO Create menu functions
MENU_FUNCTIONS = {
    'Box packing': None,
    'Files': None,
    'Game': None,
    'Settings': None
}

# Defines which text-overlay colors correspond to what
OVERLAY_COLORS = {
    (0, 0, 255, 255): MENU_TEXTS,
    (255, 0, 0, 255): 'Left',
    (0, 255, 0, 255): 'Right'
}


def get_pixels(image_path: Union[str, Path], size: Tuple[int, int]) -> list:
    """
    Gets the pixels of an image for the provided filepath, after resizing

    Returns: two-dimensional list of image pixels
    """
    # convert what is potentially just a string into a real Path object
    image_path = Path(image_path) if not isinstance(image_path, Path) else image_path
    im = Image.open(image_path.as_posix())

    # Compensates for half-width pixels
    # Nearest-neighbor resizing is used because color clarity is needed
    im = im.resize(size, Image.NEAREST)
    width, height = size
    return [[im.getpixel((x, y)) for x in range(width)] for y in range(height)]


def draw_image(terminal: Terminal, pixels: list) -> None:
    """Draws the provided pixels to the terminal"""
    for row in pixels:
        line = ''
        for pixel in row:
            line += terminal.on_color_rgb(*pixel) + ' '
        # print() is slow, which makes this method faster than printing each pixel individually
        print(line + terminal.normal)


def get_text(pixels: list) -> dict:
    """
    Processes a text overlay from the provided pixels

    Returns: dictionary of colors (as tuples) and their coordinates
    """
    out = {}
    for y, row in enumerate(pixels):
        for x, pixel in enumerate(row):
            # If pixel is not white
            if pixel != (255, 255, 255, 255):
                if pixel in out:
                    out[pixel].append((x, y))
                    continue
                out[pixel] = [(x, y)]
    return out


def update_menu(terminal: Terminal, current_menu: int, menu_text: dict, menu_pixels: list) -> None:
    """
    Updates the text of the menu

    Does not redraw each pixel of the menu, just the text
    """
    # Loops the menu back on itself
    current_menu %= len(MENU_TEXTS)
    for color in menu_text:
        pixels = menu_text[color]
        text_type = type(OVERLAY_COLORS[color])
        if text_type == list:
            text = OVERLAY_COLORS[color][current_menu].center(len(pixels))
        else:
            text = OVERLAY_COLORS[color].center(len(pixels))
        start = pixels[0]
        # Does not work with multi-colored backgrounds
        background_color = menu_pixels[start[1]][start[0]]
        print(terminal.move_xy(*start) + terminal.on_color_rgb(*background_color) + terminal.black(text))


def main() -> None:
    """Creates basic menu functionality"""
    terminal = Terminal()
    print(terminal.clear, end='')
    current_menu = 0

    # size = (terminal.width, terminal.height)
    size = (IMAGE_WIDTH * 2, IMAGE_HEIGHT)
    menu_pixels = get_pixels(MENU_BASE_PATH / 'Resources' / 'menu.png', size)
    menu_text_pixels = get_pixels(MENU_BASE_PATH / 'Resources' / 'menu_overlay.png', size)
    menu_text = get_text(menu_text_pixels)
    draw_image(terminal, menu_pixels)
    update_menu(terminal, current_menu, menu_text, menu_pixels)
    # Control loop
    with terminal.cbreak():
        key = terminal.inkey(timeout=0)
        while key.name != 'KEY_ESCAPE':
            key = terminal.inkey(timeout=0)
            if key.name == 'KEY_LEFT':
                current_menu -= 1
                update_menu(terminal, current_menu, menu_text, menu_pixels)
            elif key.name == 'KEY_RIGHT':
                current_menu += 1
                update_menu(terminal, current_menu, menu_text, menu_pixels)
        print(terminal.clear + 'Exiting!', end='')


if __name__ == '__main__':
    main()