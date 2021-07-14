from pathlib import Path
from typing import Dict, List, Tuple, Union

from blessed import Terminal
from PIL import Image

# Constants
TUI_WIDTH = 100
TUI_HEIGHT = 50


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
        colors tuple: list of coordinates with that color
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
