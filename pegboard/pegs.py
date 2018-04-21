from geoscad.as_units import inches
from solid import cylinder, rotate, cube, union, scale
from solid.utils import up, scad_render_to_file, left, right, forward, back

DEFAULT_HOLDER_THICKNESS = 0.06 @ inches
DEFAULT_PEG_DIAMETER = 0.245 @ inches
DEFAULT_PEGBOARD_CLEARANCE = 0.25 @ inches
DEFAULT_CONTAINER_CLEARANCE = DEFAULT_HOLDER_THICKNESS
DEFAULT_CLEARANCE = DEFAULT_PEGBOARD_CLEARANCE + DEFAULT_CONTAINER_CLEARANCE
DEFAULT_HOLDER_MARGIN = DEFAULT_PEG_DIAMETER
DEFAULT_PEG_SPACING = 1.0 * inches  # Not snapped to resolution


def solid_peg(
        diameter=DEFAULT_PEG_DIAMETER,
        thickness=DEFAULT_HOLDER_THICKNESS,
        clearance=DEFAULT_CLEARANCE,
        overreach=None
):
    if overreach is None:
        overreach = diameter
    radius = 0.5 * diameter
    height = thickness + clearance + overreach
    return cylinder(r=radius, h=height, segments=16)


def linch_pin_peg(
        diameter=DEFAULT_PEG_DIAMETER,
        thickness=DEFAULT_HOLDER_THICKNESS,
        clearance=DEFAULT_CLEARANCE,
        overreach=None,
        hole_size=None
):
    if overreach is None:
        overreach = diameter
    peg = solid_peg(diameter=diameter, thickness=thickness, clearance=clearance, overreach=overreach)
    if hole_size is None:
        hole_size = 0.5 * min(diameter, overreach)
    hole_radius = 0.5 * hole_size
    hole_displacement = thickness + clearance + hole_radius
    hole = up(hole_displacement)(
        rotate([90.0, 0.0, 0.0])(
            cube([hole_size, hole_size, 2 * diameter], center=True)))
    return peg - hole


def slot_peg_with_catch(
        diameter=DEFAULT_PEG_DIAMETER,
        thickness=DEFAULT_HOLDER_THICKNESS,
        clearance=DEFAULT_CLEARANCE,
        overreach=None,
        slot_width=None,
        slot_clearance=DEFAULT_CONTAINER_CLEARANCE
):
    if overreach is None:
        overreach = diameter
    peg = solid_peg(diameter=diameter, thickness=thickness, clearance=clearance, overreach=overreach)
    if slot_width is None:
        slot_width = 0.4 * min(diameter, overreach)
    hole_height = clearance + overreach
    hole_displacement = slot_clearance + thickness + 0.5 * hole_height
    round_hole_bottom = back(0.5 * hole_height)(
        cylinder(r=0.5 * slot_width, h=2 * diameter, center=True, segments=16))
    hole_cutout = cube([slot_width, hole_height, 2 * diameter], center=True)
    hole = up(hole_displacement)(
        rotate([90.0, 0.0, 0.0])(
            hole_cutout + round_hole_bottom))
    catch_height = clearance + thickness + 0.5 * diameter
    catch_offset = 0.5 * diameter
    unscaled_catch = up(catch_height)(
        rotate([90, 0, 0])(
            cylinder(r=0.5 * diameter, h=0.5 * slot_width, center=True, segments=4)))
    catch = scale([0.4, 1.0, 1.0])(unscaled_catch)
    return peg \
           + left(catch_offset)(catch) \
           + right(catch_offset)(catch) \
           - hole


def peg_holder(
        peg,
        peg_count=3,
        peg_spacing=DEFAULT_PEG_SPACING,
        margin=DEFAULT_HOLDER_MARGIN,
        thickness=DEFAULT_HOLDER_THICKNESS
):
    width = 2 * margin
    length = width + (peg_count - 1) * peg_spacing
    height = thickness
    base = up(thickness * 0.5)(
        cube([width, length, height], center=True))
    peg_offset = margin - 0.5 * length
    pegs = union()([
        forward(peg_offset + index * peg_spacing)(peg)
        for index in range(peg_count)])
    return base + pegs


if __name__ == '__main__':
    scad_render_to_file(peg_holder(slot_peg_with_catch()), 'slot_peg_holder.scad')
    scad_render_to_file(peg_holder(linch_pin_peg()), 'linch_pin_peg_holder.scad')
