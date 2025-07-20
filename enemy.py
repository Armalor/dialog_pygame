from abc import ABC, abstractmethod
import pygame
from pygame.surface import Surface
from pygame.key import ScancodeWrapper
from typing import Type, Callable
import random
from time import perf_counter


class Enemyregister:
    __instance: 'EnemyRegistry' = None
    enemies: list = list()

    def __new__(cls, *args, **kwargs):

        if not Enemyregister.__instance:
            Enemyregister.__instance = super().__new__(cls)

        return Enemyregister.__instance
    @classmethod
    def register(cls, enemy: 'Enemy'):
        cls.enemies.append(enemy)


class Enemy(ABC):
    TEXTURE_FILENAME = None

    def __init__(self, x, y, velocity, screen: Surface):
        self.texture = pygame.image.load(self.TEXTURE_FILENAME).convert_alpha()
        self.texture_rect = self.texture.get_rect()

        self.screen = screen
        screen_width, screen_height = screen.get_size()

        self.texture_rect.center = (x, y - self.texture_rect.height // 2)

        self.velocity = velocity

        self.cooldown = 0.5
        self.last_enemy = perf_counter()
        Enemyregister.register(self)
        #_ = Enemy1(25, self.texture_rect.center[0], self.texture_rect.top, self.screen)

    def spawn(self):
        if perf_counter() - self.last_enemy > self.cooldown:
            self.last_enemy = perf_counter()
            _ = Enemy1(25, self.texture_rect.center[0], self.texture_rect.top, self.screen)
    def move(self):
        if self.texture_rect.top < HEIGHT:
            self.texture_rect.move_ip(0, self.velocity)
        else:
            Enemyregister.enemies.remove(self)
    def draw(self):
        self.screen.blit(self.texture, self.texture_rect)


class Enemy1(Enemy):
    TEXTURE_FILENAME = "images/spaceship2_200_down.png"


WIDTH = 1200   # ширина игрового окна
HEIGHT = 700  # высота игрового окна
FPS = 30


if __name__ == '__main__':
    registry = Enemyregister()

    pygame.init()
    pygame.mixer.init()  # для звука
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    bullet1 = Enemy1(10, 100, 100, screen)
    bullet2 = Enemy1(10, 100, 100, screen)

    print(registry.enemies)