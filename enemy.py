from abc import ABC, abstractmethod
import pygame
from pygame.surface import Surface
from pygame.key import ScancodeWrapper
from typing import Type, Callable
import random
class Enemyregister:
    __instance: 'EnemyRegistry' = None
    enemies: list = list()

    def __new__(cls, *args, **kwargs):

        if not Enemyregister.__instance:
            Enemyregister.__instance = super().__new__(cls)

        return Enemyregister.__instance

class Enemy(ABC):
    def __init__(self, velocity, screen: Surface):
        self.texture = pygame.image.load("images/spaceship2_200_down.png").convert_alpha()
        self.texture_rect = self.texture.get_rect()

        self.screen = screen
        screen_width, screen_height = screen.get_size()

        self.texture_rect.center = (screen_width // 2, screen_height - self.texture_rect.height // 2 - 20)

        self.velocity = velocity

        self.cooldown = 0.3