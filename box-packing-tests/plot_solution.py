from matplotlib import colors
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Create rotations list
rotations_list = [0, 1, 0]

# Create starts list for each box
starts_list = [[0, 1, 0], [3, 0, 0], [0, 0, 0]]

# Create list of dimensions of each package
packages_list = [[2, 3, 4], [4, 1, 2], [3, 1, 2]]

colors_list = ["blue", "orange", "green"]

BOX_ALPHA = 0.3

# Box dimensions for the box the packages fit into
width = 4
height = 4
depth = 4

fig = plt.figure()
ax = plt.axes(projection='3d')

# Plot main box, some reason it does not plot as the top layer
ax.plot3D([0, 0, 0, 0, 0], [0, height, height, 0, 0], [0, 0, depth, depth, 0], color="red")
ax.plot3D([0, width, width, 0], [0, 0, height, height], [0, 0, 0, 0], color="red")
ax.plot3D([width, width, width, width], [0, 0, height, height], [0, depth, depth, 0], color="red")
ax.plot3D([0, width], [0, 0], [depth, depth], color="red")
ax.plot3D([0, width], [height, height], [depth, depth], color="red")

# Plot packages
for package, rotation, start, color in zip(packages_list, rotations_list, starts_list, colors_list):
    r = rotation
    w = package[0]
    h = package[1]
    d = package[2]

    if r != 0:
        wt = w
        ht = h
        dt = d
    if r == 1:
        w = dt
        h = ht
        d = wt
    elif r == 2:
        w = ht
        h = dt
        d = wt
    elif r == 3:
        w = ht
        h = wt
        d = dt
    elif r == 4:
        w = dt
        h = wt
        d = ht
    elif r == 5:
        w = wt
        h = dt
        d = ht

    startx = start[0]
    starty = start[1]
    startz = start[2]

    x = [0 + startx, 0 + startx, 0 + startx, 0 + startx]
    y = [0 + starty, h + starty, h + starty, 0 + starty]
    z = [0 + startz, 0 + startz, d + startz, d + startz]
    verts = [list(zip(x, y, z))]
    ax.add_collection3d(Poly3DCollection(verts, color=color, alpha=BOX_ALPHA))
    x = [0 + startx, w + startx, w + startx, 0 + startx]
    y = [0 + starty, 0 + starty, h + starty, h + starty]
    z = [0 + startz, 0 + startz, 0 + startz, 0 + startz]
    verts = [list(zip(x, y, z))]
    ax.add_collection3d(Poly3DCollection(verts, color=color, alpha=BOX_ALPHA))
    x = [w + startx, w + startx, w + startx, w + startx]
    y = [0 + starty, 0 + starty, h + starty, h + starty]
    z = [0 + startz, d + startz, d + startz, 0 + startz]
    verts = [list(zip(x, y, z))]
    ax.add_collection3d(Poly3DCollection(verts, color=color, alpha=BOX_ALPHA))
    x = [0 + startx, w + startx, w + startx, 0 + startx]
    y = [0 + starty, 0 + starty, h + starty, h + starty]
    z = [d + startz, d + startz, d + startz, d + startz]
    verts = [list(zip(x, y, z))]
    ax.add_collection3d(Poly3DCollection(verts, color=color, alpha=BOX_ALPHA))
    x = [0 + startx, w + startx, w + startx, 0 + startx]
    y = [0 + starty, 0 + starty, 0 + starty, 0 + starty]
    z = [d + startz, d + startz, 0 + startz, 0 + startz]
    verts = [list(zip(x, y, z))]
    ax.add_collection3d(Poly3DCollection(verts, color=color, alpha=BOX_ALPHA))
    x = [0 + startx, w + startx, w + startx, 0 + startx]
    y = [h + starty, h + starty, h + starty, h + starty]
    z = [d + startz, d + startz, 0 + startz, 0 + startz]
    verts = [list(zip(x, y, z))]
    ax.add_collection3d(Poly3DCollection(verts, color=color, alpha=BOX_ALPHA))

# ax.add_collection3d(Poly3DCollection(verts))
ax.axes.set_xlim3d(left=0.0, right=width)
ax.axes.set_ylim3d(bottom=0, top=height)
ax.axes.set_zlim3d(bottom=0, top=depth)
ax.set_box_aspect((width, height, depth))
plt.axis('off')
fig.show()

input("press to continue")
