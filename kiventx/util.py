from csv import reader
from os import walk
from os.path import join, splitext

from kivent_core.managers.resource_managers import texture_manager


def import_csv_layout(path):
    with open(path) as level_map:
        terrain_map = list(reader(level_map, delimiter=","))
        return terrain_map


def import_graphics_folder(path):
    textures = []
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = join(path, image)
            texture_manager.load_image(full_path)
            textures.append(splitext(image)[0])
    return textures


def load_model(gameworld, width, height, texture_key):
    model_name = gameworld.model_manager.load_textured_rectangle(
        format_name="vertex_format_4f",
        width=width,
        height=height,
        texture_key=texture_key,
        name=texture_key,
    )
    model = gameworld.model_manager.models[model_name]
    model.flip_textured_rectangle_vertically()
