import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from typing import List, Tuple
from py3dbp import Bin, Item, Packer

# All dimensions are in inches
BOX_LIST = [
    Bin('0', 3, 3, 3, 100),
    Bin('1', 3, 4, 3, 100),
    Bin('2', 4, 4, 4, 100),
    Bin('3', 5, 5, 6, 100),
    Bin('4', 6, 6, 6, 100),
    Bin('6', 7, 7, 8, 100),
    Bin('7', 7, 9, 7, 100),
    Bin('8', 8, 8, 8, 100),
    Bin('9', 8, 9, 8, 100),
    Bin('10', 9, 10, 12, 100),
    Bin('11', 12, 18, 6, 100)
]


def get_packages() -> Tuple[List, int]:
    """Gets the package sizes from the user
    and calculates the total volume of the packages

    Returns: packages_list and volume of packages
    """
    packages_list = []
    total_volume = 0
    number_of_packages = int(input("How many packages? "))
    for i in range(1, number_of_packages + 1):
        print(" ")
        print(f"Data for Package {i}.")
        width = float(input("Width? "))
        height = float(input("Height? "))
        depth = float(input("Depth? "))
        total_volume += (width * height * depth)
        packages_list.append({"name": str(i),
                              "width": width,
                              "height": height,
                              "depth": depth})
    return packages_list, total_volume


packages, packages_volume = get_packages()

for box in BOX_LIST:
    packer = Packer()
    packer.add_bin(box)
    for package in packages:
        packer.add_item(Item(package["name"],
                             package["width"],
                             package["height"],
                             package["depth"], 0.1))
    packer.pack(number_of_decimals=0)
    if box.unfitted_items == []:
        print("All items fit!")
        print(" ")
        fit_box = box
        break

# Box dimensions for the box the packages fit into
width = float(box.width)
height = float(box.height)
depth = float(box.depth)
rotations_list = []
positions_list = []
packages_list = []

print(f'width = {width}, height = {height}, depth = {depth}')

print(" ")
print(box.name)
print(f'Volume of box: {box.width * box.height * box.depth} cubic inches')
print(f'Volume of packages: {packages_volume} cubic inches')
print(" ")
for item in box.items:
    print(item.width)
    print(item.string())
    print(item.position)
    print(item.rotation_type)
    package_dims = [float(item.width), float(item.height), float(item.depth)]
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
               "turquiose",
               "maroon"]

BOX_ALPHA = 0.3

fig = plt.figure()
ax = plt.axes(projection='3d')

# Plot main box, some reason it does not plot as the top layer
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

# Plot packages
for package, rotation, position, color in zip(packages_list,
                                              rotations_list,
                                              positions_list,
                                              COLORS_LIST[0:len(COLORS_LIST)]):
    r = rotation
    w = package[0]
    h = package[1]
    d = package[2]
    print(f'{w} {h} {d}')
    print(f'{rotation}')
    print(f'{position}')
    print(" ")

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

ax.axes.set_xlim3d(left=0, right=width)
ax.axes.set_ylim3d(bottom=0, top=height)
ax.axes.set_zlim3d(bottom=0, top=depth)
ax.set_box_aspect((width, 1.1*height, depth))
plt.axis('off')
fig.show()

input("press to continue")
