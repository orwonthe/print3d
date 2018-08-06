from geoscad.as_units import mm
from geoscad.utilities import grounded_cube
from solid import scad_render_to_file, cylinder, union
from solid.utils import forward, down

# X dimensions
PLATTER_WIDTH = 12 @ mm

# Y dimensions
PLATTER_LENGTH = 56 @ mm
HOLE_SPACING = 2 @ mm

# Z dimensions
PLATTER_HEIGHT = 2 @ mm
HOLE_EXTENSION = 1 @ mm
HOLE_HEIGHT = PLATTER_HEIGHT + 2 * HOLE_EXTENSION


def hole_samples():
    return platter() - hole_set()


def hole_set():
    diameter_list = [1, 2, 3, 4, 5, 6, 7, 8] @ mm
    offset = -0.5 * PLATTER_LENGTH
    hole_list = []
    for diameter in diameter_list:
        radius = 0.5 * diameter
        offset += radius + HOLE_SPACING
        hole_list.append(
            down(HOLE_EXTENSION)(
                forward(offset)(
                    cylinder(r=radius, h=HOLE_HEIGHT, segments=16)
                )
            )

        )
        offset += radius
    print(offset)
    return union()(hole_list)


def platter():
    return grounded_cube([PLATTER_WIDTH, PLATTER_LENGTH, PLATTER_HEIGHT])


if __name__ == '__main__':
    scad_render_to_file(hole_samples(), 'hole_samples.scad')
