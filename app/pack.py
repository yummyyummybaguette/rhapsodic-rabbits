import math
import tkinter
from plot import plot_result
from itertools import permutations

import py3dbp


def create_containers(items: list[py3dbp.Item], max_dim: int = 30) -> list:
    """Creates containers for all permutations of dimensions.

    The maximum dimension for any side is set by max_dim.
    """
    num_list = []
    for i in range(1, max_dim + 1):
        num_list += [i] * 3   
    items_volume = int(sum([item.width * item.height * item.depth
                            for item
                            in items]))
    container_dims = list(set(permutations(num_list, 3)))
    container_vol_list = [math.prod(container_dim)
                          for container_dim
                          in container_dims]
    container_vols_sorted = sorted(container_vol_list)   
    min_volume_index = [index
                        for index, volume
                        in enumerate(container_vols_sorted)
                        if volume > items_volume][0]  
    container_start_vol = container_vols_sorted[min_volume_index-1]    
    start_index = container_vols_sorted.index(container_start_vol)
    container_dims_sort = [cont
                           for vol, cont
                           in sorted(zip(container_vol_list, container_dims))]
    container_list = [py3dbp.Bin(str(i), dim[0], dim[1], dim[2], 100)
                      for i, dim
                      in enumerate(container_dims_sort[start_index:])]
    return container_list


def pack_items(container_box: py3dbp.Bin,
               items: list[py3dbp.Item]) -> py3dbp.Packer:
    """Attempts to pack items into container"""
    packer = py3dbp.Packer()
    packer.add_bin(container_box)
    for item in items:
        packer.add_item(item)
    packer.pack(number_of_decimals=0)
    return container_box


# A small test to see if this works or not
if __name__ == '__main__':
    item_list = [py3dbp.Item('Box-1', 3, 1, 2, 1),
                 py3dbp.Item('Box-2', 3, 1, 2, 1),
                 py3dbp.Item('Box-3', 3, 1, 2, 1),
                 py3dbp.Item('Box-4', 3, 1, 2, 1),
                 py3dbp.Item('Box-5', 3, 1, 2, 1)]

    container_list = create_containers(item_list, max_dim=5)
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
