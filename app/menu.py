from pathlib import Path
from typing import Any, Tuple, Union

from blessed import Terminal

from .helpers import (
    TUI_HEIGHT, TUI_WIDTH, color_positions, draw_image, get_pixels
)


class Menu:
    """Graphical menu for terminal windows

    Renders pre-existing images in a terminal window.
    Overlays text on the menu using colors in another pre-existing image to determine the text locations
    """

    # Defines what function each menu option points to
    # TODO Create menu functions
    opts = {
        'Box packing': None,
        'Files': None,
        'Game': None,
        'Settings': None
    }
    texts = list(opts.keys())

    # Defines which text-overlay colors correspond to what
    overlay_colors = {
        (0, 0, 255, 255): texts,
        (255, 0, 0, 255): 'Left',
        (0, 255, 0, 255): 'Right'
    }

    def __init__(self,
                 terminal: Terminal,
                 background: Union[str, Path],
                 size: Tuple[int, int] = (TUI_WIDTH, TUI_HEIGHT)):
        self.terminal: Terminal = terminal
        size = (size[0] * 2, size[1])
        self.background_pixels = get_pixels(background, size)
        overlay_path = background.with_name(f'{background.stem}_overlay{background.suffix}')
        self.text_pixels = get_pixels(overlay_path, size)
        self.overlay_positions = color_positions(self.text_pixels)
        self.num = 0
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
        for color, text in self.overlay_colors.items():
            if isinstance(text, list):
                text = self.texts[self.num % len(self.texts)]
            coords = self.overlay_positions[color]
            text = text.center(len(coords))
            backgrounds = (self.get_color(x, y) for x, y in coords)

            start_x, start_y = self.origin
            offset_x, offset_y = coords[0]

            res = self.terminal.move_xy(x=start_x + offset_x, y=start_y + offset_y)
            res += ''.join(
                self.terminal.on_color_rgb(*bg) + self.terminal.black(char)
                for char, bg in zip(text, backgrounds)
            )
            print(res)

    def get_color(self, x: int, y: int) -> Tuple[int, int, int, int]:
        """Gets the 4 number color Tuple at given coordinates in the rendered background image"""
        return self.background_pixels[y][x]

    def increment(self) -> None:
        """Increment the selection index"""
        self.num -= 1
        self.draw_menu_text()

    def decrement(self) -> None:
        """Decrement the selection index"""
        self.num += 1
        self.draw_menu_text()

    @property
    def selection(self) -> Any:
        """Get the function that corresponds to the current menu selection, as defined in self.opts"""
        return self.opts[self.texts[self.num % len(self.texts)]]
