import pygame
import random

from npc_controller import *
from utility import *
from coins_controller import *
from load_image import load_image

music = ['CasualRide', 'BigOldBlues', 'OnMyWay', '47WeeksOnTheRoad']
skins = ['red', 'yellow', 'pink', 'blue', 'brown', 'green']
road_skins = ['road_basic', 'road_winter', 'road_desert']
car_skin = 0
road_skin = 0


def play():
    global car_skin
    global road_skin

    timer = Timer(-1, screen, size)
    timer.seconds = 4

    sprites = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    npc_cars = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    player = pygame.sprite.Group()
    npc_particles = pygame.sprite.Group()
    overlay_group = pygame.sprite.Group()

    road = Road(load_image(road_skins[road_skin]), sprites)

    car = Car(load_image(f'car_{skins[car_skin]}_up'), road, npc_cars, player)

    overlay = UiSprite(load_image('overlay'), (0, 0), overlay_group)

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

    score_label = ScoreLabel(screen, size, 40, '', road, 'white', (10, 17))

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

        if timer.seconds <= 0 and not lost:
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

        screen.blit(load_image('line'), (-10, 0))

        if lost:
            overlay_group.draw(screen)
            lose_label.update()
            score_lost_label.update()
        else:
            score_label.update()

        if 0 < timer.seconds:
            overlay_group.draw(screen)
            timer.render()
            timer.update()

        coins_count.update()

        clock.tick(fps)
        pygame.display.update()


def main_menu():
    global car_skin
    global road_skin

    menu_sprites = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
    npc_cars = pygame.sprite.Group()
    player = pygame.sprite.Group()
    overlay_group = pygame.sprite.Group()

    label = Text(screen, size, 50, 'Menu', 'white')
    label.dest = ((size[0] - label.render.get_width()) // 2, 10)
    road = Road(load_image(road_skins[road_skin]), sprites)

    car = Car(load_image(f'car_{skins[car_skin]}_up'), road, npc_cars, player)
    overlay = UiSprite(load_image('overlay'), (0, 0), overlay_group)

    play_button = Button(load_image('buttons/play'),
                         load_image('buttons/play_hl'), (170, 560),
                         menu_sprites)
    arrow_right = Button(load_image('buttons/arrow'),
                         load_image('buttons/arrow_hl'), (340, 420),
                         menu_sprites)
    arrow_left = Button(
        pygame.transform.flip(load_image('buttons/arrow'), True, False),
        pygame.transform.flip(load_image('buttons/arrow_hl'), True, False),
        (140 - 36, 420), menu_sprites)
    settings_button = Button(load_image('buttons/settings'),
                         load_image('buttons/settings_hl'), (60, 560),
                         menu_sprites)
    road_button = Button(load_image('buttons/road'),
                      load_image('buttons/road_hl'), (480 - 60 - 64, 560),
                      menu_sprites)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if play_button.update(event):
                play()
            if arrow_left.update(event):
                if car_skin - 1 < 0:
                    car_skin = 5
                else:
                    car_skin -= 1
                change_skin(car, skins[car_skin])
            if arrow_right.update(event):
                if car_skin + 1 > len(skins) - 1:
                    car_skin = 0
                else:
                    car_skin += 1
                change_skin(car, skins[car_skin])
            if settings_button.update(event):
                settings()
            if road_button.update(event):
                road_menu()

        screen.fill(pygame.Color('black'))

        sprites.draw(screen)
        overlay_group.draw(screen)
        player.draw(screen)
        menu_sprites.draw(screen)

        road.update()
        screen.blit(load_image('line'), (-10, 0))

        label.update()
        coins_count.update()

        clock.tick(fps)
        pygame.display.update()


def settings():
    global car_skin
    global road_skin

    menu_sprites = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
    npc_cars = pygame.sprite.Group()
    player = pygame.sprite.Group()
    overlay_group = pygame.sprite.Group()

    label = Text(screen, size, 50, 'Settings', 'white')
    label.dest = ((size[0] - label.render.get_width()) // 2, 10)
    road = Road(load_image(road_skins[road_skin]), sprites)

    car = Car(load_image(f'car_{skins[car_skin]}_up'), road, npc_cars, player)
    overlay = UiSprite(load_image('overlay'), (0, 0), overlay_group)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        screen.fill(pygame.Color('black'))

        sprites.draw(screen)
        player.draw(screen)
        overlay_group.draw(screen)
        menu_sprites.draw(screen)

        road.update()

        screen.blit(load_image('line'), (-10, 0))

        label.update()

        clock.tick(fps)
        pygame.display.update()


def road_menu():
    global car_skin
    global road_skin

    menu_sprites = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
    npc_cars = pygame.sprite.Group()
    player = pygame.sprite.Group()

    label = Text(screen, size, 50, 'Road', 'white')
    label.dest = ((size[0] - label.render.get_width()) // 2, 10)
    road = Road(load_image(road_skins[road_skin]), sprites)
    car = Car(load_image(f'car_{skins[car_skin]}_up'), road, npc_cars, player)

    arrow_right = Button(load_image('buttons/arrow'),
                         load_image('buttons/arrow_hl'), (340, 420),
                         menu_sprites)
    arrow_left = Button(
        pygame.transform.flip(load_image('buttons/arrow'), True, False),
        pygame.transform.flip(load_image('buttons/arrow_hl'), True, False),
        (140 - 36, 420), menu_sprites)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
            if arrow_left.update(event):
                if road_skin - 1 < 0:
                    road_skin = 1
                    change_road(road, road_skins[road_skin])
                else:
                    road_skin -= 1
                    change_road(road, road_skins[road_skin])
            if arrow_right.update(event):
                if road_skin + 1 > len(road_skins) - 1:
                    road_skin = 0
                    change_road(road, road_skins[road_skin])
                else:
                    road_skin += 1
                    change_road(road, road_skins[road_skin])

        screen.fill(pygame.Color('black'))

        sprites.draw(screen)
        player.draw(screen)
        menu_sprites.draw(screen)

        road.update()

        screen.blit(load_image('line'), (-10, 0))

        label.update()

        clock.tick(fps)
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    screen, size, screen_rect = set_screen((480, 640))
    coins_count = CoinsCount(screen, size, 40, '#f7e26b')
    set_music(music[-1])

    main_menu()

    pygame.quit()
