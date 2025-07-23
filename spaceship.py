import pygame, json

bullets = []
enemies = []


class Bullet:
    def __init__(self, velocity, x, y, screen: pygame.surface.Surface):
        self.texture = pygame.image.load("images/bullet.png").convert_alpha()
        self.texture_rect = self.texture.get_rect()
        self.texture_rect.center = (x, y - self.texture_rect.height // 2)
        self.screen = screen
        self.velocity = velocity
        self.alive = True
        bullets.append(self)

    def __str__(self):
        return f'Bullet: {self.texture_rect.center[0], self.texture_rect.center[1]}'

    def draw(self):
        self.screen.blit(self.texture, self.texture_rect)

    def move(self):
        if self.texture_rect.bottom > 0:
            self.texture_rect.move_ip(0, self.velocity)
        else:
            bullets.remove(self)

    def to_bytes(self):  # для передачи атрибутов по байтам
        d = {'type': 'b'}
        d['x'] = self.texture_rect.center[0]
        d['y'] = self.texture_rect.center[1]
        s = json.dumps(d)
        b = s.encode()
        return b


class Spaceship:
    def __init__(self, velocity, screen: pygame.surface.Surface, image):
        self.texture = pygame.image.load(image).convert_alpha()
        self.texture_rect = self.texture.get_rect()
        self.screen = screen
        screen_width, screen_height = screen.get_size()
        self.alive = True

        self.texture_rect.center = (screen_width // 2, screen_height - self.texture_rect.height // 2 - 20)
        self.velocity = velocity

    def move(self, keys: pygame.key.ScancodeWrapper):
        if keys[pygame.K_LEFT]:
            if self.texture_rect.left > 0:
                self.texture_rect.move_ip(-self.velocity, 0)

        if keys[pygame.K_RIGHT]:
            screen_width, _ = self.screen.get_size()
            if self.texture_rect.right < screen_width:
                self.texture_rect.move_ip(+self.velocity, 0)

    def draw(self):
        self.screen.blit(self.texture, self.texture_rect)

    def to_bytes(self):  # для передачи атрибутов по байтам
        d = {'type': 's'}
        d['x'] = self.texture_rect.center[0]
        d['y'] = self.texture_rect.center[1]
        s = json.dumps(d)
        b = s.encode()
        return b

class Enemy:
    def __init__(self, velocity, x, y, screen: pygame.surface.Surface):
        self.texture = pygame.image.load("images/enemy.png").convert_alpha()
        self.texture_rect = self.texture.get_rect()
        self.texture_rect.center = (x, y)
        self.screen = screen
        self.velocity = velocity
        self.alive = True
        enemies.append(self)

    def draw(self):
        self.screen.blit(self.texture, self.texture_rect)

    def move(self):
        self.texture_rect.move_ip(0, self.velocity)


def collusion(ship: Spaceship, height: int):
    global bullets, enemies
    for enemy in enemies[:]:
        if not enemy.alive:
            continue
        if ship.texture_rect.colliderect(enemy.texture_rect) or enemy.texture_rect.center[1] > height:
            ship.alive = False
        for bullet in bullets[:]:
            if not bullet.alive:
                continue
            if enemy.texture_rect.colliderect(bullet.texture_rect):
                enemy.alive = False
                bullet.alive = False


def update():
    global bullets, enemies
    for enemy in enemies:
        if not enemy.alive:
            enemies.remove(enemy)
    for bullet in bullets:
        if not bullet.alive:
            bullets.remove(bullet)


class Base:
    pass
