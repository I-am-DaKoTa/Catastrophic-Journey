import pygame
from support import import_folder
from math import sin


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, change_health):
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

        # Движение игрока
        self.direction = pygame.math.Vector2(0, 0)  # Устанавливаем вектор направления движения персонажа
        self.speed = 8  # Скорость перемещения персонажа
        self.gravity = 0.8  # Гравитация
        self.jump_speed = -16  # Скорость прыжка
        self.collision_rect = pygame.Rect(self.rect.topleft, (50, self.rect.height))  # Коллизия

        # Статус игрока
        self.status = 'idle'  # Изначально устанавливаем статус персонажа в "бездействие"
        self.facing_right = True  # Персонаж смотрит направо
        self.on_ground = False  # Персонаж не находится на земле
        self.on_ceiling = False  # Персонаж не находится на потолке
        self.on_left = False  # Персонаж не находится слева
        self.on_right = False  # Персонаж не находится справа

        # Здоровье
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 500
        self.hurt_time = 0

        # Аудио
        self.jump_sound = pygame.mixer.Sound('../audio/effects/jump.mp3')
        self.jump_sound.set_volume(0.5)
        self.hit_sound = pygame.mixer.Sound('../audio/effects/hit.mp3')

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
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright

        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

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

        if keys[pygame.K_SPACE] and self.on_ground:
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
        self.collision_rect.y += self.direction.y

    # Прыжок
    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_sound.play()

    # Получение урона
    def get_damage(self):
        if not self.invincible:
            self.hit_sound.play()
            self.change_health(-20)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()

    # Таймер неуязвимости
    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invincibility_timer()
        self.wave_value()
