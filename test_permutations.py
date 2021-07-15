import tkinter

import py3dbp

from app.pack import create_containers, pack_items
from app.plot import plot_result

# A small test to see if this works or not
if __name__ == '__main__':
    container_list = create_containers(max_dim=5)

    item_list = [py3dbp.Item('Box-1', 3, 1, 2, 1),
                 py3dbp.Item('Box-2', 3, 1, 2, 1),
                 py3dbp.Item('Box-3', 3, 1, 2, 1),
                 py3dbp.Item('Box-4', 3, 1, 2, 1),
                 py3dbp.Item('Box-5', 3, 1, 2, 1)]

    for container in container_list:
        result = pack_items(container, item_list)
        if not result.unfitted_items:
            print("All items fit!")
            print(" ")
            break
        else:
            result = None

    if not result:
        print("There was no fit!")
    else:
        print(f'''Container Dimensions
    Width: {result.width}
    Height: {result.height}
    Depth: {result.depth}
    ''')

    fig = plot_result(result).show()
    # https://stackoverflow.com/questions/9280171/matplotlib-python-show-returns-immediately
    tkinter.mainloop()
