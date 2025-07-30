import pygame
import random
from pygame.surface import Surface

from utils import get_pure_path


class Enemy:
    def __init__(self, x, y, screen: Surface):
        # Загружаем оригинальную текстуру
        original_texture = pygame.image.load(get_pure_path("images/monster/prisheleccc.png")).convert_alpha()
        
        # Базовый размер (уменьшенный в 5 раз от оригинала)
        base_width = original_texture.get_width() // 5
        base_height = original_texture.get_height() // 5
        
        # Добавляем случайное отклонение в размере (±20% от базового)
        size_variation = random.uniform(0.8, 1.2)  # От 80% до 120% от базового размера
        new_width = int(base_width * size_variation)
        new_height = int(base_height * size_variation)
        
        # Масштабируем текстуру
        self.texture = pygame.transform.scale(original_texture, (new_width, new_height))
        
        # Настройка прямоугольника для коллизий
        self.texture_rect = self.texture.get_rect()
        self.texture_rect.center = (x, y)
        
        self.screen = screen
        # Скорость может немного зависеть от размера (меньшие - быстрее)
        self.velocity = random.uniform(3.0, 10.0) * (1.1 - size_variation * 0.2)
    
    def draw(self):
        self.screen.blit(self.texture, self.texture_rect)
    
    def move(self):
        self.texture_rect.move_ip(0, self.velocity)
    
    def is_off_screen(self):
        return self.texture_rect.top > self.screen.get_height()
    
    def is_hit(self, bullet_rect):
        return self.texture_rect.colliderect(bullet_rect)