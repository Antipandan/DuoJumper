from player_class import Player
from constants import *
from tile_class import Tiles


class Level:
    def __init__(self, screen, level):
        self.screen = screen
        # ladda nivå
        self.level = pytmx.load_pygame(level)
        self.platform_layer = self.level.get_layer_by_name('Platforms')
        self.props_layer = self.level.get_layer_by_name("Props")
        self.fill_layer = self.level.get_layer_by_name("Fill Platforms")
        # grupper
        # TODO ska ha flera spelare kanske behöver group
        self.player_group = pygame.sprite.Group()
        self.platform_group = pygame.sprite.Group()
        self.rest_tiles = pygame.sprite.Group()
        self.prop_group = pygame.sprite.Group()
        # Ange vilka knappar som en instans av en spelar klassen kan ha. Definerar det här så att
        # spelar klass koden inte fylls med fler if satser
        self.player_1_input_method = [pygame.K_w, pygame.K_a, pygame.K_s,
                                      pygame.K_d, pygame.K_SPACE]
        self.player_2_input_metod = [pygame.K_UP, pygame.K_LEFT,
                                     pygame.K_DOWN, pygame.K_RIGHT]
        # skapa instanser lägg till i grupp
        self.player_1 = Player(start_pos[0], start_pos[1], self.player_1_input_method, 1)
        self.player_2 = Player(start_pos[0], start_pos[1], self.player_2_input_metod, 2)
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
    def make_tiles(layer):
        created_tiles = []
        for x, y, tileSurface in layer.tiles():
            tile = Tiles((x * tile_size_x, y * tile_size_y), tileSurface)
            created_tiles.append(tile)
        return created_tiles

    def update(self):
        # metoder som måste updateras för varje klass läggs här
        self.player_group.update(self.platform_group)

    def draw(self):
        # ritar klasser
        self.screen.fill("black")

        # pygame.draw.rect(self.screen, "red", self.player_1.rect, 2)
        self.prop_group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.rest_tiles.draw(self.screen)
        self.platform_group.draw(self.screen)

    def draw_debugg_outline(self):
        pygame.draw.rect(self.screen, "red", self.player_1.rect, 1)
        pygame.draw.rect(self.screen, "blue", self.player_2.rect, 1)
        for tile in self.platform_group:
            # den här delen är inte helt modulär men spelet är gjort för enbart två spelare max
            if tile.owner == "Player_1":
                pygame.draw.rect(self.screen, "red", tile.rect, 1)
            elif tile.owner == "Player_2":
                pygame.draw.rect(self.screen, "blue", tile.rect, 1)
            else:
                pygame.draw.rect(self.screen, "white", tile.rect, 1)

    def run(self):
        # för huvudprogrammet
        self.update()
        self.draw()
        self.draw_debugg_outline()
