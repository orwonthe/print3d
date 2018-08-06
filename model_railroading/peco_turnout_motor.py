from geoscad.as_units import mm, inches
from geoscad.utilities import grounded_cube, left_right_symmetric, replicate_along_y_axis, rounded_cube, smudge
from solid import scad_render_to_file, cylinder, rotate, cube, scale, mirror, intersection, union
from solid.utils import up, right, forward, down

# X dimensions

CLAMP_TROUGH_WIDTH = 8.75 @ mm
CLAMP_RUNNER_WIDTH = 2.0 @ mm
CLAMP_GRIPPER_GAP = 1.4 @ mm
CLAMP_GRIP_WIDTH = 2.0 @ mm
HOUSING_WIDTH = CLAMP_TROUGH_WIDTH + 2.0 * (CLAMP_GRIPPER_GAP + CLAMP_RUNNER_WIDTH)
CLAMP_BASE_WIDTH = HOUSING_WIDTH + 2 * CLAMP_GRIP_WIDTH
CLAMP_BUMPER_OVERHANG = CLAMP_GRIPPER_GAP + 0.4 @ mm
CLAMP_BUMPER_WIDTH = CLAMP_GRIP_WIDTH + CLAMP_BUMPER_OVERHANG
POLE_HOLE_WIDTH = 6.0 @ mm
SWITCH_HOLE_WIDTH = 8.4 @ mm
SWITCH_HOLDER_WIDTH = CLAMP_TROUGH_WIDTH + CLAMP_RUNNER_WIDTH
LEAD_HOLE_PIN_CLEARANCE = 0.1 @ inches - 1.0 @ mm
LEAD_HOLE_WIDTH = (0.2 * inches + LEAD_HOLE_PIN_CLEARANCE) @ mm
SLIDER_WIDTH = (0.86 * CLAMP_TROUGH_WIDTH) @ mm
SLIDER_HOLE_WIDTH = (POLE_HOLE_WIDTH - 0.4) @ mm
SLIDER_RADIUS = 1.0 @ mm
SOCKET_HOLE_WIDTH = 7.8 @ mm

# Y dimensions
CLAMP_LENGTH = 37.0 @ mm
HOUSING_THICKNESS = 1.0 @ mm
HOUSING_LOCATIONS = [-15.42, -3.5, 3.5, 15.42] @ mm
POLE_HOLE_LENGTH = 7 @ mm
SWITCH_HOLE_LENGTH = 8.8 @ mm
SWITCH_HOLE_Y_OFFSET = 13.0 @ mm
SWITCH_HOLDER_LENGTH = 8.0 @ mm
SWITCH_HOLDER_Y_OFFSET = (CLAMP_LENGTH - SWITCH_HOLDER_LENGTH) / 2
LEAD_HOLE_LENGTH = LEAD_HOLE_PIN_CLEARANCE
LEAD_HOLE_Y_OFFSET = ((CLAMP_LENGTH - 4.0 * mm) / 2) @ mm
SLIDER_HOLE_LENGTH = 2.0 @ mm
SLIDER_HOLE_BIAS = 1.0 @ mm
SLIDER_LENGTH = 20 @ mm - 2 * SLIDER_HOLE_BIAS
SOCKET_HOLE_LENGTH = 8 @ mm
SOCKET_HOLE_Y_OFFSET = (CLAMP_LENGTH / 2) @ mm

