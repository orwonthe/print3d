from geoscad.as_units import mm, inches
from geoscad.utilities import grounded_cube, rounded_platter
from solid import scad_render_to_file, cylinder, union, cube, intersection
from solid.utils import forward, back, down, up, right, left, math, rotate

# X dimensions
UNISTRUT_CHANNEL_WIDTH = 1.75 * inches
UNISTRUT_CHANNEL_SLOT = 1.135 * inches
CUBE_WIDTH = UNISTRUT_CHANNEL_SLOT * math.sqrt(0.5)

# Y dimensions

# Z dimensions

SHIM_LIST = [
    ('1_16', 1 / 16 * inches),
    ('2_16', 2 / 16 * inches),
    ('4_16', 4 / 16 * inches),
]

def main():
    for label, thickness in SHIM_LIST:
        render_shim(label, thickness)

def render_shim(label, thickness):
    scad_render_to_file(unistrut_shim(thickness), f'unistrut_shim_{label}.scad')

def unistrut_shim(thickness, length=UNISTRUT_CHANNEL_WIDTH):
    return up(length / 2)(bar(thickness, length) + v_channel(length) - left(thickness)( v_channel(length * 1.1)))

def v_channel(length):
    return rotate([0, 0, 45.0]) (cube([CUBE_WIDTH, CUBE_WIDTH, length], center=True))

def bar(thickness, length):
    return left(thickness / 2)(cube([thickness, UNISTRUT_CHANNEL_WIDTH, length], center=True))

if __name__ == '__main__':
    main()
