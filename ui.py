import pygame


class Ui:
    def __init__(self, screen, screen_size):
        self.screen = screen
        self.width = screen_size[0]
        self.height = screen_size[1]


class Timer(Ui):
    def __init__(self, seconds, screen, screen_size):
        super().__init__(screen, screen_size)
        self.font = pygame.font.Font('assets/PixelOperator8-Bold.ttf', 200)
        self.seconds = seconds
        self.tick = 0

    def render(self):
        output = self.font.render(str(self.seconds), True, 'black')

        self.screen.blit(output, (self.width // 2 - output.get_width() // 2, self.height // 2 - output.get_height() // 2))

    def update(self):
        if self.seconds > 0:
            if self.tick > 0:
                self.tick -= 1
            if self.tick == 0:
                self.tick = 30
                self.seconds -= 1


class Start_label(Timer):
    def __init__(self, seconds, screen, screen_size):
        super().__init__(seconds, screen, screen_size)
        self.font = pygame.font.Font('assets/PixelOperator8-Bold.ttf', 60)

    def render(self):
        output = self.font.render('Get Up!', True, 'black')

        for i in range(5 - self.seconds):
            self.screen.blit(output, (self.width // 2 - output.get_width() // 2, self.height // 2 - output.get_height() // 2 + 70 * i - 100))

