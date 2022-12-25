import math

from geoscad.as_units import mm, Degrees
from geoscad.utilities import grounded_cube
from solid import scad_render_to_file, rotate, cube, mirror, union, cylinder
from solid.utils import down, forward, back, up, right, left

THICKNESS = 1.94 * mm
WIDTH = 55.56 * mm
LENGTH = 81.2 * mm
PULL = LENGTH
HEIGHT = 18.04 * mm
RISE = HEIGHT - THICKNESS
BOTTOM_LENGTH = math.sqrt(RISE * RISE + PULL * PULL) + THICKNESS
# STRETCH = BOTTOM_LENGTH / LENGTH
HALF_LENGTH = 0.5 * BOTTOM_LENGTH
LIP = 2 * mm
BOTTOM_LENGTH_EXTENDED = BOTTOM_LENGTH + LIP
BIG = 3 * BOTTOM_LENGTH
ANGLE = math.degrees(math.atan2(RISE, LENGTH))
REACH = HEIGHT * math.cos(math.radians(ANGLE))
SIDE_OFFSET = (WIDTH - THICKNESS) / 2
CUT_WIDTH = 3.14 * mm
CUT_LENGTH = 3.0 * mm
ROD_RADIUS = 1.5 * mm
ROD_LENGTH = WIDTH + 2 * (5.52 * mm)

def gumball_door():
    return box() - spring_cut() + rod()

def box():
    floor = down(BIG)(grounded_cube([BIG, BIG, BIG]))
    side = forward(HALF_LENGTH)(grounded_cube([THICKNESS, LENGTH, HEIGHT]))
    left_side = left(SIDE_OFFSET)(side)
    right_side = right(SIDE_OFFSET)(side)
    rear = forward(THICKNESS / 2)(grounded_cube([WIDTH, THICKNESS, HEIGHT]))
    door = bottom() + left_side + right_side + rear
    return tilt_back(door) - floor

def rod():
    return up(ROD_RADIUS)(forward(BOTTOM_LENGTH)(left(0.5 * ROD_LENGTH)(rotate(90, [0, 1, 0])(cylinder(r=ROD_RADIUS, h=ROD_LENGTH, segments=16)))))

def spring_cut():
    cut = grounded_cube([CUT_WIDTH * 2, CUT_LENGTH* 2 * 2, HEIGHT * 2])
    return down(HEIGHT)(left(WIDTH * 0.5)(forward(BOTTOM_LENGTH)(cut)))

def bottom():
    offset = 0.5 * BOTTOM_LENGTH_EXTENDED - LIP
    plate = grounded_cube([WIDTH, BOTTOM_LENGTH_EXTENDED, THICKNESS])
    return tilt(forward(offset)(plate))

def tilt(target):
    return rotate(ANGLE, [1, 0, 0])(target)

def tilt_back(target):
    return rotate(-ANGLE, [1, 0, 0])(target)

def main():
    scad_render_to_file(gumball_door(), 'gumball_door.scad')


if __name__ == '__main__':
    main()
