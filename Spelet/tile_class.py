import builtins

from pygame.math import Vector2
from pygame.surface import Surface
from DuoJumper.Spelet.player_class import Player
from constants import pygame

class Tiles(pygame.sprite.Sprite):
    def __init__(self, pos: Vector2, surface: Surface) -> None:
        super().__init__()
        self.pos = pos
        self.image = surface
        self.rect = self.image.get_rect(topleft=self.pos)
        self.owner: Player = None

