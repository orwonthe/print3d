from geoscad.as_units import mm
from geoscad.utilities import smudge
from solid import cylinder, union, cube, text, linear_extrude, scale
from solid.utils import forward, back, up, rotate

from utilities.file_utilities import save_as_scad

DO_SMUDGE = True

# X dimensions
HANDLE_DIAMETER = 33 * mm
THICKNESS = 9 * mm
SLOT_WIDTH = 2.5 * mm

# Y dimensions
SLOT_LENGTH = 65 * mm
SHAFT_LENGTH = SLOT_LENGTH + THICKNESS / 2
LETTER_HEIGHT = 11 * mm

# Z dimensions
KEY_HEIGHT = THICKNESS
SMUDGE = 2 * mm
LETTERING_RISE = 1 * mm


def main():
    save_as_scad(toothpaste_key(), 'toothpaste_key.scad')


def toothpaste_key():
    non_lettering = back(1 * mm)(key_shaft()) + key_handle()
    if DO_SMUDGE:
        non_lettering = smudge(SMUDGE, non_lettering)
    key = up(THICKNESS / 2)(non_lettering + key_lettering())
    return rotate(-90, [0, 0, 1])(key)


def key_shaft():
    trunk_length = SHAFT_LENGTH - 0.5 * THICKNESS
    trunk = back(trunk_length / 2)(cube([THICKNESS, trunk_length, KEY_HEIGHT], center=True))
    slot = back(SLOT_LENGTH / 2)(cube([SLOT_WIDTH, SLOT_LENGTH, 2 * KEY_HEIGHT], center=True))
    tip = cylinder(r=THICKNESS / 2, h=KEY_HEIGHT, center=True, segments=16)
    return forward(trunk_length)(trunk + tip - slot)


def key_handle():
    radius = HANDLE_DIAMETER / 2
    base = scale([1.5, 1.0, 1.0])(cylinder(r=radius, h=KEY_HEIGHT, center=True, segments=32))
    return back(radius)(base)


def key_lettering():
    messages = ["LeRoy", "Dental"]
    layout = union()([
        forward((index - 0.5) * -LETTER_HEIGHT)(text(message, halign='center', valign='center'))
        for index, message in enumerate(messages)
    ])
    lettering = up(THICKNESS / 2 - LETTERING_RISE)(
        linear_extrude(height=2 * LETTERING_RISE)(scale([0.8, 0.8, 1])(layout))
    )
    return back(HANDLE_DIAMETER / 2)(lettering)


if __name__ == '__main__':
    main()
