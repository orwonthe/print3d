import math

from geoscad.as_units import mm
from solid import scad_render_to_file, cylinder, rotate
from solid.utils import up

from utilities.file_utilities import save_as_scad

BASE_DIAMETER = 10 * mm
BASE_HEIGHT = 12 * mm

HOLE_DIAMETER = 5 * mm
HOLE_HEIGHT = 7 * mm

COLLAR_HEIGHT = HOLE_HEIGHT - 4.7 * mm
COLLAR_DIAMETER = HOLE_DIAMETER - 0.8 * mm
COLLAR_THICKNESS = 1 * mm


def main():
    save_as_scad(peaked_button(), 'button_peaked.scad')


def peaked_button():
    return up(BASE_HEIGHT + BASE_DIAMETER * math.sqrt(3) / 4)(rotate([180, 0, 0])(base() + ridge() - mounting_hole()))


def base():
    return cylinder(r=BASE_DIAMETER / 2, h=BASE_HEIGHT)


def ridge():
    return up(BASE_HEIGHT)(rotate([90, 0, 0])(cylinder(r=BASE_DIAMETER / 2, h=BASE_DIAMETER, center=True, segments=6)))


def mounting_hole():
    return cylinder(r=HOLE_DIAMETER / 2, h=2 * HOLE_HEIGHT, center=True) - up(COLLAR_HEIGHT)(collar())


def collar():
    return cylinder(r=BASE_DIAMETER / 2, h=COLLAR_THICKNESS, center=True) - cylinder(r=COLLAR_DIAMETER / 2,
                                                                                     h=BASE_HEIGHT * 2, center=True)

if __name__ == '__main__':
    main()
