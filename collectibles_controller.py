import random

from sprite_controller import *
from utility import *


def set_coin(x_pos, car, road, coins_count, sprites):
    y_position = -100
    coin = Coin((x_pos, y_position), car, road, coins_count, sprites)

    sprites.add(coin)


def spawn_coins(car, road, coins_count, sprites):
    for i in range(4):
        spawn = False
        attempts = 1 + road.score // 50 - road.score // 100
        for j in range(attempts):
            if random.randrange(1, 10) == 9:
                spawn = True
                break
        if spawn:
            set_coin(60 + 100 * i, car, road, coins_count, sprites)
        else:
            continue


def set_spanner(x_pos, car, road, health, sprites):
    y_position = -100
    spanner = Spanner((x_pos, y_position), car, road, health, sprites)

    sprites.add(spanner)


def spawn_spanner(car, road, health, sprites):
    if random.randrange(1, 3) == 1:
        set_spanner(60 + 100 * random.randrange(4), car, road, health, sprites)
