import blessed
from py3dbp import Item, Bin, Packer

term = blessed.Terminal()

item_list = []

def centered_msg(msg):
    '''Returns a string so that when printed out, it appears in the center of the terminal'''
    msg = str(msg)
    return term.move_xy(term.width//2 - len(msg)//2, term.height//2) + msg

def main():
    with term.hidden_cursor():
        print(term.home + term.on_white + term.clear)
        msg = "How many items need to be packed?"
        number_of_items = input(term.move_xy(term.width//2 - len(msg)//2, term.height//2)
                                    + term.cyan4(msg)
                                    + term.move_xy(term.width//2 - len(msg)//2, term.height//2 + 1))
        while not number_of_items.isnumeric():
            print(term.home + term.on_white + term.clear)
            msg = "Please enter a number: "
            number_of_items = input(term.move_xy(term.width//2 - len(msg)//2, term.height//2)
                                    + term.red(msg)
                                    + term.move_xy(term.width//2 - len(msg)//2, term.height//2 + 1))
            
        number_of_items = int(number_of_items)
        
        for i in range(number_of_items):
            print(term.home + term.on_white + term.clear)
            print(term.cyan4(f"Item #{i + 1}: "))
            width = input(centered_msg(term.cyan4("Width: ")))
            print(term.home + term.on_white + term.clear)
            height = input(centered_msg(term.cyan4("Height: ")))
            print(term.home + term.on_white + term.clear)
            depth = input(centered_msg(term.cyan4("Depth: ")))
            
            item_list.append(Item(f"Item #{i+1}", width, height, depth, 0))
            
        print(term.home + term.on_white + term.clear)
        msg = "Items: "
        print(term.move_x(term.width//2 - len(msg)//2) + term.cyan4_on_white(msg))
        print()

        for item in item_list:
            msg = f"{item.name} --> width: {item.width}, height: {item.height}, depth: {item.depth}" 
            print(term.move_x(term.width//2 - len(msg)//2) + term.cyan4_on_white(msg))

if __name__ == "__main__":
    main()