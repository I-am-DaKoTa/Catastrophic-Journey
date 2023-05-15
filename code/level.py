import pygame
from tiles import Tile
from settings import tile_size, screen_width
from player import Player
from particles import ParticleEffect


class Level:
    def __init__(self, level_data, surface):

        # Настройка уровня
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0

        # Эффект
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

    # Создание эффекта при прыжке
    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    # Определение, находится ли игрок на земле
    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    # Создание эффекта падения на землю
    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    # Установка технического уровня
    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(player_sprite)

    # Прокрутка экрана по горизонтали
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    # Определение столкновений игрока с объектами по горизонтали
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    # Определение столкновений игрока с объектами по вертикали
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    # Запуск уровня
    def run(self):
        # Частицы пыли
        self.dust_sprite.update(self.world_shift)  # Обновление группы спрайтов пыли с учетом сдвига мира
        self.dust_sprite.draw(self.display_surface)  # Отображение группы спрайтов пыли на экране

        # Тайлы уровня
        self.tiles.update(self.world_shift)  # Обновление группы спрайтов тайлов с учетом сдвига мира
        self.tiles.draw(self.display_surface)  # Отображение группы спрайтов тайлов на экране
        self.scroll_x()  # Проверка и изменение сдвига мира в горизонтальной плоскости

        # Игрок
        self.player.update()  # Обновление спрайта игрока
        self.horizontal_movement_collision()  # Обработка столкновений игрока с тайлами в горизонтальной плоскости
        self.get_player_on_ground()  # Проверка, находится ли игрок на земле
        self.vertical_movement_collision()  # Обработка столкновений игрока с тайлами в вертикальной плоскости
        self.create_landing_dust()  # Создание эффекта падения пыли при приземлении игрока
        self.player.draw(self.display_surface)  # Отображение спрайта игрока на экране

