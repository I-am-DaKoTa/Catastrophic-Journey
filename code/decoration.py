from settings import vertical_tile_number, tile_size, screen_width
import pygame
from tiles import AnimatedTile, StaticTile
from support import import_folder
from random import choice, randint


class Sky:
    def __init__(self, horizon, lvl, style='level'):
        self.top = pygame.image.load('../graphics/decoration/sky_1-3/sky_top.png').convert()
        self.bottom = pygame.image.load('../graphics/decoration/sky_1-3/sky_bottom.png').convert()
        self.middle = pygame.image.load('../graphics/decoration/sky_1-3/sky_middle.png').convert()
        if lvl == 1:
            self.top = pygame.image.load('../graphics/decoration/sky_2/sky_top.png').convert()
            self.bottom = pygame.image.load('../graphics/decoration/sky_2/sky_bottom.png').convert()
            self.middle = pygame.image.load('../graphics/decoration/sky_2/sky_middle.png').convert()
        elif lvl == 3:
            self.top = pygame.image.load('../graphics/decoration/sky_4/sky_top.png').convert()
            self.bottom = pygame.image.load('../graphics/decoration/sky_4/sky_bottom.png').convert()
            self.middle = pygame.image.load('../graphics/decoration/sky_4/sky_middle.png').convert()
        elif lvl == 4:
            self.top = pygame.image.load('../graphics/decoration/sky_5/sky_top.png').convert()
            self.bottom = pygame.image.load('../graphics/decoration/sky_5/sky_bottom.png').convert()
            self.middle = pygame.image.load('../graphics/decoration/sky_5/sky_middle.png').convert()

        self.horizon = horizon

        # stretch
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size))
        self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size))

        self.style = style
        if self.style == 'overworld':
            tree_surfaces = import_folder('../graphics/overworld/trees')
            self.trees = []

            for surface in [choice(tree_surfaces) for image in range(5)]:
                x = randint(0, screen_width)
                y = (self.horizon * tile_size) + randint(50, 100)
                rect = surface.get_rect(midbottom=(x, y))
                self.trees.append((surface, rect))

            cloud_surfaces = import_folder('../graphics/overworld/clouds')
            self.clouds = []

            for surface in [choice(cloud_surfaces) for image in range(8)]:
                x = randint(0, screen_width)
                y = randint(0, (self.horizon * tile_size) - 100)
                rect = surface.get_rect(midbottom=(x, y))
                self.clouds.append((surface, rect))

    def draw(self, surface):
        for row in range(vertical_tile_number):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))

        if self.style == 'overworld':
            for tree in self.trees:
                surface.blit(tree[0], tree[1])
            for cloud in self.clouds:
                surface.blit(cloud[0], cloud[1])


class Water:
    def __init__(self, top, level_width, lvl):
        water_start = -screen_width
        water_tile_width = 192
        tile_x_amount = int((level_width + screen_width * 2) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()
        if lvl!=4:
            for tile in range(tile_x_amount):
                x = tile * water_tile_width + water_start
                y = top
                sprite = AnimatedTile(192, x, y, '../graphics/decoration/water')
                self.water_sprites.add(sprite)

    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)


class Clouds:
    def __init__(self, horizon, level_width, cloud_number, lvl):
        cloud_surf_list = import_folder('../graphics/decoration/clouds')
        min_x = -screen_width
        max_x = level_width + screen_width
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()
        if lvl != 4:
            for cloud in range(cloud_number):
                cloud = choice(cloud_surf_list)
                x = randint(min_x, max_x)
                y = randint(min_y, max_y)
                sprite = StaticTile(0, x, y, cloud)
                self.cloud_sprites.add(sprite)

    def draw(self, surface, shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)
