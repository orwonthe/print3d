from geoscad.as_units import inches, mm
from geoscad.utilities import grounded_cube
from solid.utils import back

from circuit_board_enclosures.keystone import add_keystones
from utilities.file_utilities import save_as_scad

BASE_WIDTH = 2.5 * inches
BASE_LENGTH = 3 * inches
BASE_THICKNESS = 2 * mm

NARROW_WIDTH = 2.5 * inches
WIDE_WIDTH = 3.0 * inches
PANEL_THICKNESS = 2 * mm
PANEL_HEIGHT = 2.5 * inches

CONNECTOR_ELEVATION = PANEL_HEIGHT - 0.6 * inches
JACK_OFFSET = 0.75 * inches


def front_panel():
    return back_or_front_panel(is_front=True)


def back_panel():
    return back_or_front_panel(is_front=False)


def side_panel():
    offsets = [
        (x * inches, CONNECTOR_ELEVATION)
        for x in [-0.25, 1]
    ]
    return based_jack_panel(
        offsets,
        height=PANEL_HEIGHT,
        width=WIDE_WIDTH - PANEL_THICKNESS,
        length=NARROW_WIDTH
    )


def back_or_front_panel(is_front):
    offset = JACK_OFFSET
    if is_front:
        offset = -offset

    return based_jack_panel(
        [(offset, CONNECTOR_ELEVATION + PANEL_THICKNESS)],
        height=PANEL_HEIGHT + PANEL_THICKNESS,
        width=NARROW_WIDTH,
        length=WIDE_WIDTH
    )


def based_jack_panel(jack_placements, width, length, height=PANEL_HEIGHT, thickness=BASE_THICKNESS):
    return jacked_panel(jack_placements, width, height, thickness) + \
           back(height / 2)(panel_base(width, length, thickness))


def jacked_panel(jack_placements, width, height=PANEL_HEIGHT, thickness=BASE_THICKNESS):
    face = panel_face(width, height, thickness)
    return add_keystones(face, jack_placements, height)


def panel_face(width, height=PANEL_HEIGHT, thickness=BASE_THICKNESS):
    return grounded_cube([width, height, thickness])


def panel_base(width, length, thickness=BASE_THICKNESS):
    return grounded_cube([width, thickness, length])


def main():
    save_as_scad(front_panel(), 'jack_panel_front.scad')
    save_as_scad(back_panel(), 'jack_panel_back.scad')
    save_as_scad(side_panel(), 'jack_panel_side.scad')


if __name__ == '__main__':
    main()
