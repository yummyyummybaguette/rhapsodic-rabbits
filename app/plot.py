import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from py3dbp import Packer


def plot_result(result: Packer) -> None:
    """Plots a solution. Limited to 10 items by COLORS_LIST"""
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

    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})

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
    for idx, (package, rotation, position) in enumerate(zip(packages_list,
                                                  rotations_list,
                                                  positions_list)):
        color = COLORS_LIST[idx % len(COLORS_LIST)]
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

    return fig
