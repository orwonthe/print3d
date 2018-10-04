from geoscad.as_units import mm
from geoscad.utilities import grounded_cube, rounded_platter
from solid import scad_render_to_file, cylinder, union, cube, intersection
from solid.utils import forward, back, down, up, right, left

from model_railroading.peco_turnout_motor import POLE_HOLE_WIDTH, POLE_HOLE_LENGTH

# X dimensions
MOUNT_X_CLEARANCE = 22 @ mm
SCREW_HEAD_DIAMETER = 10 @ mm
HOLE_MARGIN = 0.5 * SCREW_HEAD_DIAMETER
MOUNTING_POLE_HOLE_WIDTH = 4.0 @ mm
CORNER_HOLE_RADIUS = 1.8 @ mm
PLATTER_WIDTH = MOUNT_X_CLEARANCE + 2 * SCREW_HEAD_DIAMETER
CORNER_HOLE_X_OFFSET = 0.5 * PLATTER_WIDTH - HOLE_MARGIN
SIDE_SLOT_WIDTH = 4.8 @ mm
SIDE_SLOT_RADIUS = 0.5 * SIDE_SLOT_WIDTH
MOUNT_SLOT_WIDTH = 3.8 @ mm
MOUNT_SLOT_X_OFFSET = (0.5 * 9.4) @ mm
TOP_SLOT_LENGTH = 10.0 @ mm
SHIFTINESS = SCREW_HEAD_DIAMETER + 0.01

# Y dimensions
MOUNT_Y_CLEARANCE = 38 @ mm
MOUNT_SLOT_Y_OFFSET = 15.8 @ mm
PLATTER_LENGTH = MOUNT_Y_CLEARANCE + 2 * SCREW_HEAD_DIAMETER
CORNER_HOLE_Y_OFFSET = 0.5 * PLATTER_LENGTH - HOLE_MARGIN
SIDE_SLOT_LENGTH = 15.0 @ mm
MOUNT_SLOT_THICKNESS = 1.8 @ mm


# Z dimensions
PLATTER_HEIGHT = 4 @ mm
MOUNT_DEPRESSION = 1 @ mm
HOLE_EXTENSION = 1 @ mm
HOLE_HEIGHT = PLATTER_HEIGHT + 2 * HOLE_EXTENSION



def narrow_peco_motor_mount():
    return intersection()([
        peco_motor_mount(),
        narrow_clipper(),
    ])


def narrow_clipper():
    return grounded_cube([MOUNT_X_CLEARANCE - 0.01, 2 * PLATTER_LENGTH, HOLE_HEIGHT])

def side_peco_motor_mount():
    return intersection()([
        peco_motor_mount(),
        side_clipper(),
    ])

def side_clipper():
    return left(SHIFTINESS)(grounded_cube([PLATTER_WIDTH, 2 * PLATTER_LENGTH, HOLE_HEIGHT]))

def ul_corner_peco_motor_mount():
    return intersection()([
        peco_motor_mount(),
        ul_corner_clipper_clipper(),
    ])

def ul_corner_clipper_clipper():
    return left(SHIFTINESS)(
        back(SHIFTINESS)(
            grounded_cube([PLATTER_WIDTH, PLATTER_LENGTH, HOLE_HEIGHT])))

def ur_corner_peco_motor_mount():
    return intersection()([
        peco_motor_mount(),
        ur_corner_clipper_clipper(),
    ])

def ur_corner_clipper_clipper():
    return right(SHIFTINESS)(
        back(SHIFTINESS)(
            grounded_cube([PLATTER_WIDTH, PLATTER_LENGTH, HOLE_HEIGHT])))


def short_peco_motor_mount():
    return intersection()([
        peco_motor_mount(),
        short_clipper(),
    ])


def short_clipper():
    return grounded_cube([2 * PLATTER_WIDTH, MOUNT_Y_CLEARANCE - 0.01, HOLE_HEIGHT])


def top_peco_motor_mount():
    return intersection()([
        peco_motor_mount(),
        top_clipper(),
    ])

def top_clipper():
    return back(SHIFTINESS)(grounded_cube([2 * PLATTER_WIDTH, PLATTER_LENGTH, HOLE_HEIGHT]))

def peco_motor_mount():
    return platter() - mount_depression() - holes()


def mount_depression():
    return up(PLATTER_HEIGHT)(cube([MOUNT_X_CLEARANCE, MOUNT_Y_CLEARANCE, 2 * MOUNT_DEPRESSION], center=True))

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
        for dx, dy in [
            (-1, -1),
            (-1, -0.6),
            (-1, 0.6),
            (-1, 1.0),
            (-0.55, -1),
            (-0.55, 1.0),
            (0.55, -1),
            (0.55, 1.0),
            (1, -1),
            (1, -0.6),
            (1, 0.6),
            (1, 1.0),
        ]])


def pole_hole():
    return grounded_cube([POLE_HOLE_WIDTH, POLE_HOLE_LENGTH, HOLE_HEIGHT])


def side_slots():
    return x_side_slots() + y_side_slots()


def x_side_slots():
    slot = rounded_platter([TOP_SLOT_LENGTH, SIDE_SLOT_WIDTH, HOLE_HEIGHT], SIDE_SLOT_RADIUS)
    return forward(CORNER_HOLE_Y_OFFSET)(slot) + back(CORNER_HOLE_Y_OFFSET)(slot)


def y_side_slots():
    slot = rounded_platter([SIDE_SLOT_WIDTH, SIDE_SLOT_LENGTH,  HOLE_HEIGHT], SIDE_SLOT_RADIUS)
    return left(CORNER_HOLE_X_OFFSET)(slot) + right(CORNER_HOLE_X_OFFSET)(slot)




if __name__ == '__main__':
    scad_render_to_file(peco_motor_mount(), 'peco_motor_mount.scad')
    scad_render_to_file(short_peco_motor_mount(), 'short_peco_motor_mount.scad')
    scad_render_to_file(narrow_peco_motor_mount(), 'narrow_peco_motor_mount.scad')
    scad_render_to_file(top_peco_motor_mount(), 'top_peco_motor_mount.scad')
    scad_render_to_file(side_peco_motor_mount(), 'side_peco_motor_mount.scad')
    scad_render_to_file(ul_corner_peco_motor_mount(), 'ul_corner_peco_motor_mount.scad')
    scad_render_to_file(ur_corner_peco_motor_mount(), 'ur_peco_motor_mount.scad')
