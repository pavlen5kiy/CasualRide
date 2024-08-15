import os

import pygame

from ui import *


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
    car.rect = car.image.get_rect()
    car.rect.topleft = (240 - car.rect.width // 2, 450 - car.rect.height // 2)


def change_road(road, skin):
    road.image = load_image(skin)
    road.rect = road.image.get_rect()


def set_screen(size):
    pygame.display.set_caption('Car Game')

    size = size
    screen = pygame.display.set_mode(size)
    screen_rect = (0, 0, size[0], size[1])

    return screen, size, screen_rect


def set_music(track):
    # pygame.mixer.music.stop()
    pygame.mixer.music.load(f'assets/music/{track}.mp3')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    print(f'Music on: {track}.')

