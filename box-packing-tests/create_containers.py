import math
from itertools import permutations

import py3dbp


def create_containers(max_dim=12):
    """Creates containers with dimensions of all permutations with
     sides up to the max_dim. The containers are sorted by volume.
    """
    num_list = []
    for i in range(1, max_dim + 1):
        num_list += [i]*3
    container_dims = list(set(permutations(num_list, 3)))
    container_vol_list = [math.prod(container_dim)
                          for container_dim
                          in container_dims]
    container_dims_sort = [cont
                           for cont, vol
                           in sorted(zip(container_dims, container_vol_list))]
    container_list = [py3dbp.Bin(str(i), dim[0], dim[1], dim[2], 100)
                      for i, dim
                      in enumerate(container_dims_sort)]
    return container_list


def pack_items(container_box, items):
    """Attempts to pack items into container"""
    packer = py3dbp.Packer()
    packer.add_bin(container_box)
    for item in items:
        packer.add_item(item)
    packer.pack(number_of_decimals=0)
    return container_box


# A small test to see if this works or not
if __name__ == '__main__':
    container_list = create_containers(max_dim=6)

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
