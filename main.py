import pygame
import random
import json
import sys

from npc_controller import *
from utility import *
from coins_controller import *
from load_image import load_image

music = ['CasualRide', 'HighwayToTheWest', 'OnMyWay', '47WeeksOnTheRoad',
         'WeHaveNotGottenReallyFar']
skins = ['red', 'yellow', 'pink', 'blue', 'brown', 'green']
road_skins = ['road_basic', 'road_winter', 'road_desert']

saving = {
    'coins': 0,
    'high_score': 0,
    'car_skin': 0,
    'road_skin': 0
}
settings_file = {
    'music_volume': 1,
    'sfx_volume': 0.5,
    'song': 0
}


def close(*args):

    global settings_file
    global saving

    song, coins, car_skin, road_skin = args

    settings_file['song'] = song
    saving['coins'] = coins
    saving['car_skin'] = car_skin
    saving['road_skin'] = road_skin

    with open('saving.json', 'w') as f:
        json.dump(saving, f)
        print('All scores successfully saved.')
    with open('settings_file.json', 'w') as f:
        json.dump(settings_file, f)
        print('All settings successfully saved.')

    pygame.quit()
    sys.exit()


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
    updated = False

    spawn_tick = 0
    coin_spawn_tick = 0

    lose_label = Text(screen, size, 50, 'You lost!', 'white')
    lose_label.dest = ((size[0] - lose_label.render.get_width()) // 2, 100)

    score_lost_label = ScoreLabel(screen, size, 20, '', road, 'white')
    score_lost_label.dest = (
        (size[0] // 2 - score_lost_label.render.get_width() // 2) - 20, 150)

    score_label = ScoreLabel(screen, size, 40, '', road, 'white', (10, 17))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close(current_song, coins_count.coins_count, car_skin, road_skin)
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
            if not updated:
                if road.score <= saving['high_score']:
                    sll_msg = 'Score: '
                else:
                    sll_msg = 'New high score: '
                    saving['high_score'] = road.score
                updated = True

                score_lost_label.message = sll_msg
                score_lost_label.render = score_lost_label.font.render(score_lost_label.message, True, score_lost_label.color)
                score_lost_label.dest = (
                    (size[0] // 2 - score_lost_label.render.get_width() // 2) - 20,
                    150)

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
                close(current_song, coins_count.coins_count, car_skin, road_skin)
            if play_button.update(event):
                play()
            if arrow_left.update(event):
                if car_skin - 1 < 0:
                    car_skin = len(skins) - 1
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
    global current_song

    menu_sprites = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
    npc_cars = pygame.sprite.Group()
    player = pygame.sprite.Group()
    overlay_group = pygame.sprite.Group()

    label = Text(screen, size, 50, 'Settings', 'white')
    label.dest = ((size[0] - label.render.get_width()) // 2, 10)
    road = Road(load_image(road_skins[road_skin]), sprites)

    current_song_name = music[current_song]
    rendering_song_name = current_song_name if len(current_song_name) <= 10 else current_song_name[0:6] + '...'
    song_name = HiddenText(screen, size, 30, rendering_song_name, 'white')
    song_name.dest = ((size[0] - song_name.render.get_width()) // 2, 100 + 30 - song_name.render.get_height() // 2)

    car = Car(load_image(f'car_{skins[car_skin]}_up'), road, npc_cars, player)
    overlay = UiSprite(load_image('overlay'), (0, 0), overlay_group)

    song_section = Text(screen, size, 20, 'Song', 'white')
    song_section.dest = ((size[0] - song_section.render.get_width()) // 2, 80)

    arrow_right = Button(load_image('buttons/arrow'),
                         load_image('buttons/arrow_hl'), (430 - 36, 100),
                         menu_sprites)
    arrow_left = Button(
        pygame.transform.flip(load_image('buttons/arrow'), True, False),
        pygame.transform.flip(load_image('buttons/arrow_hl'), True, False),
        (50, 100), menu_sprites)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close(current_song, coins_count.coins_count, car_skin, road_skin)
            if arrow_left.update(event):
                if current_song - 1 < 0:
                    current_song = len(music) - 1
                else:
                    current_song -= 1
                song_name = change_song(screen, size, music, current_song)
                settings_file['song'] = current_song

            if arrow_right.update(event):
                if current_song + 1 > len(music) - 1:
                    current_song = 0
                else:
                    current_song += 1
                song_name = change_song(screen, size, music, current_song)
                settings_file['song'] = current_song

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
        song_section.update()
        song_name.update(hidden_message=music[current_song])

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
                close(current_song, coins_count.coins_count, car_skin, road_skin)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
            if arrow_left.update(event):
                if road_skin - 1 < 0:
                    road_skin = len(road_skins) - 1
                else:
                    road_skin -= 1
                change_road(road, road_skins[road_skin])
            if arrow_right.update(event):
                if road_skin + 1 > len(road_skins) - 1:
                    road_skin = 0
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

    try:
        with open('saving.json') as f:
            saving = json.load(f)
    except:
        print('No saving file created yet')
    try:
        with open('settings_file.json') as f:
            settings_file = json.load(f)
    except:
        print('No settings file created yet')

    car_skin = saving['car_skin']
    road_skin = saving['road_skin']

    coins_count = CoinsCount(screen, size, 40, '#f7e26b')
    coins_count.coins_count = saving['coins']
    current_song = settings_file['song']

    set_music(music[current_song])

    main_menu()
    close(current_song, coins_count.coins_count, car_skin, road_skin)