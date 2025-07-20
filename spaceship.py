import pygame
from pygame.surface import Surface
from pygame.key import ScancodeWrapper

bullets = []
enemies = []

class Bullet:
    def __init__(self, velocity, x, y, screen: Surface):
        self.texture = pygame.image.load("images/blaster/blaster_1_85.png").convert_alpha()
        self.texture_rect = self.texture.get_rect()
        self.texture_rect.center = (x, y - self.texture_rect.height // 2)
        self.screen = screen
        self.velocity = velocity

        bullets.append(self)

    def draw(self):
        self.screen.blit(self.texture, self.texture_rect)

    def move(self):
        if self.texture_rect.bottom > 0:
            self.texture_rect.move_ip(0, self.velocity)
        else:
            bullets.remove(self)

class Spaceship:
    def __init__(self, velocity, screen: Surface):
        self.texture = pygame.image.load("images/spaceship3_200.png").convert_alpha()
        self.texture_rect = self.texture.get_rect()
        self.screen = screen
        screen_width, screen_height = screen.get_size()

        self.texture_rect.center = (screen_width // 2, screen_height - self.texture_rect.height // 2 - 20)
        self.velocity = velocity

    def move(self, keys: ScancodeWrapper):
        if keys[pygame.K_LEFT]:
            if self.texture_rect.left > 0:
                self.texture_rect.move_ip(-self.velocity, 0)

        if keys[pygame.K_RIGHT]:
            screen_width, _ = self.screen.get_size()
            if self.texture_rect.right < screen_width:
                self.texture_rect.move_ip(+self.velocity, 0)

    def draw(self):
        self.screen.blit(self.texture, self.texture_rect)


class Enemy:
    def __init__(self, velocity, x, y, screen: Surface):
        self.texture = pygame.image.load("images/prisheleccc.png").convert_alpha()
        self.texture_rect = self.texture.get_rect()
        self.texture_rect.center = (0, 100)
        self.screen = screen
        self.velocity = velocity

        enemies.append(self)

    def draw(self):
        self.screen.blit(self.texture, self.texture_rect)

    def move(self):
        if self.texture_rect.bottom > 0:
            self.texture_rect.move_ip(0, self.velocity)
        else:
            enemies.remove(self)
