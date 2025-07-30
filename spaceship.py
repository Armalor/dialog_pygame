import pygame
from pygame.surface import Surface



from utils import get_pure_path


class Bullet:
    def __init__(self, velocity, x, y, screen: Surface):
        self.texture = pygame.image.load(get_pure_path("images/blaster/buuuleeet.png")).convert_alpha()
        self.texture_rect = self.texture.get_rect()
        self.texture_rect.center = (x, y - self.texture_rect.height // 2)
        self.screen = screen
        self.velocity = velocity

    def draw(self):
        self.screen.blit(self.texture, self.texture_rect)

    def move(self):
        self.texture_rect.move_ip(0, self.velocity)

class Spaceship:
    def __init__(self, velocity, screen: Surface):
        self.texture = pygame.image.load(get_pure_path("images/spaceship_200.png")).convert_alpha()
        self.texture_rect = self.texture.get_rect()
        self.screen = screen
        screen_width, screen_height = screen.get_size()

        self.texture_rect.center = (screen_width // 2, screen_height - self.texture_rect.height // 2 - 20)
        self.velocity = velocity

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            if self.texture_rect.left > 0:
                self.texture_rect.move_ip(-self.velocity, 0)

        if keys[pygame.K_RIGHT]:
            screen_width, _ = self.screen.get_size()
            if self.texture_rect.right < screen_width:
                self.texture_rect.move_ip(+self.velocity, 0)

    def draw(self):
        self.screen.blit(self.texture, self.texture_rect)