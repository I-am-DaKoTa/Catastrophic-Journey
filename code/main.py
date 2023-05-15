import pygame
import sys

from level import Level
from settings import *

# Запуск
pygame.init()

# Окно с заданными настройками ширины и высоты
screen = pygame.display.set_mode((screen_width, screen_height))
# Часы для контроля времени в игре
clock = pygame.time.Clock()
# Создание уровня
level = Level(level_map, screen)


while True:
    # Перебор событий
    for event in pygame.event.get():
        # Закрытие окна
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    # Запуск уровня игры
    level.run()

    pygame.display.update()
    clock.tick(60)
