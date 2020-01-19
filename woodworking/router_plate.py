import math

from geoscad.as_units import nscale_feet, nscale_inches, AsUnits, inches, mm
from geoscad.utilities import grounded_cube
from solid import scad_render_to_file, cylinder, rotate, cube, mirror, multmatrix, scale
from solid.utils import up, right, forward, left, back, union, down

from utilities.file_utilities import save_as_scad

INFLATION_DEFAULT = 0.05 * mm
PLATE_DIAMETER = 3.90 * inches
PLATE_THICKNESS = 0.28 * inches
TOP_PLATE_THICKNESS = 0.09 * inches
TOOL_HOLE_DIAMETER = 0.29 * inches
TOOL_HOLE_DISPLACEMENT = 3.11 * inches
GROOVE_THICKNESS = 0.11 * inches
GROOVE_DEPTH = 0.12 * inches
TAB_DEPTH = 0.06 * inches
INNER_DIAMETER = PLATE_DIAMETER - 2 * GROOVE_DEPTH
TAB_DIAMETER = PLATE_DIAMETER - 2 * TAB_DEPTH
TAB_WIDTH = 1.64 * inches
TAB_SINE = TAB_WIDTH / INNER_DIAMETER
TAB_ANGLE = math.asin(TAB_SINE)


def main():
    for index in range(8, 17):
        scad_file_name = f'router_plate_{index}.scad'
        opening_diameter = index / 8
        print(opening_diameter, scad_file_name)
        save_as_scad(RouterPlate()(opening_diameter * inches), scad_file_name)


class RouterPlate:
    def __init__(self, inflation=INFLATION_DEFAULT):
        self.inflation = inflation

    def __call__(self, opening_diameter):
        plate = self.router_plate(opening_diameter) - self.center_opening(opening_diameter) - self.tool_holes()
        return rotate(15, [0, 0, 1])(plate)

    def router_plate(self, opening_diameter):
        return self.top_plate() + self.inner_cylinder() + self.tabs() - self.groove_cuts()


    def top_plate(self):
        radius = PLATE_DIAMETER / 2
        thickness = TOP_PLATE_THICKNESS
        height = thickness - 2 * self.inflation
        vertical_offset = height / 2
        return up(vertical_offset)(
            cylinder(
                r=radius - self.inflation,
                h=thickness - 2 * self.inflation,
                center=True,
                segments=64
            ))

    def inner_cylinder(self):
        height = PLATE_THICKNESS - 2 * self.inflation
        return up(height/2)(cylinder(
            r=INNER_DIAMETER / 2 - self.inflation,
            h=height,
            center=True,
            segments=64
        ))

    def tab_cylinder(self):
        height = PLATE_THICKNESS - 2 * self.inflation
        return up(height/2)(cylinder(
            r=TAB_DIAMETER / 2 - self.inflation,
            h=height,
            center=True,
            segments=64
        ))

    def tabs(self):
        c = math.cos(TAB_ANGLE)
        s = math.sin(TAB_ANGLE)
        alpha = 1.0 / (math.sqrt(4.0 - c * c) / (2 * s))
        post = self.inner_cylinder()
        ytabs = scale([2, alpha, 1])(post)
        xtabs = scale([alpha, 2, 1])(post)
        return self.tab_cylinder() * (xtabs + ytabs)

    def groove_cuts(self):
        steps = 10
        delta = 1.0 / steps
        return union()([self.single_groove_cut(delta * (1 + index)) for index in range(steps)])

    def single_groove_cut(self, ratio):
        angle = -math.degrees(TAB_ANGLE) * ratio
        side = TAB_DIAMETER + 2 * self.inflation
        offset = TAB_DIAMETER - ratio * GROOVE_THICKNESS
        vertical_offset = TOP_PLATE_THICKNESS
        single = grounded_cube([side, side, GROOVE_THICKNESS + 2 * self.inflation])
        grooves = left(offset)(single) + right(offset)(single) + forward(offset)(single) + back(offset)(single)
        return up(vertical_offset)(rotate(angle , v=[0, 0, 1])(grooves))

    def center_opening(self, opening_diameter):
        return cylinder(
            r=opening_diameter/2 + self.inflation,
            h=PLATE_THICKNESS*2,
            center=True,
            segments=64
        )

    def tool_holes(self):
        offset = TOOL_HOLE_DISPLACEMENT / 2
        hole = cylinder(
            r=TOOL_HOLE_DIAMETER/2 + self.inflation,
            h=2 * PLATE_THICKNESS,
            center=True,
            segments=32
        )
        return left(offset)(hole) + right(offset)(hole)


if __name__ == '__main__':
    main()
