from abc import ABC, abstractmethod
import pygame
from pygame.surface import Surface
from pygame.key import ScancodeWrapper
from typing import Type, Callable


class BulletRegistry:

    __instance: 'BulletRegistry' = None

    bullets: list = list()

    def __new__(cls, *args, **kwargs):

        if not BulletRegistry.__instance:
            BulletRegistry.__instance = super().__new__(cls)

        return BulletRegistry.__instance

    @classmethod
    def register(cls, bullet: 'Bullet'):
        cls.bullets.append(bullet)


class Bullet(ABC):
    TEXTURE_FILENAME = None

    def __init__(self, velocity, x, y, screen: Surface):
        self.texture = pygame.image.load(self.TEXTURE_FILENAME).convert_alpha()
        self.texture_rect = self.texture.get_rect()

        self.texture_rect.center = (x, y - self.texture_rect.height // 2)

        self.screen = screen
        self.velocity = velocity

        BulletRegistry.register(self)

    def move(self):
        if self.texture_rect.bottom > 0:
            self.texture_rect.move_ip(0, -self.velocity)
        else:
            BulletRegistry.bullets.remove(self)

    def draw(self):
        self.screen.blit(self.texture, self.texture_rect)


class Bullet1(Bullet):
    TEXTURE_FILENAME = "images/blaster/blaster_1_85.png"


class Bullet2(Bullet):
    TEXTURE_FILENAME = "images/blaster/blaster_2_85.png"


WIDTH = 1200   # ширина игрового окна
HEIGHT = 1000  # высота игрового окна
FPS = 30  # частота кадров в секунду

if __name__ == '__main__':
    registry = BulletRegistry()

    pygame.init()
    pygame.mixer.init()  # для звука
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    bullet1 = Bullet1(10, 100, 100, screen)
    bullet2 = Bullet1(10, 100, 100, screen)

    print(registry.bullets)
