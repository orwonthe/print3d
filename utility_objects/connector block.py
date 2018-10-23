from typing import Optional

from geoscad.as_units import mm, inches
from geoscad.utilities import grounded_cube
from solid import scad_render_to_file, cylinder, union, rotate, sphere, cube
from solid.utils import up, right, forward, box_align, left, back, down

HOLE_MARGIN = 0.2 * mm
DEFAULT_CONNECTOR_BLOCK_THICKNESS = 1.5 * mm

DEFAULT_PEG_DIAMETER = 3 * mm
DEFAULT_PEG_HOLE_DIAMETER = DEFAULT_PEG_DIAMETER + HOLE_MARGIN

DEFAULT_SPHERE_DIAMETER = 2 * DEFAULT_CONNECTOR_BLOCK_THICKNESS
DEFAULT_SPHERE_HOLE_DIAMETER = DEFAULT_SPHERE_DIAMETER + HOLE_MARGIN

CONNECTOR_PLACES = [(i, j) for i in [-1, 1] for j in [-1, 1]]
POSITIVE_PLACES = [(i, j) for i, j in CONNECTOR_PLACES if i * j > 0]
NEGATIVE_PLACES = [(i, j) for i, j in CONNECTOR_PLACES if i * j < 0]

THUMB_HOLE_DIAMETER = 0.9 * inches

SWITCH_HOLE_DIAMETER = 0.25 * inches

LED_HOLE_DIAMETER = 5.3 * mm
LED_OFFSET = 0.5 * 0.78 * inches

SWITCH_CLEAT_WIDTH = 1.0 * mm
SWITCH_CLEAT_LENGTH = 2.5 * mm
SWITCH_CLEAT_OFFSET = 6 * mm

GROOVE_DIAMETER = 2 * mm
GROOVE_OFFSET = 7.5 * mm


def main():
    cube_size = 1.25 * inches
    scad_render_to_file(sphere_connector_block(cube_size), 'sphere_connector_block.scad')
    scad_render_to_file(peg_connector_block(cube_size), 'peg_connector_block.scad')
    scad_render_to_file(panel_block(cube_size), 'panel_block.scad')


def panel_block(cube_size):
    block = sphere_connector_block(cube_size * inches)
    thumb_hole_cylinder = rotate(45 / 2, [0, 0, 1])(  # rotate octogon so top is flat
        cylinder(r=THUMB_HOLE_DIAMETER / 2, h=3 * cube_size, center=True, segments=8)  # octogon
    )
    x_hole = rotate(90, [1, 0, 0])(thumb_hole_cylinder)
    y_hole = rotate(90, [0, 1, 0])(thumb_hole_cylinder)
    thumb_holes = up(cube_size / 2)(x_hole + y_hole)
    switch_hole = cylinder(r=SWITCH_HOLE_DIAMETER / 2, h=cube_size, center=True, segments=16)
    led_hole = cylinder(r=LED_HOLE_DIAMETER / 2, h=cube_size, center=True, segments=16)
    led_holes = left(LED_OFFSET)(led_hole) + right(LED_OFFSET)(led_hole)
    cleat_hole = down(DEFAULT_CONNECTOR_BLOCK_THICKNESS)(back(SWITCH_CLEAT_LENGTH / 2)(right(SWITCH_CLEAT_OFFSET)(
        cube([SWITCH_CLEAT_WIDTH, SWITCH_CLEAT_LENGTH, 3 * DEFAULT_CONNECTOR_BLOCK_THICKNESS])
    )))
    groove = rotate(90, [0, 1, 0])(cylinder(r=GROOVE_DIAMETER / 2, h=cube_size * 1.1, center=True, segments=16))
    grooves = forward(GROOVE_OFFSET)(groove) + back(GROOVE_OFFSET)(groove)

    holes = thumb_holes + switch_hole + led_holes + cleat_hole + grooves
    return block - holes


def peg_connector_block(
        width: float,
        thickness: float = DEFAULT_CONNECTOR_BLOCK_THICKNESS,
        margin=None,
):
    return connector_block(
        connector_peg(thickness=thickness),
        connector_hole(thickness=thickness),
        width,
        thickness,
        margin
    )


def sphere_connector_block(
        width: float,
        thickness: float = DEFAULT_CONNECTOR_BLOCK_THICKNESS,
        margin=None,
):
    return connector_block(
        connector_sphere(),
        connector_sphere_hole(),
        width,
        thickness,
        margin
    )


def connector_block(
        male_connector,
        female_connector,
        width: float,
        thickness: float = DEFAULT_CONNECTOR_BLOCK_THICKNESS,
        margin=None,
):
    if margin is None:
        margin = DEFAULT_PEG_DIAMETER
    if male_connector is None:
        male_connector = connector_peg(thickness=thickness)
    if female_connector is None:
        female_connector = connector_hole(thickness=thickness)
    inner_width = width - 2 * thickness
    outer_cube = grounded_cube([width, width, width])
    inner_cube = up(thickness)(grounded_cube([inner_width, inner_width, width]))
    connector_offset = width / 2 - margin - thickness
    the_male_connectors = male_connectors(male_connector, connector_offset, width)
    the_female_connectors = female_connectors(female_connector, connector_offset, width)
    return outer_cube - inner_cube + the_male_connectors - the_female_connectors


def connector_peg(
        peg_diameter: float = DEFAULT_PEG_DIAMETER,
        peg_length: Optional[float] = None,
        thickness: float = DEFAULT_CONNECTOR_BLOCK_THICKNESS
):
    if peg_length is None:
        peg_length = peg_diameter
    return cylinder(r=peg_diameter / 2, h=peg_length + thickness, center=False, segments=16)


def connector_hole(
        hole_diameter: float = DEFAULT_PEG_HOLE_DIAMETER,
        thickness: float = DEFAULT_CONNECTOR_BLOCK_THICKNESS
):
    return cylinder(r=hole_diameter / 2, h=3 * thickness, center=True, segments=16)


def connector_sphere(
        diameter: float = DEFAULT_SPHERE_DIAMETER,
):
    return sphere(r=diameter / 2, segments=16)


def connector_sphere_hole(
        diameter: float = DEFAULT_SPHERE_HOLE_DIAMETER,
):
    return sphere(r=diameter / 2, segments=16)


def male_connectors(male_connector, connector_offset, width):
    return markers(POSITIVE_PLACES, male_connector, connector_offset, width)


def female_connectors(female_connector, connector_offset, width):
    return markers(NEGATIVE_PLACES, female_connector, connector_offset, width)


def markers(places, target, target_offset, width):
    offsets = [(i * target_offset, j * target_offset) for i, j in places]
    flat_targets = [right(x)(forward(y)(target)) for x, y in offsets]
    return up(width / 2)(faces(flat_targets, width / 2))


def faces(target, offset):
    rot_target = rotate(a=90, v=[0, 0, 1])(target)
    return union()([
        box_align(target, right, offset),
        box_align(target, left, offset),
        box_align(rot_target, forward, offset),
        box_align(rot_target, back, offset),
    ])


if __name__ == '__main__':
    main()
