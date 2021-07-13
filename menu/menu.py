from pathlib import Path
from typing import Dict, List, Tuple, Union

from blessed import Terminal
from PIL import Image

# Constants
IMAGE_WIDTH = 100
IMAGE_HEIGHT = 50

# Filepaths for images
# Text overlays have the same filepath, with "_overlay" appended
# All images are .png files and are saved in a "Resources" directory
# Images have a pixel size of 100x50
MENU_BASE_PATH = Path('menu')

# Defines what function each menu option points to
# TODO Create menu functions
MENU_FUNCTIONS = {
    'Box packing': None,
    'Files': None,
    'Game': None,
    'Settings': None
}

# Defines the options available on the menu
MENU_TEXTS = list(MENU_FUNCTIONS.keys())

# Defines which text-overlay colors correspond to what
OVERLAY_COLORS = {
    (0, 0, 255, 255): MENU_TEXTS,
    (255, 0, 0, 255): 'Left',
    (0, 255, 0, 255): 'Right'
}


class Menu:
    """Graphical menu for terminal windows

    Renders pre-existing images in a terminal window.
    Overlays text on the menu using colors in another pre-existing image to determine the text locations
    """

    def __init__(self,
                 terminal: Terminal,
                 background: Union[str, Path],
                 size: Tuple[int, int] = (IMAGE_WIDTH, IMAGE_HEIGHT)):
        self.terminal: Terminal = terminal
        size = (size[0] * 2, size[1])
        self.background_pixels = get_pixels(background, size)
        overlay_path = background.with_name(f'{background.stem}_overlay{background.suffix}')
        self.text_pixels = get_pixels(overlay_path, size)
        self.overlay_positions = color_positions(self.text_pixels)
        self.selection = 0
        self.draw_background()
        self.draw_menu_text()

    def draw_background(self) -> None:
        """Renders the background image in the terminal"""
        if not hasattr(self, 'origin'):
            self.origin = self.terminal.get_location()
        else:
            self.terminal.move_xy(*self.origin)

        with self.terminal.location():
            draw_image(self.terminal, self.background_pixels)

    def draw_menu_text(self) -> None:
        """Overlays text on the background image using colors in the overlay image"""
        for color, text in OVERLAY_COLORS.items():
            if isinstance(text, list):
                text = MENU_TEXTS[self.selection % len(MENU_TEXTS)]
            coords = self.overlay_positions[color]
            text = text.center(len(coords))
            backgrounds = (self.get_color(x, y) for x, y in coords)

            start_x, start_y = self.origin
            offset_x, offset_y = coords[0]

            res = self.terminal.move_xy(x=start_x+offset_x, y=start_y+offset_y)
            res += ''.join(
                self.terminal.on_color_rgb(*bg) + self.terminal.black(char)
                for char, bg in zip(text, backgrounds)
            )
            print(res)

    def get_color(self, x: int, y: int) -> Tuple[int, int, int, int]:
        """Gets the 4 number color Tuple at given coordinates in the rendered background image"""
        return self.background_pixels[y][x]


def get_pixels(image_path: Union[str, Path], size: Tuple[int, int]) -> List[List[Tuple[int, int, int, int]]]:
    """
    Gets the pixels of an image for the provided background, after resizing

    Returns: List[List[Tuple[int, int, int, int]]]
        two-dimensional list of image pixels
    """
    # convert what is potentially just a string into a real Path object
    image_path = Path(image_path) if not isinstance(image_path, Path) else image_path
    im = Image.open(image_path.as_posix())

    # Compensates for half-width pixels
    # Nearest-neighbor resizing is used because color clarity is needed
    im = im.resize(size, Image.NEAREST)
    return [[im.getpixel((x, y)) for x in range(im.width)] for y in range(im.height)]


def draw_image(terminal: Terminal, pixels: List[List[Tuple[int, int, int, int]]]) -> None:
    """Draws the provided pixels to the terminal"""
    print('\n'.join(
        ''.join(
            terminal.on_color_rgb(*pixel) + ' '
            for pixel in row
        )
        for row in pixels
    ))


def color_positions(
        pixels: List[List[Tuple[int, int, int, int]]]
) -> Dict[Tuple[int, int, int, int], List[Tuple[int, int]]]:
    """
    Processes a text overlay from the provided pixels

    Returns: Dict[Tuple[int, int, int, int], List[Tuple[int, int]]]
        dictionary of colors (as tuples) and their coordinates
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


def main() -> None:
    """Creates basic menu functionality"""
    terminal = Terminal()
    print(terminal.clear, end='')
    terminal = Terminal()
    m = Menu(
        terminal,
        MENU_BASE_PATH / 'Resources' / 'menu.png',
        # size=(50, 25)
    )
    with terminal.cbreak():
        key = terminal.inkey(timeout=0)
        while key.name != 'KEY_ESCAPE':
            key = terminal.inkey(timeout=0)            
            if key.name == 'KEY_LEFT':
                m.selection -= 1
                m.draw_menu_text()
            elif key.name == 'KEY_RIGHT':
                m.selection += 1
                m.draw_menu_text()
    print(terminal.clear + 'Exiting!', end='')

if __name__ == '__main__':    
    main()    