from pathlib import Path
from typing import Tuple

from blessed import Terminal

from menu import Menu

TUI_WIDTH = 100
TUI_HEIGHT = 50


class InsideTheBoxTUI:
    """Top-level class for the TUI"""

    def __init__(self, terminal: Terminal, size: Tuple[int, int] = (TUI_WIDTH, TUI_HEIGHT)):
        self.terminal = terminal
        print(self.terminal.clear, end='')
        self.menu = Menu(
            terminal=self.terminal,
            background=Path('resources') / 'menu.png',
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
                        print(self.menu.selection)
        self.exit()

    def exit(self) -> None:
        """Clear the terminal and exit the TUI"""
        print(self.terminal.clear + 'Exiting!', end='')


if __name__ == '__main__':
    app = InsideTheBoxTUI(terminal=Terminal())
    app.run()
