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


def render_hitbox(screen, car, npc_cars, rect=True, hitbox=True):
    if rect:
        pygame.draw.rect(screen, pygame.Color('blue'), car.rect)

    for npc in npc_cars:
        if rect:
            pygame.draw.rect(screen, pygame.Color('purple'), npc.rect)
        if hitbox:
            pygame.draw.rect(screen, pygame.Color('red'), npc.hitbox)

    if hitbox:
        pygame.draw.rect(screen, pygame.Color('green'), car.hitbox)


def change_skin(car, skin):
    car.default_image = load_image(f'car_{skin}_up')
    car.image = load_image(f'car_{skin}_up')
