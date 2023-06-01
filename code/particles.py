import pygame
from support import import_folder


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.5
        # Проверка типа эффекта
        if type == 'jump':
            self.frames = import_folder('../graphics/character/dust_particles/jump')
        if type == 'land':
            self.frames = import_folder('../graphics/character/dust_particles/land')
        if type == 'explosion':
            self.frames = import_folder('../graphics/enemy/explosion')

        # Установка начального изображения для эффекта
        self.image = self.frames[self.frame_index]
        # Установка позиции эффекта
        self.rect = self.image.get_rect(center=pos)

    # Анимация эффекта
    def animate(self):
        # Изменение индекса текущего кадра
        self.frame_index += self.animation_speed
        # Проверка, достигнут ли конец списка кадров
        if self.frame_index >= len(self.frames):
            # Удаление объекта из группы спрайтов
            self.kill()
        else:
            # Обновление текущего изображения
            self.image = self.frames[int(self.frame_index)]

    # Обновление положения эффекта на экране
    def update(self, x_shift):
        # Запуск анимации
        self.animate()
        # Изменение координаты x
        self.rect.x += x_shift
