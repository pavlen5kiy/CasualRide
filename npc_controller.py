import random

from sprite_controller import *
from utility import *


def set_npc(sprites, road, x_pos):
    images = ['car_blue', 'car_green', 'car_brown', 'car_red', 'car_yellow', 'car_pink']
    directions = [1, -1]

    direction = random.choice(directions)
    image = random.choice(images)

    if direction == 1:
        image += '_down'
    else:
        image += '_up'

    if direction == -1:
        speed = random.randrange(1, road.non_changed_speed)
    else:
        speed = random.randrange(road.non_changed_speed + 1, road.non_changed_speed + 4)

    if direction == 1:
        speed += road.speed

    y_position = -random.randrange(110, 330)
    car = NpcCar(load_image(image), direction, (x_pos, y_position), speed,
                 sprites)

    sprites.add(car)


def spawn_npc(sprites, road):
    for i in range(4):
        if random.randrange(1, 3 + road.score // 50) == 2:
            continue
        else:
            offset = random.randrange(1, 20) * random.choice([1, -1])
            set_npc(sprites, road, 50 + 100 * i + offset)
