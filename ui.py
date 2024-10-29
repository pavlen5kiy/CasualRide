import pygame

from load_image import load_image


class Ui:
    def __init__(self, screen, screen_size):
        self.screen = screen
        self.width = screen_size[0]
        self.height = screen_size[1]


class Text(Ui):
    def __init__(self, screen, screen_size, font_size, message, color,
                 dest=(0, 0)):
        super().__init__(screen, screen_size)
        self.font = pygame.font.Font('assets/fonts/PixelOperator8-Bold.ttf',
                                     font_size)
        self.message = message
        self.dest = dest
        self.color = pygame.Color(color)
        self.render = self.font.render(self.message, True, self.color)

    def update(self):
        self.screen.blit(self.render, self.dest)

    def set_text(self, message):
        self.message = message
        self.render = self.font.render(self.message, True, self.color)


class ScoreLabel(Text):
    def __init__(self, screen, screen_size, font_size, message, road, color,
                 dest=(0, 0)):
        super().__init__(screen, screen_size, font_size, message, color,
                         dest)
        self.road = road
        self.screen_size = screen_size

    def update(self, dynamic_update=False):
        message = ''.join((self.message, str(self.road.score)))
        self.render = self.font.render(message, True, self.color)
        if dynamic_update:
            self.dest = (
                (self.screen_size[0] // 2 - self.render.get_width() // 2), 12)
        self.screen.blit(self.render, self.dest)


class Timer(Ui):
    def __init__(self, seconds, screen, screen_size):
        super().__init__(screen, screen_size)
        self.font = pygame.font.Font('assets/fonts/PixelOperator8-Bold.ttf',
                                     200)
        self.seconds = seconds
        self.tick = 0

    def render(self):
        output = self.font.render(str(self.seconds), True, 'white')

        self.screen.blit(output, (self.width // 2 - output.get_width() // 2,
                                  self.height // 2 - output.get_height() // 2))

    def update(self):
        if self.seconds > 0:
            if self.tick > 0:
                self.tick -= 1
            if self.tick == 0:
                self.tick = 60
                self.seconds -= 1
            # if self.tick == 60 and self.seconds == 0:
            #     sfx = pygame.mixer.Sound('assets/sfx/Horn.mp3')
            #     sfx.set_volume(0.5)
            #     sfx.play()


class Startlabel(Timer):
    def __init__(self, seconds, screen, screen_size):
        super().__init__(seconds, screen, screen_size)
        self.font = pygame.font.Font('assets/fonts/PixelOperator8-Bold.ttf',
                                     60)

    def render(self):
        output = self.font.render('Get Up!', True, 'black')

        for i in range(5 - self.seconds):
            self.screen.blit(output, (
                self.width // 2 - output.get_width() // 2,
                self.height // 2 - output.get_height() // 2 + 70 * i - 100))


class CoinsCount(Text):
    def __init__(self, screen, screen_size, font_size, color, dest=(0, 0)):
        self.coins_count = 0
        super().__init__(screen, screen_size, font_size, str(self.coins_count),
                         color, dest)

    def update(self):
        self.render = self.font.render(str(self.coins_count), True, self.color)
        self.dest = (self.width - self.render.get_width() - 60, 20)
        coin_image = load_image('coin_small')
        self.screen.blit(self.render, self.dest)
        self.screen.blit(coin_image, (430, 10))


class HiddenText(Text):
    def __init__(self, screen, screen_size, font_size, message,
                 color,
                 dest=(0, 0)):
        super().__init__(screen, screen_size, font_size, message, color,
                         dest)
        self.hidden_msg_font = pygame.font.Font('assets/fonts/PixelOperator8-Bold.ttf',
                                     15)

    def update(self, hidden_message=''):
        self.screen.blit(self.render, self.dest)
        if pygame.Rect(*self.dest, self.render.get_width(), self.render.get_height()).collidepoint(pygame.mouse.get_pos()):
            hidden_msg_render = self.hidden_msg_font.render(hidden_message, True,
                                                 self.color)
            pygame.draw.rect(self.screen, pygame.Color('black'),
                             pygame.Rect(pygame.mouse.get_pos()[0] + 14 - 70, pygame.mouse.get_pos()[1] + 14,
                                         hidden_msg_render.get_width() + 8,
                                         hidden_msg_render.get_height() + 8))
            self.screen.blit(hidden_msg_render, (pygame.mouse.get_pos()[0] + 14 + 4 - 70 , pygame.mouse.get_pos()[1] + 14 + 4))


class Health(Ui):
    def __init__(self, screen, screen_size, dest):
        super().__init__(screen, screen_size)
        self.health = 3
        self.full = load_image('spanner')
        self.empty = load_image('spanner_empty')
        self.dest = dest

    def update(self):
        for i in range(3):
            if i > self.health - 1:
                self.screen.blit(self.empty,
                                 (self.dest[0] + 50 * i, self.dest[1]))
            else:
                self.screen.blit(self.full, (self.dest[0] + 50 * i, self.dest[1]))
