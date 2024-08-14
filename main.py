import pygame
import random

from npc_controller import *
from set_functions import *
from utility import *
from coins_controller import *

tracks = ['CasualRide', 'BigOldBlues', 'OnMyWay']
skins = ['red', 'yellow', 'pink', 'blue', 'brown', 'green']


def main():
    pygame.init()
    clock = pygame.time.Clock()

    screen, size, screen_rect = set_screen((480, 640))

    timer = Timer(-1, screen, size)
    timer.seconds = 4

    car_skin = random.choice(skins)

    sprites = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    npc_cars = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    player = pygame.sprite.Group()
    npc_particles = pygame.sprite.Group()
    overlay_group = pygame.sprite.Group()
    main_menu_sprites = pygame.sprite.Group()

    road = Road(load_image('road'), sprites)
    car = Car(load_image(f'car_{car_skin}_up'), road, npc_cars, player)
    coins_count = CoinsCount(screen, size, 40, '#f7e26b')

    overlay = UiSprite(load_image('overlay'), (0, 0), overlay_group)

    pause_label = Text(screen, size, 50, 'Pause', 'white')
    pause_label.dest = ((size[0] - pause_label.render.get_width()) // 2, 10)

    menu_label = Text(screen, size, 50, 'Menu', 'white')
    menu_label.dest = ((size[0] - menu_label.render.get_width()) // 2, 10)

    pygame.display.set_caption('Car Game')

    fps = 60

    running = True

    show_rect = False
    show_hitbox = False

    timer_start = False

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
                    if not timer_start:
                        timer_start = True
                        set_music(random.choice(tracks))

                    if start:
                        if not lost:
                            play = not play
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if car.rect.x >= 0:
                        car.x_movement = -1
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if car.rect.x <= 420:
                        car.x_movement = 1
                    car.x_movement = 1
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if car.rect.y <= 580:
                        car.y_movement = 1
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if car.rect.y >= 0:
                        car.y_movement = -1
                if event.key == pygame.K_ESCAPE and not play and timer_start and timer.seconds <= 0:
                    sprites = pygame.sprite.Group()
                    npc_cars = pygame.sprite.Group()
                    coins = pygame.sprite.Group()
                    player = pygame.sprite.Group()

                    road = Road(load_image('road'), sprites)
                    car = Car(load_image(f'car_{car_skin}_up'), road, npc_cars,
                              player)

                    timer.seconds = 3

                    (play, lost, start, speed_change, spawn_tick,
                     coin_spawn_tick,
                     start_label, lose_label, score_label,
                     score_lost_label) = set_game(screen,
                                                  size,
                                                  road)
                    timer_start = False

                if event.key == pygame.K_r:
                    set_music(random.choice(tracks))

                    sprites = pygame.sprite.Group()
                    npc_cars = pygame.sprite.Group()
                    coins = pygame.sprite.Group()
                    player = pygame.sprite.Group()

                    road = Road(load_image('road'), sprites)
                    car = Car(load_image(f'car_{car_skin}_up'), road, npc_cars,
                              player)

                    timer.seconds = 3

                    (play, lost, start, speed_change, spawn_tick,
                     coin_spawn_tick,
                     start_label, lose_label, score_label,
                     score_lost_label) = set_game(screen,
                                                  size,
                                                  road)

                if event.key == pygame.K_F1:
                    show_rect = not show_rect
                if event.key == pygame.K_F2:
                    show_hitbox = not show_hitbox

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    car.x_movement = 0
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    car.x_movement = 0
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    car.y_movement = 0
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    car.y_movement = 0

        if timer.seconds == 0 and timer_start:
            if not start:
                start = True
                play = True

        if play:

            road.update()

            if car.update(particles):
                play = False
                lost = True

            if not npc_cars:
                pass
                spawn_npc(npc_cars, road)

            if spawn_tick == 300:
                for npc in npc_cars:
                    npc.update(npc_particles)
            else:
                spawn_tick += 1

            for coin in coins:
                coin.update()

            if coin_spawn_tick == 120:
                coin_spawn_tick = 0
                spawn_coins(car, road, coins_count, coins)

            coin_spawn_tick += 1

        particles.update(screen_rect)
        npc_particles.update(screen_rect)

        clock.tick(fps)

        screen.fill(pygame.Color('black'))
        sprites.draw(screen)
        coins.draw(screen)
        particles.draw(screen)
        player.draw(screen)
        npc_particles.draw(screen)
        npc_cars.draw(screen)

        if not play:
            overlay_group.draw(screen)
            if timer_start and timer.seconds <= 0 and not lost:
                pause_label.update()
            if not timer_start:
                menu_label.update()

        render_hitbox(screen, car, npc_cars, show_rect, show_hitbox)

        if lost:
            lose_label.update()
            score_lost_label.update()
        else:
            score_label.update()

        coins_count.update()

        if timer_start:
            timer.update()

            if 0 < timer.seconds:
                timer.render()

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
