import asyncio

import pygame
import random
import os
import json
import sys
import time

from npc_controller import *
from utility import *
from collectibles_controller import *
from load_image import load_image

music = ['CasualRide', 'HighwayToTheWest', 'OnMyWay', '47WeeksOnTheRoad',
         'WeHaveNotGottenReallyFar', 'Off']
skins = {'red': ['open', 0],
         'yellow': ['locked', 500],
         'pink': ['locked', 1000],
         'blue': ['locked', 300],
         'brown': ['locked', 100],
         'green': ['locked', 750]}
road_skins = {'road_basic': ['open', 0],
              'road_winter': ['locked', 2000],
              'road_desert': ['locked', 1000],
              'road_city': ['locked', 750],
              'road_racetrack': ['locked', 3000],
              'road_ocean': ['locked', 1500]}

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
    'song': 0,
    'render_hints': 0
}

last_time = time.time()
dt = time.time() - last_time
dt *= 60


def render_hint(hint, rect, hints_on=0):
    if rect.collidepoint(pygame.mouse.get_pos()) and hints_on:
        hint_font = pygame.font.Font(
            'assets/fonts/PixelOperator8-Bold.ttf',
            15)
        hint_render = hint_font.render(hint, True, pygame.Color('white'))
        pygame.draw.rect(screen, pygame.Color('black'),
                         pygame.Rect(pygame.mouse.get_pos()[0] + 14 - 70,
                                     pygame.mouse.get_pos()[1] + 14,
                                     hint_render.get_width() + 8,
                                     hint_render.get_height() + 8))
        screen.blit(hint_render, (pygame.mouse.get_pos()[0] + 14 + 4 - 70,
                                  pygame.mouse.get_pos()[1] + 14 + 4))


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

    # with open(saving_file_path, 'w') as f:
    #     json.dump(saving, f)
    #     print('All scores successfully saved.')
    # with open(settings_file_path, 'w') as f:
    #     json.dump(settings_file, f)
    #     print('All settings successfully saved.')

    pygame.quit()
    sys.exit()


