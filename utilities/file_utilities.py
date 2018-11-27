from solid import scad_render_to_file


def save_as_scad(thing, filename):
    output_file = f'/home/willy/print_output/{filename}'
    scad_render_to_file(thing, output_file)

