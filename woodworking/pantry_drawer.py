import math

from geoscad.as_units import nscale_feet, nscale_inches, AsUnits, inches, mm
from geoscad.utilities import grounded_cube
from solid import scad_render_to_file, cylinder, rotate, cube, mirror, multmatrix, scale
from solid.utils import up, right, forward, left, back, union, down

from utilities.file_utilities import save_as_scad

FRAME_THICKNESS = 0.5 * inches
BOTTOM_THICKNESS = 0.25 * inches
BOTTOM_ELEVATION = 0.25 * inches
WIDTH = 19 * inches
DEPTH = 23 * inches
DOOR_DEPTH = 11 * inches
DADO_DEPTH = 0.25 * inches
DADO_WIDTH = 0.25 * inches
FRONT_HEIGHT = 2 * inches + BOTTOM_ELEVATION + BOTTOM_THICKNESS
BACK_HEIGHT = 5 * inches + BOTTOM_ELEVATION + BOTTOM_THICKNESS
MIDDLE_HEIGHT = (FRONT_HEIGHT + BACK_HEIGHT) / 2
TRANSITION_RADIUS = (BACK_HEIGHT - MIDDLE_HEIGHT)
TRANSITION_DEPTH = DEPTH - DOOR_DEPTH + TRANSITION_RADIUS
FRONT_OFFSET = (DEPTH - FRAME_THICKNESS) / 2
BACK_OFFSET = (DEPTH - FRAME_THICKNESS) / 2
SIDE_OFFSET = (WIDTH - FRAME_THICKNESS) / 2
EXPLOSION_FACTOR = 5 * inches
BOTTOM_CLEARANCE = 2 * 1.0 / 16 * inches

measurements = {'transition': {'depth': TRANSITION_DEPTH / inches, 'radius': TRANSITION_RADIUS / inches}}
def main():
    save_as_scad(display_drawer(), 'pantry_drawer.scad')
    print(measurements)


def display_drawer():
    return assembled_drawer() + exploded_drawer()


def assembled_drawer():
    return pantry_drawer(False)


def exploded_drawer():
    return pantry_drawer(True)


def pantry_drawer(explode):
    return drawer_front(explode) + drawer_back(explode) + drawer_bottom(explode) + drawer_right(explode) + drawer_left(
        explode)
    # return drawer_front(explode)  + drawer_bottom(explode) + drawer_right(explode) + drawer_left(explode)


def drawer_front(explode):
    offset = FRONT_OFFSET
    if explode:
        offset += EXPLOSION_FACTOR
    bottom_dado = back(FRAME_THICKNESS / 2)(up(BOTTOM_ELEVATION)(
        grounded_cube([WIDTH - FRAME_THICKNESS * 2 + DADO_DEPTH * 2, 2 * DADO_DEPTH, BOTTOM_THICKNESS])))
    side_dado = back(FRAME_THICKNESS / 2)(cube([DADO_WIDTH, 2 * DADO_DEPTH, 3 * BACK_HEIGHT], center=True))
    side_dado_offset = WIDTH / 2 - FRAME_THICKNESS + DADO_WIDTH / 2
    width = WIDTH
    measurements['front'] = {'width': width / inches, 'height': FRONT_HEIGHT / inches}
    return forward(offset)(
        grounded_cube([width, FRAME_THICKNESS, FRONT_HEIGHT]) - bottom_dado - left(side_dado_offset)(side_dado) - right(
            side_dado_offset)(side_dado))


