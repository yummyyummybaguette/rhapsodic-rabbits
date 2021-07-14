import blessed
from blessed import Terminal
from py3dbp import Item

term = blessed.Terminal()

item_list = []


class UserInput:
    """Interface to collect data about boxes from a user"""

    def __init__(self, terminal: Terminal) -> None:
        self.terminal = terminal

    def run(self) -> None:
        """Start the interface to collect input from the user"""
        with self.terminal.hidden_cursor():
            print(self.terminal.home + self.terminal.on_white + self.terminal.clear)
            msg = "How many items need to be packed?"
            number_of_items = input(self.terminal.move_xy(self.terminal.width // 2 - len(msg) // 2,
                                                          self.terminal.height // 2)
                                    + self.terminal.cyan4(msg)
                                    + self.terminal.move_xy(self.terminal.width // 2 - len(msg) // 2,
                                                            self.terminal.height // 2 + 1))
            while not number_of_items.isnumeric():
                print(self.terminal.home + self.terminal.on_white + self.terminal.clear)
                msg = "Please enter a number: "
                number_of_items = input(self.terminal.move_xy(self.terminal.width // 2 - len(msg) // 2,
                                                              self.terminal.height // 2)
                                        + self.terminal.red(msg)
                                        + self.terminal.move_xy(self.terminal.width // 2 - len(msg) // 2,
                                                                self.terminal.height // 2 + 1))

            number_of_items = int(number_of_items)

            for i in range(number_of_items):
                print(self.terminal.home + self.terminal.on_white + self.terminal.clear)
                print(self.terminal.cyan4(f"Item #{i + 1}: "))
                width = input(centered_msg(self.terminal, self.terminal.cyan4("Width: ")))
                print(self.terminal.home + self.terminal.on_white + self.terminal.clear)
                height = input(centered_msg(self.terminal, self.terminal.cyan4("Height: ")))
                print(self.terminal.home + self.terminal.on_white + self.terminal.clear)
                depth = input(centered_msg(self.terminal, self.terminal.cyan4("Depth: ")))

                item_list.append(Item(f"Item #{i + 1}", width, height, depth, 0))

            print(self.terminal.home + self.terminal.on_white + self.terminal.clear)
            msg = "Items: "
            print(self.terminal.move_x(self.terminal.width // 2 - len(msg) // 2) + self.terminal.cyan4_on_white(msg))
            print()

            for item in item_list:
                msg = f"{item.name} --> width: {item.width}, height: {item.height}, depth: {item.depth}"
                print(self.terminal.move_x(self.terminal.width // 2 - len(msg) // 2)
                      + self.terminal.cyan4_on_white(msg))


def centered_msg(terminal: Terminal, msg: str) -> None:
    """Returns a string so that when printed out, it appears in the center of the terminal"""
    msg = str(msg)
    return terminal.move_xy(terminal.width // 2 - len(msg) // 2, terminal.height // 2) + msg


if __name__ == "__main__":
    UserInput(Terminal()).run()
