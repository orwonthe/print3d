from geoscad.as_units import mm
from geoscad.utilities import grounded_cube, left_right_symmetric, replicate_along_y_axis
from solid import scad_render_to_file, cylinder, rotate, cube, scale

# X dimensions
from solid.utils import up, right

CLAMP_TROUGH_WIDTH = 8.75 @ mm
CLAMP_RUNNER_WIDTH = 2.0 @ mm
CLAMP_GRIPPER_GAP = 1.4 @ mm
CLAMP_GRIP_WIDTH = 2.0 @ mm
HOUSING_WIDTH = CLAMP_TROUGH_WIDTH + 2.0 * (CLAMP_GRIPPER_GAP + CLAMP_RUNNER_WIDTH)
CLAMP_BASE_WIDTH = HOUSING_WIDTH + 2 * CLAMP_GRIP_WIDTH
CLAMP_BUMPER_OVERHANG = CLAMP_GRIPPER_GAP + 0.4 @ mm
CLAMP_BUMPER_WIDTH = CLAMP_GRIP_WIDTH + CLAMP_BUMPER_OVERHANG
POLE_HOLE_WIDTH = 5.2 @ mm

# Y dimensions
CLAMP_LENGTH = 37.0 @ mm
HOUSING_THICKNESS = 1.0 @ mm
HOUSING_LOCATIONS = [-15.42, -3.5, 3.5, 15.42] @ mm
POLE_HOLE_LENGTH = 6.4 @ mm

# Z dimensions
CLAMP_BASE_HEIGHT = 2.0 @ mm
CLAMP_TROUGH_HEIGHT = 7.4 @ mm
CLAMP_RUNNER_HEIGHT = 9.4 @ mm
CLAMP_GRIP_HEIGHT = 13.0 @ mm
CLAMP_BUMPER_THICKNESS = 2.0 @ mm
HOUSING_ELEVATION = CLAMP_RUNNER_HEIGHT + 0.001
HOUSING_HEIGHT = 4 @ mm
POLE_HOLE_HEIGHT = 2 * CLAMP_GRIP_HEIGHT
CLAMP_TOP_CLIP = CLAMP_RUNNER_HEIGHT + 2.2 @ mm

def peco_turnout_motor_clamp():
    return clamp_base() + runners() + grabbers() - turnout_housing()


def clamp_base():
    base_shape = [CLAMP_BASE_WIDTH, CLAMP_LENGTH, CLAMP_BASE_HEIGHT]
    base = grounded_cube(base_shape)

    runner_base_shape = [CLAMP_TROUGH_WIDTH + 2 * CLAMP_RUNNER_WIDTH, CLAMP_LENGTH, CLAMP_TROUGH_HEIGHT]
    runner_base = grounded_cube(runner_base_shape)
    return base + runner_base - pole_hole()


def pole_hole():
    hole_shape = [POLE_HOLE_WIDTH, POLE_HOLE_LENGTH, POLE_HOLE_HEIGHT]
    return cube(hole_shape, center=True)


def runners():
    runner_shape = [CLAMP_RUNNER_WIDTH, CLAMP_LENGTH, CLAMP_RUNNER_HEIGHT]
    runner = grounded_cube(runner_shape)
    runner_offset = (CLAMP_TROUGH_WIDTH + CLAMP_RUNNER_WIDTH) / 2
    return left_right_symmetric(runner_offset, runner)


def grabbers():
    gripper_shape = [CLAMP_GRIP_WIDTH, CLAMP_LENGTH, CLAMP_GRIP_HEIGHT]
    gripper = grounded_cube(gripper_shape)
    gripper_offset = (CLAMP_BASE_WIDTH - CLAMP_GRIP_WIDTH) / 2
    grippers = left_right_symmetric(gripper_offset, gripper)

    bumper_shape = [CLAMP_BUMPER_WIDTH, CLAMP_LENGTH, CLAMP_BUMPER_THICKNESS]
    bumper_elevation = CLAMP_GRIP_HEIGHT - CLAMP_BUMPER_THICKNESS
    bumper_offset = (CLAMP_BASE_WIDTH - CLAMP_BUMPER_WIDTH) / 2

    round_bumper_radius = CLAMP_BUMPER_WIDTH / 2
    shrinkage = CLAMP_BUMPER_THICKNESS / round_bumper_radius
    round_bumper = right(0)(
        rotate([90, 0, 0])(
            scale([1.0, shrinkage, 1.0])(
                cylinder(r=round_bumper_radius, h=CLAMP_LENGTH, segments=4, center=True))))

    bumper = up(bumper_elevation)(round_bumper)
    # grounded_cube(bumper_shape) + )
    bumpers = left_right_symmetric(bumper_offset, bumper)

    clipper_shape = [CLAMP_BASE_WIDTH, CLAMP_LENGTH, CLAMP_TOP_CLIP]
    clipper = grounded_cube(clipper_shape)
    return (grippers + bumpers) * clipper


def turnout_housing():
    housing_shape = [HOUSING_WIDTH, HOUSING_THICKNESS, HOUSING_HEIGHT]
    housing = up(HOUSING_ELEVATION)(grounded_cube(housing_shape))
    return replicate_along_y_axis(HOUSING_LOCATIONS, housing)


if __name__ == '__main__':
    scad_render_to_file(peco_turnout_motor_clamp(), 'peco_turnout_motor_clamp.scad')
