import pygame
from spaceship import Spaceship
from spaceship import Bullet
from enemy import Enemy
from pathlib import Path, PurePath
import random
import math
import os
import sys


from utils import get_pure_path

WIDTH = 1200
HEIGHT = 700
FPS = 30

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic Intruders")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 24)
big_font = pygame.font.SysFont('Arial', 120)



# Загрузка текстур
def load_texture(path, scale=1):
    p = os.path.join("images", "circles", path)

    pure_p = get_pure_path(p)

    texture = pygame.image.load(pure_p).convert_alpha()
    if scale != 1:
        new_size = (int(texture.get_width() * scale), int(texture.get_height() * scale))
        texture = pygame.transform.scale(texture, new_size)
    return texture

# Текстуры для бонусов и пуль
purple_bonus_texture = load_texture("purple_bonus.png", 0.5)
red_bonus_texture = load_texture("red_bonus.png", 0.5)
green_bonus_texture = load_texture("green_bonus.png", 0.5)  # Новый бонус
enemy_bullet_texture = load_texture("enemy_bullet.png", 0.3)

# Класс для звёзд фона
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-50, HEIGHT)
        self.size = random.uniform(0.5, 2.5)
        self.speed = random.uniform(0.1, 20.0)
        
    def move(self):
        self.y += self.speed
        if self.y > HEIGHT + 5:
            self.y = random.randint(-20, -5)
            self.x = random.randint(0, WIDTH)
            
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), int(self.size))

# Создаём звёзды для фона
stars = [Star() for _ in range(150)]

class BonusCircle:
    def __init__(self, x, y, screen: pygame.Surface, bonus_type):
        self.x = x
        self.y = y
        self.screen = screen
        self.type = bonus_type
        self.velocity = random.uniform(4.0, 6.0)
        
        if bonus_type == 'rapid_fire':
            self.texture = purple_bonus_texture
        elif bonus_type == 'speed_boost':
            self.texture = red_bonus_texture
        elif bonus_type == 'slow_spawn':  # Новый тип бонуса
            self.texture = green_bonus_texture
            
        self.rect = self.texture.get_rect(center=(x, y))
    
    def move(self):
        self.y += self.velocity
        self.rect.center = (self.x, self.y)
    
    def draw(self):
        self.screen.blit(self.texture, self.rect)
    
    def is_off_screen(self):
        return self.y - self.rect.height/2 > self.screen.get_height()
    
    def check_collision(self, ship_rect):
        return self.rect.colliderect(ship_rect)

# Игровые объекты
bullets = []
enemies = []
bonuses = []
enemy_bullets = []

# Таймеры
enemy_spawn_timer = 0
enemy_spawn_delay = 35
difficulty_timer = 0
difficulty_increase_interval = 75
enemy_shoot_timer = 0
enemy_shoot_delay = 3000

# Состояния бонусов
rapid_fire_active = False
rapid_fire_end_time = 0
speed_boost_active = False
speed_boost_end_time = 0
slow_spawn_active = False  # Новый флаг бонуса
slow_spawn_end_time = 0
original_ship_velocity = 20
original_spawn_delay = enemy_spawn_delay  # Запоминаем оригинальную задержку

# Статистика
enemies_killed = 0

# Флаги состояния игры
game_over = False
game_over_time = 0
game_over_delay = 7000  # 7 секунд

# Создание корабля игрока
ship = Spaceship(velocity=original_ship_velocity, screen=screen)

