from geoscad.as_units import mm
from geoscad.utilities import grounded_cube
from solid.utils import down, back, forward, up, cube, right

from utilities.file_utilities import save_as_scad

KEYSTONE_THICKNESS = 1.5 * mm
KEYSTONE_WIDTH = 15.4 * mm
KEYSTONE_OPENING = 18.6 * mm
KEYSTONE_CLASP_OPENING = 22 * mm
KEYSTONE_BOTTOM_SHELF_LENGTH = 1.7 * mm
KEYSTONE_TOP_SHELF_LENGTH = 4 * mm
KEYSTONE_CLASP_DEPTH = 1 * mm
KEYSTONE_DEPTH = 6.6 * mm
KEYSTONE_REACH = KEYSTONE_DEPTH - KEYSTONE_CLASP_DEPTH
KEYSTONE_LENGTH = KEYSTONE_OPENING + KEYSTONE_BOTTOM_SHELF_LENGTH + KEYSTONE_TOP_SHELF_LENGTH
KEYSTONE_CLASP_LENGTH = (KEYSTONE_LENGTH - KEYSTONE_CLASP_OPENING) / 2

def main():
    save_as_scad(keystone(), 'keystone.scad')

def add_keystones(face, jack_placements, height):
    jack = keystone()
    keyhole = keystone_hole()
    for x, h in jack_placements:
        y = h - height / 2
        face -= forward(y)(right(x)(keyhole))
        face += forward(y)(right(x)(jack))
    return face

def keystone_hole():
    depth = KEYSTONE_DEPTH + 3* KEYSTONE_THICKNESS
    return down(KEYSTONE_THICKNESS/2)(grounded_cube([
        KEYSTONE_WIDTH + KEYSTONE_THICKNESS,
        KEYSTONE_LENGTH + KEYSTONE_THICKNESS,
        depth
    ]))

def keystone():
    return keystone_box() + \
           keystone_bottom_shelf() + \
           keystone_top_shelf() + \
           keystone_clasps()


def keystone_box():
    return grounded_cube([
        KEYSTONE_WIDTH + 2 * KEYSTONE_THICKNESS,
        KEYSTONE_LENGTH + 2 * KEYSTONE_THICKNESS,
        KEYSTONE_DEPTH + 2 * KEYSTONE_THICKNESS
    ]) - down(KEYSTONE_THICKNESS)(
        grounded_cube([KEYSTONE_WIDTH, KEYSTONE_LENGTH, KEYSTONE_DEPTH + 4 * KEYSTONE_THICKNESS])
    )

def keystone_bottom_shelf():
    return back((KEYSTONE_LENGTH - KEYSTONE_BOTTOM_SHELF_LENGTH) / 2)(
        grounded_cube([
            KEYSTONE_WIDTH + 2 * KEYSTONE_THICKNESS,
            KEYSTONE_BOTTOM_SHELF_LENGTH + KEYSTONE_THICKNESS,
            KEYSTONE_THICKNESS
        ])
    )

def keystone_top_shelf():
    return forward((KEYSTONE_LENGTH - KEYSTONE_TOP_SHELF_LENGTH) / 2)(
        grounded_cube([
            KEYSTONE_WIDTH + 2 * KEYSTONE_THICKNESS,
            KEYSTONE_TOP_SHELF_LENGTH + KEYSTONE_THICKNESS,
            KEYSTONE_THICKNESS
        ])
    )

def keystone_clasps():
    clasp = up(KEYSTONE_THICKNESS + KEYSTONE_REACH + KEYSTONE_THICKNESS)(
        grounded_cube(
        [
            KEYSTONE_WIDTH + 2 * KEYSTONE_THICKNESS,
            KEYSTONE_CLASP_LENGTH + KEYSTONE_THICKNESS,
            KEYSTONE_CLASP_DEPTH
        ])
    )
    offset = (KEYSTONE_LENGTH - KEYSTONE_CLASP_LENGTH) / 2
    return back(offset)(clasp) + forward(offset)(clasp)

if __name__ == '__main__':
    main()
