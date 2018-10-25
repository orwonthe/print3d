import math
from typing import Optional

from geoscad.as_units import mm, inches
from geoscad.utilities import grounded_cube
from solid import scad_render_to_file, cylinder, union, rotate, sphere, cube, mirror
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
BUTTON_HOLE_DIAMETER = 0.27 * inches
BUTTON_HOLE_X_OFFSETS = [8.2 * mm, -3 * mm]
BUTTON_HOLE_Y_OFFSETS = [3 * mm, -3 * mm]

LED_HOLE_DIAMETER = 5.3 * mm
LED_OFFSET = 0.5 * 0.78 * inches
BUTTON_LED_X_OFFSETS = [-11.5 * mm, 4.2 * mm]
BUTTON_LED_Y_OFFSETS = [-0.2 * mm, 11.5 * mm]

SWITCH_CLEAT_WIDTH = 1.0 * mm
SWITCH_CLEAT_LENGTH = 2.5 * mm
SWITCH_CLEAT_OFFSET = 6 * mm

GROOVE_DIAMETER = 2 * mm
GROOVE_OFFSET = 7.5 * mm

INSERT_HEIGHT = GROOVE_DIAMETER
TAB_HEIGHT = 2 * INSERT_HEIGHT
TAB_WIDTH = GROOVE_DIAMETER
TAB_LENGTH = 2 * GROOVE_DIAMETER

INSERT_THICKNESS = TAB_WIDTH - 0.8 * mm
INSERT_TAB_HEIGHT = INSERT_HEIGHT + DEFAULT_CONNECTOR_BLOCK_THICKNESS
INSERT_TAB_LENGTH = TAB_LENGTH - 0.8 * mm
INSERT_SIZES = ['turnout_left', 'turnout_right', 'short', 'medium', 'long']


def main():
    cube_size = 1.25 * inches
    for insert_sizing in INSERT_SIZES:
        scad_render_to_file(groove_insert(cube_size, insert_sizing), f'{insert_sizing}_insert.scad')
    scad_render_to_file(turnout_block(cube_size), 'turnout_right.scad')
    scad_render_to_file(turnout_block(cube_size, left_hand=True), 'turnout_left.scad')
    scad_render_to_file(diagonal_block(cube_size), 'diagonal_block.scad')
    scad_render_to_file(diagonal_block(cube_size, True), 'double_diagonal_block.scad')
    scad_render_to_file(empty_block(cube_size), 'empty_block.scad')
    scad_render_to_file(panel_block(cube_size), 'panel_block.scad')
    scad_render_to_file(panel_block(cube_size, True), 'crossed_block.scad')


def groove_insert(cube_size, insert_sizing):
    assert insert_sizing in INSERT_SIZES
    is_diagonal = not insert_sizing == 'long'
    is_turn_out = 'turnout' in insert_sizing
    is_short = insert_sizing == 'short'
    is_right_handed_turnout = is_turn_out and 'right' in insert_sizing
    if is_diagonal:
        spread = 2 * GROOVE_OFFSET
        if is_short or is_turn_out:
            spread = -spread
        insert_length = (cube_size + spread) * math.sqrt(0.5) + INSERT_THICKNESS
        limiting_length = insert_length * math.sqrt(0.5)
        limiter = rotate(45, [0, 1, 0])(cube([limiting_length, limiting_length, limiting_length]))
        if is_turn_out:
            limiter *= up(INSERT_THICKNESS)(right(INSERT_THICKNESS)(limiter))
    else:
        insert_length = cube_size
        limiter = None

    insert = cube([insert_length, INSERT_HEIGHT, INSERT_THICKNESS])
    if limiter:
        insert *= limiter
    tab = right((insert_length - INSERT_TAB_HEIGHT) / 2)(cube([INSERT_TAB_LENGTH, INSERT_TAB_HEIGHT, INSERT_THICKNESS]))
    result = insert + tab
    if is_turn_out:
        result = left(INSERT_THICKNESS)(result)
    if is_right_handed_turnout:
        result = right(insert_length - INSERT_THICKNESS)(mirror([1, 0, 0])(result))
    return result


def turnout_block(cube_size, left_hand=False):
    grooving = grooves(cube_size)
    diagonal_grooves = grooves(cube_size, diagonal=True, turnout=True)
    leds = turnout_led_holes(cube_size)
    button_holes = button_switch_holes(cube_size)
    if not left_hand:
        diagonal_grooves = mirror([1, 0, 0])(diagonal_grooves)
        leds = mirror([1, 0, 0])(leds)
        button_holes = mirror([1, 0, 0])(button_holes)
    holes = leds + grooving + diagonal_grooves + button_holes
    return empty_block(cube_size) - holes


