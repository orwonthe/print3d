from geoscad.as_units import inches, mm
from geoscad.utilities import grounded_cube
from solid.utils import back, cylinder, rotate, right, up, forward, union, left, down

from circuit_board_enclosures.keystone import add_keystones
from utilities.file_utilities import save_as_scad

NARROW_WIDTH = 2.5 * inches
WIDE_WIDTH = 3.0 * inches
PANEL_THICKNESS = 2 * mm
PANEL_HEIGHT = 1.75 * inches
QUAD_PANEL_HEIGHT = 3 * inches

CONNECTOR_ELEVATION = PANEL_HEIGHT - 0.6 * inches
JACK_OFFSET = 0.925 * inches
PANEL_HOLE_SPACING = 0.8125 * inches
PANEL_HOLE_DIAMETER = 5 * mm


def panel_set():

    front = back(NARROW_WIDTH)(
        rotate(180, [0, 0, 1])(
            rotate(90, [1, 0, 0])(
                forward(PANEL_HEIGHT / 2 + PANEL_THICKNESS)(
                    front_panel()
                )
            )
        )
    )
    back_piece = forward(NARROW_WIDTH)(
        rotate(0, [0, 0, 1])(
            rotate(90, [1, 0, 0])(
                forward(PANEL_HEIGHT / 2 + PANEL_THICKNESS)(
                    back_panel()
                )
            )
        )
    )
    side = up(1.5 * PANEL_THICKNESS)(left(WIDE_WIDTH / 2)(
        rotate(90, [0, 0, 1])(
            rotate(90, [1, 0, 0])(
                forward(PANEL_HEIGHT / 2)(
                    side_panel()
                )
            )
        )
    ))
    mount = down(PANEL_THICKNESS)(
        right(1.5 * inches + PANEL_THICKNESS)(
            rotate([90, 0, -90])(
                mount_panel()
            )
        )
    )
    # return mount
    return front + \
           back_piece + \
           mount + \
           forward((NARROW_WIDTH - PANEL_THICKNESS) / 2)(side) + \
           back((NARROW_WIDTH - PANEL_THICKNESS) / 2)(side)


def front_panel():
    return back_or_front_panel(is_front=True)


def back_panel():
    return back_or_front_panel(is_front=False)


def mount_panel():
    width = 3.0 * inches
    length = 2.0 * inches + 2.0 * PANEL_THICKNESS
    height = 3.0 * inches
    punches = mount_hole_punch(width, length, height)
    bottom_punches = rotate([-90,0,0])(punches)
    back_piece = grounded_cube([width, PANEL_THICKNESS, height]) - punches
    bottom = grounded_cube([width, length, PANEL_THICKNESS])
    return forward(length / 2)(
        back((length - PANEL_THICKNESS) / 2)(
            back_piece
        ) + bottom
    ) - bottom_punches


def mount_hole_punch(width, length, height):
    offsets = [0, PANEL_HEIGHT / 2, WIDE_WIDTH / 2 + PANEL_THICKNESS]
    x_spacing = [(x - 1.5) * PANEL_HOLE_SPACING for x in range(4)]
    z_spacing = [(z - 1) * PANEL_HOLE_SPACING for z in range(3)]
    return spaced_hole_punch(
        offsets,
        [x_spacing, z_spacing],
        diameter=PANEL_HOLE_DIAMETER,
        thickness=length

    )


def side_panel():
    offsets = [
        (x * inches, CONNECTOR_ELEVATION)
        for x in [-0.675, 0.675]
    ]
    return based_jack_panel(
        offsets,
        height=PANEL_HEIGHT,
        width=NARROW_WIDTH - PANEL_THICKNESS,
        length=WIDE_WIDTH
    ) - side_hole_punch()


def side_quadruple_panel():
    offsets = [
        (x * inches, CONNECTOR_ELEVATION + y)
        for x in [-0.675, 0.675]
        for y in [0, 1.30 * inches]
    ]
    return based_jack_panel(
        offsets,
        height=QUAD_PANEL_HEIGHT,
        width=NARROW_WIDTH - PANEL_THICKNESS,
        length=WIDE_WIDTH
    ) - side_hole_punch()


def back_or_front_panel(is_front):
    offset = JACK_OFFSET
    if is_front:
        offset = -offset

    return based_jack_panel(
        [(offset, CONNECTOR_ELEVATION + PANEL_THICKNESS)],
        height=PANEL_HEIGHT + PANEL_THICKNESS,
        width=WIDE_WIDTH,
        length=NARROW_WIDTH
    ) - front_back_hole_punch()


def front_back_hole_punch():
    return hole_punch(
        [0, PANEL_HEIGHT / 2, (NARROW_WIDTH + PANEL_THICKNESS) / 2],
        PANEL_HOLE_SPACING,
        diameter=PANEL_HOLE_DIAMETER,
        thickness=PANEL_THICKNESS * 2
    )


def side_hole_punch():
    return hole_punch(
        [0, PANEL_HEIGHT / 2, WIDE_WIDTH / 2],
        PANEL_HOLE_SPACING,
        diameter=PANEL_HOLE_DIAMETER,
        thickness=PANEL_HEIGHT
    )


def based_jack_panel(jack_placements, width, length, height=PANEL_HEIGHT, thickness=PANEL_THICKNESS):
    return jacked_panel(jack_placements, width, height, thickness) + \
           back(height / 2)(panel_base(width, length, thickness))


def jacked_panel(jack_placements, width, height=PANEL_HEIGHT, thickness=PANEL_THICKNESS):
    face = panel_face(width, height, thickness)
    return add_keystones(face, jack_placements, height)


def panel_face(width, height=PANEL_HEIGHT, thickness=PANEL_THICKNESS):
    return grounded_cube([width, height, thickness])


def panel_base(width, length, thickness=PANEL_THICKNESS):
    return grounded_cube([width, thickness, length])


def hole_punch(offsets, spacing, diameter, thickness):
    spacings = [-spacing, 0, spacing]
    return spaced_hole_punch(offsets, [spacings, spacings], diameter, thickness)


def spaced_hole_punch(offsets, spacings, diameter, thickness):
    x_offset, y_offset, z_offset = offsets
    x_spacings, z_spacings = spacings
    hole = back(y_offset)(
        up(z_offset)(
            right(x_offset)(
                punch_hole(diameter, thickness)
            )
        )
    )
    return union()([
        up(z)(right(x)(hole))
        for z in z_spacings
        for x in x_spacings
    ])


def punch_hole(diameter, thickness):
    return rotate(90, [1, 0, 0])(
        cylinder(r=diameter / 2, h=thickness * 2, center=True, segments=16)
    )


def main():
    save_as_scad(mount_panel(), 'jack_panel_mount.scad')
    save_as_scad(front_panel(), 'jack_panel_front.scad')
    save_as_scad(back_panel(), 'jack_panel_back.scad')
    save_as_scad(side_panel(), 'jack_panel_side.scad')
    save_as_scad(side_quadruple_panel(), 'jack4_panel_side.scad')
    save_as_scad(panel_set(), 'jack_panel_set.scad')


if __name__ == '__main__':
    main()
