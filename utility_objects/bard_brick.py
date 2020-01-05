import math

from geoscad.as_units import mm
from geoscad.utilities import grounded_cube
from solid import scad_render_to_file, rotate, cube, mirror, union
from solid.utils import down, forward, back, up, right

WIDTH = 57 * mm
HEIGHT = 10 * mm
LENGTH = 68 * mm
THICKNESS = 1.6 * mm

HANDLE_WIDTH = 20 * mm
HANDLE_HEIGHT = 4 * mm
HANDLE_LENGTH = 20 * mm

CHOP_WIDTH = 12.6 * mm
CHOP_GAP = 2 * mm
CHOP_HEIGHT = HEIGHT - CHOP_GAP - THICKNESS
CHOP_LENGTH = 3 * THICKNESS
END_RIDGE_Y = 44.7 * mm - LENGTH / 2
END_RIDGE_W = 22 * mm
RIDGE_X = [-0.5 * END_RIDGE_W * mm, 0.5 * END_RIDGE_W * mm]

def bard_brick():
    double_thickness = 2 * THICKNESS
    base = basic_brick(WIDTH, LENGTH, HEIGHT)
    interior = down(THICKNESS)(basic_brick(
        WIDTH - double_thickness,
        LENGTH - double_thickness,
        HEIGHT
    ))
    handle = up(HEIGHT - HANDLE_HEIGHT)(
        forward((LENGTH + HANDLE_LENGTH) / 2 - THICKNESS)(
            grounded_cube([HANDLE_WIDTH, THICKNESS + HANDLE_LENGTH, HANDLE_HEIGHT])
        )
    )
    chop = back(LENGTH / 2)(cube([CHOP_WIDTH, CHOP_LENGTH, 2 * CHOP_HEIGHT], center=True))
    side_ridge = grounded_cube([THICKNESS, LENGTH, HEIGHT])
    side_ridges = union()([
        right(x)(side_ridge)
        for x in RIDGE_X
    ])
    end_ridge = forward(END_RIDGE_Y)(grounded_cube([END_RIDGE_W + THICKNESS, THICKNESS, HEIGHT]))
    brick = base - interior + handle - chop + side_ridges + end_ridge
    return mirror([0,0,1])(
        down(HEIGHT)(brick)
    )


def basic_brick(width, length, height):
    base = grounded_cube([width, length, height])
    limitation_length = math.sqrt(0.5) * (width + height)
    limiter = (rotate(45, [0, 1, 0]))(cube([limitation_length, length * 2, limitation_length], center=True))
    return base * limiter


def main():
    scad_render_to_file(bard_brick(), 'bard_brick.scad')


if __name__ == '__main__':
    main()