def panel_block(cube_size, crossed=False):
    grooving = grooves(cube_size)
    if crossed:
        grooving += rotate(90, [0, 0, 1])(grooving)
    holes = toggle_switch_hole(cube_size) + block_led_holes(cube_size) + grooving
    return empty_block(cube_size) - holes


def diagonal_block(cube_size, doubled=False):
    return empty_block(cube_size) - grooves(cube_size, diagonal=True, doubled=doubled)


def empty_block(cube_size):
    return sphere_connector_block(cube_size) - thumb_holes(cube_size)


def thumb_holes(cube_size):
    thumb_hole_cylinder = rotate(45 / 2, [0, 0, 1])(  # rotate octogon so top is flat
        cylinder(r=THUMB_HOLE_DIAMETER / 2, h=3 * cube_size, center=True, segments=8)  # octogon
    )
    x_hole = rotate(90, [1, 0, 0])(thumb_hole_cylinder)
    y_hole = rotate(90, [0, 1, 0])(thumb_hole_cylinder)
    return up(cube_size / 2)(x_hole + y_hole)


def turnout_led_holes(cube_size):
    single_led_hole = led_hole(cube_size)
    leds = [
        right(BUTTON_LED_X_OFFSETS[index])(
            forward(BUTTON_LED_Y_OFFSETS[index])(single_led_hole)
        )
        for index in range(len(BUTTON_LED_Y_OFFSETS))
    ]
    return union()(leds)


def block_led_holes(cube_size):
    single_led_hole = led_hole(cube_size)
    return left(LED_OFFSET)(single_led_hole) + right(LED_OFFSET)(single_led_hole)


def led_hole(cube_size):
    return cylinder(r=LED_HOLE_DIAMETER / 2, h=cube_size, center=True, segments=16)


def toggle_switch_hole(cube_size):
    main_hole = cylinder(r=SWITCH_HOLE_DIAMETER / 2, h=cube_size, center=True, segments=16)
    return main_hole + cleat_opening()


def button_switch_holes(cube_size):
    hole_cylinder = cylinder(r=BUTTON_HOLE_DIAMETER / 2, h=cube_size, center=True, segments=16)
    cylinder_with_cleat = hole_cylinder + cleat_opening()
    button_holes = [
        right(BUTTON_HOLE_X_OFFSETS[index])(
            forward(BUTTON_HOLE_Y_OFFSETS[index])(
                rotate(90 + ((index + 1) % 2) * 180)(cylinder_with_cleat)
            )
        )
        for index in range(len(BUTTON_LED_Y_OFFSETS))
    ]
    return union()(button_holes)


def cleat_opening():
    return down(DEFAULT_CONNECTOR_BLOCK_THICKNESS)(back(SWITCH_CLEAT_LENGTH / 2)(right(SWITCH_CLEAT_OFFSET)(
        cube([SWITCH_CLEAT_WIDTH, SWITCH_CLEAT_LENGTH, 3 * DEFAULT_CONNECTOR_BLOCK_THICKNESS])
    )))


def grooves(cube_size, diagonal=False, doubled=False, turnout=False):
    groove = groove_cylinder(cube_size)
    if diagonal:
        groove = rotate(-45)(groove)
        short_offset = 0.5 * (cube_size / 2 - GROOVE_OFFSET)
        long_offset = 0.5 * (cube_size / 2 + GROOVE_OFFSET)
        if turnout:
            x_offsets = [2 * short_offset - long_offset, long_offset]
            y_offsets = [long_offset, long_offset]
        else:
            x_offsets = y_offsets = [short_offset, long_offset]
    else:
        x_offsets = [0, 0]
        y_offsets = [-GROOVE_OFFSET, GROOVE_OFFSET]
    groove_pair = union()([
        right(x_offset)(forward(y_offset)(groove))
        for x_offset, y_offset in zip(x_offsets, y_offsets)
    ])
    if turnout:
        limiting_block = forward(cube_size + GROOVE_OFFSET)(
            cube([2 * cube_size, 2 * cube_size, 2 * cube_size], center=True))
        groove_pair *= limiting_block
    if doubled:
        groove_pair += rotate(180, [0, 0, 1])(groove_pair)
    return groove_pair


def groove_cylinder(cube_size):
    groove = rotate(90, [0, 1, 0])(cylinder(r=GROOVE_DIAMETER / 2, h=cube_size * 2.1, center=True, segments=16))
    groove += cube([TAB_LENGTH, TAB_WIDTH, 3 * DEFAULT_CONNECTOR_BLOCK_THICKNESS], center=True)
    return groove


def peg_connector_block(
        width: float,
        thickness: float = DEFAULT_CONNECTOR_BLOCK_THICKNESS,
        margin=None,
):
    return connector_block(
        connector_peg(thickness=thickness),
        peg_connector_hole(thickness=thickness),
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
        female_connector = peg_connector_hole(thickness=thickness)
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


def peg_connector_hole(
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