# Z dimensions
CLAMP_BASE_HEIGHT = 2.0 @ mm
CLAMP_TROUGH_HEIGHT = 6.8 @ mm
CLAMP_RUNNER_HEIGHT = 9.4 @ mm
CLAMP_GRIP_HEIGHT = 13.0 @ mm
CLAMP_BUMPER_THICKNESS = 2.0 @ mm
HOUSING_ELEVATION = CLAMP_RUNNER_HEIGHT + 0.001
HOUSING_HEIGHT = 4 @ mm
POLE_HOLE_HEIGHT = 2 * CLAMP_GRIP_HEIGHT
CLAMP_TOP_CLIP = CLAMP_RUNNER_HEIGHT + 2.2 @ mm
SWITCH_HOLE_HEIGHT = 3.2 @ mm
SWITCH_HOLDER_HEIGHT = CLAMP_RUNNER_HEIGHT
SWITCH_HOLE_ELEVATION = CLAMP_RUNNER_HEIGHT - SWITCH_HOLE_HEIGHT
LEAD_HOLE_HEIGHT = CLAMP_RUNNER_HEIGHT
SLIDER_HEIGHT = 1.6 @ mm
SLIDER_HOLE_HEIGHT = 3 * SLIDER_HEIGHT
SOCKET_HOLE_DROP = 2 @ mm
SOCKET_HOLE_HEIGHT = SWITCH_HOLE_ELEVATION + 0.001

def y_symmetric_intersection(target):
    return intersection()([target, y_symmetric(target)])

def y_symmetric_union(target):
    return union()([target, y_symmetric(target)])

def y_symmetric(target):
    return mirror([0, 1, 0])(target)

def peco_motor_clamp_with_socket_hole():
    return peco_motor_clamp_with_switch_hole() - y_symmetric_union(socket_hole())

def socket_hole():
    socket_hole_shape = [SOCKET_HOLE_WIDTH, SOCKET_HOLE_LENGTH, 2 * SOCKET_HOLE_HEIGHT]
    return down(SOCKET_HOLE_HEIGHT)(forward(SOCKET_HOLE_Y_OFFSET)(
        grounded_cube(socket_hole_shape)
    ))


def peco_motor_clamp_with_switch_hole():
    return peco_turnout_motor_clamp() \
           + y_symmetric_union(switch_holder()) \
           - y_symmetric_union(switch_hole()) \
           - y_symmetric_union(lead_hole())


def lead_hole():
    lead_hole_shape = [LEAD_HOLE_WIDTH, LEAD_HOLE_LENGTH, LEAD_HOLE_HEIGHT]
    return down(0.1)(forward(LEAD_HOLE_Y_OFFSET)(
        grounded_cube(lead_hole_shape)
    ))


def switch_holder():
    holder_shape = [SWITCH_HOLDER_WIDTH, SWITCH_HOLDER_LENGTH, SWITCH_HOLDER_HEIGHT]
    return forward(SWITCH_HOLDER_Y_OFFSET)(
        grounded_cube(holder_shape)
    )


def switch_hole():
    base_shape = [SWITCH_HOLE_WIDTH, SWITCH_HOLE_LENGTH, SWITCH_HOLE_HEIGHT * 2]
    base_elevation = SWITCH_HOLE_ELEVATION
    base = forward(SWITCH_HOLE_Y_OFFSET)(up(base_elevation)(
        grounded_cube(base_shape))
    )
    return base


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


def slider():
    slider_shape = [SLIDER_WIDTH, SLIDER_LENGTH, SLIDER_HEIGHT]
    slider_hole_shape = [SLIDER_HOLE_WIDTH, SLIDER_HOLE_LENGTH, SLIDER_HOLE_HEIGHT]
    slider_hole = forward(SLIDER_HOLE_BIAS)(cube(slider_hole_shape, center=True))
    return rounded_cube(slider_shape, SLIDER_RADIUS) - slider_hole


if __name__ == '__main__':
    scad_render_to_file(peco_motor_clamp_with_socket_hole(), 'peco_motor_clamp_with_socket_hole.scad')
    scad_render_to_file(peco_motor_clamp_with_switch_hole(), 'peco_motor_clamp_with_switch_hole.scad')
    scad_render_to_file(slider(), 'slider.scad')
    scad_render_to_file(smudge(0.8, slider()), 'smudged_slider.scad')
    print(SLIDER_WIDTH, SLIDER_HEIGHT)
