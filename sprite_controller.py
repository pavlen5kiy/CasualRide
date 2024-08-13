import random

import pygame

from utility import load_image


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

    def update(self):
        if self.rect.y >= -10:
            self.rect.y = -970
            self.score += 1

        self.speed = int((self.default_speed + self.score // 10) - 3 * (
                    self.score // 50) - 2 * (self.score // 100) + self.speed_change)
        self.non_changed_speed = self.speed - self.speed_change
        self.rect.y += self.speed
        # print(self.speed, self.speed_change)


class Car(Sprite):
    def __init__(self, image, road, npc_group, *group):
        super().__init__(*group)
        self.default_image = image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (360 - 30, 450 - 52)
        self.x_movement = 0
        self.x_speed = 5
        self.y_movement = 0
        self.y_speed = 2
        self.hitbox = pygame.Rect(0, 0, 44, 83)
        self.hitbox.topleft = (self.rect.x + self.rect.width // 2 - 22, self.rect.y + 12)
        self.npc_group = npc_group
        self.road = road

    def update(self, particles_group):

        if 30 <= self.rect.x + self.x_speed * self.x_movement <= 390:
            self.rect.x += self.x_speed * self.x_movement
            self.hitbox.x += self.x_speed * self.x_movement

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
            if self.hitbox.colliderect(npc.hitbox):
                return True
            pass

        create_particles((self.rect.x + self.rect.width // 2 - 6, self.rect.y + 90),
                         generate_particles('particle'),
                         1, self.road.speed,
                         particles_group)


class NpcCar(Sprite):
    def __init__(self, image, direction, position, speed, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (position[0] + 1, position[1] + 1)
        self.direction = direction
        self.rect.topleft = position
        self.speed = speed
        self.hitbox = pygame.Rect(0, 0, 44, 83)
        self.hitbox.topleft = (self.rect.x + self.rect.width // 2 - 22, self.rect.y + 12)
        self.speed_change = 0
        self.alt_speed = 0

    def update(self):
        self.rect.y += self.speed + self.speed_change
        self.hitbox.y += self.speed + self.speed_change
        if self.rect.y > 641 or self.rect.y < -400:
            self.kill()


class Particle(Sprite):
    def __init__(self, pos, dx, dy, particles, speed, *group):
        super().__init__(*group)
        self.particles = particles
        self.image = random.choice(self.particles)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.tick = 0
        self.max_tick = random.randrange(1, (speed // 2 + 1) * 10)

    def update(self, screen_rect):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        self.tick += 1

        if self.tick == self.max_tick:
            self.kill()


# Particles functions
def create_particles(position, particles, particle_count, speed, *group):
    for _ in range(particle_count):
        Particle(position, random.randint(0, 20) / 10 - 1, random.randrange(1, 4),
                 particles, speed, *group)


def generate_particles(filename):
    particles = [load_image(filename)]
    for scale in range(1, 20):
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

    def update(self):
        self.rect.y += self.road.speed
        if self.rect.colliderect(self.car.rect):
            self.coins_count.coins_count += 1
            self.kill()
