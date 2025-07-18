import pygame

if __name__ == '__main__':
    pygame.init()

    # Установка размеров окна
    screen_width = 1600
    screen_height = 1024
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Текстура в Pygame")

    # Загрузка текстуры
    texture = pygame.image.load("images/spaceship_200.png").convert_alpha()

    # Получение прямоугольника текстуры (для позиционирования)
    texture_rect = texture.get_rect()
    # texture_rect.height = texture_rect.height // 2
    # texture_rect.width = texture_rect.width // 2

    # Установка позиции текстуры (например, в центре)
    texture_rect.center = (screen_width // 2, screen_height - texture_rect.height // 2 - 200)

    # Игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Очистка экрана
        screen.fill((0, 0, 0))  # Черный фон

        # Отображение текстуры
        screen.blit(texture, texture_rect)

        # Обновление экрана
        pygame.display.flip()

    pygame.quit()
