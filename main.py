import pygame
import random

from npc_controller import *
from utility import *
from coins_controller import *

tracks = ['CasualRide', 'BigOldBlues', 'OnMyWay', '47WeeksOnTheRoad']
skins = ['red', 'yellow', 'pink', 'blue', 'brown', 'green']
car_skin = skins[0]


def play():
    timer = Timer(-1, screen, size)
    timer.seconds = 4

    sprites = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    npc_cars = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    player = pygame.sprite.Group()
    npc_particles = pygame.sprite.Group()
    overlay_group = pygame.sprite.Group()

    road = Road(load_image('road'), sprites)
    car = Car(load_image(f'car_{car_skin}_up'), road, npc_cars, player)
    coins_count = CoinsCount(screen, size, 40, '#f7e26b')

    overlay = UiSprite(load_image('overlay'), (0, 0), overlay_group)

    set_music(random.choice(tracks))

    show_rect = False
    show_hitbox = False

    lost = False

    spawn_tick = 0
    coin_spawn_tick = 0

    lose_label = Text(screen, size, 50, 'You lost!', 'white')
    lose_label.dest = ((size[0] - lose_label.render.get_width()) // 2, 100)

    score_lost_label = ScoreLabel(screen, size, 30, 'Score: ', road, 'white')
    score_lost_label.dest = (
        (size[0] // 2 - score_lost_label.render.get_width() // 2) - 20, 150)

    score_label = ScoreLabel(screen, size, 40, '', road, 'white', (10, 10))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
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
                if event.key == pygame.K_ESCAPE:
                    main_menu()

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

        if timer.seconds <= 0:
            road.update()

            if car.update(particles):
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

        screen.fill(pygame.Color('black'))

        sprites.draw(screen)
        coins.draw(screen)
        particles.draw(screen)
        player.draw(screen)
        npc_particles.draw(screen)
        npc_cars.draw(screen)

        render_hitbox(screen, car, npc_cars, show_rect, show_hitbox)

        if lost:
            lose_label.update()
            score_lost_label.update()
        else:
            score_label.update()

        coins_count.update()

        if 0 < timer.seconds:
            overlay_group.draw(screen)
            timer.render()
            timer.update()

        clock.tick(fps)
        pygame.display.update()


def main_menu():

    global car_skin

    set_music('47WeeksOnTheRoad')

    main_menu_sprites = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
    npc_cars = pygame.sprite.Group()
    player = pygame.sprite.Group()
    overlay_group = pygame.sprite.Group()

    menu_label = Text(screen, size, 50, 'Menu', 'white')
    menu_label.dest = ((size[0] - menu_label.render.get_width()) // 2, 10)
    road = Road(load_image('road'), sprites)
    car = Car(load_image(f'car_{car_skin}_up'), road, npc_cars, player)
    overlay = UiSprite(load_image('overlay'), (0, 0), overlay_group)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play()

                if event.key == pygame.K_1:
                    car_skin = skins[0]
                    change_skin(car, car_skin)
                if event.key == pygame.K_2:
                    car_skin = skins[1]
                    change_skin(car, car_skin)
                if event.key == pygame.K_3:
                    car_skin = skins[2]
                    change_skin(car, car_skin)
                if event.key == pygame.K_4:
                    car_skin = skins[3]
                    change_skin(car, car_skin)
                if event.key == pygame.K_5:
                    car_skin = skins[4]
                    change_skin(car, car_skin)
                if event.key == pygame.K_6:
                    car_skin = skins[5]
                    change_skin(car, car_skin)

        screen.fill(pygame.Color('black'))

        sprites.draw(screen)
        overlay_group.draw(screen)
        player.draw(screen)
        main_menu_sprites.draw(screen)

        road.update()
        menu_label.update()

        clock.tick(fps)
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    screen, size, screen_rect = set_screen((480, 640))

    main_menu()

    pygame.quit()
