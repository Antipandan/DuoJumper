import builtins
import pygame
import pytmx
import random
import os

from pygame.math import Vector2
from pygame.sprite import Group
from pytmx import TiledMap

from tile_class import Tiles

screen_width: int = 1280
screen_height: int = 720
tile_size_x: int = 32
tile_size_y: int = 30

gravity: int = 40
friction: float | int = 0.972
amount: int = 30
jump_strength: int = 750
resistance_in_air: float = 0.5
max_speed_air: float = 450
max_speed_grounded: float = 1200
RUNNING: bool = True
standard_offset_x: int = 50
standard_offset_y: int = 90
space_in_between: int = 90
standard_image_width: int = 210

acceleration: int = amount
delta_time: float | int = 16.67 / 1000
start_pos: Vector2 = pygame.Vector2(screen_width / 2, 10)

asset_path: str = "assets/"
level_path: str = asset_path + "levels/"
player_character: str = asset_path + "player_sprites/player.png"
bg_path: str = asset_path + "showcase_levels/main_menu_level.tmx"
images_path: str = asset_path + "level_pics/"
all_maps: list[str] = os.listdir(asset_path + "showcase_levels")
chosen_map_path: str = random.choice(all_maps)


def make_tiles(layer) -> list[Tiles]:
    created_tiles: list[Tiles] = []
    for x, y, tileSurface in layer.tiles():
        tile: Tiles = Tiles(Vector2(x * tile_size_x, y * tile_size_y), tileSurface)
        created_tiles.append(tile)
    return created_tiles


def render_level_only(draw_surface, level) -> None:
    platform_group: Group = Group()
    props_group: Group = Group()
    menu_level: TiledMap = pytmx.load_pygame(level)
    platform_layer: int = menu_level.get_layer_by_name("Platforms")
    props_layer: int = menu_level.get_layer_by_name("Props")

    for platform in make_tiles(platform_layer):
        platform_group.add(platform)

    for prop in make_tiles(props_layer):
        props_group.add(prop)

    platform_group.draw(draw_surface)
    props_group.draw(draw_surface)


def check_all_are_alive(player_group: Group) -> bool:
    for player in player_group.sprites():
        if not player.alive:
            return False
    return True
