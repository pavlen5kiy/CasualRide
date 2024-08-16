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
