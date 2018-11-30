from geoscad.as_units import inches, mm
from geoscad.utilities import grounded_cube
from solid.utils import back, cylinder, rotate, right, up, forward, union, left

from circuit_board_enclosures.keystone import add_keystones
from utilities.file_utilities import save_as_scad

NARROW_WIDTH = 2.5 * inches
WIDE_WIDTH = 3.0 * inches
PANEL_THICKNESS = 2 * mm
PANEL_HEIGHT = 1.75 * inches

CONNECTOR_ELEVATION = PANEL_HEIGHT - 0.6 * inches
JACK_OFFSET = 0.925 * inches
PANEL_HOLE_SPACING = 0.8125 * inches

def panel_set():
    front = back(NARROW_WIDTH)(
        rotate(180, [0,0,1])(
            rotate(90, [1,0,0])(
                forward(PANEL_HEIGHT/2 + PANEL_THICKNESS)(
                    front_panel()
                )
            )
        )
    )
    back_piece = forward(NARROW_WIDTH)(
        rotate(0, [0,0,1])(
            rotate(90, [1,0,0])(
                forward(PANEL_HEIGHT/2 + PANEL_THICKNESS)(
                    back_panel()
                )
            )
        )
    )
    side = up(1.5*PANEL_THICKNESS)(left(WIDE_WIDTH/2)(
        rotate(90, [0,0,1])(
            rotate(90, [1,0,0])(
                forward(PANEL_HEIGHT/2)(
                    side_panel()
                )
            )
        )
    ))
    return front + \
           back_piece +\
           forward((NARROW_WIDTH-PANEL_THICKNESS)/2)(side) +\
           back((NARROW_WIDTH-PANEL_THICKNESS)/2)(side)

def front_panel():
    return back_or_front_panel(is_front=True)


def back_panel():
    return back_or_front_panel(is_front=False)


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
        diameter=5 * mm,
        thickness=PANEL_THICKNESS * 2
    )

def side_hole_punch():
    return hole_punch(
        [0, PANEL_HEIGHT / 2, WIDE_WIDTH / 2],
        PANEL_HOLE_SPACING,
        diameter=5 * mm,
        thickness=PANEL_THICKNESS * 2
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
    x_offset, y_offset, z_offset = offsets
    hole = back(y_offset)(up(z_offset)(right(x_offset)(rotate(90, [1, 0, 0])(
        cylinder(r=diameter / 2, h=thickness * 2, center=True, segments=16)
    ))))
    spacings = [-spacing, 0, spacing]
    return union()([
        up(z)(right(x)(hole))
        for z in spacings
        for x in spacings
    ])


def main():
    save_as_scad(front_panel(), 'jack_panel_front.scad')
    save_as_scad(back_panel(), 'jack_panel_back.scad')
    save_as_scad(side_panel(), 'jack_panel_side.scad')
    save_as_scad(panel_set(), 'jack_panel_set.scad')


if __name__ == '__main__':
    main()
