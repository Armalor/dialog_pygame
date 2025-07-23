from abc import ABC
import pygame
from pygame.surface import Surface

bullets = []


class Bullet(ABC):
    TEXTURE_FILENAME = None

    def __init__(self, velocity, x, y, screen: Surface):
        self.texture = pygame.image.load(self.TEXTURE_FILENAME).convert_alpha()
        self.texture_rect = self.texture.get_rect()

        self.texture_rect.center = (x, y - self.texture_rect.height // 2)

        self.screen = screen
        self.velocity = velocity

        bullets.append(self)

    def move(self):
        if self.texture_rect.bottom > 0:
            self.texture_rect.move_ip(0, -self.velocity)
        else:
            bullets.remove(self)

    def draw(self):
        self.screen.blit(self.texture, self.texture_rect)


class Bullet1(Bullet):
    TEXTURE_FILENAME = "images/blaster/blaster_1_85.png"


class Bullet2(Bullet):
    TEXTURE_FILENAME = "images/blaster/blaster_2_75.png"


class Bullet3(Bullet):
    TEXTURE_FILENAME = "images/blaster/blaster_3_75.png"
