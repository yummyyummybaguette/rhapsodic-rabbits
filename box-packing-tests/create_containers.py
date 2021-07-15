import math
from itertools import permutations

import py3dbp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


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


def plot_result(result):
    """Plots a solution"""
    width = float(result.width)
    height = float(result.height)
    depth = float(result.depth)
    rotations_list = []
    positions_list = []
    packages_list = []

    for item in result.items:
        package_dims = [float(item.width),
                        float(item.height),
                        float(item.depth)]
        packages_list.append(package_dims)
        position = [float(i) for i in item.position]
        positions_list.append(position)
        rotations_list.append(item.rotation_type)

    COLORS_LIST = ["blue",
                   "orange",
                   "green",
                   "brown",
                   "purple",
                   "lime",
                   "yellow",
                   "pink",
                   "turquoise",
                   "maroon"]

    BOX_ALPHA = 0.3

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    ax.plot3D([0, 0, 0, 0, 0],
              [0, height, height, 0, 0],
              [0, 0, depth, depth, 0],
              color="red")
    ax.plot3D([0, width, width, 0],
              [0, 0, height, height],
              [0, 0, 0, 0],
              color="red")
    ax.plot3D([width, width, width, width],
              [0, 0, height, height],
              [0, depth, depth, 0],
              color="red")
    ax.plot3D([0, width],
              [0, 0],
              [depth, depth],
              color="red")
    ax.plot3D([0, width],
              [height, height],
              [depth, depth],
              color="red")

    # Plot items
    for package, rotation, position, color in zip(packages_list,
                                                  rotations_list,
                                                  positions_list,
                                                  COLORS_LIST):
        r = rotation
        w = package[0]
        h = package[1]
        d = package[2]

        if r != 0:
            wt = w
            ht = h
            dt = d
        if r == 1:
            w = ht
            h = wt
            d = dt
        elif r == 2:
            w = ht
            h = dt
            d = wt
        elif r == 3:
            w = dt
            h = ht
            d = wt
        elif r == 4:
            w = dt
            h = wt
            d = ht
        elif r == 5:
            w = wt
            h = dt
            d = ht

        position_x = position[0]
        position_y = position[1]
        position_z = position[2]

        x = [0 + position_x, 0 + position_x, 0 + position_x, 0 + position_x]
        y = [0 + position_y, h + position_y, h + position_y, 0 + position_y]
        z = [0 + position_z, 0 + position_z, d + position_z, d + position_z]
        verts = [list(zip(x, y, z))]
        ax.add_collection3d(Poly3DCollection(verts,
                                             color=color,
                                             alpha=BOX_ALPHA))
        x = [0 + position_x, w + position_x, w + position_x, 0 + position_x]
        y = [0 + position_y, 0 + position_y, h + position_y, h + position_y]
        z = [0 + position_z, 0 + position_z, 0 + position_z, 0 + position_z]
        verts = [list(zip(x, y, z))]
        ax.add_collection3d(Poly3DCollection(verts,
                                             color=color,
                                             alpha=BOX_ALPHA))
        x = [w + position_x, w + position_x, w + position_x, w + position_x]
        y = [0 + position_y, 0 + position_y, h + position_y, h + position_y]
        z = [0 + position_z, d + position_z, d + position_z, 0 + position_z]
        verts = [list(zip(x, y, z))]
        ax.add_collection3d(Poly3DCollection(verts,
                                             color=color,
                                             alpha=BOX_ALPHA))
        x = [0 + position_x, w + position_x, w + position_x, 0 + position_x]
        y = [0 + position_y, 0 + position_y, h + position_y, h + position_y]
        z = [d + position_z, d + position_z, d + position_z, d + position_z]
        verts = [list(zip(x, y, z))]
        ax.add_collection3d(Poly3DCollection(verts,
                                             color=color,
                                             alpha=BOX_ALPHA))
        x = [0 + position_x, w + position_x, w + position_x, 0 + position_x]
        y = [0 + position_y, 0 + position_y, 0 + position_y, 0 + position_y]
        z = [d + position_z, d + position_z, 0 + position_z, 0 + position_z]
        verts = [list(zip(x, y, z))]
        ax.add_collection3d(Poly3DCollection(verts,
                                             color=color,
                                             alpha=BOX_ALPHA))
        x = [0 + position_x, w + position_x, w + position_x, 0 + position_x]
        y = [h + position_y, h + position_y, h + position_y, h + position_y]
        z = [d + position_z, d + position_z, 0 + position_z, 0 + position_z]
        verts = [list(zip(x, y, z))]
        ax.add_collection3d(Poly3DCollection(verts,
                                             color=color,
                                             alpha=BOX_ALPHA))

    ax.axes.set_xlim3d(left=0, right=width)
    ax.axes.set_ylim3d(bottom=0, top=height)
    ax.axes.set_zlim3d(bottom=0, top=depth)
    ax.set_box_aspect((width, 1.1*height, depth))
    plt.axis('off')
    fig.show()

    input("press to continue")


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

    plot_result(result)
