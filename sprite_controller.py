import random

import pygame

from load_image import load_image


class Sprite(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)


class Road(Sprite):
    def __init__(self, image, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.y = -970
        self.score = 0
        self.speed = 5
        self.default_speed = 5
        self.speed_change = 0
        self.non_changed_speed = 5

    def update(self, dt):
        if self.rect.y >= -10:
            self.rect.y = -970
            self.score += 1

        self.non_changed_speed = int(
            (self.default_speed + self.score // 10) - 3 * (
                    self.score // 50) - 2 * (self.score // 100))
        self.speed = self.non_changed_speed + self.speed_change
        self.rect.y += self.speed * dt


class Car(Sprite):
    def __init__(self, image, road, npc_group, *group):
        super().__init__(*group)
        self.default_image = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (240 - self.rect.width // 2, 450 - self.rect.height // 2)
        self.x_movement = 0
        self.x_speed = 5
        self.y_movement = 0
        self.y_speed = 2
        self.hitbox = pygame.Rect(0, 0, 44, 83)
        self.hitbox.topleft = (
        self.rect.x + self.rect.width // 2 - 22, self.rect.y + 12)
        self.npc_group = npc_group
        self.road = road
        self.tick = 120

    def update(self, particles_group, dt, hit_particles_group=None):

        if 30 <= self.rect.x + self.x_speed * self.x_movement <= 390:
            self.rect.x += (self.x_speed * self.x_movement) * dt
            self.hitbox.x += (self.x_speed * self.x_movement) * dt

        speed_change = self.y_speed * -self.y_movement

        if self.y_movement == -1:
            self.x_speed = 2
            self.road.speed_change = speed_change * 2
            for npc in self.npc_group:
                npc.speed_change = speed_change * 2

        elif self.y_movement == 1:
            self.x_speed = 4
            self.road.speed_change = speed_change
            for npc in self.npc_group:
                npc.speed_change = speed_change
        else:
            self.road.speed_change = 0
            self.x_speed = 5
            for npc in self.npc_group:
                npc.speed_change = 0

        if self.x_movement == -1:
            self.image = pygame.transform.rotate(self.default_image, 9)
        elif self.x_movement == 1:
            self.image = pygame.transform.rotate(self.default_image, -9)
        else:
            self.image = self.default_image

        for npc in self.npc_group:
            if self.hitbox.colliderect(npc.hitbox) and self.tick == 120:
                sfx = pygame.mixer.Sound('assets/sfx/Crash.wav')
                sfx.set_volume(0.5)
                sfx.play()

                create_particles(
                    (self.rect.x + self.rect.width // 2 - 6, self.rect.y),
                    generate_particles('hit_particle'), 50, 30, 2, hit_particles_group)

                self.tick = 0
                return True
            pass

        if self.tick < 120:
            self.tick += 1

        create_particles(
            (self.rect.x + self.rect.width // 2 - 6, self.rect.y + 90),
            generate_particles('particle'),
            1, self.road.speed, 1,
            particles_group)


class NpcCar(Sprite):
    def __init__(self, image, direction, position, speed, road, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (position[0] + 1, position[1] + 1)
        self.direction = direction
        self.rect.topleft = position
        self.speed = speed
        self.hitbox = pygame.Rect(0, 0, 44, 83)
        self.hitbox.topleft = (
        self.rect.x + self.rect.width // 2 - 22, self.rect.y + 12)
        self.speed_change = 0
        self.road = road

    def update(self, particles_group, dt):
        self.rect.y += (self.speed + self.speed_change) * dt
        self.hitbox.y += (self.speed + self.speed_change) * dt
        if self.rect.y > 641 or self.rect.y < -400:
            self.kill()

        if self.direction == -1:
            direction_modifier = 1
            particle_speed = abs(self.road.non_changed_speed - self.speed) * 2
            if self.speed_change > 0:
                direction_modifier = 2
            particle_y = self.rect.y + 90
        else:
            direction_modifier = 0
            particle_speed = abs(self.speed // 4)
            particle_y = self.rect.y

        create_particles(
            (self.rect.x + self.rect.width // 2 - 6, particle_y),
            generate_particles('particle'),
            1, particle_speed, 1 + direction_modifier,
            particles_group)


class Particle(Sprite):
    def __init__(self, pos, dx, dy, particles, speed, *group):
        super().__init__(*group)
        self.particles = particles
        self.image = random.choice(self.particles)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.tick = 0
        self.max_tick = random.randrange(1, (speed // 2 + 1) * 5)

    def update(self, screen_rect, dt):
        self.rect.x += self.velocity[0] * dt
        self.rect.y += self.velocity[1] * dt

        self.tick += 1

        if self.tick == self.max_tick:
            self.kill()


# Particles functions
def create_particles(position, particles, particle_count, speed, direction,
                     *group):
    for _ in range(particle_count):
        Particle(position, random.randint(-10, 10) / 10,
                 direction * random.randrange(1, 4),
                 particles, speed, *group)


def generate_particles(filename):
    particles = [load_image(filename)]
    for scale in [1, 5, 10, 15, 20]:
        particles.append(pygame.transform.scale(particles[0], (scale, scale)))
    return particles


class Coin(Sprite):
    def __init__(self, pos, car, road, coins_count, *group):
        super().__init__(*group)
        self.image = load_image('coin')
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.car = car
        self.coins_count = coins_count
        self.road = road

    def update(self, dt):
        self.rect.y += self.road.speed * dt
        if self.rect.colliderect(self.car.rect):
            self.coins_count.coins_count += 1
            sfx = pygame.mixer.Sound('assets/sfx/CoinPickup.mp3')
            sfx.set_volume(0.5)
            sfx.play()
            self.kill()
        if self.rect.y > 750:
            self.kill()


class UiSprite(Sprite):
    def __init__(self, image, pos, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class Button(Sprite):
    def __init__(self, image, highlight, pos=(0, 0), *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.orig = image
        self.highlight = highlight
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, *args):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.x <= mouse_pos[
            0] <= self.rect.x + self.orig.get_width() and self.rect.y <= \
                mouse_pos[1] <= self.rect.y + self.orig.get_height():
            self.image = self.highlight
        else:
            self.image = self.orig

        if (args and args[0].type == pygame.MOUSEBUTTONDOWN and
                self.rect.collidepoint(args[0].pos)):
            sfx = pygame.mixer.Sound('assets/sfx/ButtonClick2.wav')
            sfx.set_volume(0.7)
            sfx.play()
            return True

        return False


class Spanner(Sprite):
    def __init__(self, pos, car, road, health, *group):
        super().__init__(*group)
        self.image = load_image('spanner_big')
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.car = car
        self.health = health
        self.road = road

    def update(self, dt):
        self.rect.y += self.road.speed * dt
        if self.rect.colliderect(self.car.rect):
            if self.health.health < 3:
                self.health.health += 1
            sfx = pygame.mixer.Sound('assets/sfx/SpannerPickup.wav')
            sfx.set_volume(0.5)
            sfx.play()
            self.kill()
        if self.rect.y > 750:
            self.kill()