async def play():
    global main_skin
    global main_road_skin
    global last_time
    global dt

    timer = Timer(-1, screen, size)
    timer.seconds = 4

    pause_menu_sprites = pygame.sprite.Group()
    restart_button_group = pygame.sprite.Group()
    home_button_group = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    hit_particles = pygame.sprite.Group()
    npc_cars = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
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
    spanner_spawn_tick = 0

    lose_label = Text(screen, size, 50, 'You lost!', 'white')
    lose_label.dest = ((size[0] - lose_label.render.get_width()) // 2, 100)

    score_lost_label = ScoreLabel(screen, size, 20, '', road, 'white')
    score_lost_label.dest = (
        (size[0] // 2 - score_lost_label.render.get_width() // 2) - 20, 150)

    score_label = ScoreLabel(screen, size, 50, '', road, 'white')

    pause_label = Text(screen, size, 50, 'Pause', 'white')
    pause_label.dest = ((size[0] - pause_label.render.get_width()) // 2, 10)

    home_button = Button(load_image('buttons/home'),
                         load_image('buttons/home_hl'), (12, 560),
                         home_button_group)

    continue_button = Button(load_image('buttons/continue'),
                             load_image('buttons/continue_hl'), (396, 560),
                             pause_menu_sprites)

    restart_button = Button(load_image('buttons/restart'),
                             load_image('buttons/restart_hl'), (396, 560),
                             restart_button_group)

    warning = Text(screen, size, 15, "Score won't be saved if you leave!",
                   'white')
    warning.dest = ((size[0] - warning.render.get_width()) // 2, 530)

    health = Health(screen, size, (10, 10))

    timer_sfx = pygame.mixer.Sound('assets/sfx/Countdown.mp3')
    timer_sfx.set_volume(1)
    timer_sfx.play()

    while True:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close(current_song, coins_count.coins_count, main_skin,
                      main_road_skin, skins, road_skins)

            if paused:
                if home_button.update(event):
                    await main_menu()

                if continue_button.update(event):
                    paused = not paused

            if lost:
                if home_button.update(event):
                    await main_menu()
                if restart_button.update(event):
                    await play()

            if event.type == pygame.KEYDOWN:
                if lost:
                    if event.key == pygame.K_r:
                        await play()

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
                        await main_menu()
                if event.key == pygame.K_F3:
                    settings_file['render_hints'] = int(
                        not bool(settings_file['render_hints']))

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
            road.update(dt)

            if car.update(particles, dt, hit_particles):
                health.health -= 1

            if not npc_cars:
                pass
                spawn_npc(npc_cars, road)

            if spawn_tick == 300:
                for npc in npc_cars:
                    npc.update(npc_particles, dt)
            else:
                spawn_tick += 1

            for collectible in collectibles:
                collectible.update(dt)

            if coin_spawn_tick == 120:
                coin_spawn_tick = 0
                spawn_coins(car, road, coins_count, collectibles)

            if spanner_spawn_tick == 630:
                spanner_spawn_tick = 0
                spawn_spanner(car, road, health, collectibles)

            coin_spawn_tick += 1
            spanner_spawn_tick += 1

        particles.update(screen_rect, dt)
        npc_particles.update(screen_rect, dt)
        hit_particles.update(screen_rect, dt)

        screen.fill(pygame.Color('black'))

        sprites.draw(screen)
        collectibles.draw(screen)
        particles.draw(screen)
        player.draw(screen)
        npc_particles.draw(screen)
        npc_cars.draw(screen)
        hit_particles.draw(screen)

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
            restart_button_group.draw(screen)
            render_hint('[Esc]', home_button.rect,
                        settings_file['render_hints'])
            render_hint('[R]', restart_button.rect,
                        settings_file['render_hints'])

        else:
            if health.health <= 0:
                lost = True
            score_label.update(dynamic_update=True)

        if 0 < timer.seconds:
            overlay_group.draw(screen)
            timer.render()
            timer.update()

        coins_count.update()
        health.update()

        if paused:
            overlay_group.draw(screen)
            pause_label.update()
            pause_menu_sprites.draw(screen)
            home_button_group.draw(screen)
            warning.update()
            render_hint('[Esc]', continue_button.rect,
                        settings_file['render_hints'])

        clock.tick(fps)
        pygame.display.flip()
        await asyncio.sleep(0)


async def main_menu():
    global car_skin
    global main_road_skin
    global skins
    global main_skin
    global last_time
    global dt

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

    score_label = Text(screen, size, 30, f'High score: {saving["high_score"]}',
                       'white', (10, 80))

    while True:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close(current_song, coins_count.coins_count, main_skin,
                      main_road_skin, skins, road_skins)
            if play_button.update(
                    event) or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                await play()
            if skins[list(skins.keys())[car_skin]][0] == 'locked':
                if lock_button.update(
                        event) or event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    if coins_count.coins_count - \
                            skins[list(skins.keys())[car_skin]][1] >= 0:
                        skins[list(skins.keys())[car_skin]][0] = 'open'
                        main_skin = car_skin
                        coins_count.coins_count = coins_count.coins_count - \
                                                  skins[list(skins.keys())[
                                                      car_skin]][1]
            if arrow_left.update(
                    event) or event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if car_skin - 1 < 0:
                    car_skin = len(skins) - 1
                else:
                    car_skin -= 1
                change_skin(car, list(skins.keys())[car_skin])
                if skins[list(skins.keys())[car_skin]][0] == 'open':
                    main_skin = car_skin

                skin_info_msg = f'{skins[list(skins.keys())[car_skin]][0].capitalize()}. Price: {skins[list(skins.keys())[car_skin]][1]}'
                skin_info.set_text(skin_info_msg)
                skin_info.dest = (
                    (size[0] - skin_info.render.get_width()) // 2, 350)
            if arrow_right.update(
                    event) or event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if car_skin + 1 > len(skins) - 1:
                    car_skin = 0
                else:
                    car_skin += 1
                change_skin(car, list(skins.keys())[car_skin])
                if skins[list(skins.keys())[car_skin]][0] == 'open':
                    main_skin = car_skin

                skin_info_msg = f'{skins[list(skins.keys())[car_skin]][0].capitalize()}. Price: {skins[list(skins.keys())[car_skin]][1]}'
                skin_info.set_text(skin_info_msg)
                skin_info.dest = (
                    (size[0] - skin_info.render.get_width()) // 2, 350)
            if settings_button.update(event) or event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                await settings()
            if road_button.update(event) or event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                await road_menu()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F3:
                    settings_file['render_hints'] = int(
                        not bool(settings_file['render_hints']))

        screen.fill(pygame.Color('black'))

        sprites.draw(screen)
        overlay_group.draw(screen)
        player.draw(screen)
        menu_sprites.draw(screen)

        if skins[list(skins.keys())[car_skin]][0] == 'locked':
            skin_info.update()
            lock_button_group.draw(screen)
            render_hint('[E]', lock_button.rect)

        score_label.update()

        render_hint('[Space]', play_button.rect, settings_file['render_hints'])
        render_hint('[Left arrow]', arrow_left.rect,
                    settings_file['render_hints'])
        render_hint('[Right arrow]', arrow_right.rect,
                    settings_file['render_hints'])
        render_hint('[S]', settings_button.rect, settings_file['render_hints'])
        render_hint('[R]', road_button.rect,
                    settings_file['render_hints'])

        road.update(dt)
        screen.blit(load_image('line'), (-10, 0))

        label.update()
        coins_count.update()

        clock.tick(fps)
        pygame.display.flip()
        await asyncio.sleep(0)


async def settings():
    global car_skin
    global main_road_skin
    global current_song
    global last_time
    global dt

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

    information_button = Button(load_image('buttons/information'),
                         load_image('buttons/information_hl'), (396, 560),
                         menu_sprites)

    while True:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()

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
                await main_menu()

            if information_button.update(event):
                secret_sfx = pygame.mixer.Sound('assets/sfx/Secret.mp3')
                secret_sfx.set_volume(0.2)
                secret_sfx.play()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    await main_menu()
                if event.key == pygame.K_F3:
                    settings_file['render_hints'] = int(
                        not bool(settings_file['render_hints']))

        screen.fill(pygame.Color('black'))

        sprites.draw(screen)
        player.draw(screen)
        overlay_group.draw(screen)
        menu_sprites.draw(screen)

        road.update(dt)

        render_hint('[Esc]', back_button.rect, settings_file['render_hints'])
        render_hint('[F3]', information_button.rect, True)

        screen.blit(load_image('line'), (-10, 0))

        label.update()
        song_section.update()
        song_name.update(hidden_message=music[current_song])

        clock.tick(fps)
        pygame.display.flip()
        await asyncio.sleep(0)


async def road_menu():
    global car_skin
    global main_road_skin
    global road_skin
    global last_time
    global dt

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
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close(current_song, coins_count.coins_count, main_skin,
                      main_road_skin, skins, road_skins)
            if road_skins[list(road_skins.keys())[road_skin]][0] == 'locked':
                if lock_button.update(
                        event) or event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    if coins_count.coins_count - \
                            road_skins[list(road_skins.keys())[road_skin]][
                                1] >= 0:
                        road_skins[list(road_skins.keys())[road_skin]][
                            0] = 'open'
                        main_road_skin = road_skin
                        coins_count.coins_count = coins_count.coins_count - \
                                                  road_skins[
                                                      list(road_skins.keys())[
                                                          road_skin]][1]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    await main_menu()
                if event.key == pygame.K_F3:
                    settings_file['render_hints'] = int(
                        not bool(settings_file['render_hints']))

            if arrow_left.update(
                    event) or event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if road_skin - 1 < 0:
                    road_skin = len(road_skins) - 1
                else:
                    road_skin -= 1
                change_road(road, list(road_skins.keys())[road_skin])

                if road_skins[list(road_skins.keys())[road_skin]][0] == 'open':
                    main_road_skin = road_skin

                skin_info_msg = f'{road_skins[list(road_skins.keys())[road_skin]][0].capitalize()}. Price: {road_skins[list(road_skins.keys())[road_skin]][1]}'
                skin_info.set_text(skin_info_msg)
                skin_info.dest = (
                    (size[0] - skin_info.render.get_width()) // 2, 350)

            if arrow_right.update(
                    event) or event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if road_skin + 1 > len(road_skins) - 1:
                    road_skin = 0
                else:
                    road_skin += 1
                change_road(road, list(road_skins.keys())[road_skin])

                if road_skins[list(road_skins.keys())[road_skin]][0] == 'open':
                    main_road_skin = road_skin

                skin_info_msg = f'{road_skins[list(road_skins.keys())[road_skin]][0].capitalize()}. Price: {road_skins[list(road_skins.keys())[road_skin]][1]}'
                skin_info.set_text(skin_info_msg)
                skin_info.dest = (
                    (size[0] - skin_info.render.get_width()) // 2, 350)

            if back_button.update(event):
                await main_menu()

        screen.fill(pygame.Color('black'))

        sprites.draw(screen)
        player.draw(screen)
        menu_sprites.draw(screen)

        road.update(dt)

        render_hint('[Esc]', back_button.rect, settings_file['render_hints'])
        render_hint('[Left arrow]', arrow_left.rect,
                    settings_file['render_hints'])
        render_hint('[Right arrow]', arrow_right.rect,
                    settings_file['render_hints'])

        screen.blit(load_image('line'), (-10, 0))

        label.update()
        coins_count.update()

        if road_skins[list(road_skins.keys())[road_skin]][0] == 'locked':
            skin_info.update()
            lock_button_group.draw(screen)
            render_hint('[E]', lock_button.rect,
                        settings_file['render_hints'])

        clock.tick(fps)
        pygame.display.flip()
        await asyncio.sleep(0)


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    screen, size, screen_rect = set_screen((480, 640))

    # user_home = os.path.expanduser("~")
    # save_dir = os.path.join(user_home, 'CasualRide')
    # if not os.path.exists(save_dir):
    #     os.makedirs(save_dir)
    #
    # saving_file_path = os.path.join(save_dir, 'saving.json')
    # settings_file_path = os.path.join(save_dir, 'settings_file.json')
    #
    # try:
    #     with open(saving_file_path) as f:
    #         saving = json.load(f)
    # except:
    #     print('No saving file created yet')
    # try:
    #     with open(settings_file_path) as f:
    #         settings_file = json.load(f)
    # except:
    #     print('No settings file created yet')

    car_skin = saving['car_skin']
    main_skin = car_skin
    road_skin = saving['road_skin']
    main_road_skin = road_skin
    skins = saving['car_skins']
    road_skins = saving['road_skins']

    coins_count = CoinsCount(screen, size, 30, '#f7e26b')
    coins_count.coins_count = saving['coins']
    current_song = settings_file['song']

    set_music(music[current_song])

    asyncio.run(main_menu())
    close(current_song, coins_count.coins_count, main_skin,
          main_road_skin, skins, road_skins)
