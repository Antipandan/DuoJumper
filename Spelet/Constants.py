import pygame
import pytmx
import random
import os
from Tile_class import Tiles

# Fuck config file all my homies hardcode FUCK config file
screen_width = 1280  # 1600
screen_height = 720  # 900
tile_size_x = 32
tile_size_y = 30

gravity = 40
friction = 0.972
amount = 30
jump_strength = 750
resistance_in_air = 0.5
max_speed_air = 450
switch_delay = 3  # ändra senare till 30
RUNNING = True

radius = 20
acceleration = amount
delta_time = 16.67 / 1000
start_pos = pygame.Vector2(screen_width / 2, 10)

asset_path = "Assets/"
level_path = asset_path + "Levels/"
player_character = asset_path + "Player_sprites/Player 1.png"
bg_path = level_path + "Showcase_levels/Main Menu Level.tmx"
images_path = level_path + "Level_pics/"
all_maps = os.listdir(r"C:\Users\06jaco06\PycharmProjects\pythonProject\GymnasieArbete\Spelet\Assets\Levels\Showcase_levels")
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
