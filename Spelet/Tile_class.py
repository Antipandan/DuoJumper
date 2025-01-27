from Constants import pygame


class Tiles(pygame.sprite.Sprite):
    def __init__(self, pos, surface):
        super().__init__()
        self.pos = pos
        self.image = surface
        self.rect = self.image.get_rect(topleft=self.pos)
        self.owner = None

    def change_owner(self, new_owner):
        if self.owner is None:
            self.owner = new_owner
