import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)


class Road(Sprite):
    def __init__(self, image, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.y = -1290
        self.speed = 10
        self.acceleration = 4
        self.step = 0

    def update(self, speed_change):
        if self.rect.y >= -10:
            self.rect.y = -1290

        self.rect.y += self.speed

        if speed_change == -1:
            if self.speed > 2:
                self.step += 1
                if self.step == 100:
                    if self.acceleration > 2:
                        self.acceleration -= 1
                    self.step = 0
                    self.speed -= self.acceleration
        else:
            self.acceleration = 4
            self.step = 0


class Car(Sprite):
    def __init__(self, image, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (360 - 30, 320 - 52)
        self.movement = 0
        self.speed = 5
        self.acceleration = 2
        self.step = 0
        self.limit_reached = False

    def update(self, speed_change, overall_speed):
        self.rect.x += self.speed * self.movement

        if speed_change == -1:
            if overall_speed > 2:
                if self.acceleration > -(overall_speed // 2):
                    self.step += 1
                    self.rect.y += self.acceleration
                    if self.step == 10:
                        if not self.limit_reached:
                            if self.acceleration < (overall_speed // 2):
                                self.acceleration += self.acceleration // 2
                            else:
                                self.limit_reached = True
                        else:
                            self.acceleration -= self.acceleration // 2 + 1
                        self.step = 0

        if speed_change == 1:
            if overall_speed < 10:
                if self.acceleration < (overall_speed // 2):
                    self.step += 1
                    self.rect.y += self.acceleration
                    if self.step == 10:
                        if not self.limit_reached:
                            if self.acceleration < (overall_speed // 2):
                                self.acceleration += self.acceleration // 2
                            else:
                                self.limit_reached = True
                        else:
                            self.acceleration -= self.acceleration // 2 + 1
                        self.step = 0
        else:
            self.step = 0
            self.limit_reached = False






    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play = not play
                if event.key == pygame.K_a:
                    car.movement = -1
                if event.key == pygame.K_d:
                    car.movement = 1
                if event.key == pygame.K_s:
                    if road.speed > 2:
                        speed_change = -1
                if event.key == pygame.K_w:
                    if road.speed < 10:
                        speed_change = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    car.movement = 0
                if event.key == pygame.K_d:
                    car.movement = 0
                if event.key == pygame.K_s:
                    speed_change = 0
                if event.key == pygame.K_w:
                    speed_change = 0

        if play:
            pygame.display.set_caption('Play')
        else:
            pygame.display.set_caption('Pause')

        clock.tick(fps)

        screen.fill(pygame.Color('black'))
        sprites.draw(screen)

        road.update(speed_change)
        car.update(speed_change, road.speed)

        pygame.display.flip()

    pygame.quit()


from sprite_controller import *
from utility import *

import random
import pygame


previous_npc = {1: {'speed': 3,'x_pos': -9999},
                -1: {'speed': 3,'x_pos': -9999}}
previous_direction = 1


def set_npc(sprites, road_speed):

    global previous_npc
    global previous_direction

    images = ['car_blue', 'car_green', 'car_brown']
    directions = [1, -1]

    direction = random.choice(directions)
    image = random.choice(images)

    if direction == 1:
        image += '_down'
    else:
        image += '_up'

    speed = random.randrange(1, 7)
    while speed == previous_npc[direction]['speed']:
        speed = random.randrange(1, 7)

    if direction == 1:
        speed += road_speed

    x_position = 202 - 120 * direction + random.randrange(0, 50) * random.choice(directions)
    y_position = -105
    car = NpcCar(load_image(image), direction, (x_position, y_position), speed, sprites)

    sprites.add(car)


def spawn_npc(sprites, road_speed):
    if True:
        set_npc(sprites, road_speed)
        print('a')


def main():
    clock = pygame.time.Clock()
    pygame.init()

    size = 480, 640
    screen = pygame.display.set_mode(size)

    sprites = pygame.sprite.Group()
    npc_cars = pygame.sprite.Group()

    road = Road(load_image('road'), sprites)
    car = Car(load_image('car'), sprites)

    pygame.display.set_caption('Pause')

    fps = 60

    running = True
    play = True

    road_speed = road.speed
    speed_change = 0
    npc_limit = 4
    spawn_tick = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play = not play
                if event.key == pygame.K_a:
                    car.x_movement = -1
                if event.key == pygame.K_d:
                    car.x_movement = 1
                if event.key == pygame.K_s:
                    car.y_movement = 1
                if event.key == pygame.K_w:
                    car.y_movement = -1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    car.x_movement = 0
                if event.key == pygame.K_d:
                    car.x_movement = 0
                if event.key == pygame.K_s:
                    car.y_movement = 0
                if event.key == pygame.K_w:
                    car.y_movement = 0

        if play:
            pygame.display.set_caption('Play')

            spawn_tick += 1

            road.update()
            car.update()

            if len(npc_cars) <= npc_limit and spawn_tick >= 20:
                spawn_tick = 0
                spawn_npc(npc_cars, road_speed)

            for npc in npc_cars:
                npc.update()

        else:
            pygame.display.set_caption('Pause')

        clock.tick(fps)

        screen.fill(pygame.Color('black'))
        sprites.draw(screen)
        npc_cars.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
