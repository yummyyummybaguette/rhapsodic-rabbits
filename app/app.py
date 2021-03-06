from pathlib import Path
from typing import Tuple

from blessed import Terminal

from .helpers import TUI_HEIGHT, TUI_WIDTH
from .menu import Menu

PACKAGE_DIR = Path(__file__).parents[0]


class InsideTheBoxTUI:
    """Top-level class for the TUI"""

    def __init__(self, terminal: Terminal, size: Tuple[int, int] = (TUI_WIDTH, TUI_HEIGHT)):
        self.terminal = terminal
        print(self.terminal.clear + self.terminal.normal + self.terminal.home, end='')
        self.menu = Menu(
            terminal=self.terminal,
            background=PACKAGE_DIR / 'resources' / 'menu.png',
            animations=PACKAGE_DIR / 'resources' / 'animations',
            size=size
        )

    def run(self) -> None:
        """Runs the main event loop for the TUI"""
        with self.terminal.cbreak():
            while (key := self.terminal.inkey(timeout=0)).name != 'KEY_ESCAPE':
                if key.name == 'KEY_LEFT':
                    self.menu.decrement()
                elif key.name == 'KEY_RIGHT':
                    self.menu.increment()
                elif key.name == 'KEY_ENTER':
                    with self.terminal.location():
                        # print(self.menu.selection)
                        self.menu.animation()
        self.exit()

    def exit(self) -> None:
        """Clear the terminal and exit the TUI"""
        print(self.terminal.normal + self.terminal.clear + 'Exiting!', end='')
