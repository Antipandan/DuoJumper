from pygame.surface import Surface
from player_class import Player
from constants import *

class Level:
    def __init__(self, screen, level) -> None:
        self.screen: Surface = screen
        # ladda nivå
        self.level: TiledMap = pytmx.load_pygame(level)
        self.platform_layer: int = self.level.get_layer_by_name('Platforms')
        self.props_layer: int = self.level.get_layer_by_name("Props")
        self.fill_layer: int = self.level.get_layer_by_name("Fill Platforms")
        # grupper

        self.player_group: Group = pygame.sprite.Group()
        self.platform_group: Group = pygame.sprite.Group()
        self.rest_tiles: Group = pygame.sprite.Group()
        self.prop_group: Group = pygame.sprite.Group()
        # Ange vilka knappar som en instans av en spelar klassen kan ha. Definerar det här så att
        # spelar klass koden inte fylls med fler if satser
        self.player_1_input_method: list[int] = [
            pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE]

        self.player_2_input_metod: list[int] = [
            pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT]

        # skapa instanser lägg till i grupp
        self.player_1: Player = Player(start_pos[0], start_pos[1], self.player_1_input_method)
        self.player_2: Player = Player(start_pos[0], start_pos[1], self.player_2_input_metod)
        # lägg till spelare 2 först så att spelare 1 är ritad över spelare 2
        self.player_group.add(self.player_2)
        self.player_group.add(self.player_1)

        for tile in self.make_tiles(self.platform_layer):
            self.platform_group.add(tile)

        for prop in self.make_tiles(self.props_layer):
            self.prop_group.add(prop)

        for fill in self.make_tiles(self.fill_layer):
            self.rest_tiles.add(fill)

    @staticmethod
    def make_tiles(layer: int) -> list[Tiles]:
        created_tiles: list[Tiles] = []
        for x, y, tileSurface in layer.tiles():
            tile: Tiles = Tiles(Vector2(x * tile_size_x, y * tile_size_y), tileSurface)
            created_tiles.append(tile)
        return created_tiles

    def update(self) -> None:
        self.player_group.update(self.platform_group)

    def draw(self) -> None:
        self.screen.fill("black")
        self.prop_group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.rest_tiles.draw(self.screen)
        self.platform_group.draw(self.screen)

    def draw_debug_outline(self) -> None:
        pygame.draw.rect(self.screen, "red", self.player_1.rect, 1)
        pygame.draw.rect(self.screen, "blue", self.player_2.rect, 1)
        for tile in self.platform_group:
            # den här delen är inte helt modulär men spelet är gjort för enbart två spelare max
            if tile.owner == self.player_1:
                pygame.draw.rect(self.screen, "red", tile.rect, 1)
            elif tile.owner == self.player_2:
                pygame.draw.rect(self.screen, "blue", tile.rect, 1)
            else:
                pygame.draw.rect(self.screen, "white", tile.rect, 1)

    def run(self) -> None:
        # för huvudprogrammet
        self.update()
        self.draw()
        self.draw_debug_outline()
