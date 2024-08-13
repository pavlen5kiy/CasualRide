import pygame

from npc_controller import *
from set_functions import *
from utility import *
from coins_controller import *


def main():
    pygame.init()
    clock = pygame.time.Clock()

    screen, size, screen_rect = set_screen((480, 640))
    set_music('GetUpAction')

    timer = Timer(-1, screen, size)
    timer.seconds = 9

    car_skin = 'yellow'

    sprites = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    npc_cars = pygame.sprite.Group()
    coins = pygame.sprite.Group()

    road = Road(load_image('road'), sprites)
    car = Car(load_image(f'car_{car_skin}_up'), road, npc_cars, sprites)
    coins_count = CoinsCount(screen, size, 40, '#f7e26b')

    pygame.display.set_caption('Get ready!')

    fps = 60

    running = True
    first_launch = True

    show_rect = False
    show_hitbox = False

    road_speed = road.speed

    (play, lost, start, speed_change, spawn_tick, coin_spawn_tick,
     start_label, lose_label, score_label, score_lost_label) = set_game(screen,
                                                                        size,
                                                                        road)

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
                    coins = pygame.sprite.Group()

                    road = Road(load_image('road'), sprites)
                    car = Car(load_image(f'car_{car_skin}_up'), road, npc_cars,
                              sprites)

                    pygame.display.set_caption('Pause')

                    timer.seconds = 9
                    road_speed = road.speed

                    (play, lost, start, speed_change, spawn_tick, coin_spawn_tick,
                     start_label, lose_label, score_label,
                     score_lost_label) = set_game(screen,
                                                  size,
                                                  road)

                if event.key == pygame.K_F1:
                    show_rect = not show_rect
                if event.key == pygame.K_F2:
                    show_hitbox = not show_hitbox

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
                first_launch = False

        if play:
            pygame.display.set_caption('Play')

            road.update()

            if car.update(particles):
                play = False
                pygame.display.set_caption('Hehe')
                lost = True

            if not npc_cars:
                pass
                spawn_npc(npc_cars, road)

            if spawn_tick == 300:
                for npc in npc_cars:
                    npc.update()
            else:
                spawn_tick += 1

            for coin in coins:
                coin.update()

            if coin_spawn_tick == 120:
                coin_spawn_tick = 0
                spawn_coins(car, road, coins_count, coins)

            coin_spawn_tick += 1

        clock.tick(fps)

        # particles.update(screen_rect)
        screen.fill(pygame.Color('black'))
        sprites.draw(screen)
        coins.draw(screen)
        npc_cars.draw(screen)
        # particles.draw(screen)

        render_hitbox(screen, car, npc_cars, show_rect, show_hitbox)

        if lost:
            lose_label.update()
            score_lost_label.update()
        else:
            score_label.update()

        coins_count.update()

        timer.update()

        if first_launch:
            start_label.update()

            if 0 < timer.seconds <= 4:
                timer.render()

            if 0 < start_label.seconds:
                start_label.render()

        else:
            if 0 < timer.seconds:
                timer.render()

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
