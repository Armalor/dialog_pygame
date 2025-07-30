import pygame
from pygame.surface import Surface
import random

class BonusCircle:
    def __init__(self, x, y, screen: Surface, bonus_type):
        self.radius = 15
        self.x = x
        self.y = y
        self.velocity = random.uniform(2.0, 4.0)
        self.screen = screen
        self.type = bonus_type  # 'rapid_fire' или 'speed_boost'
        
        # Устанавливаем цвет в зависимости от типа бонуса
        if bonus_type == 'rapid_fire':
            self.color = (189, 113, 227)  # Фиолетовый
        else:
            self.color = (191, 8, 8)  # Красный
            
        self.active = True
    
    def draw(self):
        if self.active:
            pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def move(self):
        if self.active:
            self.y += self.velocity
    
    def is_off_screen(self):
        return self.y - self.radius > self.screen.get_height()
    
    def check_collision(self, ship_rect):
        if not self.active:
            return False
            
        circle_rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
        return circle_rect.colliderect(ship_rect)