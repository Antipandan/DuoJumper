import pygame
import pytmx
import random
import os
from tile_class import Tiles

screen_width = 1280
screen_height = 720
tile_size_x = 32
tile_size_y = 30

gravity = 40
friction = 0.972
amount = 30
jump_strength = 750
resistance_in_air = 0.5
max_speed_air = 450
max_speed_grounded = 1200
RUNNING = True
standard_offset_x = 50
standard_offset_y = 90
space_in_between = 90
standard_image_width = 210
# detta värde används ej
standard_image_height = 120

acceleration = amount
delta_time = 16.67 / 1000
start_pos = pygame.Vector2(screen_width / 2, 10)

asset_path = "assets/"
level_path = asset_path + "levels/"
player_character = asset_path + "player_sprites/player.png"
bg_path = asset_path + "showcase_levels/main_menu_level.tmx"
images_path = asset_path + "level_pics/"
all_maps = os.listdir(asset_path + "showcase_levels")
chosen_map_path = random.choice(all_maps)


def make_tiles(layer):
    created_tiles = []
    for x, y, tileSurface in layer.tiles():
        tile = Tiles((x * tile_size_x, y * tile_size_y), tileSurface)
        created_tiles.append(tile)
    return created_tiles


def render_level_only(draw_surface, level):
    platform_group = pygame.sprite.Group()
    props_group = pygame.sprite.Group()
    menu_level = pytmx.load_pygame(level)
    platform_layer = menu_level.get_layer_by_name("Platforms")
    props_layer = menu_level.get_layer_by_name("Props")

    for platform in make_tiles(platform_layer):
        platform_group.add(platform)
    for prop in make_tiles(props_layer):
        props_group.add(prop)
    platform_group.draw(draw_surface)
    props_group.draw(draw_surface)


def check_all_are_alive(player_group: pygame.sprite.Group):
    all_alive = True
    for player in player_group.sprites():
        if player.alive != all_alive:
            all_alive = False
            return all_alive
    return all_alive
