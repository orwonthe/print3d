import math

from geoscad.as_units import nscale_feet, nscale_inches, AsUnits, inches
from geoscad.utilities import grounded_cube
from solid import scad_render_to_file, cylinder, rotate, cube, mirror, multmatrix, scale
from solid.utils import up, right, forward, left, back, union

ho_scale_inches = AsUnits(1 / 87 * inches, 'ho"') # HO Scale model railroading uses 1:87 scaling ratio.

# self.beam_size = 4 * nscale_inches
# self.plank_size = 2 * nscale_inches
# self.table_length = 8 * 12 * nscale_inches
# self.table_width = 4 * 12 * nscale_inches
# self.table_height = 30 * nscale_inches
# self.table_plank_count = 6
# self.seat_plank_count = 2
# self.leg_angle = 30
# self.seat_width = 15 * nscale_inches

# self.beam_under_hang = self.plank_size
# self.merge_factor = 0.1 * nscale_inches
# self.plank_groove = 0.5 * nscale_inches


# self.table_beam_width = self.table_width - 2 * self.beam_under_hang
# self.seat_height = self.table_height / 2
# self.seat_offset_x = self.table_beam_width / 2 + self.seat_height
# self.frame_offset_y = 0.5 * self.table_length - 18 * nscale_inches - self.beam_size - self.merge_factor
# self.horizontal_beam_offset_y = self.frame_offset_y + self.beam_size

# self.leg_offset_x = self.table_beam_width / 2 - 3 * nscale_inches

BEAM_LUMBER_THICKNESS_INCHES = 4
PLANK_LUMBER_THICKNESS_INCHES = 2
TABLE_LENGTH_INCHES = 8 * 12
TABLE_WIDTH_INCHES = 4 * 12
TABLE_HEIGHT_INCHES = 30
TABLE_PLANK_COUNT = 6
SEAT_PLANK_COUNT = 2
LEG_ANGLE_DEGREES = 30
SEAT_WIDTH_INCHES = 15

class picnic_table:
    def __init__(
            self,
            table_width=TABLE_WIDTH_INCHES,
            table_length=TABLE_LENGTH_INCHES,
            table_height=TABLE_HEIGHT_INCHES,
            seat_width=SEAT_WIDTH_INCHES,
            beam_size=BEAM_LUMBER_THICKNESS_INCHES,
            plank_size=PLANK_LUMBER_THICKNESS_INCHES,
            seat_plank_count=SEAT_PLANK_COUNT,
            table_plank_count=TABLE_PLANK_COUNT,
            leg_angle=LEG_ANGLE_DEGREES,
            beam_under_hang=None,
            plank_groove=None,
            merge_factor=None,
    ):
        if beam_under_hang is None:
            beam_under_hang = plank_size
        if plank_groove is None:
            plank_groove = plank_size / 4
        if merge_factor is None:
            merge_factor = 0.01 * plank_size
        self.seat_width = seat_width
        self.table_width = table_width
        self.table_length = table_length
        self.table_height = table_height
        self.beam_size = beam_size
        self.plank_size = plank_size
        self.seat_plank_count = seat_plank_count
        self.table_plank_count = table_plank_count
        self.beam_under_hang = beam_under_hang
        self.merge_factor = merge_factor
        self.plank_groove = plank_groove
        self.leg_angle = leg_angle

    def __call__(self, scaling=nscale_inches):
        table = self.picnic_table_top() + self.picnic_seats() + self.picnic_frame()
        return scale(1 * scaling)(
            up(self.table_length/2) (
                rotate([90, 0, 0]) (
                    table
                )
            )
        )

    @property
    def table_beam_width(self):
        return self.table_width - 2 * self.beam_under_hang

    @property
    def seat_height(self):
        return self.table_height / 2

    @property
    def seat_offset_x(self):
        return self.table_beam_width / 2 + self.seat_height

    @property
    def frame_offset_y(self):
        return 0.5 * self.table_length - self.seat_height - self.beam_size - self.merge_factor

    @property
    def horizontal_beam_offset_y(self):
        return self.frame_offset_y + self.beam_size

    @property
    def angled_leg_width(self):
        return self.beam_size / math.cos(math.radians(self.leg_angle))

    @property
    def leg_offset_x(self):
        return self.table_beam_width / 2 - self.angled_leg_width

    def picnic_table_top(self):
        return up(self.table_height - self.merge_factor)(self.long_plank(self.table_width, self.table_plank_count))

    def long_plank(self, width, plank_count):
        board = grounded_cube([width, self.table_length, self.plank_size])
        groove = up(self.plank_size - self.plank_groove)(
            rotate([0, -45, 0])(
                right(self.plank_size / 2)(
                    grounded_cube([self.plank_size, 2 * self.table_length, self.plank_size])
                )
            )
        )
        groove_offsets = [
            width / (plank_count) * (index - (plank_count - 2) / 2)
            for index in range(plank_count - 1)
        ]
        grooves = union()([
            right(groove_offset)(groove)
            for groove_offset in groove_offsets
        ])
        return board - grooves

    def picnic_seats(self):
        seat = self.picnic_seat()
        return up(self.seat_height - self.merge_factor)(
            left(self.seat_offset_x)(seat) + right(self.seat_offset_x)(seat)
        )

    def picnic_seat(self):
        return self.long_plank(self.seat_width, self.seat_plank_count)

    def picnic_frame(self):
        return self.picnic_bench_beams() + self.picnic_table_beams() + self.leg_frame()

    def picnic_bench_beams(self):
        return self.horizontal_beams(self.seat_width + 2 * self.seat_offset_x - 2 * self.beam_under_hang, self.seat_height)

    def picnic_table_beams(self):
        return self.horizontal_beams(self.table_beam_width, self.table_height)

    def horizontal_beams(self, width, elevation):
        cross_beam = up(elevation - self.beam_size)(
            grounded_cube([width, self.beam_size, self.beam_size])
        )
        return forward(self.horizontal_beam_offset_y)(cross_beam) + back(self.horizontal_beam_offset_y)(cross_beam)

    def leg_frame(self):
        return union()([
            self.single_leg(-self.leg_angle * x, self.leg_offset_x * x, self.frame_offset_y * y)
            for x in [-1, 1]
            for y in [-1, 1]
        ])

    def single_leg(self, angle, offset_x, offset_y):
        chopper = grounded_cube([self.table_beam_width, self.beam_size, self.table_height])
        beam = cube([self.beam_size, self.beam_size, 4 * self.table_height], center=True)
        angled_beam = up(self.table_height)(
            rotate([0, angle, 0])(beam)
        )
        return right(offset_x)(
            forward(offset_y)(
                angled_beam * chopper
            )
        )


def main():
    save_as_scad(picnic_table()(ho_scale_inches), 'picnic_table')
    # save_as_scad(picnic_table()(nscale_inches), 'picnic_table')




def save_as_scad(thing, filename):
    output_file = f'/home/willy/print_output/{filename}.scad'
    scad_render_to_file(thing, output_file)


if __name__ == '__main__':
    main()
