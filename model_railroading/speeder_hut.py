import math

from geoscad.as_units import nscale_feet, nscale_inches
from geoscad.utilities import grounded_cube
from solid import scad_render_to_file, cylinder, rotate, cube, mirror, multmatrix
from solid.utils import up, right, forward, left, back


# HUT_WIDTH = 6 * nscale_feet
# HUT_HEIGHT = 6 * nscale_feet
# HUT_LENGTH = 12 * nscale_feet
#
# ROOF_OVERHANG = 1 * nscale_feet
# WALL_THICKNESS = 4 * nscale_inches
# POST_RADIUS = 6 * nscale_inches
# CROWN_RADIUS = 2.5 * nscale_inches
#
# DOORWAY_OVERHEAD = 1.5 * nscale_feet
# DOOR_OPENING_WIDTH = 6 * nscale_feet
# DOOR_OPENING_MARGIN = 1 * nscale_feet
# DOOR_OPENING_THRESHOLD = 6 * nscale_inches
# DOOR_OVERSIZE = 4 * nscale_inches
# DOOR_THICKNESS = 4 * nscale_inches
# DOOR_CRACK = 3 * nscale_feet
# DOOR_BEAM_WIDTH = 6 * nscale_inches
# DOOR_BEAM_BULGE = 2 * nscale_inches
#

