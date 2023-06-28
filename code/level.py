import csv

import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Coin, Flag, Deco
from enemy import Enemy
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect
from game_data import levels


class Level:
    def __init__(self, current_level, surface, create_overworld, change_coins, change_health):
        # Настройка уровня
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        # аудио
        self.coin_sound = pygame.mixer.Sound('../audio/effects/coin.mp3')
        self.stomp_sound = pygame.mixer.Sound('../audio/effects/stomp.mp3')

        # связь с картой мира
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']

        # игрок
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)

        # интерфейс
        self.change_coins = change_coins

        # частицы пыли
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # частицы взрыва
        self.explosion_sprites = pygame.sprite.Group()

        # Создание ландшафта
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain', current_level)

        # Монетки
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins', current_level)

        # Декорации
        deco_sprites = import_csv_layout(level_data['deco'])
        self.deco_sprites = self.create_tile_group(deco_sprites, 'deco', current_level)

        # Враги
        enemy_layout = import_csv_layout(level_data['enemy'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemy', current_level)

        # Ограничение
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraint', current_level)

        # Облака
        self.sky = Sky(8, current_level)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 20, level_width, current_level)
        self.clouds = Clouds(400, level_width, 30, current_level)

    def create_tile_group(self, layout, type, current_lvl):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        if current_lvl == 0:
                            terrain_tile_list = import_cut_graphics('../graphics/tilesets/tileset_forest.png')
                            tile_surface = terrain_tile_list[int(val)]
                            sprite = StaticTile(tile_size, x, y, tile_surface)
                        if current_lvl == 1:
                            terrain_tile_list = import_cut_graphics('../graphics/tilesets/tileset_desert.png')
                            tile_surface = terrain_tile_list[int(val)]
                            sprite = StaticTile(tile_size, x, y, tile_surface)
                        if current_lvl == 2:
                            terrain_tile_list = import_cut_graphics('../graphics/tilesets/tileset_snow.png')
                            tile_surface = terrain_tile_list[int(val)]
                            sprite = StaticTile(tile_size, x, y, tile_surface)
                        if current_lvl == 3:
                            terrain_tile_list = import_cut_graphics('../graphics/tilesets/tileset_water.png')
                            tile_surface = terrain_tile_list[int(val)]
                            sprite = StaticTile(tile_size, x, y, tile_surface)
                        if current_lvl == 4:
                            terrain_tile_list = import_cut_graphics('../graphics/tilesets/tileset_lava.png')
                            tile_surface = terrain_tile_list[int(val)]
                            sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'coins':
                        if val == '0':
                            sprite = Coin(tile_size, x, y, '../graphics/coins/gold', 5)
                            sprite.abs_x = x
                            sprite.abs_y = y
                        if val == '1':
                            sprite = Coin(tile_size, x, y, '../graphics/coins/silver', 1)
                            sprite.abs_x = x
                            sprite.abs_y = y

                    if type == 'deco':
                        if val == '0':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/bush.png')
                        if val == '1':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/log_wall.png')
                        if val == '2':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/rock_a.png')
                        if val == '3':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/rock_b.png')
                        if val == '4':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/tree.png')
                        if val == '5':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/tree_b.png')
                        if val == '6':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/tree_c.png')
                        if val == '7':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/tree_trunk.png')
                        if val == '8':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/0_grass_0.png')
                        if val == '9':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/0_grass_1.png')
                        if val == '10':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/0_rock.png')
                        if val == '11':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/1_pyramid.png')
                        if val == '12':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/1_rock_0.png')
                        if val == '13':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/1_rock_1.png')
                        if val == '14':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/2_rock_0.png')
                        if val == '15':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/2_rock_1.png')
                        if val == '16':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/2_snow_0.png')
                        if val == '17':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/2_snow_1.png')
                        if val == '18':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/2_snowman.png')
                        if val == '19':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/3_grass_0.png')
                        if val == '20':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/3_grass_1.png')
                        if val == '21':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/3_grass_2.png')
                        if val == '22':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/3_rock_0.png')
                        if val == '23':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/3_rock_1.png')
                        if val == '24':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/4_rock_0.png')
                        if val == '25':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/4_rock_1.png')
                        if val == '26':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/4_rock_3.png')
                        if val == '27':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/sun_0.png')
                        if val == '28':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/sun_1.png')
                        if val == '29':
                            sprite = Deco(tile_size, x, y, '../graphics/deco/sun_3.png')

                    if type == 'enemy':
                        if current_lvl == 0:
                            sprite = Enemy(tile_size, x, y, '../graphics/enemy/brown_bear')
                        if current_lvl == 1:
                            sprite = Enemy(tile_size, x, y, '../graphics/enemy/snake')
                        if current_lvl == 2:
                            sprite = Enemy(tile_size, x, y, '../graphics/enemy/polar_bear')
                        if current_lvl == 3:
                            sprite = Enemy(tile_size, x, y, '../graphics/enemy/crab')
                        if current_lvl == 4:
                            sprite = Enemy(tile_size, x, y, '../graphics/enemy/slime_red')

                    if type == 'constraint':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout, change_health):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles, change_health)
                    self.player.add(sprite)
                if val == '1':
                    sprite = Flag(tile_size, x, y, '../graphics/character/flag', 64)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

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

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level, self.current_level)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)
        if collided_coins:
            self.coin_sound.play()
            for coin in collided_coins:
                filename = f"../levels/{self.current_level}/level_{self.current_level}_coins.csv"
                coin_row = coin.abs_x // tile_size
                coin_col = coin.abs_y // tile_size
                self.change_coins(coin.value)
                self.update_coin_value_in_csv(filename, coin_row, coin_col, -1)

    def update_coin_value_in_csv(self, filename, row, col, new_value):

        with open(filename, 'r') as csvfile:
            coins_data = list(csv.reader(csvfile))
            coins_data[col][row] = str(new_value)

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(coins_data)

    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.stomp_sound.play()
                    self.player.sprite.direction.y = -15
                    explosion_sprite = ParticleEffect(enemy.rect.center, 'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    # Запуск уровня
    def run(self):

        # небо
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        # задний план
        self.deco_sprites.update(self.world_shift)
        self.deco_sprites.draw(self.display_surface)

        # частицы пыли
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # ландшафт
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # враги
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)

        # монетки
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # игрок
        self.player.update()
        self.horizontal_movement_collision()

        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()

        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.check_death()
        self.check_win()

        self.check_coin_collisions()
        self.check_enemy_collisions()

        # вода
        self.water.draw(self.display_surface, self.world_shift)
