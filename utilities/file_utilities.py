import os

from solid import scad_render_to_file

def save_as_scad(thing, filename, directory=None):
    if directory is None:
        directory = os.environ.get('SCAD_DIRECTORY', '.')
    output_file = os.path.join(directory, filename)
    scad_render_to_file(thing, output_file)

