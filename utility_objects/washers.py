from geoscad.as_units import mm
from solid import cylinder
from solid.utils import down

from utilities.file_utilities import save_as_scad


def main():
    save_as_scad(washer(10 * mm, 4 * mm, 2.75 * mm), 'washer.scad')
    save_as_scad(washer(6.4 * mm, 3.4 * mm, 2 * mm), 'washer_small.scad')


def washer(outer_diameter, inner_diameter, thickness):
    return cylinder(r=outer_diameter / 2, h=thickness, segments=32) - down(thickness / 2)(
        cylinder(r=inner_diameter / 2, h=2 * thickness, segments=32))


if __name__ == '__main__':
    main()
