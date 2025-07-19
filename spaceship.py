import pygame
from pygame.surface import Surface
from pygame.key import ScancodeWrapper


class Bullet:
    def __init__(self, velocity, x, y, screen: Surface):
        self.texture = pygame.image.load("images/blaster/buuuleeet.png").convert_alpha()
        self.texture_rect = self.texture.get_rect()

        self.texture_rect.center = (x, y - self.texture_rect.height // 2)


class Spaceship:
    def __init__(self, velocity, screen: Surface):
        self.texture = pygame.image.load("images/spaceship_200.png").convert_alpha()
        self.texture_rect = self.texture.get_rect()

        self.screen = screen
        screen_width, screen_height = screen.get_size()

        self.texture_rect.center = (screen_width // 2, screen_height - self.texture_rect.height // 2 - 20)

        self.velocity = velocity

        self.bullet = Bullet(25, self.texture_rect.center[0], self.texture_rect.top, self.screen)

    def move(self, keys: ScancodeWrapper):
        if keys[pygame.K_LEFT]:
            if self.texture_rect.left > 0:
                self.texture_rect.move_ip(-self.velocity, 0)

                self.bullet.texture_rect.move_ip(0, -self.velocity)

        if keys[pygame.K_RIGHT]:
            screen_width, _ = self.screen.get_size()
            if self.texture_rect.right < screen_width:
                self.texture_rect.move_ip(+self.velocity, 0)

                self.bullet.texture_rect.move_ip(0, -self.velocity)

    def draw(self):
        # Отображение текстуры
        self.screen.blit(self.texture, self.texture_rect)
        self.screen.blit(self.bullet.texture, self.bullet.texture_rect)
