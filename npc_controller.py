import random

from sprite_controller import *
from utility import *


def set_npc(sprites, road, x_pos):
    images = ['car_blue', 'car_green', 'car_brown', 'car_red', 'car_yellow',
              'car_pink']
    directions = [1, -1]

    direction = random.choices(directions, weights=[
        1 + road.score // 50 + road.score // 100, 2 + road.score // 50], k=1)[
        0]
    image = random.choice(images)

    if direction == 1:
        image += '_down'
    else:
        image += '_up'

    if direction == -1:
        speed = random.randrange(1, road.non_changed_speed)
    else:
        speed = random.randrange(road.non_changed_speed + 1,
                                 road.non_changed_speed + road.score // 100 + 3)

    if direction == 1:
        speed += road.non_changed_speed

    y_position = -random.randrange(110, 330)
    car = NpcCar(load_image(image), direction, (x_pos, y_position), speed,
                 road,
                 sprites)

    sprites.add(car)


def spawn_npc(sprites, road):
    for i in range(4):
        skip = False
        skip_attempts = 3 - road.score // 50
        if skip_attempts > 0:
            for j in range(skip_attempts):
                if random.randrange(1, 3 + road.score // 50) == 1:
                    skip = True
                    break
        else:
            if random.randrange(1, 5) == 1:
                skip = True
        if skip:
            continue
        else:
            offset = random.randrange(1, 20) * random.choice([1, -1])
            set_npc(sprites, road, 50 + 100 * i + offset)
