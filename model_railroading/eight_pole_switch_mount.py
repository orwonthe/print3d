from geoscad.as_units import mm
from geoscad.utilities import grounded_cube, rounded_platter
from solid import scad_render_to_file, cylinder, union, cube, intersection
from solid.utils import forward, back, down, up, right, left

# X dimensions
PLATTER_WIDTH = 34 * mm
TROUGH_WIDTH = 18 * mm
SLOT_SPACING_X = 6 * mm
SLOT_WIDTH = 1.4 * mm
SLOT_COUNT_X = 2
SLOT_OFFSET_X = ((SLOT_COUNT_X - 1) * SLOT_SPACING_X) / 2
CORNER_HOLE_X_OFFSET = 13 * mm
CORNER_HOLE_RADIUS = 1.8 @ mm

# Y dimensions
PLATTER_LENGTH = 39 * mm
SLOT_SPACING_Y = 4 * mm
SLOT_LENGTH = 3.0 * mm
SLOT_COUNT_Y = 10
SLOT_OFFSET_Y = ((SLOT_COUNT_Y - 1) * SLOT_SPACING_Y) / 2
TROUGH_LENGTH = PLATTER_LENGTH + 2 * mm
CORNER_HOLE_Y_OFFSET = 16 * mm

# Z dimensions
PLATTER_HEIGHT = 3 * mm
SLOT_SPACING_Z = 4 * mm
SLOT_HEIGHT = 3 * PLATTER_HEIGHT
TROUGH_ELEVATION = PLATTER_HEIGHT - 0.4 * mm
TROUGH_HEIGHT = PLATTER_HEIGHT
HOLE_HEIGHT = SLOT_HEIGHT




def eight_pole_switch_mount():
    return mount_base() - trough() - slots() - corner_holes()


def mount_base():
    return grounded_cube([PLATTER_WIDTH, PLATTER_LENGTH, PLATTER_HEIGHT])

def trough():
    return up(TROUGH_ELEVATION)(grounded_cube([TROUGH_WIDTH, TROUGH_LENGTH, TROUGH_HEIGHT]))


def slots():
    slot = single_slot()

    return left(SLOT_OFFSET_X)(
        back(SLOT_OFFSET_Y)(
            union()([
                    right(ix * SLOT_SPACING_X)(forward(iy * SLOT_SPACING_Y)(slot))
                for ix in range(SLOT_COUNT_X)
                for iy in range(SLOT_COUNT_Y)
                ])
            )
        )

def single_slot():
    return cube([SLOT_WIDTH, SLOT_LENGTH, SLOT_HEIGHT], center=True)

def corner_holes():
    hole = down(0.1 * mm)(cylinder(r=CORNER_HOLE_RADIUS, h=HOLE_HEIGHT, segments=16))
    return union()([
        right(dx * CORNER_HOLE_X_OFFSET)
        (forward(dy * CORNER_HOLE_Y_OFFSET)
         (hole))
        for dx, dy in [
            (-1, -1),
            (-1, 1),
            (-1, 0),
            (1, 0),
            (1, -1),
            (1, 1),
        ]])

if __name__ == '__main__':
    scad_render_to_file(eight_pole_switch_mount(), 'eight_pole_switch_mount.scad')