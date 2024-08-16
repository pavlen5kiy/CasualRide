import pygame
import random
import json
import sys

from npc_controller import *
from utility import *
from coins_controller import *
from load_image import load_image

music = ['CasualRide', 'HighwayToTheWest', 'OnMyWay', '47WeeksOnTheRoad',
         'WeHaveNotGottenReallyFar', 'Off']
skins = {'red': ['open', 0],
         'yellow': ['locked', 100],
         'pink': ['locked', 500],
         'blue': ['locked', 50],
         'brown': ['locked', 20],
         'green': ['locked', 250]}
road_skins = {'road_basic': ['open', 0],
              'road_winter': ['locked', 1500],
              'road_desert': ['locked', 1000]}

saving = {
    'coins': 0,
    'high_score': 0,
    'car_skin': 0,
    'road_skin': 0,
    'car_skins': skins,
    'road_skins': road_skins
}
settings_file = {
    'music_volume': 1,
    'sfx_volume': 0.5,
    'song': 0
}


def close(*args):
    global settings_file
    global saving

    song, coins, main_skin, main_road_skin, skins, road_skins = args

    settings_file['song'] = song
    saving['coins'] = coins
    saving['car_skin'] = main_skin
    saving['road_skin'] = main_road_skin
    saving['car_skins'] = skins
    saving['road_skins'] = road_skins

    with open('saving.json', 'w') as f:
        json.dump(saving, f)
        print('All scores successfully saved.')
    with open('settings_file.json', 'w') as f:
        json.dump(settings_file, f)
        print('All settings successfully saved.')

    pygame.quit()
    sys.exit()