class SpeederHut:
    def __init__(self):
        self.suffix = ''
        self.hut_width = 8 * nscale_feet
        self.hut_length = 12 * nscale_feet
        self.hut_height = 6 * nscale_feet

        self.roof_overhang = 1 * nscale_feet
        self.wall_thickness = 4 * nscale_inches
        self.post_radius = 6 * nscale_inches
        self.crown_radius = 2.5 * nscale_inches

        self.doorway_overhead = 1.5 * nscale_feet
        self.door_opening_width = 6 * nscale_feet
        self.door_opening_margin = 1 * nscale_feet
        self.door_opening_threshold = 6 * nscale_inches
        self.door_oversize = 4 * nscale_inches
        self.door_thickness = 4 * nscale_inches
        self.door_crack = 3 * nscale_feet
        self.door_beam_width = 6 * nscale_inches
        self.door_beam_bulge = 2 * nscale_inches

    @property
    def roof_length(self):
        return self.hut_length + self.roof_overhang

    @property
    def roof_thickness(self):
        return self.wall_thickness

    @property
    def roof_line(self):
        return math.sqrt(0.5) * self.hut_width

    @property
    def roof_side_width(self):
        return self.roof_line + self.roof_overhang

    @property
    def wall_x_offset(self):
        return (self.hut_length - self.wall_thickness) / 2

    @property
    def wall_y_offset(self):
        return (self.hut_width - self.wall_thickness) / 2

    @property
    def post_height(self):
        return self.hut_height + 0.5 * self.roof_thickness

    @property
    def door_opening_height(self):
        return self.hut_height - self.doorway_overhead

    @property
    def door_height(self):
        return self.door_opening_height + self.door_oversize

    @property
    def door_width(self):
        return 0.5 * (self.door_opening_width + self.door_oversize)

    @property
    def door_opening_offset(self):
        return (self.hut_length - self.door_opening_width) / 2 - self.door_opening_margin

    @property
    def door_beam_thickness(self):
        return self.door_thickness + self.door_beam_bulge

    @property
    def floor_thickness(self):
        return self.wall_thickness

    @property
    def floor_margin(self):
        return self.post_radius - self.wall_thickness

    @property
    def floor_width(self):
        return self.hut_width + self.floor_margin

    @property
    def floor_length(self):
        return self.hut_length + self.floor_margin

    def scad_ensemble(self):
        save_as_scad(self.speeder_hut(), f'speeder_hut{self.suffix}.scad')
        save_as_scad(self.printable_roof(), f'speeder_hut_roof{self.suffix}.scad')
        save_as_scad(self.printable_walls(), f'speeder_hut_walls{self.suffix}.scad')

    def speeder_hut(self):
        return self.walls() + self.raised_roof()

    def walls(self):
        return self.front_wall() + self.back_wall() + self.left_wall() + self.right_wall() + self.posts() + self.floor()

    def front_wall(self):
        door_opening = left(self.door_opening_offset)(
            up(self.door_opening_threshold)(
                grounded_cube([self.door_opening_width, 2 * self.wall_thickness, self.door_opening_height])
            )
        )
        single_door = self.door()
        reverse_door = mirror([1, 0, 0])(single_door)
        single_offset = (self.door_width + self.door_crack) / 2
        right_door = left(self.door_opening_offset - single_offset)(single_door)
        left_door = left(self.door_opening_offset + single_offset)(reverse_door)
        return forward(self.wall_y_offset)(self.main_wall() - door_opening + right_door + left_door)

    def back_wall(self):
        return back(self.wall_y_offset)(self.main_wall())

    def main_wall(self):
        return grounded_cube([self.hut_length, self.wall_thickness, self.hut_height])

    def left_wall(self):
        return left(self.wall_x_offset)(self.side_wall())

    def right_wall(self):
        return right(self.wall_x_offset)(self.side_wall())

    def side_wall(self):
        return grounded_cube([self.wall_thickness, self.hut_width, self.hut_height]) + self.peaking()

    def peaking(self):
        return up(self.hut_height)(
            rotate(45, [1, 0, 0])(
                cube([self.wall_thickness, self.roof_line, self.roof_line], center=True)
            )
        )

    def door(self):
        forward_offset = self.door_thickness / 2 - 0.5 * nscale_inches  # slight merge into frame
        main_panel = grounded_cube([self.door_width, self.door_thickness, self.door_height])
        horizontal_beam = grounded_cube([self.door_width, self.door_beam_thickness, self.door_beam_width])
        vertical_beam = grounded_cube([self.door_beam_width, self.door_beam_thickness, self.door_height])
        horizontal_offset = (self.door_width - self.door_beam_thickness) / 2
        vertical_offset = self.door_height - self.door_beam_thickness / 2
        diagonal_offset = (self.door_width - self.door_beam_width) / 2
        diagonal_skew = 2 * diagonal_offset / self.door_height
        diagonal_beam = multmatrix([
            [1, 0, diagonal_skew, -diagonal_offset],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
        ])(vertical_beam)
        beams = horizontal_beam + up(vertical_offset)(horizontal_beam)
        beams += left(horizontal_offset)(vertical_beam)
        beams += right(horizontal_offset)(vertical_beam)
        beams += diagonal_beam
        return up(self.door_opening_threshold - 0.5 * self.door_oversize)(
            forward(forward_offset)(
                main_panel + forward((self.door_beam_thickness - self.door_thickness) / 2)(beams)
            )
        )

    def floor(self):
        return grounded_cube([self.floor_length, self.floor_width, self.floor_thickness])

    def posts(self):
        post = cylinder(r=self.crown_radius, h=self.post_height, segments=16)
        post_pair = forward(self.wall_y_offset)(post) + back(self.wall_y_offset)(post)
        return left(self.wall_x_offset)(post_pair) + right(self.wall_x_offset)(post_pair)

    def printable_roof(self):
        return rotate(-135, [0, 0, 1])(rotate(90, [0, 1, 0])(left(0.5 * self.roof_length)(self.roof())))

    def printable_walls(self):
        return self.walls() - self.raised_roof()

    def roof(self):
        return self.crown() + self.roof_sides()

    def crown(self):
        return up(self.crown_radius)(
            rotate(90, [0, 1, 0])(
                cylinder(r=self.crown_radius, h=self.roof_length, segments=16, center=True)
            )
        )

    def roof_sides(self):
        ridge = self.crown()
        ridge_offset = self.roof_side_width / 6
        single_side = grounded_cube([self.roof_length, self.roof_side_width, self.roof_thickness])
        single_side += forward(ridge_offset)(ridge)
        single_side += back(ridge_offset)(ridge)
        offset = 0.5 * self.roof_side_width
        back_side = rotate(45, [1, 0, 0])(back(offset)(single_side))
        front_side = rotate(180, [0, 0, 1])(back_side)
        return back_side + front_side

    def raised_roof(self):
        return up(self.hut_height + 0.5 * self.hut_width)(self.roof())


class NarrowSpeederHut(SpeederHut):
    def __init__(self):
        super().__init__()
        self.suffix = '_narrow'
        self.hut_width = 6 * nscale_feet


def main():
    SpeederHut().scad_ensemble()
    NarrowSpeederHut().scad_ensemble()


def save_as_scad(thing, filename):
    output_file = f'/home/willy/print_output/{filename}'
    scad_render_to_file(thing, output_file)


if __name__ == '__main__':
    main()
