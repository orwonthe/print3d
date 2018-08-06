from geoscad.as_units import mm
from geoscad.utilities import grounded_cube, rounded_platter
from solid import scad_render_to_file, cylinder, union, cube
from solid.utils import forward, back, down, up, right, left

from model_railroading.peco_turnout_motor import POLE_HOLE_WIDTH, POLE_HOLE_LENGTH

# X dimensions
MOUNT_X_CLEARANCE = 22 @ mm
SCREW_HEAD_DIAMETER = 10 @ mm
HOLE_MARGIN = 0.5 * SCREW_HEAD_DIAMETER
MOUNTING_POLE_HOLE_WIDTH = 4.0 @ mm
CORNER_HOLE_RADIUS = 2 @ mm
PLATTER_WIDTH = MOUNT_X_CLEARANCE + 2 * SCREW_HEAD_DIAMETER
CORNER_HOLE_X_OFFSET = 0.5 * PLATTER_WIDTH - HOLE_MARGIN
SIDE_SLOT_WIDTH = 5 @ mm
SIDE_SLOT_RADIUS = 0.5 * SIDE_SLOT_WIDTH
MOUNT_SLOT_WIDTH = 4.2 @ mm
MOUNT_SLOT_X_OFFSET = (0.5 * 9.4) @ mm

# Y dimensions
MOUNT_Y_CLEARANCE = 38 @ mm
MOUNT_SLOT_Y_OFFSET = 15.8 @ mm
PLATTER_LENGTH = MOUNT_Y_CLEARANCE + 2 * SCREW_HEAD_DIAMETER
CORNER_HOLE_Y_OFFSET = 0.5 * PLATTER_LENGTH - HOLE_MARGIN
SIDE_SLOT_LENGTH = 11.0 @ mm
MOUNT_SLOT_THICKNESS = 2 @ mm


# Z dimensions
PLATTER_HEIGHT = 4 @ mm
MOUNT_DEPRESSION = 1 @ mm
HOLE_EXTENSION = 1 @ mm
HOLE_HEIGHT = PLATTER_HEIGHT + 2 * HOLE_EXTENSION


def mount_depression():
    return up(PLATTER_HEIGHT)(cube([MOUNT_X_CLEARANCE, MOUNT_Y_CLEARANCE, 2 * MOUNT_DEPRESSION], center=True))


def peco_motor_mount():
    return platter() - mount_depression() - holes()


def platter():
    return rounded_platter([PLATTER_WIDTH, PLATTER_LENGTH, PLATTER_HEIGHT], 2)


def mounting_slots():
    slot = grounded_cube([MOUNT_SLOT_WIDTH, MOUNT_SLOT_THICKNESS, HOLE_HEIGHT])
    return union()([
        right(x)(forward(y)(slot))
        for x in [-MOUNT_SLOT_X_OFFSET, MOUNT_SLOT_X_OFFSET]
        for y in [-MOUNT_SLOT_Y_OFFSET, 0, MOUNT_SLOT_Y_OFFSET]
    ])


def holes():
    return down(HOLE_EXTENSION)(
        corner_holes() +
        pole_hole() +
        side_slots() + mounting_slots()
    )


def corner_holes():
    return union()([
        right(dx * CORNER_HOLE_X_OFFSET)
        (forward(dy * CORNER_HOLE_Y_OFFSET)
         (cylinder(r=CORNER_HOLE_RADIUS, h=HOLE_HEIGHT, segments=16)))
        for dx in [-1, 1]
        for dy in [-1, 1]])


def pole_hole():
    return grounded_cube([POLE_HOLE_WIDTH, POLE_HOLE_LENGTH, HOLE_HEIGHT])


def side_slots():
    return x_side_slots() + y_side_slots()


def x_side_slots():
    slot = rounded_platter([SIDE_SLOT_LENGTH, SIDE_SLOT_WIDTH, HOLE_HEIGHT], SIDE_SLOT_RADIUS)
    return forward(CORNER_HOLE_Y_OFFSET)(slot) + back(CORNER_HOLE_Y_OFFSET)(slot)


def y_side_slots():
    slot = rounded_platter([SIDE_SLOT_WIDTH, SIDE_SLOT_LENGTH,  HOLE_HEIGHT], SIDE_SLOT_RADIUS)
    return left(CORNER_HOLE_X_OFFSET)(slot) + right(CORNER_HOLE_X_OFFSET)(slot)




if __name__ == '__main__':
    scad_render_to_file(peco_motor_mount(), 'peco_motor_mount.scad')
