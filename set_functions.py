import pygame

from ui import *


def set_screen(size):
    size = size
    screen = pygame.display.set_mode(size)
    screen_rect = (0, 0, size[0], size[1])

    return screen, size, screen_rect


def set_labels(screen, size, road):
    lose_label = Text(screen, size, 50, 'You lost!', 'black')
    lose_label.dest = ((size[0] - lose_label.render.get_width()) // 2, 100)

    score_lost_label = ScoreLabel(screen, size, 30, 'Score: ', road, 'black')
    score_lost_label.dest = (
        (size[0] // 2 - score_lost_label.render.get_width() // 2) - 20, 150)

    score_label = ScoreLabel(screen, size, 40, '', road, 'white', (10, 10))

    return lose_label, score_label, score_lost_label


def set_game(screen, size, road):
    play = False
    lost = False
    start = False

    speed_change = 0
    spawn_tick = 0
    coin_spawn_tick = 0

    start_label = Startlabel(5, screen, size)

    lose_label, score_label, score_lost_label = set_labels(screen, size, road)

    return play, lost, start, speed_change, spawn_tick, coin_spawn_tick, start_label, lose_label, score_label, score_lost_label


def set_music(track):
    # pygame.mixer.music.stop()
    pygame.mixer.music.load(f'assets/{track}.mp3')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    print(f'Music on: {track}.')
