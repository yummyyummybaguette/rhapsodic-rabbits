import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

width = 3
height = 4
depth = 3


fig = plt.figure()

ax = plt.axes(projection='3d', alpha=1.0)


ax.plot3D([0, 0, 0, 0, 0], [0, height, height, 0, 0], [0, 0, depth, depth, 0], color="red")
ax.plot3D([0, width, width, 0], [0, 0, height, height], [0, 0, 0, 0], color="red")
ax.plot3D([width, width, width, width], [0, 0, height, height], [0, depth, depth, 0], color="red")
ax.plot3D([0, width], [0, 0], [depth, depth], color="red")
ax.plot3D([0, width], [height, height], [depth, depth], color="red")

r = 0

w = 1
h = 2
d = 3

if r != 0:
    wt = w
    ht = h
    dt = d
if r == 1:
    d = wt
    w = dt
elif r == 2:
    d = wt
    h = dt
elif r == 3:
    w = ht
    h = wt
elif r == 4:
    w = dt
    h = wt
    d = ht
elif r == 5:
    w = ht
    h = dt
    d = wt

startx = 0
starty = 0
startz = 0

x = [0 + startx, 0 + startx, 0 + startx, 0 + startx]
y = [0 + starty, h + starty, h + starty, 0 + starty]
z = [0 + startz, 0 + startz, d + startz, d + startz]
verts = [list(zip(x, y, z))]
ax.add_collection3d(Poly3DCollection(verts, color="blue", alpha=0.2))
x = [0 + startx, w + startx, w + startx, 0 + startx]
y = [0 + starty, 0 + starty, h + starty, h + starty]
z = [0 + startz, 0 + startz, 0 + startz, 0 + startz]
verts = [list(zip(x, y, z))]
ax.add_collection3d(Poly3DCollection(verts, color="blue", alpha=0.2))
x = [w + startx, w + startx, w + startx, w + startx]
y = [0 + starty, 0 + starty, h + starty, h + starty]
z = [0 + startz, d + startz, d + startz, 0 + startz]
verts = [list(zip(x, y, z))]
ax.add_collection3d(Poly3DCollection(verts, color="blue", alpha=0.2))
x = [0 + startx, w + startx, w + startx, 0 + startx]
y = [0 + starty, 0 + starty, h + starty, h + starty]
z = [d + startz, d + startz, d + startz, d + startz]
verts = [list(zip(x, y, z))]
ax.add_collection3d(Poly3DCollection(verts, color="blue", alpha=0.2))
x = [0 + startx, w + startx, w + startx, 0 + startx]
y = [0 + starty, 0 + starty, 0 + starty, 0 + starty]
z = [d + startz, d + startz, 0 + startz, 0 + startz]
verts = [list(zip(x, y, z))]
ax.add_collection3d(Poly3DCollection(verts, color="blue", alpha=0.2))
x = [0 + startx, w + startx, w + startx, 0 + startx]
y = [h + starty, h + starty, h + starty, h + starty]
z = [d + startz, d + startz, 0 + startz, 0 + startz]
verts = [list(zip(x, y, z))]
ax.add_collection3d(Poly3DCollection(verts, color="blue", alpha=0.2))

# ax.add_collection3d(Poly3DCollection(verts))
ax.axes.set_xlim3d(left=0.0, right=width) 
ax.axes.set_ylim3d(bottom=0, top=height) 
ax.axes.set_zlim3d(bottom=0, top=depth)
ax.set_box_aspect((width, height, depth))  # xy aspect ratio is 1:1, but stretches z axis
#plt.grid(False)
#plt.axis('off')
fig.show()

input("press to continue")
