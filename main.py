from sprite_controller import *
from load_image import *
from ui import Timer

import random
import pygame


def set_npc(sprites, road_speed, x_pos):
    images = ['car_blue', 'car_green', 'car_brown']
    directions = [1, -1]

    direction = random.choice(directions)
    image = random.choice(images)

    if direction == 1:
        image += '_down'
    else:
        image += '_up'

    if direction == -1:
        speed = random.randrange(1, road_speed)
    else:
        speed = random.randrange(road_speed + 1, road_speed + 4)

    if direction == 1:
        speed += road_speed

    y_position = -random.randrange(110, 500)
    car = NpcCar(load_image(image), direction, (x_pos, y_position), speed,
                 sprites)

    sprites.add(car)


def spawn_npc(sprites, road_speed):
    for i in range(4):
        if random.randrange(1, 3) == 2:
            continue
        else:
            offset = random.randrange(1, 10) * random.choice([1, -1])
            set_npc(sprites, road_speed, 40 + 100 * i + offset)


def set_music(track):
    # pygame.mixer.music.stop()
    pygame.mixer.music.load(f'assets/{track}.mp3')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    print(f'Music on: {track}.')


def main():
    clock = pygame.time.Clock()
    pygame.init()

    size = 480, 640
    screen = pygame.display.set_mode(size)

    timer = Timer(-1, screen, size)

    font = pygame.font.Font('assets/PixelOperator8-Bold.ttf', 40)

    set_music('GetUpAction')

    sprites = pygame.sprite.Group()
    npc_cars = pygame.sprite.Group()

    road = Road(load_image('road'), sprites)
    car = Car(load_image('car'), sprites)

    pygame.display.set_caption('Get ready!')

    fps = 60

    running = True
    play = False
    lost = False
    start = False

    road_speed = road.speed
    speed_change = 0
    spawn_tick = 0

    timer.seconds = 9

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if start:
                        if not lost:
                            play = not play
                            if not play:
                                pygame.display.set_caption('Pause')
                if event.key == pygame.K_a:
                    if car.rect.x >= 0:
                        car.x_movement = -1
                if event.key == pygame.K_d:
                    if car.rect.x <= 420:
                        car.x_movement = 1
                    car.x_movement = 1
                if event.key == pygame.K_s:
                    if car.rect.y <= 580:
                        car.y_movement = 1
                if event.key == pygame.K_w:
                    if car.rect.y >= 0:
                        car.y_movement = -1

                if event.key == pygame.K_r:
                    sprites = pygame.sprite.Group()
                    npc_cars = pygame.sprite.Group()

                    road = Road(load_image('road'), sprites)
                    car = Car(load_image('car'), sprites)

                    pygame.display.set_caption('Pause')

                    play = False
                    lost = False
                    start = False
                    spawn_tick = 0

                    timer.seconds = 9

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    car.x_movement = 0
                if event.key == pygame.K_d:
                    car.x_movement = 0
                if event.key == pygame.K_s:
                    car.y_movement = 0
                if event.key == pygame.K_w:
                    car.y_movement = 0

        if timer.seconds == 0:
            if not start:
                play = True
                start = True

        if play:
            pygame.display.set_caption('Play')

            road.update()
            if car.update(npc_cars):
                play = False
                pygame.display.set_caption('Hehe')
                lost = True

            if not npc_cars:
                pass
                spawn_npc(npc_cars, road_speed)

            if spawn_tick == 300:
                for npc in npc_cars:
                    npc.update()
            else:
                spawn_tick += 1

        clock.tick(fps)

        screen.fill(pygame.Color('black'))
        sprites.draw(screen)
        npc_cars.draw(screen)

        # pygame.draw.rect(screen, pygame.Color('blue'), car.rect)
        #
        # for npc in npc_cars:
        #     pygame.draw.rect(screen, pygame.Color('purple'), npc.rect)
        #     pygame.draw.rect(screen, pygame.Color('red'), npc.hitbox)
        #
        # pygame.draw.rect(screen, pygame.Color('green'), car.hitbox)

        if lost:
            lose_output = font.render('You lost!', True, 'red')
            text_width, text_height = lose_output.get_size()

            screen.blit(lose_output, ((size[0] - text_width) // 2, 100))

        score_output = font.render(str(road.score), True, 'white')

        screen.blit(score_output, (10, 10))

        timer.render()

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