running = True
while running:
    current_time = pygame.time.get_ticks()
    clock.tick(FPS)
    screen.fill((0, 0, 0))  # Чёрный фон

    # Отрисовка и движение звёзд
    for star in stars:
        star.move()
        star.draw(screen)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP and not game_over:
            if event.key == pygame.K_SPACE and not rapid_fire_active:
                bullets.append(Bullet(-10, ship.texture_rect.center[0] + 1, ship.texture_rect.center[1] - 70, screen))

    if game_over:
        # Отображение GAME OVER
        game_over_text = big_font.render("GAME OVER!", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(game_over_text, game_over_rect)
        
        # Отображение итогового счёта
        score_text = font.render(f"Total kills: {enemies_killed}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
        screen.blit(score_text, score_rect)
        
        # Закрытие игры через 7 секунд
        if current_time - game_over_time >= game_over_delay:
            running = False
            
        pygame.display.flip()
        continue

    keys = pygame.key.get_pressed()
    
    # Режим быстрой стрельбы
    if rapid_fire_active:
        bullets.append(Bullet(-10, ship.texture_rect.center[0] + 1, ship.texture_rect.center[1] - 70, screen))

    # Управление сложностью (если не активен slow_spawn)
    if not slow_spawn_active:
        difficulty_timer += 1
        if difficulty_timer >= difficulty_increase_interval:
            difficulty_timer = 0
            enemy_spawn_delay = max(10, enemy_spawn_delay - 5)
    
    # Спавн врагов (с учётом бонуса slow_spawn)
    enemy_spawn_timer += 1
    current_spawn_delay = enemy_spawn_delay * 2 if slow_spawn_active else enemy_spawn_delay
    
    if enemy_spawn_timer >= current_spawn_delay:
        enemy_spawn_timer = 0
        x = random.randint(50, WIDTH - 50)
        enemies.append(Enemy(x, -50, screen))

    # Стрельба врагов
    if current_time - enemy_shoot_timer >= enemy_shoot_delay and enemies:
        enemy_shoot_timer = current_time
        if random.random() < 0.6:
            shooter = random.choice(enemies)
            
            dx = ship.texture_rect.center[0] - shooter.texture_rect.center[0]
            dy = ship.texture_rect.center[1] - shooter.texture_rect.center[1]
            distance = max(1, math.sqrt(dx*dx + dy*dy))
            
            speed = 20
            velocity_x = (dx / distance) * speed
            velocity_y = (dy / distance) * speed
            
            enemy_bullets.append({
                'x': shooter.texture_rect.center[0],
                'y': shooter.texture_rect.center[1],
                'velocity_x': velocity_x,
                'velocity_y': velocity_y,
                'texture': enemy_bullet_texture,
                'rect': enemy_bullet_texture.get_rect(center=(shooter.texture_rect.center[0], shooter.texture_rect.center[1]))
            })

    # Обновление пуль игрока
    for bullet in bullets:
        bullet.move()
        bullet.draw()
        if bullet.texture_rect.bottom < 0:
            bullets.remove(bullet)

    # Обновление врагов
    for enemy in enemies:
        enemy.move()
        enemy.draw()
        
        for bullet in bullets:
            if enemy.is_hit(bullet.texture_rect):
                enemies_killed += 1
                
                rand = random.random()
                if rand < 0.02:  # 2% - красный бонус
                    bonuses.append(BonusCircle(
                        enemy.texture_rect.centerx,
                        enemy.texture_rect.centery,
                        screen,
                        'speed_boost'
                    ))
                elif rand < 0.13:  # 11% - зелёный бонус (было 0.17, теперь 0.13 + 0.04)
                    bonuses.append(BonusCircle(
                        enemy.texture_rect.centerx,
                        enemy.texture_rect.centery,
                        screen,
                        'slow_spawn'
                    ))
                elif rand < 0.17:  # 4% - фиолетовый бонус (оставшиеся от 15%)
                    bonuses.append(BonusCircle(
                        enemy.texture_rect.centerx,
                        enemy.texture_rect.centery,
                        screen,
                        'rapid_fire'
                    ))
                
                enemies.remove(enemy)
                bullets.remove(bullet)
                break
        
        if enemy.is_off_screen():
            game_over = True
            game_over_time = current_time

    # Обновление бонусов
    for bonus in bonuses[:]:
        bonus.move()
        bonus.draw()
        
        if bonus.check_collision(ship.texture_rect):
            if bonus.type == 'rapid_fire':
                rapid_fire_active = True
                rapid_fire_end_time = current_time + 2000
            elif bonus.type == 'speed_boost':
                speed_boost_active = True
                speed_boost_end_time = current_time + 2000
                ship.velocity = original_ship_velocity * 2
            elif bonus.type == 'slow_spawn':  # Обработка нового бонуса
                slow_spawn_active = True
                slow_spawn_end_time = current_time + 2000
            
            bonuses.remove(bonus)
        
        if bonus.is_off_screen():
            bonuses.remove(bonus)

    # Обновление вражеских пуль
    for bullet in enemy_bullets[:]:
        bullet['x'] += bullet['velocity_x']
        bullet['y'] += bullet['velocity_y']
        bullet['rect'].center = (int(bullet['x']), int(bullet['y']))
        
        screen.blit(bullet['texture'], bullet['rect'])
        
        if (bullet['x'] < 0 or bullet['x'] > WIDTH or
            bullet['y'] < 0 or bullet['y'] > HEIGHT):
            enemy_bullets.remove(bullet)
        
        if bullet['rect'].colliderect(ship.texture_rect):
            game_over = True
            game_over_time = current_time

    # Проверка времени действия бонусов
    if rapid_fire_active and current_time >= rapid_fire_end_time:
        rapid_fire_active = False
        
    if speed_boost_active and current_time >= speed_boost_end_time:
        speed_boost_active = False
        ship.velocity = original_ship_velocity
        
    if slow_spawn_active and current_time >= slow_spawn_end_time:
        slow_spawn_active = False

    # Отображение статусов
    status_texts = []
    if rapid_fire_active:
        remaining_time = max(0, (rapid_fire_end_time - current_time) // 1000)
        status_texts.append(f"RAPID FIRE: {remaining_time}s")
        
    if speed_boost_active:
        remaining_time = max(0, (speed_boost_end_time - current_time) // 1000)
        status_texts.append(f"SPEED BOOST: {remaining_time}s")
    
    if slow_spawn_active:  # Статус нового бонуса
        remaining_time = max(0, (slow_spawn_end_time - current_time) // 1000)
        status_texts.append(f"SLOW SPAWN: {remaining_time}s")
        
    for i, text in enumerate(status_texts):
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10 + i * 30))

    # Отображение счётчика убийств
    kills_text = font.render(f"Kills: {enemies_killed}", True, (255, 255, 255))
    kills_text_rect = kills_text.get_rect()
    kills_text_rect.topright = (WIDTH - 10, 10)
    screen.blit(kills_text, kills_text_rect)

    # Управление кораблем и отрисовка (если не game over)
    if not game_over:
        ship.move(keys)
        ship.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()