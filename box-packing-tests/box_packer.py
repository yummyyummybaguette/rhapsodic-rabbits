from typing import List
import enum

import py3dbp

class Axis(enum.Enum):
    width = 1
    height = 2
    depth = 3


class Dimensions:
    def __init__(self, width, height, depth) -> None:
        self.width = width
        self.height = height
        self.depth = depth


class Orientation:
    def __init__(self, x_axis: Axis, y_axis: Axis, z_axis: Axis) -> None:
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.z_axis = z_axis


def rotate_container(container: py3dbp.Bin, new_orientation: Orientation, original_dims: Dimensions) -> None:
    """
    Rotates the container to the orientation specified by `new_orienation`. This would be ideally a class method but
    the API provided by py3dbp does not allow this...
    """
    if new_orientation.x_axis == Axis.width:
        container.width = original_dims.width
    elif new_orientation.x_axis == Axis.height:
        container.height = original_dims.height
    else:
        container.depth = original_dims.depth

    if new_orientation.y_axis == Axis.width:
        container.height = original_dims.width
        pass
    elif new_orientation.y_axis == Axis.height:
        container.height = original_dims.height
    else:
        container.height = original_dims.depth

    if new_orientation.z_axis == Axis.width:
        container.depth = original_dims.width
    elif new_orientation.z_axis == Axis.height:
        container.depth = original_dims.height
    else:
        container.depth = original_dims.depth
    


def pack_items(container: py3dbp.Bin, items: List[py3dbp.Item]) -> py3dbp.Packer:
    """
    Attempts to pack the items using the heuristic algorithm outlined here:

    https://www.semanticscholar.org/paper/OPTIMIZING-THREE-DIMENSIONAL-BIN-PACKING-THROUGH-Dube
    /bb9986af2f26f7726fcef1bc684eac8239c9b853.

    There is a slight modification to this algorithm as certain rotations produces false negatives where the algorithm
    believes that the boxes cannot be packed but a rotation of the outer box will produce a solution. All six rotation
    orientation will be attempted (or until a solution is found) to reduce the possibility of a false negative.
     """

    original_dims = Dimensions(container.width, container.height, container.depth)

    orientations = [
        Orientation(Axis.width, Axis.height, Axis.depth),
        Orientation(Axis.height, Axis.width, Axis.depth),
        Orientation(Axis.height, Axis.depth, Axis.width),
        Orientation(Axis.depth, Axis.height, Axis.width),
        Orientation(Axis.depth, Axis.width, Axis.height),
        Orientation(Axis.width, Axis.depth, Axis.height)]


    for orientation in orientations:
        packer = py3dbp.Packer()
        rotate_container(container, orientation, original_dims)
        packer.add_bin(container)
        for item in items:
            packer.add_item(item)

        packer.pack()

        if not packer.unfit_items:
            return packer

    return None


# A small test to see if this works or not
if __name__ == '__main__':
    container = py3dbp.Bin('Bin-1', 6, 1, 5, 100)
    item_list = [
        py3dbp.Item('Box-1', 3, 1, 2, 1),
        py3dbp.Item('Box-2', 3, 1, 2, 1),
        py3dbp.Item('Box-3', 3, 1, 2, 1),
        py3dbp.Item('Box-4', 3, 1, 2, 1),
        py3dbp.Item('Box-5', 3, 1, 2, 1)]

    result = pack_items(container, item_list)
    if result.unfit_items:
        print("Error, Should have fit all items")
    else:
        print("All items were fitted as expected")
