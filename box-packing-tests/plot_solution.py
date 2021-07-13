from matplotlib import colors
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# This code is to test the algorithm from the py3dbp package

# Box dimensions for the box the packages fit into
width = 5
height = 5
depth = 5

# Create list of dimensions of each package
packages_list = [[2, 3, 4], [4, 2, 2], [1, 2, 1], [3, 1, 4]]

# Create rotations list
rotations_list = [3, 0, 0, 0]

# x,y,z position for each package
positions_list = [[0, 2, 2], [0, 2, 0], [0, 0, 0], [1, 0, 0]]

colors_list = ["blue", "orange", "green", "brown"]

BOX_ALPHA = 0.3

fig = plt.figure()
ax = plt.axes(projection='3d')

# Plot main box, some reason it does not plot as the top layer
ax.plot3D([0, 0, 0, 0, 0], [0, height, height, 0, 0], [0, 0, depth, depth, 0], color="red")
ax.plot3D([0, width, width, 0], [0, 0, height, height], [0, 0, 0, 0], color="red")
ax.plot3D([width, width, width, width], [0, 0, height, height], [0, depth, depth, 0], color="red")
ax.plot3D([0, width], [0, 0], [depth, depth], color="red")
ax.plot3D([0, width], [height, height], [depth, depth], color="red")

# Plot packages
for package, rotation, position, color in zip(packages_list, rotations_list, positions_list, colors_list):
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
    ax.add_collection3d(Poly3DCollection(verts, color=color, alpha=BOX_ALPHA))
    x = [0 + position_x, w + position_x, w + position_x, 0 + position_x]
    y = [0 + position_y, 0 + position_y, h + position_y, h + position_y]
    z = [0 + position_z, 0 + position_z, 0 + position_z, 0 + position_z]
    verts = [list(zip(x, y, z))]
    ax.add_collection3d(Poly3DCollection(verts, color=color, alpha=BOX_ALPHA))
    x = [w + position_x, w + position_x, w + position_x, w + position_x]
    y = [0 + position_y, 0 + position_y, h + position_y, h + position_y]
    z = [0 + position_z, d + position_z, d + position_z, 0 + position_z]
    verts = [list(zip(x, y, z))]
    ax.add_collection3d(Poly3DCollection(verts, color=color, alpha=BOX_ALPHA))
    x = [0 + position_x, w + position_x, w + position_x, 0 + position_x]
    y = [0 + position_y, 0 + position_y, h + position_y, h + position_y]
    z = [d + position_z, d + position_z, d + position_z, d + position_z]
    verts = [list(zip(x, y, z))]
    ax.add_collection3d(Poly3DCollection(verts, color=color, alpha=BOX_ALPHA))
    x = [0 + position_x, w + position_x, w + position_x, 0 + position_x]
    y = [0 + position_y, 0 + position_y, 0 + position_y, 0 + position_y]
    z = [d + position_z, d + position_z, 0 + position_z, 0 + position_z]
    verts = [list(zip(x, y, z))]
    ax.add_collection3d(Poly3DCollection(verts, color=color, alpha=BOX_ALPHA))
    x = [0 + position_x, w + position_x, w + position_x, 0 + position_x]
    y = [h + position_y, h + position_y, h + position_y, h + position_y]
    z = [d + position_z, d + position_z, 0 + position_z, 0 + position_z]
    verts = [list(zip(x, y, z))]
    ax.add_collection3d(Poly3DCollection(verts, color=color, alpha=BOX_ALPHA))

# ax.add_collection3d(Poly3DCollection(verts))
ax.axes.set_xlim3d(left=0, right=width)
ax.axes.set_ylim3d(bottom=0, top=height)
ax.axes.set_zlim3d(bottom=0, top=depth)
ax.set_box_aspect((width, 1.1*height, depth))
plt.axis('off')
fig.show()

input("press to continue")
