import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        # Поверхность размером size x size
        self.image = pygame.Surface((size, size))
        # Заполняем поверхность серым цветом
        self.image.fill((128, 128, 128))
        # Получаем прямоугольник, описывающий изображение, и устанавливаем его начальное положение
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift
