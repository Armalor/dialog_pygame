import pygame
from pygame.surface import Surface
from pygame.key import ScancodeWrapper
from time import perf_counter

from bullet import Bullet1, Bullet2, Bullet3


class Spaceship:

    TEXTURE = "images/spaceship3_200.png"
    BULLET = Bullet3

    L = pygame.K_LEFT
    R = pygame.K_RIGHT
    S = pygame.K_SPACE

    DELTA_X = -200
    DELTA_Y = 20

    def __init__(self, velocity, screen: Surface):
        self.texture = pygame.image.load(self.TEXTURE).convert_alpha()
        self.texture_rect = self.texture.get_rect()

        w, h, = self.texture_rect.size

        # Уменьшаем размер кораблика вдвое
        self.texture = pygame.transform.scale(self.texture, (w // 2, h // 2))
        # Пересохраняем texture_rect, иначе останутся старые размеры:
        self.texture_rect = self.texture.get_rect()

        self.screen = screen
        screen_width, screen_height = screen.get_size()

        self.texture_rect.center = (screen_width // 2 - self.DELTA_X, screen_height - self.texture_rect.height // 2 - self.DELTA_Y)

        self.velocity = velocity

        self.cooldown = 0.1
        self.last_shoot = perf_counter()

        # self.bullet = Bullet1(25, self.texture_rect.center[0], self.texture_rect.top, self.screen)

    def move(self, keys: set):
        if self.L in keys:
            if self.texture_rect.left > 0:
                self.texture_rect.move_ip(-self.velocity, 0)
                #
                # self.bullet.texture_rect.move_ip(0, -self.velocity)

        if self.R in keys:
            screen_width, _ = self.screen.get_size()
            if self.texture_rect.right < screen_width:
                self.texture_rect.move_ip(+self.velocity, 0)
                #
                # self.bullet.texture_rect.move_ip(0, -self.velocity)

        if self.S in keys:
            if perf_counter() - self.last_shoot > self.cooldown:
                self.last_shoot = perf_counter()
                _ = self.BULLET(25, self.texture_rect.center[0], self.texture_rect.top, self.screen)

    def draw(self):
        # Отображение текстуры
        self.screen.blit(self.texture, self.texture_rect)


class Spaceship2(Spaceship):

    TEXTURE = "images/spaceship2_200.png"
    BULLET = Bullet2

    L = pygame.K_a
    R = pygame.K_d
    S = pygame.K_s

    DELTA_X = 200
    DELTA_Y = 20
