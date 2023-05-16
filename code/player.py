import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles):
        super().__init__()
        self.import_character_assets()  # Загружаем изображения персонажа
        self.frame_index = 0  # Индекс текущего кадра
        self.animation_speed = 0.15  # Скорость анимации
        self.image = self.animations['idle'][self.frame_index]  # Устанавливаем изображение в статусе "бездействие"
        self.rect = self.image.get_rect(topleft=pos)  # Устанавливаем позицию персонажа

        # Частицы пыли
        self.import_dust_run_particles()  # Загружаем изображения частиц пыли при беге
        self.dust_frame_index = 0  # Индекс текущего кадра анимации частиц пыли
        self.dust_animation_speed = 0.15  # Скорость анимации частиц пыли
        self.display_surface = surface  # Устанавливаем поверхность, на которой будет отображаться персонаж
        self.create_jump_particles = create_jump_particles  # Функция для создания частиц при прыжке

        # движение персонажа
        self.direction = pygame.math.Vector2(0, 0)  # Устанавливаем вектор направления движения персонажа
        self.speed = 8  # Скорость перемещения персонажа
        self.gravity = 0.8  # Гравитация
        self.jump_speed = -16  # Скорость прыжка

        # статус персонажа
        self.status = 'idle'  # Изначально устанавливаем статус персонажа в "бездействие"
        self.facing_right = True  # Персонаж смотрит направо
        self.on_ground = False  # Персонаж не находится на земле
        self.on_ceiling = False  # Персонаж не находится на потолке
        self.on_left = False  # Персонаж не находится слева
        self.on_right = False  # Персонаж не находится справа

    # Изображения персонажа
    def import_character_assets(self):
        character_path = '../graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    # Изображения частиц пыли при беге
    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('../graphics/character/dust_particles/run')

    # Анимация
    def animate(self):
        animation = self.animations[self.status]  # Выбирается нужная анимация в зависимости от статуса игрока

        # Цикл по индексу кадра
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Выбирается нужный кадр из анимации
        image = animation[int(self.frame_index)]
        # Поворот анимации
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # Устанавливается прямоугольник игрока
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    # Функция, которая осуществляет анимацию пыли при беге игрока
    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:  # если игрок бежит и находится на земле
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            # Текущий кадр анимации пыли при беге игрока
            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            # Поворот анимации
            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    def get_input(self):
        # Получаем состояние всех клавиш
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)

    # Функция для определения статуса игрока
    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    # Функция для гравитации игрока
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    # Прыжок
    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()  # Получаем входные данные (нажатие клавиш) от пользователя
        self.get_status()  # Определяем статус игрока
        self.animate()  # Анимируем игрока
        self.run_dust_animation()  # Анимируем пыль, которая поднимается при беге игрока
