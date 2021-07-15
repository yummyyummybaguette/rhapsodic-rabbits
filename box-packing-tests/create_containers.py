import enum
import math
from itertools import combinations_with_replacement, permutations
from dataclasses import dataclass
from decimal import Decimal
from typing import List

import py3dbp


class Axis(enum.Enum):
    """
    Represents a single axis.

    Width is on the x-axis, height is on the y-axis and depth is on the z-axis given a right handed coordinate system.
    """

    width = 1
    height = 2
    depth = 3


@dataclass
class Dimensions:
    """
    Represents the dimensions of a container.

    Width is on the x-axis, height is on the y-axis and depth is on the z-axis given a right handed coordinate system.
    """

    width: Decimal
    height: Decimal
    depth: Decimal


@dataclass
class Orientation:
    """Represents an orientation of a container in space"""

    x_axis: Axis
    y_axis: Axis
    z_axis: Axis


def rotate_container(container_box: py3dbp.Bin, new_orientation: Orientation, original_dims: Dimensions) -> None:
    """
    Rotates the container to the orientation specified by `new_orienation`.

    This would be ideally a class method but the API provided by py3dbp does not allow this...
    """
    if new_orientation.x_axis == Axis.width:
        container_box.width = original_dims.width
    elif new_orientation.x_axis == Axis.height:
        container_box.height = original_dims.height
    else:
        container_box.depth = original_dims.depth

    if new_orientation.y_axis == Axis.width:
        container_box.height = original_dims.width
        pass
    elif new_orientation.y_axis == Axis.height:
        container_box.height = original_dims.height
    else:
        container_box.height = original_dims.depth

    if new_orientation.z_axis == Axis.width:
        container_box.depth = original_dims.width
    elif new_orientation.z_axis == Axis.height:
        container_box.depth = original_dims.height
    else:
        container_box.depth = original_dims.depth


def pack_items(container_box: py3dbp.Bin, items: List[py3dbp.Item]) -> py3dbp.Packer:
    """
    Attempts to pack the items using the heuristic algorithm outlined here:

    https://www.semanticscholar.org/paper/OPTIMIZING-THREE-DIMENSIONAL-BIN-PACKING-THROUGH-Dube
    /bb9986af2f26f7726fcef1bc684eac8239c9b853.

    There is a slight modification to this algorithm as certain rotations produces false negatives where the algorithm
    believes that the boxes cannot be packed but a rotation of the outer box will produce a solution. All six rotation
    orientation will be attempted (or until a solution is found) to reduce the possibility of a false negative.
    """
    original_dims = Dimensions(container_box.width, container_box.height, container_box.depth)

    orientations = [
        Orientation(Axis.width, Axis.height, Axis.depth),
        Orientation(Axis.height, Axis.width, Axis.depth),
        Orientation(Axis.height, Axis.depth, Axis.width),
        Orientation(Axis.depth, Axis.height, Axis.width),
        Orientation(Axis.depth, Axis.width, Axis.height),
        Orientation(Axis.width, Axis.depth, Axis.height)]

    for orientation in orientations:
        packer = py3dbp.Packer()
        rotate_container(container_box, orientation, original_dims)
        packer.add_bin(container_box)
        for item in items:
            packer.add_item(item)

        packer.pack()

        if not packer.unfit_items:
            return packer

    return None

def pack_items_2(container_box, items):
    packer = py3dbp.Packer()
    packer.add_bin(container_box)
    for item in items:
        packer.add_item(item)
    packer.pack(number_of_decimals=0)
    return container_box
    
# A small test to see if this works or not
if __name__ == '__main__':
    # Create all combinations of dimensions up to max_dim
    max_dim = 3
    num_list = []
    for i in range(1, max_dim + 1):
        num_list += [i]*3
    container_dims = list(set(permutations(num_list, 3)))
    print(container_dims)
    container_volumes_list = [math.prod(container_dim) for container_dim in container_dims]
    print(container_volumes_list) 
    container_list = [py3dbp.Bin(str(i), dim[0], dim[1], dim[2], 100) for i, dim in enumerate(container_dims)]
    
    item_list = [py3dbp.Item('Box-1', 3, 1, 2, 1),
                 py3dbp.Item('Box-2', 3, 1, 2, 1),
                 py3dbp.Item('Box-3', 3, 1, 2, 1),
                 py3dbp.Item('Box-4', 3, 1, 2, 1),
                 py3dbp.Item('Box-5', 3, 1, 2, 1)]

    for container in container_list:
        packer = py3dbp.Packer()
        packer.add_bin(container)
        for item in item_list:
            packer.add_item(item)
        packer.pack(number_of_decimals=0)
        if not container.unfitted_items:
            print("All items fit!")
            print(" ")
            result = container
            break
'''
    print(result)
    print(result.items)
    print(result.width)
    print(result.height)
    print(result.depth)
'''