def drawer_back(explode):
    offset = BACK_OFFSET
    if explode:
        offset += EXPLOSION_FACTOR
    width = WIDTH - 2 * FRAME_THICKNESS + 2 * DADO_DEPTH
    bottom_dado = forward(FRAME_THICKNESS / 2)(
        up(BOTTOM_ELEVATION)(grounded_cube([2 * WIDTH, 2 * DADO_DEPTH, BOTTOM_THICKNESS])))
    tongue_offset = width / 2
    tongue_cut_depth = FRAME_THICKNESS - DADO_WIDTH
    tongue_cut = back(FRAME_THICKNESS / 2)(cube([2 * DADO_DEPTH, 2 * tongue_cut_depth, 3 * BACK_HEIGHT], center=True))
    measurements['back'] = {'width': width / inches, 'height': BACK_HEIGHT / inches}
    return back(offset)(
        grounded_cube([width, FRAME_THICKNESS, BACK_HEIGHT]) - bottom_dado - left(tongue_offset)(tongue_cut) - right(
            tongue_offset)(tongue_cut))


def drawer_left(explode):
    offset = SIDE_OFFSET
    if explode:
        offset += EXPLOSION_FACTOR
    lower_back_offset = (FRAME_THICKNESS - DADO_DEPTH) / 2
    depth = DEPTH - FRAME_THICKNESS + DADO_DEPTH
    measurements['side'] = {'depth': depth / inches, 'height': FRONT_HEIGHT / inches}
    upper_depth = DEPTH - TRANSITION_DEPTH
    upper_back_offset = lower_back_offset + (depth - upper_depth) / 2
    lower_section = back(lower_back_offset)(grounded_cube([FRAME_THICKNESS, depth, FRONT_HEIGHT]))
    upper_section = back(upper_back_offset)(grounded_cube([FRAME_THICKNESS, upper_depth, BACK_HEIGHT]))
    roller = rotate(a=90, v=[0, 1, 0])(cylinder(r=TRANSITION_RADIUS, h=FRAME_THICKNESS, segments=32, center=True))
    transition_offset = TRANSITION_DEPTH - DEPTH / 2
    rolldown = up(MIDDLE_HEIGHT)(back(transition_offset)(roller))
    filler_cube = back(transition_offset - TRANSITION_RADIUS)(
        grounded_cube([FRAME_THICKNESS - 0.1, 2 * TRANSITION_RADIUS, MIDDLE_HEIGHT]))
    filler = filler_cube - forward(2 * TRANSITION_RADIUS)(rolldown)
    bottom_dado = forward(FRAME_THICKNESS - lower_back_offset)(
        right(FRAME_THICKNESS / 2)(up(BOTTOM_ELEVATION)(grounded_cube([2 * DADO_DEPTH, depth, BOTTOM_THICKNESS]))))
    side_dado = right(FRAME_THICKNESS / 2)(cube([2 * DADO_DEPTH, DADO_WIDTH, 3 * BACK_HEIGHT], center=True))
    side_dado_offset = DEPTH / 2 - FRAME_THICKNESS + DADO_WIDTH / 2
    tongue_offset = depth / 2
    tongue_cut_depth = FRAME_THICKNESS - DADO_WIDTH
    tongue_cut = left(FRAME_THICKNESS / 2)(cube([2 * tongue_cut_depth, 2 * DADO_DEPTH, 3 * BACK_HEIGHT], center=True))
    cuts = bottom_dado + back(side_dado_offset)(side_dado) + forward(tongue_offset)(tongue_cut)
    return left(offset)(lower_section + upper_section + rolldown + filler - cuts)


def drawer_bottom(explode):
    offset = BOTTOM_ELEVATION
    if explode:
        offset -= EXPLOSION_FACTOR
    width = WIDTH - 2 * FRAME_THICKNESS + 2 * DADO_DEPTH - BOTTOM_CLEARANCE
    depth = DEPTH - 2 * FRAME_THICKNESS + 2 * DADO_DEPTH - BOTTOM_CLEARANCE
    measurements['bottom'] = {'depth': depth / inches, 'width': width / inches}
    return up(offset)(grounded_cube([width, depth, BOTTOM_THICKNESS]))


def drawer_right(explode):
    return mirror([1, 0, 0])(drawer_left(explode))


if __name__ == '__main__':
    main()