def play():
    global main_skin
    global main_road_skin

    timer = Timer(-1, screen, size)
    timer.seconds = 4

    pause_menu_sprites = pygame.sprite.Group()
    home_button_group = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    npc_cars = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    player = pygame.sprite.Group()
    npc_particles = pygame.sprite.Group()
    overlay_group = pygame.sprite.Group()

    road = Road(load_image(list(road_skins.keys())[main_road_skin]), sprites)

    car = Car(load_image(f'car_{list(skins.keys())[main_skin]}_up'), road,
              npc_cars, player)

    overlay = UiSprite(load_image('overlay'), (0, 0), overlay_group)

    show_rect = False
    show_hitbox = False

    lost = False
    updated = False

    paused = False

    spawn_tick = 0
    coin_spawn_tick = 0

    lose_label = Text(screen, size, 50, 'You lost!', 'white')
    lose_label.dest = ((size[0] - lose_label.render.get_width()) // 2, 100)

    score_lost_label = ScoreLabel(screen, size, 20, '', road, 'white')
    score_lost_label.dest = (
        (size[0] // 2 - score_lost_label.render.get_width() // 2) - 20, 150)

    score_label = ScoreLabel(screen, size, 40, '', road, 'white', (10, 17))

    pause_label = Text(screen, size, 50, 'Pause', 'white')
    pause_label.dest = ((size[0] - pause_label.render.get_width()) // 2, 10)

    home_button = Button(load_image('buttons/home'),
                         load_image('buttons/home_hl'), (12, 560),
                         home_button_group)

    continue_button = Button(load_image('buttons/continue'),
                             load_image('buttons/continue_hl'), (396, 560),
                             pause_menu_sprites)

    warning = Text(screen, size, 15, "Score won't be saved if you leave!",
                   'white')
    warning.dest = ((size[0] - warning.render.get_width()) // 2, 530)

    timer_sfx = pygame.mixer.Sound('assets/sfx/Countdown.mp3')
    timer_sfx.set_volume(1)
    timer_sfx.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close(current_song, coins_count.coins_count, main_skin,
                      main_road_skin, skins, road_skins)

            if paused:
                if home_button.update(event):
                    main_menu()

                if continue_button.update(event):
                    paused = not paused

            if lost:
                if home_button.update(event):
                    main_menu()

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
                    if not lost and timer.seconds <= 0:
                        paused = not paused
                    elif lost:
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

        if timer.seconds <= 0 and not lost and not paused:
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
                score_lost_label.render = score_lost_label.font.render(
                    score_lost_label.message, True, score_lost_label.color)
                score_lost_label.dest = (
                    (size[
                         0] // 2 - score_lost_label.render.get_width() // 2) - 20,
                    150)

            overlay_group.draw(screen)
            lose_label.update()
            score_lost_label.update()
            home_button_group.draw(screen)

        else:
            score_label.update()

        if 0 < timer.seconds:
            overlay_group.draw(screen)
            timer.render()
            timer.update()

        coins_count.update()

        if paused:
            overlay_group.draw(screen)
            pause_label.update()
            pause_menu_sprites.draw(screen)
            home_button_group.draw(screen)
            warning.update()

        clock.tick(fps)
        pygame.display.update()


def main_menu():
    global car_skin
    global main_road_skin
    global skins
    global main_skin

    menu_sprites = pygame.sprite.Group()
    lock_button_group = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
    npc_cars = pygame.sprite.Group()
    player = pygame.sprite.Group()
    overlay_group = pygame.sprite.Group()

    label = Text(screen, size, 50, 'Menu', 'white')
    label.dest = (10, 10)
    road = Road(load_image(list(road_skins.keys())[main_road_skin]), sprites)

    car = Car(load_image(f'car_{list(skins.keys())[main_skin]}_up'), road,
              npc_cars, player)
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
    lock_button = Button(load_image('buttons/lock'),
                         load_image('buttons/lock_hl'), (216, 415),
                         lock_button_group)
    car_skin = main_skin
    skin_info_msg = f'{skins[list(skins.keys())[car_skin]][0].capitalize()}. Price: {skins[list(skins.keys())[car_skin]][1]}'
    skin_info = Text(screen, size, 20, skin_info_msg, 'white')
    skin_info.dest = ((size[0] - skin_info.render.get_width()) // 2, 350)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close(current_song, coins_count.coins_count, main_skin,
                      main_road_skin, skins, road_skins)
            if play_button.update(event):
                play()
            if skins[list(skins.keys())[car_skin]][0] == 'locked':
                if lock_button.update(event):
                    if coins_count.coins_count - \
                            skins[list(skins.keys())[car_skin]][1] >= 0:
                        skins[list(skins.keys())[car_skin]][0] = 'open'
                        main_skin = car_skin
                        coins_count.coins_count = coins_count.coins_count - \
                                                  skins[list(skins.keys())[
                                                      car_skin]][1]
            if arrow_left.update(event):
                if car_skin - 1 < 0:
                    car_skin = len(skins) - 1
                else:
                    car_skin -= 1
                change_skin(car, list(skins.keys())[car_skin])
                if skins[list(skins.keys())[car_skin]][0] == 'open':
                    main_skin = car_skin
                    print(main_skin)

                skin_info_msg = f'{skins[list(skins.keys())[car_skin]][0].capitalize()}. Price: {skins[list(skins.keys())[car_skin]][1]}'
                skin_info.set_text(skin_info_msg)
                skin_info.dest = (
                    (size[0] - skin_info.render.get_width()) // 2, 350)
            if arrow_right.update(event):
                if car_skin + 1 > len(skins) - 1:
                    car_skin = 0
                else:
                    car_skin += 1
                change_skin(car, list(skins.keys())[car_skin])
                if skins[list(skins.keys())[car_skin]][0] == 'open':
                    main_skin = car_skin
                    print(main_skin)

                skin_info_msg = f'{skins[list(skins.keys())[car_skin]][0].capitalize()}. Price: {skins[list(skins.keys())[car_skin]][1]}'
                skin_info.set_text(skin_info_msg)
                skin_info.dest = (
                    (size[0] - skin_info.render.get_width()) // 2, 350)
            if settings_button.update(event):
                settings()
            if road_button.update(event):
                road_menu()

        screen.fill(pygame.Color('black'))

        sprites.draw(screen)
        overlay_group.draw(screen)
        player.draw(screen)
        menu_sprites.draw(screen)

        if skins[list(skins.keys())[car_skin]][0] == 'locked':
            skin_info.update()
            lock_button_group.draw(screen)

        road.update()
        screen.blit(load_image('line'), (-10, 0))

        label.update()
        coins_count.update()

        clock.tick(fps)
        pygame.display.update()


def settings():
    global car_skin
    global main_road_skin
    global current_song

    menu_sprites = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
    npc_cars = pygame.sprite.Group()
    player = pygame.sprite.Group()
    overlay_group = pygame.sprite.Group()

    label = Text(screen, size, 50, 'Settings', 'white')
    label.dest = ((size[0] - label.render.get_width()) // 2, 10)
    road = Road(load_image(list(road_skins.keys())[main_road_skin]), sprites)

    current_song_name = music[current_song]
    rendering_song_name = current_song_name if len(
        current_song_name) <= 10 else current_song_name[0:6] + '...'
    song_name = HiddenText(screen, size, 30, rendering_song_name, 'white')
    song_name.dest = ((size[0] - song_name.render.get_width()) // 2,
                      100 + 30 - song_name.render.get_height() // 2)

    car = Car(load_image(f'car_{list(skins.keys())[main_skin]}_up'), road,
              npc_cars, player)
    overlay = UiSprite(load_image('overlay'), (0, 0), overlay_group)

    song_section = Text(screen, size, 20, 'Music', 'white')
    song_section.dest = ((size[0] - song_section.render.get_width()) // 2, 80)

    arrow_right = Button(load_image('buttons/arrow'),
                         load_image('buttons/arrow_hl'), (430 - 36, 100),
                         menu_sprites)
    arrow_left = Button(
        pygame.transform.flip(load_image('buttons/arrow'), True, False),
        pygame.transform.flip(load_image('buttons/arrow_hl'), True, False),
        (50, 100), menu_sprites)

    back_button = Button(load_image('buttons/back'),
                         load_image('buttons/back_hl'), (12, 560),
                         menu_sprites)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close(current_song, coins_count.coins_count, main_skin,
                      main_road_skin, skins, road_skins)
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

            if back_button.update(event):
                main_menu()

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
    global main_road_skin
    global road_skin

    menu_sprites = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
    npc_cars = pygame.sprite.Group()
    player = pygame.sprite.Group()
    lock_button_group = pygame.sprite.Group()

    road_skin = main_road_skin

    label = Text(screen, size, 50, 'Road', 'white')
    label.dest = (10, 10)
    road = Road(load_image(list(road_skins.keys())[main_road_skin]), sprites)
    car = Car(load_image(f'car_{list(skins.keys())[main_skin]}_up'), road,
              npc_cars, player)

    arrow_right = Button(load_image('buttons/arrow'),
                         load_image('buttons/arrow_hl'), (340, 420),
                         menu_sprites)
    arrow_left = Button(
        pygame.transform.flip(load_image('buttons/arrow'), True, False),
        pygame.transform.flip(load_image('buttons/arrow_hl'), True, False),
        (140 - 36, 420), menu_sprites)

    back_button = Button(load_image('buttons/back'),
                         load_image('buttons/back_hl'), (12, 560),
                         menu_sprites)

    lock_button = Button(load_image('buttons/lock'),
                         load_image('buttons/lock_hl'), (216, 415),
                         lock_button_group)

    skin_info_msg = f'{road_skins[list(road_skins.keys())[road_skin]][0].capitalize()}. Price: {road_skins[list(road_skins.keys())[road_skin]][1]}'
    skin_info = Text(screen, size, 20, skin_info_msg, 'Black')
    skin_info.dest = ((size[0] - skin_info.render.get_width()) // 2, 350)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close(current_song, coins_count.coins_count, main_skin,
                      main_road_skin, skins, road_skins)
            if road_skins[list(road_skins.keys())[road_skin]][0] == 'locked':
                if lock_button.update(event):
                    if coins_count.coins_count - \
                            road_skins[list(road_skins.keys())[road_skin]][1] >= 0:
                        road_skins[list(road_skins.keys())[road_skin]][0] = 'open'
                        main_road_skin = road_skin
                        coins_count.coins_count = coins_count.coins_count - \
                                                  road_skins[list(road_skins.keys())[
                                                      road_skin]][1]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
            if arrow_left.update(event):
                if road_skin - 1 < 0:
                    road_skin = len(road_skins) - 1
                else:
                    road_skin -= 1
                change_road(road, list(road_skins.keys())[road_skin])

                if road_skins[list(road_skins.keys())[road_skin]][0] == 'open':
                    main_road_skin = road_skin
                    print(main_road_skin)

                skin_info_msg = f'{road_skins[list(road_skins.keys())[road_skin]][0].capitalize()}. Price: {road_skins[list(road_skins.keys())[road_skin]][1]}'
                skin_info.set_text(skin_info_msg)
                skin_info.dest = (
                    (size[0] - skin_info.render.get_width()) // 2, 350)

            if arrow_right.update(event):
                if road_skin + 1 > len(road_skins) - 1:
                    road_skin = 0
                else:
                    road_skin += 1
                change_road(road, list(road_skins.keys())[road_skin])

                if road_skins[list(road_skins.keys())[road_skin]][0] == 'open':
                    main_road_skin = road_skin
                    print(main_road_skin)

                skin_info_msg = f'{road_skins[list(road_skins.keys())[road_skin]][0].capitalize()}. Price: {road_skins[list(road_skins.keys())[road_skin]][1]}'
                skin_info.set_text(skin_info_msg)
                skin_info.dest = (
                    (size[0] - skin_info.render.get_width()) // 2, 350)

            if back_button.update(event):
                main_menu()

        screen.fill(pygame.Color('black'))

        sprites.draw(screen)
        player.draw(screen)
        menu_sprites.draw(screen)

        road.update()

        screen.blit(load_image('line'), (-10, 0))

        label.update()
        coins_count.update()

        if road_skins[list(road_skins.keys())[road_skin]][0] == 'locked':
            skin_info.update()
            lock_button_group.draw(screen)

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
    main_skin = car_skin
    road_skin = saving['road_skin']
    main_road_skin = road_skin
    skins = saving['car_skins']
    road_skins = saving['road_skins']

    coins_count = CoinsCount(screen, size, 40, '#f7e26b')
    coins_count.coins_count = saving['coins']
    current_song = settings_file['song']

    set_music(music[current_song])

    main_menu()
    close(current_song, coins_count.coins_count, main_skin,
          main_road_skin, skins, road_skins)
