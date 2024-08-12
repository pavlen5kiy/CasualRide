import pygame
from load_image import load_image

import random


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

    def update(self):
        if self.rect.y >= -10:
            self.rect.y = -970
            self.score += 1
            self.speed = self.default_speed + self.score // 10

        self.rect.y += self.speed


class Car(Sprite):
    def __init__(self, image, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (360 - 30, 450 - 52)
        self.x_movement = 0
        self.x_speed = 5
        self.y_movement = 0
        self.y_speed = 2
        self.hitbox = pygame.Rect(0, 0, 48, 87)
        self.hitbox.topleft = (360 - 30 + 6, 450 - 52 + 10)

    def update(self, npc_group, particles_group):

        if 0 <= self.rect.x + self.x_speed * self.x_movement <= 420:
            self.rect.x += self.x_speed * self.x_movement
            self.hitbox.x += self.x_speed * self.x_movement

        if self.y_movement == -1:
            if 0 <= self.rect.y + self.y_speed * 2 * self.y_movement <= 580:
                self.rect.y += self.y_speed * 2 * self.y_movement
                self.hitbox.y += self.y_speed * 2 * self.y_movement
        else:
            if 0 <= self.rect.y + self.y_speed * self.y_movement <= 536:
                self.rect.y += self.y_speed * self.y_movement
                self.hitbox.y += self.y_speed * self.y_movement

        if self.x_movement == -1:
            self.image = load_image('car_left')
        elif self.x_movement == 1:
            self.image = load_image('car_right')
        else:
            self.image = load_image('car')

        for npc in npc_group:
            if self.rect.colliderect(npc.hitbox):
                return True

        create_particles(self.rect.center,
                         generate_particles('particle'),
                         1,
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
        self.hitbox = pygame.Rect(0, 0, 48, 87)
        self.hitbox.topleft = (
        position[0] + (self.rect.width - 48) // 2, position[1] + 10)

    def update(self):
        self.rect.y += self.speed
        self.hitbox.y += self.speed
        if self.rect.y > 641:
            self.kill()


class Particle(Sprite):
    def __init__(self, pos, dx, dy, particles, *group):
        super().__init__(*group)
        self.particles = particles
        self.image = random.choice(self.particles)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = 0.1

    def update(self, screen_rect):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


# Particles functions
def create_particles(position, particles, particle_count, *group):
    for _ in range(particle_count):
        Particle(position, 0, 0.1,
                 particles, *group)


def generate_particles(filename):
    particles = [load_image(filename)]
    for scale in (5, 10, 15):
        particles.append(pygame.transform.scale(particles[0], (scale, scale)))
    return particles
