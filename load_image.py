import os
import pygame


def load_image(name, color_key=None):
    fullname = os.path.join("assets/sprites/", name + '.png')

    try:
        image = pygame.image.load(fullname).convert_alpha()
    except pygame.error as e:
        print(f"Err: {e}")
        raise SystemExit(e)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)

    else:
        image = image.convert_alpha()

    return image
