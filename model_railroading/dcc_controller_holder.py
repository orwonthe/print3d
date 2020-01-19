import math

from geoscad.as_units import nscale_feet, nscale_inches, AsUnits, inches, mm
from geoscad.utilities import grounded_cube
from solid import scad_render_to_file, cylinder, rotate, cube, mirror, multmatrix, scale
from solid.utils import up, right, forward, left, back, union, down

from utilities.file_utilities import save_as_scad

HOLDER_THICKNESS = 5.0 * mm

# X
HOLDER_WIDTH = 2.5 * inches
CORNER_RADIUS = 0.15* inches
FLANGE_WIDTH = 0.5 * inches + CORNER_RADIUS
TAB_OVERLAP = 0.3 * inches
SCREW_HOLE_DIAMETER = 3 / 16 * inches

TOTAL_WIDTH = HOLDER_WIDTH + 2 * HOLDER_THICKNESS + 2 * FLANGE_WIDTH

# Y
HOLDER_DEPTH = 1.25 * inches

TOTAL_DEPTH = HOLDER_DEPTH + 2 * HOLDER_THICKNESS

# Z
HOLDER_HEIGHT = 0.2 * inches


def main():
    save_as_scad(dcc_contoller_holder(), 'dcc_controller_holder.scad')


def dcc_contoller_holder():
    # return down(0.5 * HOLDER_HEIGHT)(cuts())
    return outer_block() - down(0.5 * HOLDER_HEIGHT)(cuts())


def outer_block():
    return back(HOLDER_THICKNESS)(forward_cube([TOTAL_WIDTH, TOTAL_DEPTH, HOLDER_HEIGHT]))


def cuts():
    return tab_cut() + back_side_cuts() + flange_side_cuts() + flange_corners() + inner_wide_cut() + inner_narrow_cut()


def tab_cut():
    width = HOLDER_WIDTH - 2 * TAB_OVERLAP
    height = 2 * HOLDER_HEIGHT
    depth = 2 * HOLDER_DEPTH
    return forward_cube([width, depth, height])

def back_side_cuts():
    width = FLANGE_WIDTH * 2
    offset_x = 0.5 * width + 0.5 * HOLDER_WIDTH + HOLDER_THICKNESS + CORNER_RADIUS
    height = 2 * HOLDER_HEIGHT
    depth = 2 * HOLDER_DEPTH
    cut = forward_cube([width, depth, height])
    return left(offset_x)(cut) + right(offset_x)(cut)

def flange_side_cuts():
    width = FLANGE_WIDTH * 2
    offset_x = 0.5 * width + 0.5 * HOLDER_WIDTH + HOLDER_THICKNESS
    offset_y = CORNER_RADIUS
    height = 2 * HOLDER_HEIGHT
    depth = 2 * HOLDER_DEPTH
    cut = forward(offset_y)(forward_cube([width, depth, height]))
    return left(offset_x)(cut) + right(offset_x)(cut)

def flange_corners():
    outer_offset_x = 0.5 * HOLDER_WIDTH + HOLDER_THICKNESS + CORNER_RADIUS
    inner_offset_x = 0.5 * HOLDER_WIDTH - CORNER_RADIUS
    offset_y = HOLDER_DEPTH - 2 * CORNER_RADIUS
    corner = corner_cylinder()
    inner_corners = left(inner_offset_x)(corner) + right(inner_offset_x)(corner)
    tab_corners = forward(offset_y)(inner_corners)
    outer_corners = left(outer_offset_x)(corner) + right(outer_offset_x)(corner)
    return inner_corners + tab_corners + outer_corners

def inner_narrow_cut():
    width = HOLDER_WIDTH - 2 * CORNER_RADIUS
    depth = HOLDER_DEPTH
    height = 2 * HOLDER_HEIGHT
    return forward_cube([width, depth, height])

def inner_wide_cut():
    width = HOLDER_WIDTH
    depth = HOLDER_DEPTH  - 2 * CORNER_RADIUS
    height = 2 * HOLDER_HEIGHT
    offset_y = CORNER_RADIUS
    return forward(offset_y)(forward_cube([width, depth, height]))


def forward_cube(shape):
    offset_y = 0.5 * shape[1]
    return forward(offset_y)(grounded_cube(shape))

def corner_cylinder():
    return forward(CORNER_RADIUS)(cylinder(r=CORNER_RADIUS, h=3 * HOLDER_HEIGHT))

if __name__ == '__main__':
    main()
