from geoscad.as_units import mm, inches
from geoscad.utilities import grounded_cube, rounded_platter
from solid import scad_render_to_file, cylinder, union, cube, intersection, scale
from solid.utils import forward, back, down, up, right, left, math, rotate



def main():
    # scad_render_to_file(battery_cup(), 'battery_cup.scad')
    # scad_render_to_file(coffee_cover(85 * mm), 'coffee_cover.scad')
    scad_render_to_file(coffee_cover(95 * mm), 'coffee_cover.scad')

def coffee_cover(diameter):
    height = 19 * mm
    thickness = 2 * mm
    notch = forward(diameter/2 - 5*mm)((up(height)(rotate([-90, 0, 0])(cylinder(r=12 * mm, h=10 * mm)))))
    return cup(diameter, height, thickness, segments=96) - notch

def cup(diameter, height, thickness, segments=32):
    outer = cylinder(r=diameter/2 + thickness, h=height, segments=segments)
    inner = cylinder(r=diameter/2, h=height, segments=segments)
    return outer - up(thickness)(inner)


def battery_cup():
    height = 39 * mm
    diameter = 36 * mm
    squish = 31 * mm / diameter
    thickness = 2 * mm
    return scale([1.0, squish, 1.0])(cup(diameter, height, thickness))

if __name__ == '__main__':
    main()
