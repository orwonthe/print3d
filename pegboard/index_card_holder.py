from geoscad.as_units import inches
from solid.utils import right, up, cube, scad_render_to_file, union, left, forward, down, rotate, back

from pegboard.pegs import DEFAULT_PEG_SPACING, solid_peg, DEFAULT_HOLDER_MARGIN

DEFAULT_CARD_HOLDER_HEIGHT = 3.0 @ inches
DEFAULT_CARD_HOLDER_LENGTH = 3.25 @ inches
DEFAULT_CARD_HOLDER_THICKNESS = 0.06 @ inches
DEFAULT_FRONT_CUT_LENGTH = 2.0 @ inches
DEFAULT_BACK_CUT_LENGTH = 1.0 @ inches
DEFAULT_CUT_OUT_ELEVATION = 0.5 @ inches
DEFAULT_PEG_HOLE_DIAMETER = 0.28 @ inches
DEFAULT_MARGIN = DEFAULT_HOLDER_MARGIN

DEFAULT_THIN_WIDTH = 0.8 @ inches
DEFAULT_FAT_WIDTH = 1.8 @ inches


def fat_card_holder(width=DEFAULT_FAT_WIDTH):
    return index_card_holder(width)


def thin_card_holder(width=DEFAULT_THIN_WIDTH):
    return index_card_holder(width)


def index_card_holder(
        width,
        length=DEFAULT_CARD_HOLDER_LENGTH,
        height=DEFAULT_CARD_HOLDER_HEIGHT,
        thickness=DEFAULT_CARD_HOLDER_THICKNESS,
        cut_out_elevation=DEFAULT_CUT_OUT_ELEVATION,
        front_cut_length=DEFAULT_FRONT_CUT_LENGTH,
        back_cut_length=DEFAULT_BACK_CUT_LENGTH,
        margin=DEFAULT_MARGIN,
):
    shape = [width, length, height]
    box = open_top_box(shape, thickness)
    cutouts = box_cut_out(
        shape,
        thickness,
        elevation=cut_out_elevation,
        front_length=front_cut_length,
        back_length=back_cut_length,
    )
    single_peg = down(DEFAULT_PEG_HOLE_DIAMETER)(
        solid_peg(diameter=DEFAULT_PEG_HOLE_DIAMETER))
    holes = bottom_pegs(single_peg, shape, margin) \
            + back_pegs(single_peg, shape, margin) \
            + side_pegs(single_peg, shape, margin)
    return box - cutouts - holes


def bottom_pegs(
        single_peg,
        shape, margin
):
    return grid_pegs(
        single_peg,
        centered_grid(width=shape[0], length=shape[1], margin=margin))


def side_pegs(
        single_peg,
        shape, margin
):
    peg_set = up(shape[2] / 2)(
        rotate([90, 0, 0])(
            grid_pegs(
                single_peg,
                centered_grid(width=shape[0], length=shape[2], margin=margin))))
    half_length = shape[1] / 2
    left_pegs = back(half_length)(peg_set)
    right_pegs = forward(half_length)(peg_set)
    return left_pegs + right_pegs


def back_pegs(
        single_peg,
        shape,
        margin
):
    return up(shape[2] / 2)(left(shape[0] / 2)(
        rotate([0, 90, 0])(
            grid_pegs(
                single_peg,
                centered_grid(width=shape[1], length=shape[2], margin=margin)))))


def grid_pegs(
        single_peg,
        grid
):
    return union()([
        left(x)(
            forward(y)(single_peg)
        ) for (y, x) in grid
    ])


def open_top_box(
        shape,
        thickness
):
    double_thickness = thickness * 2
    outer_shape = thickened_shape(shape, double_thickness)
    inner_shape = raised_shape(shape, double_thickness)
    outer_box = cube(outer_shape, center=True)
    inner_box = up(thickness)(
        cube(inner_shape, center=True))
    return up(0.5 * outer_shape[2])(
        outer_box - inner_box)


def thickened_shape(
        shape,
        thickness
):
    return [dim + thickness for dim in shape]


def raised_shape(
        shape,
        thickness
):
    return [shape[0], shape[1], shape[2] + thickness]


def box_cut_out(
        shape,
        thickness,
        elevation,
        front_length=None,
        back_length=None
):
    params = [(0.5, front_length), (-0.5, back_length)]
    cube_width = thickness * 4
    cube_height = shape[2]
    up_distance = elevation + 0.5 * cube_height
    return [right(scale * shape[0])(
        up(up_distance)(
            cube([cube_width, length, cube_height], center=True)
        )
    ) for scale, length in params if length is not None]


def centered_grid(
        width,
        length,
        spacing=DEFAULT_PEG_SPACING,
        margin=0
):
    x_spacings = centered_spacing(width - 2 * margin, spacing)
    y_spacings = centered_spacing(length - 2 * margin, spacing)
    return [(y, x) for y in y_spacings for x in x_spacings]


def centered_spacing(
        span,
        spacing=DEFAULT_PEG_SPACING
):
    count = int(1 + span // spacing)
    offset = -0.5 * (count - 1) * spacing
    return [offset + index * spacing for index in range(count)]


if __name__ == '__main__':
    scad_render_to_file(fat_card_holder(), 'fat_card_holder.scad')
    scad_render_to_file(thin_card_holder(), 'thin_card_holder.scad')
